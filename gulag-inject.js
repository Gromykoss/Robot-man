(function () {
    "use strict";

    const TEXT_REPLACEMENTS = new Map([
        ["Sign In", "GULAG.online"],
        ["Homeserver", "СЕРВЕР"],
        ["Username", "НОМЕР ЗАКЛЮЧЕННОГО"],
        ["Password", "ПАРОЛЬ ДОСТУПА"],
        ["Log In", "ВОЙТИ В ЗОНУ"],
        ["Log in with SSO", "ВХОД ЧЕРЕЗ ЕДИНЫЙ ПРОПУСК"],
        ["or", "или"],
        ["Choose a room on the left side.", "ВЫБЕРИТЕ КАМЕРУ"],
        ["Fetching available login options...", "ПРОВЕРКА ПРОПУСКНОГО ПУНКТА..."],
        ["Go back", "НАЗАД"],
        ["Loading your conversations…", "ЗАГРУЗКА ПЕРЕПИСКИ…"],
    ]);

    const PLACEHOLDER_REPLACEMENTS = new Map([
        ["Your matrix homeserver", "сервер зоны"],
        ["Username", "номер"],
        ["Password", "пароль"],
    ]);

    let debounceTimer = 0;
    let observer = null;
    let isApplying = false;

    function ensureRuntimeStyle() {
        if (document.getElementById("gulag-inject-style")) {
            return;
        }
        const style = document.createElement("style");
        style.id = "gulag-inject-style";
        style.textContent = `
            .hydrogen .PreSessionScreen > .GulagLoginPanel {
                width: 420px !important;
                max-width: calc(100vw - 40px) !important;
                border: 2px solid #8a7a60 !important;
                outline: 1px solid #d4c5a0 !important;
                outline-offset: 4px !important;
            }
            .hydrogen .GulagLoginPanel > .PasswordLoginView,
            .hydrogen .GulagLoginPanel > .LoginView_sso,
            .hydrogen .GulagLoginPanel > .StartSSOLoginView,
            .hydrogen .GulagLoginPanel > .LoginView_separator,
            .hydrogen .GulagLoginPanel > p,
            .hydrogen .GulagLoginPanel > .logo {
                width: auto !important;
                max-width: none !important;
                background: transparent !important;
                border: 0 !important;
                outline: 0 !important;
                box-shadow: none !important;
                backdrop-filter: none !important;
            }
            .hydrogen .GulagLoginPanel > .PasswordLoginView,
            .hydrogen .GulagLoginPanel > .LoginView_sso,
            .hydrogen .GulagLoginPanel > .StartSSOLoginView {
                padding: 0 !important;
            }
            .hydrogen .GulagLoginPanel > .logo {
                padding: 0 !important;
            }
            .hydrogen .GulagBarbedWire {
                background: transparent !important;
                border: 0 !important;
                outline: 0 !important;
                box-shadow: none !important;
                backdrop-filter: none !important;
                padding: 0 !important;
            }
            .hydrogen .PreSessionScreen .LoginView_sso,
            .hydrogen .PreSessionScreen .GulagLoginPanel a[href*="github"],
            .hydrogen .PreSessionScreen .GulagLoginPanel a[href*="Github"],
            .hydrogen .PreSessionScreen .LoginView_back,
            .hydrogen .PreSessionScreen .logo {
                display: none !important;
            }

        `;
        document.head.appendChild(style);
    }

    function setStyles(element, styles) {
        for (const [property, value] of Object.entries(styles)) {
            element.style[property] = value;
        }
    }

    function setText(element, text) {
        if (element && element.textContent !== text) {
            element.textContent = text;
        }
    }

    function replaceExactText(root) {
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
            acceptNode(node) {
                const parent = node.parentElement;
                if (!parent || ["SCRIPT", "STYLE", "TEXTAREA"].includes(parent.tagName)) {
                    return NodeFilter.FILTER_REJECT;
                }
                return NodeFilter.FILTER_ACCEPT;
            }
        });

        const nodes = [];
        while (walker.nextNode()) {
            nodes.push(walker.currentNode);
        }

        for (const node of nodes) {
            const trimmed = node.textContent.trim();
            if (TEXT_REPLACEMENTS.has(trimmed)) {
                const next = node.textContent.replace(trimmed, TEXT_REPLACEMENTS.get(trimmed));
                if (node.textContent !== next) {
                    node.textContent = next;
                }
            } else if (trimmed.includes("You will connect to")) {
                const next = node.textContent.replace("You will connect to", "ПОДКЛЮЧЕНИЕ К");
                if (node.textContent !== next) {
                    node.textContent = next;
                }
            }
        }
    }

    function replacePlaceholders(root) {
        root.querySelectorAll("input[placeholder]").forEach(input => {
            const replacement = PLACEHOLDER_REPLACEMENTS.get(input.getAttribute("placeholder"));
            if (replacement) {
                input.setAttribute("placeholder", replacement);
            }
        });
    }

    function replaceLoginLabels(root) {
        const labels = {
            homeserver: "СЕРВЕР",
            username: "НОМЕР ЗАКЛЮЧЕННОГО",
            password: "ПАРОЛЬ ДОСТУПА",
        };
        for (const [id, text] of Object.entries(labels)) {
            const label = root.querySelector(`label[for="${id}"]`);
            if (label) {
                setText(label, text);
            }
        }
    }

    function ensureLoginPanel(screen) {
        let panel = screen.querySelector(":scope > .GulagLoginPanel");
        if (!panel) {
            panel = document.createElement("div");
            panel.className = "GulagLoginPanel";

            const movable = Array.from(screen.childNodes).filter(node => {
                return !(node.nodeType === Node.ELEMENT_NODE &&
                    node.classList.contains("GulagLoginPanel"));
            });
            for (const node of movable) {
                panel.appendChild(node);
            }
            screen.appendChild(panel);
        }

        setStyles(panel, {
            position: "relative",
            boxSizing: "border-box",
            width: "420px",
            maxWidth: "calc(100vw - 40px)",
            border: "2px solid #8a7a60",
            outline: "1px solid #d4c5a0",
            outlineOffset: "4px",
        });

        return panel;
    }

    function ensureStamp(container, className, text, styles, insertAfter) {
        let stamp = container.querySelector(`:scope > .${className}`);
        if (!stamp) {
            stamp = document.createElement("div");
            stamp.className = className;
            stamp.setAttribute("aria-hidden", "true");
            setText(stamp, text);
            if (insertAfter && insertAfter.parentNode === container) {
                insertAfter.after(stamp);
            } else {
                container.appendChild(stamp);
            }
        }
        setText(stamp, text);
        setStyles(stamp, styles);
        return stamp;
    }

    function applyLogin(screen) {
        ensureRuntimeStyle();

        setStyles(screen, {
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            minHeight: "100vh",
            width: "100%",
            margin: "0",
            position: "relative",
            boxSizing: "border-box",
        });

        const panel = ensureLoginPanel(screen);

        ensureStamp(panel, "GulagBarbedWire", "✧ ✧ ✧ ✧ ✧ ✧ ✧ ✧ ✧ ✧ ✧", {
            position: "absolute",
            top: "-62px",
            left: "50%",
            transform: "translateX(-50%)",
            width: "420px",
            maxWidth: "calc(100vw - 40px)",
            textAlign: "center",
            color: "#8a7a60",
            fontSize: "18px",
            letterSpacing: "8px",
            opacity: "0.65",
            pointerEvents: "none",
            background: "transparent",
            border: "0",
            outline: "0",
            padding: "0",
            zIndex: "2",
        });

        replaceLoginLabels(panel);
        replaceExactText(panel);
        replacePlaceholders(panel);

        // Hide Hydrogen version footer
        panel.querySelectorAll("a").forEach(a => {
            if (a.textContent.includes("Hydrogen") || a.href.includes("github")) {
                a.style.display = "none";
            }
        });

        const h1 = panel.querySelector("h1");
        if (h1) {
            setText(h1, "GULAG.online");
            setStyles(h1, {
                color: "#8b1a1a",
                fontFamily: "Georgia, 'Courier New', Courier, monospace",
                letterSpacing: "5px",
                textTransform: "uppercase",
            });
            ensureStamp(panel, "GulagDspStamp", "✦ ДСП ✦", {
                position: "absolute",
                top: "10px",
                right: "15px",
                transform: "rotate(-5deg)",
                color: "#7a1515",
                opacity: "0.7",
                fontSize: "11px",
                letterSpacing: "2px",
                pointerEvents: "none",
                zIndex: "3",
            }, h1.previousElementSibling);

            // Add subtitle "СИСТЕМА ВНУТРЕННЕЙ СВЯЗИ"
            let subtitle = panel.querySelector(".GulagSubtitle");
            if (!subtitle) {
                subtitle = document.createElement("div");
                subtitle.className = "GulagSubtitle";
                subtitle.textContent = "СИСТЕМА ВНУТРЕННЕЙ СВЯЗИ";
                subtitle.style.cssText = "text-align:center;font-size:9px;letter-spacing:3px;color:#8b1a1a;text-transform:uppercase;margin:4px 0 8px;font-family:'Courier New',Courier,monospace;";
                h1.after(subtitle);
            }

            // Add gold divider + "АВТОРИЗАЦИЯ" + gold divider
            let authSection = panel.querySelector(".GulagAuthSection");
            if (!authSection) {
                authSection = document.createElement("div");
                authSection.className = "GulagAuthSection";
                authSection.innerHTML = '<hr style="border:none;border-top:1px solid #8a7a60;width:70%;margin:8px auto;">' +
                '<div style="text-align:center;font-size:9px;letter-spacing:3px;color:#8b1a1a;text-transform:uppercase;margin:4px 0;">АВТОРИЗАЦИЯ</div>' +
                '<hr style="border:none;border-top:1px solid #8a7a60;width:70%;margin:8px auto;">';
                subtitle.after(authSection);
            }
        }

        screen.classList.add('gulag-ready');

        const loginButton = panel.querySelector("button.button-action.primary");
        if (loginButton) {
            setText(loginButton, "ВОЙТИ В ЗОНУ");

            // Add "ПОДАТЬ ПРОШЕНИЕ НА ПЕРЕПИСКУ" after the button-row
            const buttonRow = loginButton.closest(".button-row");
            let petitionBtn = panel.querySelector(".GulagPetitionBtn");
            if (!petitionBtn && buttonRow) {
                petitionBtn = document.createElement("a");
                petitionBtn.className = "GulagPetitionBtn button-action primary";
                petitionBtn.href = "/anketa.html";
                petitionBtn.textContent = "ПОДАТЬ ПРОШЕНИЕ НА ПЕРЕПИСКУ";
                petitionBtn.style.display = "block";
                petitionBtn.style.width = "100%";
                petitionBtn.style.marginTop = "8px";
                buttonRow.after(petitionBtn);
            }
        }
    }

    function ensureLeftPanelTitle(session) {
        const leftPanel = session.querySelector(".LeftPanel");
        if (!leftPanel || leftPanel.querySelector(":scope > .GulagRoomsTitle")) {
            return;
        }
        const title = document.createElement("div");
        title.className = "GulagRoomsTitle";
        setText(title, "▸ СПИСОК КАМЕР");
        setStyles(title, {
            padding: "14px 16px 6px",
            fontSize: "10px",
            letterSpacing: "3px",
            color: "#b8a18b",
            textTransform: "uppercase",
            borderBottom: "1px solid #8a7a60",
            flex: "0 0 auto",
        });

        const roomList = leftPanel.querySelector(".RoomList");
        leftPanel.insertBefore(title, roomList || leftPanel.firstChild);
    }

    function applySession(session) {
        replaceExactText(session);
        replacePlaceholders(session);

        session.querySelectorAll(".room-placeholder").forEach(placeholder => {
            setText(placeholder, "ВЫБЕРИТЕ КАМЕРУ");
        });

        ensureLeftPanelTitle(session);
        session.classList.add("gulag-ready");
    }

    function applyMutations() {
        if (isApplying || !document.body) {
            return;
        }
        isApplying = true;
        try {
            document.querySelectorAll(".PreSessionScreen").forEach(applyLogin);
            document.querySelectorAll(".SessionView").forEach(applySession);
        } finally {
            isApplying = false;
        }
    }

    function scheduleApply() {
        window.clearTimeout(debounceTimer);
        if (!window._gulagFirstRun) {
            window._gulagFirstRun = true;
            applyMutations();
            return;
        }
        debounceTimer = window.setTimeout(applyMutations, 200);
    }

    function start() {
        if (!document.body) {
            document.addEventListener("DOMContentLoaded", start, {once: true});
            return;
        }
        if (!observer) {
            observer = new MutationObserver(scheduleApply);
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                characterData: true,
            });
        }
        scheduleApply();
    }

    // ============================================================
    // BUTTON FIXES — Hydrogen button behavior patches
    // Fix 1: Send file — skip 3-option menu, open file picker directly
    // Fix 2: Room options (👥) — show members page directly
    // ============================================================

    function patchSendFileButton() {
        const sendFileBtn = document.querySelector('.sendFile');
        if (!sendFileBtn || sendFileBtn._gulagPatched) return;
        sendFileBtn._gulagPatched = true;

        // Create hidden file input
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.style.display = 'none';
        fileInput.multiple = true;
        document.body.appendChild(fileInput);

        // When files are selected, dispatch custom event
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                const event = new CustomEvent('gulag-file-selected', {
                    detail: { files: Array.from(this.files) }
                });
                document.dispatchEvent(event);
            }
            // Reset so same file can be selected again
            this.value = '';
        });

        // Intercept click on sendFile button — capture phase to beat Hydrogen
        sendFileBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            fileInput.click();
            return false;
        }, true);

        // MutationObserver to hide the popup menu if it appears anyway
        const popupObserver = new MutationObserver(function(mutations) {
            for (const mutation of mutations) {
                for (const node of mutation.addedNodes) {
                    if (!node.classList) continue;
                    const isPopup = node.classList.contains('popupContainer') ||
                        (node.querySelector && node.querySelector('.popupContainer'));
                    if (!isPopup) continue;
                    // Check if popup contains send-related menu items
                    const menuItems = node.querySelectorAll
                        ? node.querySelectorAll('.menu-item')
                        : [];
                    const texts = Array.from(menuItems).map(m => m.textContent || '');
                    if (texts.some(t => /send\s+(video|picture|file)/i.test(t))) {
                        node.style.display = 'none';
                        setTimeout(function() {
                            if (node.parentNode) node.parentNode.removeChild(node);
                        }, 100);
                    }
                }
            }
        });
        popupObserver.observe(document.body, { childList: true, subtree: true });
    }

    function patchRoomOptionsButton() {
        const roomOptionsBtn = document.querySelector('.room-options');
        if (!roomOptionsBtn || roomOptionsBtn._gulagPatched) return;
        roomOptionsBtn._gulagPatched = true;

        roomOptionsBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();

            // Navigate to room members/details
            const hash = window.location.hash;
            const roomMatch = hash.match(/room\/(![^/?]+)/);
            const sessionMatch = hash.match(/session\/(\d+)/);

            if (roomMatch && sessionMatch) {
                const roomId = decodeURIComponent(roomMatch[1]);
                const sessionId = sessionMatch[1];
                // REMOVED: window.location.hash = '#/session/' + sessionId + '/room/' +
                    // REMOVED: encodeURIComponent(roomId) + '/members';

            }

            return false;
        }, true);
    }

    function applyButtonFixes() {
        patchSendFileButton();
        patchRoomOptionsButton();
    }

    // ============================================================
    // Extend the start sequence to also apply button fixes
    // ============================================================
    const _origScheduleApply = scheduleApply;
    scheduleApply = function() {
        _origScheduleApply();
        // Apply button fixes on a short delay (after room view renders)
        setTimeout(applyButtonFixes, 1000);
    };

    start();
    // Fallback: show page after 3s even if injection fails
    setTimeout(function() {
        document.querySelectorAll('.PreSessionScreen, .SessionView').forEach(function(el) {
            el.classList.add('gulag-ready');
        });
    }, 3000);
})();

