# Spec Drift Log — <node-name>

> Fail-closed журнал: spec-affecting мутация без записи = нарушение.
> Append-only (старые строки не редактировать). Поля: awk -F'|' → 2=время, 3=что меняю, 4=зачем, 5=что НЕ трогаю, 6=SHA/пусто. `|` в ячейках запрещён (использовать `\|`).

| Время (UTC) | Что меняю | Зачем | Что НЕ трогаю | SHA/пусто |
|---|---|---|---|---|
| 2026-09-07T03:22 | .gitignore | ignore data/secrets/ (agentmail envs не должны попасть в git) | контент, данные, код |  |
| 2026-09-07T03:22 | data/, DRAFT_BANK_RTJ.md, SHADOWBAN_RECOVERY.md, TACTICS.md, TACTICS_GROMYKOSS.md, VOICE_PROFILE.md, VOICE_PROFILE_GROMYKOSS.md, CONTENT_BRIEF_tailcat_20260901.md, ENGINEERING_POST_TEMPLATE.md, TACTICS_GROMYKOSS_2026-09-04.md, TACTICS_GROMYKOSS_20260905.md | рабочие данные аналитики и доки голоса/тактики за 01-06.09 (зачистка рабочего дерева) | data/secrets/, serga personal files |  |
