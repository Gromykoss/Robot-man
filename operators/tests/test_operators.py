from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import loop_guard
from loop_guard import Guard
from operators import operator_account, operator_checklist, operator_pipeline
from operators.published_topic_check import MANUAL_THEMES, tokens
from operators.verdict import CheckResult, Verdict


def brief_table(**fields: str) -> str:
    rows = ["| Параметр | Значение |", "|---|---|"]
    rows.extend(f"| {key} | {value} |" for key, value in fields.items())
    return "\n".join(rows)


class VerdictContractTests(unittest.TestCase):
    @pytest.mark.scenario("operators-gate.verdict_contract")
    def test_verdict_passes_only_satisfied(self):
        expected = {
            Verdict.SATISFIED: True,
            Verdict.NOT_SATISFIED: False,
            Verdict.INCONCLUSIVE: False,
        }
        for verdict, passes in expected.items():
            with self.subTest(verdict=verdict):
                self.assertIs(verdict.passes, passes)

    @pytest.mark.scenario("operators-gate.verdict_contract")
    def test_check_result_passes_delegates_to_verdict(self):
        expected = {
            Verdict.SATISFIED: True,
            Verdict.NOT_SATISFIED: False,
            Verdict.INCONCLUSIVE: False,
        }
        for verdict, passes in expected.items():
            with self.subTest(verdict=verdict):
                self.assertIs(CheckResult(verdict, "message").passes, passes)


