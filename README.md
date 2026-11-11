# gameforge-agents

Orquestador multiagente del estudio GameForge (indie unipersonal: Phaser.js + TypeScript, publica en su propia web).

Tú solo hablas con el **director** (`gameforge-director`). Él descompone tu petición en sprints y tareas atómicas y **delega automáticamente** en los 17 subagentes especialistas (uno por skill de `skills/`), esperando todos sus informes antes de responderte.

## Requisitos

- Python 3.12+ y [uv](https://docs.astral.sh/uv/)
- Una API key de Mistral (`MISTRAL_API_KEY`, créala en console.mistral.ai → API keys)

## Uso

```bash
git clone https://github.com/nebaslu/gameforge-agents.git
cd gameforge-agents
uv sync
cp .env.example .env   # pega tu MISTRAL_API_KEY
uv run --env-file .env agents chat
```

Escribe lo que quieras en el chat: solo le hablas al director y él orquesta al resto.

Comandos útiles:

- `uv run --env-file .env agents chat -m "mensaje único"` — un solo mensaje y salir
- `uv run agents info` — entrypoint y capacidades del agente
- `uv run --env-file .env agents serve` / `agents deploy` — servir o desplegar el agente (ver docs del SDK)

## Estructura

- `main.py` — exporta `agent` (el director con sus 17 subagentes); es el entrypoint del CLI `agents`.
- `gameforge/specialists.py` — carga `skills/*/SKILL.md` y construye el director y los subagentes.
- `skills/<nombre>/SKILL.md` — las 17 skills (fuente única de verdad; las mismas están en el registro de skills de Studio).
- `.vibe/skills/<nombre>/SKILL.md` — copia para Vibe CLI y la extensión de VS Code: al abrir este repo, las skills están disponibles con `/nombre-skill`.

## Especialistas (subagentes del director)

`asset-scout`, `sound-designer`, `game-designer`, `story-architect`, `lead-ts-engineer`, `genre-specialist`, `game-ui-ux`, `localization`, `web-publisher`, `qa-tester`, `best-practices-reviewer`, `backend-architect`, `backend-best-practices`, `security-lead`, `legal-privacy`, `marketing-analytics`.

## Añadir o editar una skill

1. Edita `skills/<nombre>/SKILL.md`.
2. Cópialo también a `.vibe/skills/<nombre>/SKILL.md`.
3. Reinicia el chat del agente. El director añadirá el subagente nuevo en el siguiente arranque; en Vibe CLI/VS Code, `/reload`.
