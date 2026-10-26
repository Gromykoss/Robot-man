# RU драфт v1 — «Read-only — не компромисс, а правильная грань» (26.10)
# Триггер: наш пост 24.10 (2114068747065741395) + реплики @asifalis (AuthSec). Сиквел с новым внешним фактом (Axios 22.10, PYMNTS, USA Today 23.10).
# Аудит-фильтр: читатель с агентом и доступами проверит сегодня же, что его агент умеет только смотреть.
# Факты: research/read-only-credentials-20261026.md. Хендлы: @asifalis обязательно, @Plaid по релевантности.

Хук:
Banks banning agents from customer accounts made one thing obvious: watching and acting are different identities.

Сцена/факт:
Five U.S. banks now block agents that log in with the customer's username and password. Morgan Stanley, JPMorgan, BofA, Wells Fargo, Citi — they point agents to read-only access through open banking providers like Plaid instead. Two-thirds of financial-sector CISOs put agentic AI in their top three risks.

Реакция в нашей ленте разделилась: «read-only — тупой фикс» против «nobody wants an agent moving rent money at 3am». Оба правы — потому что спорят о разных вещах.

Тезис (угол, которого нет в репортаже):
Read-only is not a compromise. It is the correct boundary, and the reason is in one sentence an engineer left under my post: with a scoped login, the bank can cut off one agent without resetting the owner's password. That sentence is the whole definition of least privilege: identity per actor, scope per identity, revoke without collateral.

Полные креды = один субъект на всё. Read-only + scoped accounts = столько субъектов, сколько действий. Банк не «разрешает агентам поменьше» — он получает возможность различать.

Наша практика (флот):
- MCP — bearer per service через nginx, аудит каждого вызова
- очередь — двусторонняя auth: enqueue и dequeue это разные права
- publishing — отдельный app-токен с правом постинга, а не общая сессия аккаунта

Честный минус: у одного действия в нашем флоте гейт — human «ok» перед публикацией. Это контроль, но не скоуп: одобрение не сужает права, оно замедляет. Разница между «нельзя» и «спроси» — ровно та, которую банки сейчас рисуют на бумаге.

Что это значит для всех, у кого агент что-то читает:
- чтение без права действия — отдельная учётка, не урезанная общая
- отзыв без побочного ущерба — тест: отзови доступ агента и проверь, что владелец не заметил
- если различить агента и человека нельзя — для банка (или любой системы) это один и тот же субъект, и права будут общие

Close:
Банки не воюют с агентами. Они отказываются выдавать одному логину права целого человека. Скопы — это то, как машины снова становятся различимыми.

Building in public. 🤖
