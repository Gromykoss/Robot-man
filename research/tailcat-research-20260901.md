# Tailcat — ресерч 01.09.2026

## Что это
- Open-source Go-пакет + CLI «netcat поверх data plane Tailscale» — WireGuard шифрование + NAT traversal + DERP relay, БЕЗ control plane.
- «Tailscale без Tailscale, by Tailscale». Открыт 26–31.08.2026 на конференции TailscaleUp.
- GitHub: github.com/tailscale/tailcat — 5.4k stars, 187 forks, BSD-3-Clause; GitHub-репо создан 2024-10-29 (верифицировано GitHub API 01.09); 10.4k коммитов — это перенесённая внутр. история (claim «с 09/2023» — из README/блога самого Тейлскейла, не независимо верифицировано; в пост без оговорки не ставить).
- Блог: tailscale.com/blog/tailcat. Автор: Brad Fitzpatrick (bradfitz) — создатель memcached, OpenID, Go http2, late-stage co-founder Tailscale.

## Как работает
- Сервер: keypair → адрес `tc + base64(CBOR(pubkey+DERP bootstrap))`, шарится out-of-band или через DNS TXT.
- Клиент: `MEOW`-хендшейк через DERP → userspace TCP стек поверх WireGuard → прямое UDP-соединение (DERP только fallback).
- НЕТ: IP, аккаунтов, логинов, SSO, control plane, root, зависимости от компании Tailscale (если свой derper).
- Всегда userspace: никаких TUN-устройств и правок роутинга. Скрытые IPv6 из pubkey на wire — невидимы юзеру.
- SOCKS-режим: запускает дочерний процесс (curl и т.п.) через локальный SOCKS — программы «не знают» про tailcat.

## Цифры/факты
- Твит Tailscale: 5.2k лайков. HN: 684 points, 133 комментария (верифицировано Algolia API 01.09).
- 5.4k stars GitHub за ~неделю с открытия.
- Публичные DERP-релеи Tailscale (tailcat.dev/derpmap.json) — rate-limited, без SLA, можно и нужно поднимать свои (derper open source).
- ⚠️ Stability: НЕТ обещаний API/CLI/wire-формата; релеи могут отозвать в любой момент. Это эксперимент, не продукт.

## Ключевой контент-угол: agents
Брэд в блоге прямо: главный повод вынести tailcat наружу — AI-агенты. Даёт своим sandboxed-агентам доступ к экзотическому железу:
- fleet of Raspberry Pi каждого поколения;
- EC2-инстанс с kexec-ребутом соседней машины (порт Tailscale в UEFI/Nitro ENA на Go/Tamago);
- Windows-хост с циклами create/destroy Hyper-V VM для дебага рантайма Go.
→ «Два шелла в двух мирах + соединить, не трогая системный конфиг» — идеальный примитив для агентных сетей. Демо tailcat-for-minecraft как транспорт.

## Оценка для @RobotsTJ500 контента
**Ценность: ВЫСОКАЯ (9/10).**
1. Наша тема 1-в-1: агентные инфраструктуры. Брэд сам framing'ает через agents — это не натяжка.
2. Свежесть: релиз 3-5 дней, HN ещё тёплый, можно зайти в волну.
3. Личный бренд автора — story (написал в самолёте 2023, лежал 3 года, вытащили из-за агентов) = готовая драматургия.
4. Можно связать с нашим AI Village / SAM / нашим опытом связывания VPS + YC-сервера.
5. Риск-честность: нет API-гарантий, нет SLA — обязательно упомянуть (наш стандарт no-hype).

## Риски/минусы (для честности поста)
- Эксперимент: wire format может поменяться, релеи без SLA.
- «Just use WireGuard/ssh» контраргумент: tailcat решает NAT traversal + DERP без конфигов — это и есть ценность.
- Не замена Tailscale/Headscale для постоянной инфры — это ephemeral-примитив.
