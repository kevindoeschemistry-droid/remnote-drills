# remnote-drills — Claude instructions

Kuta-style drill plugin for RemNote ("Wiki Sync", plugin id `wiki-sync` — never change the id: RemNote keys the card map, streaks and PDF links to it).

- Skill graph: `drills/skills.yaml` (skills), `drills/sources/*.yaml` (textbooks), `drills/courses/*.yaml` (courses), `drills/problems/*.yaml` (problems as data, preferred for numeric multi-step drills; verified by `tests/verify/data.py`). See README for how to add a skill.
- Generators/checkers: `src/drills/`. Build problems backward from clean answers; check answers by property, never by string match.
- Every generator change: `npm test` (JS checker + negative controls + KaTeX over every template × 30 seeds, then an independent sympy verifier). Numeric engineering answers need a first-principles case in `tests/verify_sympy.py` (`heat_expected`), not a copy of the generator's formula.
- `npm run build` → `dist/` + `PluginZip.zip`. Local dev: RemNote → Plugins → Build → Develop from localhost (port 3005). Published as an unlisted plugin via Build → Upload plugin.
- Bump `version` in both `package.json` and `public/manifest.json`.
