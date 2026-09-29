# Контакт: @Itsuugo (Antonio Ojea) — 16.09.2026

## Кто это

**Antonio Ojea (@Itsuugo)** — инженер **Google Cloud** (Networking and Kubernetes), раньше Red Hat, SUSE, Midokura. Аккаунт с 2013, **1942 followers**, 5296 твитов, 24 листа. Настоящий инфраструктурный инженер-инфлюенсер в нише cloud-native, не бот.

## Что сделал

**Сегодня (16.09) сделал ретвит нашего SAM-поста** (2091532750889070867 от 23.08 — «I ran someone else's code on someone else's machine over a p2p tunnel... SAM Sovereign Agent Mesh»).

SAM-пост: 105 imp, 4❤, 1 RT (единственный RT — его). Наш пост трёхнедельной давности ожил сегодня на волне тренда.

## Почему это важно

1. **Google сегодня открыл SAM (Sovereign Agent Mesh)** — наш пост от 23.08 был про SAM ещё до анонса, и лента сегодня завалилена SAM-RT'ами (hank_aibtc, akhil_027, hasantoxr, saltyq — крупные агентные аккаунты). Наш пост попал в волну ретроспективного интереса.
2. Его RT = наш контент увидела его аудитория (1942, cloud-native + K8s инженеры) — целевая для нас.
3. Паттерн «мы писали раньше, тренд подтвердил» — сильный кейс для серии.

## Взаимодействие с chrome-agent постом (16.09)

Лайков/RT на chrome-agent пост (2100148268093055247) от него НЕ зафиксировано (likers/reposted_by пусты, 15 imp). Взаимодействие = RT SAM-поста.

## Связи/статус

- Мы не follow'им друг друга (following 232 — его нет; проверено API)
- Ответов/mentions нам не писал

## Возможные действия (на решение Сергея)

1. **Follow** — user-directed, можно сразу
2. **Reply на его RT** (не через API — non-mention 403; вручную или ждать mention)
3. Использовать момент: SAM трендит сегодня — можно сделать follow-up пост «мы писали про SAM 23.08, сегодня Google подтвердил» (если Сергей даст ок и тему)

## Хронология взаимодействия

- 23.08: наш SAM-пост
- 16.09: его RT нашего поста (в волне анонса SAM Google)

## Действия 16.09 (выполнено)

- ✅ Follow: `following:true` (API подтверждено)
- ✅ 2 лайка его оригинальных постов: SAM architecture (2091507139256766604, 23.08 — день нашего SAM-поста!) и agents.net spec (2083072179088834706, 31.07)

## Его GitHub — интересно

**github.com/aojea — Antonio Ojea.** Ведущий сетевой инженер Kubernetes-экосистемы (SIG-Network, kind/cloud-provider-kind, VRF/MPLS фон).

**Гем: `aojea/agents.net` — Agent Networking Specification (Apache-2.0, 16★, 26 коммитов, последний 15.09 — активный):**
- Спека «сетевого интерфейса между sandbox и policy-enforcing proxy»: приложения используют обычные сокеты, адаптер конвертирует соединения в HTTP CONNECT, boundary применяет политику. Сандбокс не имеет прямого внешнего пути — агент физически не может обойти политику.
- Go reference implementation (tun2connect), 6-сценарный бенчмарк-сьют (3 MicroVM режима + 3 контейнерных, включая «Double TCP Stack Tax» через slirp4netns), auth + transport-integrity регресс-тесты.
- Это **инфраструктурная проекция нашего zero-trust стека для агентов**: та же ниша, что tailcat (наш пост 02.09, 507 imp) и AWS Kiro Crew — «как дать агенту сеть без доверия».
- Твиты его: «Second iteration on my journey through agentic networking... From proxies to Un...» (27.08), «Stepped out of my Kubernetes comfort zone this year to build an internet for ag[ents]» (17.08), «Last piece for the next SAM release: the agentic architecture» (23.08 — **он сам участвует в разработке SAM!**).

## Ключевой инсайт

Itsuugo — не просто читатель: **он контрибьютор SAM** (Sovereign Agent Mesh от Google) и автор собственной спеки agent-сетей. Его RT нашего SAM-поста = признание от человека, который строит эту область. Кандидат на содержательный диалог (его agents.net ↔ наш zero-trust опыт/tailcat кейс), но API-реплай невозможен (non-mention) — только если он ответит сам или вручную.