class ChecklistValidationTests(unittest.TestCase):
    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_normalize_account_strips_at_and_whitespace_but_preserves_case(self):
        self.assertEqual(operator_checklist._normalize_account(" @RobotsTJ500 "), "RobotsTJ500")
        self.assertEqual(operator_checklist._normalize_account("@robotstj500"), "robotstj500")
        self.assertEqual(operator_checklist._normalize_account(""), "")
        self.assertEqual(operator_checklist._normalize_account(None), "")

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_cyrillic_ratio_handles_empty_cyrillic_and_mixed_text(self):
        self.assertEqual(operator_checklist._cyrillic_ratio("123 !!!"), 0.0)
        self.assertEqual(operator_checklist._cyrillic_ratio("Привет"), 1.0)
        ratio = operator_checklist._cyrillic_ratio("abcд")
        self.assertGreater(ratio, 0.0)
        self.assertLess(ratio, 1.0)

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_parse_brief_fields_reads_table_rows_and_skips_headers(self):
        fields = operator_checklist.parse_brief_fields(
            brief_table(Mentions="@AgentMail @NetMindAI", **{"Изображение": "yes"})
        )
        self.assertEqual(fields["Mentions"], "@AgentMail @NetMindAI")
        self.assertEqual(fields["Изображение"], "yes")
        self.assertNotIn("Параметр", fields)

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_language_allows_english_robotstj500_final(self):
        self.assertIsNone(operator_checklist._check_language("I build with operator gates.", "@RobotsTJ500"))

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_language_blocks_russian_robotstj500_final(self):
        result = operator_checklist._check_language("Это русский рабочий черновик.", "RobotsTJ500")
        self.assertEqual(result.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("final language not EN", result.message)

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_language_skips_non_robotstj500_accounts(self):
        self.assertIsNone(operator_checklist._check_language("Русский текст", "@gromykoss"))

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_mentions_pass_when_required_handles_are_present(self):
        fields = {"Mentions": "@AgentMail @NetMindAI"}
        self.assertIsNone(operator_checklist._check_mentions("Thanks @AgentMail and @NetMindAI", fields))

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_mentions_block_when_required_handle_is_missing(self):
        result = operator_checklist._check_mentions("Thanks @AgentMail", {"Mentions": "@AgentMail @NetMindAI"})
        self.assertEqual(result.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("@NetMindAI", result.message)

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_media_opt_out_allows_missing_cover_and_default_robotstj500_blocks(self):
        self.assertIsNone(operator_checklist._check_media({"Изображение": "нет"}, None, "RobotsTJ500"))
        result = operator_checklist._check_media({}, None, "@RobotsTJ500")
        self.assertEqual(result.verdict, Verdict.NOT_SATISFIED)
        self.assertIn("cover required", result.message)

    @pytest.mark.scenario("operators-gate.checklist_validation")
    def test_media_yes_accepts_existing_cover(self):
        with tempfile.TemporaryDirectory() as tmp:
            cover = Path(tmp) / "cover.png"
            cover.write_bytes(b"png")
            self.assertIsNone(operator_checklist._check_media({"Изображение": "yes"}, str(cover), "RobotsTJ500"))


class AccountNormalizeTests(unittest.TestCase):
    @pytest.mark.scenario("operators-gate.account_normalize")
    def test_check_account_allows_normalized_requested_account(self):
        result = operator_account.check_account("@RobotsTJ500", {"RobotsTJ500"})
        self.assertEqual(result.verdict, Verdict.SATISFIED)

    @pytest.mark.scenario("operators-gate.account_normalize")
    def test_check_account_is_case_sensitive_after_normalization(self):
        result = operator_account.check_account("@robotstj500", {"RobotsTJ500"})
        self.assertEqual(result.verdict, Verdict.NOT_SATISFIED)

    @pytest.mark.scenario("operators-gate.account_normalize")
    def test_check_account_fails_closed_on_missing_allowed_accounts(self):
        self.assertEqual(operator_account.check_account("@RobotsTJ500", None).verdict, Verdict.INCONCLUSIVE)
        self.assertEqual(operator_account.check_account("@RobotsTJ500", []).verdict, Verdict.INCONCLUSIVE)

    @pytest.mark.scenario("operators-gate.account_normalize")
    def test_check_account_blocks_missing_requested_account(self):
        self.assertEqual(operator_account.check_account(None, {"RobotsTJ500"}).verdict, Verdict.NOT_SATISFIED)
        self.assertEqual(operator_account.check_account("", {"RobotsTJ500"}).verdict, Verdict.NOT_SATISFIED)


class PipelineApprovalTests(unittest.TestCase):
    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_approve_post_passes_with_token_limit_facts_and_media_opt_out(self):
        ok, reason = operator_pipeline.approve_post(
            draft_text="I build publication gates before posting.",
            approval_token="human-ok",
            account="@RobotsTJ500",
            writes_used_today=0,
            allowed_facts=[],
            brief_content=brief_table(**{"Изображение": "no"}),
        )
        self.assertTrue(ok)
        self.assertEqual(reason, "all operator gates satisfied")

    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_approve_post_blocks_missing_approval_token(self):
        ok, reason = operator_pipeline.approve_post(
            "I build publication gates.",
            None,
            "@RobotsTJ500",
            0,
            brief_content=brief_table(**{"Изображение": "no"}),
        )
        self.assertFalse(ok)
        self.assertIn("approval: NOT_SATISFIED", reason)

    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_approve_post_allows_public_write_after_quota_removed(self):
        ok, reason = operator_pipeline.approve_post(
            "I build publication gates.",
            "human-ok",
            "@RobotsTJ500",
            3,
            brief_content=brief_table(**{"Изображение": "no"}),
        )
        self.assertTrue(ok)
        self.assertEqual(reason, "all operator gates satisfied")

    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_approve_post_blocks_uncovered_fact_tokens(self):
        ok, reason = operator_pipeline.approve_post(
            "This happened in 2026.",
            "human-ok",
            "@RobotsTJ500",
            0,
            allowed_facts=["no year here"],
            brief_content=brief_table(**{"Изображение": "no"}),
        )
        self.assertFalse(ok)
        self.assertIn("factcheck: NOT_SATISFIED", reason)

    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_write_counter_missing_invalid_stale_and_current_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "write_counter.json"
            self.assertEqual(operator_pipeline.read_writes_used_today(path), 0)
            path.write_text("not json", encoding="utf-8")
            self.assertEqual(operator_pipeline.read_writes_used_today(path), 3)
            path.write_text(json.dumps({"date": "2000-01-01", "writes": 2}), encoding="utf-8")
            self.assertEqual(operator_pipeline.read_writes_used_today(path), 0)
            path.write_text(json.dumps({"date": date.today().isoformat(), "writes": 2}), encoding="utf-8")
            self.assertEqual(operator_pipeline.read_writes_used_today(path), 2)

    @pytest.mark.scenario("operators-gate.pipeline_approval")
    def test_increment_writes_and_consume_token_use_supplied_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            counter = Path(tmp) / "nested" / "write_counter.json"
            operator_pipeline.increment_writes(counter)
            self.assertEqual(operator_pipeline.read_writes_used_today(counter), 1)
            operator_pipeline.increment_writes(counter)
            self.assertEqual(operator_pipeline.read_writes_used_today(counter), 2)

            token = Path(tmp) / "approval.token"
            token.write_text("human-ok", encoding="utf-8")
            operator_pipeline.consume_approval_token(token)
            self.assertFalse(token.exists())


class TopicDedupeTests(unittest.TestCase):
    @pytest.mark.scenario("operators-gate.topic_dedupe")
    def test_tokens_lowercase_filter_stop_words_and_short_words(self):
        self.assertEqual(tokens("The SAM mesh in X, p2p tunnel 2026"), {"mesh", "tunnel", "2026"})

    @pytest.mark.scenario("operators-gate.topic_dedupe")
    def test_recent_post_overlap_threshold_is_three_tokens(self):
        draft = tokens("agentmail inbox scope smoke test")
        post = tokens("agentmail inbox scope")
        self.assertEqual(draft & post, {"agentmail", "inbox", "scope"})
        self.assertGreaterEqual(len(draft & post), 3)

    @pytest.mark.scenario("operators-gate.topic_dedupe")
    def test_manual_theme_threshold_flags_two_keyword_overlap(self):
        theme = MANUAL_THEMES[0]
        draft = tokens("alikhan whatsapp status")
        overlap = draft & theme["keywords"]
        self.assertGreaterEqual(len(overlap), theme["min_overlap"])

    @pytest.mark.scenario("operators-gate.topic_dedupe")
    def test_manual_theme_threshold_does_not_flag_single_keyword_overlap(self):
        theme = MANUAL_THEMES[0]
        draft = tokens("alikhan unrelated topic")
        overlap = draft & theme["keywords"]
        self.assertLess(len(overlap), theme["min_overlap"])


class LoopGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_loop_dir = loop_guard.LOOP_DIR
        loop_guard.LOOP_DIR = Path(self.tmp.name)

    def tearDown(self):
        loop_guard.LOOP_DIR = self.original_loop_dir
        self.tmp.cleanup()

    @pytest.mark.scenario("operators-gate.loop_guard")
    def test_check_stops_at_max_iterations(self):
        guard = Guard("maxed", max_iterations=1)
        self.assertTrue(guard.check())
        guard.iterations = 1
        self.assertFalse(guard.check())

    @pytest.mark.scenario("operators-gate.loop_guard")
    def test_check_stops_at_budget_limit(self):
        guard = Guard("budget", budget_limit=0.10)
        guard.total_cost = 0.10
        self.assertFalse(guard.check())

    @pytest.mark.scenario("operators-gate.loop_guard")
    def test_record_success_counts_iteration_cost_and_idempotency(self):
        guard = Guard("record")
        guard.record(True, cost=0.02, item_id="tweet-1")
        self.assertEqual(guard.iterations, 1)
        self.assertEqual(guard.total_cost, 0.02)
        self.assertEqual(guard.consecutive_failures, 0)
        self.assertTrue(guard.is_duplicate("tweet-1"))

    @pytest.mark.scenario("operators-gate.loop_guard")
    def test_record_failures_trip_human_escalation_threshold(self):
        guard = Guard("failures", human_escalation_threshold=2)
        guard.record(False)
        self.assertTrue(guard.check())
        guard.record(False)
        self.assertFalse(guard.check())