// ===== FIX 3: CUSTOM MEMBER LIST POPUP =====
(function() {
    const ACCESS_TOKEN = 'syt_Z3JvbXlrb3Nz_NkHNxYQupRnmnDquIOge_0evxpg';
    
    function getCurrentRoomId() {
        var hash = window.location.hash;
        var m = hash.match(/room\/(![^/?]+)/);
        return m ? decodeURIComponent(m[1]) : null;
    }
    
    var currentUserId = null;
    
    function getCurrentUserId() {
        if (currentUserId) return currentUserId;
        // Try to get from localStorage or Hydrogen store
        try {
            var hash = window.location.hash;
            var m = hash.match(/session\/(\d+)/);
            if (m) {
                // Store the session id — we'll try to figure out the user later
            }
        } catch(e) {}
        // Fallback: fetch whoami
        fetch('/_matrix/client/v3/account/whoami?access_token=' + ACCESS_TOKEN)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.user_id) currentUserId = data.user_id;
            })
            .catch(function() {});
        return null;
    }
    
    function kickMember(roomId, userId) {
        if (!roomId || !userId) return;
        if (confirm('Удалить участника ' + userId + '?')) {
            fetch('/_matrix/client/v3/rooms/' + encodeURIComponent(roomId) + '/kick?access_token=' + ACCESS_TOKEN, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user_id: userId, reason: 'Изгнан администратором'})
            })
            .then(function(r) {
                if (!r.ok) throw new Error('Kick failed: ' + r.status);
                // Refresh the list
                fetchAndShowMembers();
            })
            .catch(function(err) {
                alert('Ошибка удаления: ' + err.message);
            });
        }
    }
    
    function inviteUser(roomId, userId) {
        if (!roomId || !userId) return;
        fetch('/_matrix/client/v3/rooms/' + encodeURIComponent(roomId) + '/invite?access_token=' + ACCESS_TOKEN, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user_id: userId})
        })
        .then(function(r) {
            if (!r.ok) throw new Error('Invite failed: ' + r.status);
            fetchAndShowMembers();
        })
        .catch(function(err) {
            alert('Ошибка приглашения: ' + err.message);
        });
    }
    
    function copyInviteLink() {
        var roomId = getCurrentRoomId();
        if (!roomId) return;
        var hash = window.location.hash;
        var sessionMatch = hash.match(/session\/(\d+)/);
        var sessionId = sessionMatch ? sessionMatch[1] : '';
        var link = 'https://spacegulag.online/hydrogen/#/session/' + sessionId + '/room/' + encodeURIComponent(roomId);
        
        if (navigator.clipboard && navigator.clipboard.writeText) {
            navigator.clipboard.writeText(link).then(function() {
                showNotification('Ссылка скопирована');
            }).catch(function() {
                fallbackCopy(link);
            });
        } else {
            fallbackCopy(link);
        }
    }
    
    function fallbackCopy(text) {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try {
            document.execCommand('copy');
            showNotification('Ссылка скопирована');
        } catch(e) {
            alert('Не удалось скопировать ссылку');
        }
        document.body.removeChild(ta);
    }
    
    function showNotification(msg) {
        var n = document.createElement('div');
        n.style.cssText = 'position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:#1a1510;color:#d4c5a0;border:1px solid #8b1a1a;padding:10px 20px;font-family:"Courier New",monospace;font-size:13px;z-index:10000;';
        n.textContent = msg;
        document.body.appendChild(n);
        setTimeout(function() { n.remove(); }, 2000);
    }
    
    function searchUsers(query, callback) {
        if (!query || query.length < 2) {
            callback([]);
            return;
        }
        var cleanQuery = query.replace(/^@/, '');
        fetch('/_matrix/client/v3/user_directory/search?access_token=' + ACCESS_TOKEN, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({search_term: cleanQuery, limit: 5})
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            callback(data.results || []);
        })
        .catch(function() {
            callback([]);
        });
    }
    
    function createMemberPopup(members) {
        var roomId = getCurrentRoomId();
        if (!roomId) return;
        
        // Remove existing popup
        var existing = document.querySelector('.gulag-member-popup');
        if (existing) existing.remove();
        
        var overlay = document.createElement('div');
        overlay.className = 'gulag-member-popup';
        overlay.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);z-index:9999;display:flex;align-items:center;justify-content:center;font-family:"Courier New",monospace;';
        
        var box = document.createElement('div');
        box.style.cssText = 'background:#1a1510;border:2px solid #8b1a1a;padding:20px;max-width:380px;width:90%;max-height:80vh;overflow-y:auto;';
        
        // Header
        var hdr = document.createElement('div');
        hdr.style.cssText = 'color:#d4c5a0;font-size:16px;font-weight:bold;border-bottom:1px solid #4a3a25;padding-bottom:10px;margin-bottom:10px;display:flex;justify-content:space-between;';
        hdr.innerHTML = '<span>👥 УЧАСТНИКИ (' + members.length + ')</span><span style="cursor:pointer;color:#8b1a1a;" onclick="this.closest(\'.gulag-member-popup\').remove()">✕</span>';
        box.appendChild(hdr);
        
        // Member list container
        var listContainer = document.createElement('div');
        listContainer.style.cssText = 'max-height:300px;overflow-y:auto;margin-bottom:10px;';
        
        // Member list
        members.forEach(function(m, i) {
            var row = document.createElement('div');
            row.style.cssText = 'display:flex;align-items:center;padding:6px 0;border-bottom:1px solid #2a1f12;';
            
            var avatar = document.createElement('div');
            avatar.style.cssText = 'width:32px;height:32px;background:#6b1010;color:#d4c5a0;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:14px;margin-right:10px;flex-shrink:0;';
            avatar.textContent = (m.displayName || m.userId)[0].toUpperCase();
            row.appendChild(avatar);
            
            var info = document.createElement('div');
            info.style.cssText = 'flex:1;min-width:0;';
            var name = document.createElement('div');
            name.style.cssText = 'color:#d4c5a0;font-size:13px;font-weight:bold;';
            name.textContent = m.displayName || m.userId.split(':')[0].replace('@', '');
            info.appendChild(name);
            var uid = document.createElement('div');
            uid.style.cssText = 'color:#6a5a40;font-size:10px;overflow:hidden;text-overflow:ellipsis;';
            uid.textContent = m.userId;
            info.appendChild(uid);
            row.appendChild(info);
            
            // Delete button — only for other users, not self
            var isSelf = m.userId === currentUserId;
            if (!isSelf) {
                var delBtn = document.createElement('button');
                delBtn.style.cssText = 'background:#8b1a1a;color:#d4c5a0;border:1px solid #5a1010;cursor:pointer;font-family:"Courier New",monospace;font-size:11px;padding:4px 8px;margin-left:6px;flex-shrink:0;';
                delBtn.textContent = '✕';
                delBtn.title = 'Удалить участника';
                delBtn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    kickMember(roomId, m.userId);
                });
                row.appendChild(delBtn);
            }
            
            listContainer.appendChild(row);
        });
        
        box.appendChild(listContainer);
        
        // --- Search + Add section ---
        var searchSection = document.createElement('div');
        searchSection.style.cssText = 'border-top:1px solid #4a3a25;padding-top:10px;margin-bottom:10px;';
        
        var searchRow = document.createElement('div');
        searchRow.style.cssText = 'display:flex;gap:6px;';
        
        var searchInput = document.createElement('input');
        searchInput.type = 'text';
        searchInput.placeholder = '@username для добавления';
        searchInput.style.cssText = 'flex:1;background:#080603;border:1px solid #4a3a25;color:#d4c5a0;padding:6px 8px;font-family:"Courier New",monospace;font-size:12px;outline:none;';
        searchRow.appendChild(searchInput);
        
        var addBtn = document.createElement('button');
        addBtn.style.cssText = 'background:#4a3a25;color:#d4c5a0;border:1px solid #6a5a40;cursor:pointer;font-family:"Courier New",monospace;font-size:11px;padding:6px 10px;flex-shrink:0;';
        addBtn.textContent = 'ДОБАВИТЬ';
        searchRow.appendChild(addBtn);
        
        searchSection.appendChild(searchRow);
        
        // Search results container
        var resultsContainer = document.createElement('div');
        resultsContainer.style.cssText = 'margin-top:6px;display:none;';
        searchSection.appendChild(resultsContainer);
        
        // Search on input
        var searchTimer = 0;
        searchInput.addEventListener('input', function() {
            window.clearTimeout(searchTimer);
            var q = searchInput.value.trim();
            if (q.length < 2) {
                resultsContainer.style.display = 'none';
                resultsContainer.innerHTML = '';
                return;
            }
            searchTimer = window.setTimeout(function() {
                searchUsers(q, function(results) {
                    resultsContainer.innerHTML = '';
                    if (results.length === 0) {
                        resultsContainer.style.display = 'none';
                        return;
                    }
                    resultsContainer.style.display = 'block';
                    results.forEach(function(r) {
                        var resRow = document.createElement('div');
                        resRow.style.cssText = 'display:flex;align-items:center;padding:4px 6px;cursor:pointer;border-bottom:1px solid #2a1f12;';
                        resRow.style.background = '#0f0b07';
                        resRow.addEventListener('mouseenter', function() { resRow.style.background = '#1a1510'; });
                        resRow.addEventListener('mouseleave', function() { resRow.style.background = '#0f0b07'; });
                        
                        var resName = document.createElement('span');
                        resName.style.cssText = 'color:#d4c5a0;font-size:12px;flex:1;';
                        resName.textContent = (r.display_name || r.user_id || '');
                        resRow.appendChild(resName);
                        
                        var resUid = document.createElement('span');
                        resUid.style.cssText = 'color:#6a5a40;font-size:10px;';
                        resUid.textContent = r.user_id || '';
                        resRow.appendChild(resUid);
                        
                        resRow.addEventListener('click', function() {
                            inviteUser(roomId, r.user_id);
                            resultsContainer.innerHTML = '';
                            resultsContainer.style.display = 'none';
                            searchInput.value = '';
                        });
                        
                        resultsContainer.appendChild(resRow);
                    });
                });
            }, 300);
        });
        
        // Add button click: treat as direct invite by user_id
        addBtn.addEventListener('click', function() {
            var q = searchInput.value.trim();
            if (!q) return;
            var userId = q.startsWith('@') ? q : '@' + q;
            if (!userId.includes(':')) {
                userId += ':spacegulag.online';
            }
            inviteUser(roomId, userId);
            searchInput.value = '';
            resultsContainer.innerHTML = '';
            resultsContainer.style.display = 'none';
        });
        
        box.appendChild(searchSection);
        
        // --- Invite link button ---
        var linkBtn = document.createElement('button');
        linkBtn.style.cssText = 'background:#4a3a25;color:#d4c5a0;border:1px solid #6a5a40;cursor:pointer;font-family:"Courier New",monospace;font-size:12px;padding:8px 12px;width:100%;text-align:center;margin-bottom:8px;';
        linkBtn.textContent = '📋 ССЫЛКА-ПРИГЛАШЕНИЕ';
        linkBtn.addEventListener('click', copyInviteLink);
        box.appendChild(linkBtn);
        
        overlay.appendChild(box);
        
        // Close on overlay click
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) overlay.remove();
        });
        
        document.body.appendChild(overlay);
        
        // Focus search input
        setTimeout(function() { searchInput.focus(); }, 100);
    }
    
    function fetchAndShowMembers() {
        var roomId = getCurrentRoomId();
        if (!roomId) return;
        
        // Fetch current user info
        getCurrentUserId();
        
        fetch('/_matrix/client/v3/rooms/' + encodeURIComponent(roomId) + '/members?access_token=' + ACCESS_TOKEN)
            .then(function(r) { return r.json(); })
            .then(function(data) {
                var members = (data.chunk || []).filter(function(m) {
                    return m.type === 'm.room.member' && m.content && m.content.membership === 'join';
                }).map(function(m) {
                    return {
                        userId: m.user_id || m.state_key,
                        displayName: (m.content || {}).displayname || '',
                    };
                });
                // Deduplicate by userId
                var seen = {};
                members = members.filter(function(m) {
                    if (seen[m.userId]) return false;
                    seen[m.userId] = true;
                    return true;
                });
                createMemberPopup(members);
            })
            .catch(function() {
                // Fallback: show simple count
                createMemberPopup([{userId: 'Загрузка не удалась', displayName: 'Попробуйте позже'}]);
            });
    }
    
    // Patch the room-options button to show popup instead of navigating
    function patchRoomOptionsForPopup() {
        var btn = document.querySelector('.room-options');
        if (!btn || btn._gulagPopupPatched) return;
        btn._gulagPopupPatched = true;
        
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            fetchAndShowMembers();
            return false;
        }, true);
    }
    
    // Run on page changes
    patchRoomOptionsForPopup();
    window.addEventListener('hashchange', function() {
        setTimeout(patchRoomOptionsForPopup, 500);
    });
    
    var obs = new MutationObserver(function() {
        if (document.querySelector('.room-options')) {
            patchRoomOptionsForPopup();
        }
    });
    obs.observe(document.body, {childList: true, subtree: true});
})();
