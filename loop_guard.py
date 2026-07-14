"""
Loop Guard — control loop safety for Robot-man.
Implements: budget brakes, idempotency, observability, human escalation.

Usage in any Robot-man script:
    from loop_guard import Guard
    guard = Guard("reply_engine", max_iterations=10, budget_limit=0.05, idempotency_window=3600)
    
    for item in items:
        if not guard.check(): break
        result = do_work(item)
        guard.record(result)
"""

import json
import time
import os
from pathlib import Path
from datetime import datetime, timedelta

LOOP_DIR = Path(__file__).parent / ".loop_state"
LOOP_DIR.mkdir(exist_ok=True)


class Guard:
    """Safety controller for autonomous agent loops.
    
    Every Robot-man cron job should instantiate this before its main loop.
    """
    
    def __init__(
        self,
        name: str,
        max_iterations: int = 50,
        budget_limit: float = 0.10,  # USD
        idempotency_window: int = 3600,  # seconds — prevent re-processing same items
        run_timeout: int = 300,  # seconds — hard kill
        human_escalation_threshold: int = 3,  # consecutive failures → stop + alert
    ):
        self.name = name
        self.max_iterations = max_iterations
        self.budget_limit = budget_limit
        self.idempotency_window = idempotency_window
        self.run_timeout = run_timeout
        self.human_escalation_threshold = human_escalation_threshold
        
        self.iterations = 0
        self.total_cost = 0.0
        self.consecutive_failures = 0
        self.start_time = time.time()
        self.processed_ids = set()
        
        self.state_file = LOOP_DIR / f"{name}.json"
        self._load_state()
    
    
    def _load_state(self):
        """Load idempotency cache from disk."""
        try:
            if self.state_file.exists():
                data = json.loads(self.state_file.read_text())
                cutoff = (datetime.now() - timedelta(seconds=self.idempotency_window)).isoformat()
                self.processed_ids = {
                    eid for eid, ts in data.get("processed", {}).items()
                    if ts > cutoff
                }
        except Exception:
            self.processed_ids = set()
    
    
    def _save_state(self):
        """Persist processed IDs with timestamps."""
        data = {
            "name": self.name,
            "updated": datetime.now().isoformat(),
            "processed": {eid: datetime.now().isoformat() for eid in self.processed_ids},
        }
        self.state_file.write_text(json.dumps(data, indent=2))
    
    
    def check(self) -> bool:
        """Gate check before each iteration. Returns False if loop should STOP."""
        # Hard timeout
        if time.time() - self.start_time > self.run_timeout:
            print(f"[GUARD:{self.name}] ⛔ HARD TIMEOUT ({self.run_timeout}s)")
            return False
        
        # Max iterations
        if self.iterations >= self.max_iterations:
            print(f"[GUARD:{self.name}] ⛔ MAX ITERATIONS ({self.max_iterations})")
            return False
        
        # Budget brake
        if self.total_cost >= self.budget_limit:
            print(f"[GUARD:{self.name}] ⛔ BUDGET EXCEEDED (${self.total_cost:.4f} / ${self.budget_limit:.2f})")
            return False
        
        # Human escalation — too many consecutive failures
        if self.consecutive_failures >= self.human_escalation_threshold:
            print(f"[GUARD:{self.name}] 🚨 HUMAN ESCALATION: {self.consecutive_failures} consecutive failures")
            return False
        
        return True
    
    
    def is_duplicate(self, item_id: str) -> bool:
        """Check if this item was already processed."""
        return item_id in self.processed_ids
    
    
    def record(self, success: bool, cost: float = 0.0, item_id: str | None = None):
        """Record iteration result."""
        self.iterations += 1
        self.total_cost += cost
        
        if success:
            self.consecutive_failures = 0
            if item_id:
                self.processed_ids.add(item_id)
        else:
            self.consecutive_failures += 1
        
        self._save_state()
    
    
    def status(self) -> dict:
        """Current loop health for logging."""
        elapsed = time.time() - self.start_time
        return {
            "name": self.name,
            "iterations": self.iterations,
            "max": self.max_iterations,
            "cost": f"${self.total_cost:.5f}",
            "budget": f"${self.budget_limit:.2f}",
            "consecutive_failures": self.consecutive_failures,
            "elapsed": f"{elapsed:.0f}s",
            "timeout": f"{self.run_timeout}s",
            "processed": len(self.processed_ids),
        }
