from pathlib import Path

from mistralai import agents

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"
MODEL = "mistral-large-4"
DIRECTOR_SKILL = "gameforge-director"

ORCHESTRATION_RULES = """
## Orquestación automática con subagentes

Eres el agente raíz de un sistema multiagente: tienes subagentes especialistas (uno por skill del estudio). Reglas:

1. Para cada petición del usuario, descompón primero en sprints y tareas atómicas.
2. Inicia el subagente especialista adecuado para cada tarea usando su nombre. Si varias tareas son independientes, inicia varios subagentes en paralelo.
3. ESPERA a que TODOS los subagentes terminen y te informen antes de responder al usuario.
4. Integra los informes y responde al usuario con el plan o el resumen final.
5. NUNCA hagas tú el trabajo de un especialista: siempre delega en el subagente correspondiente (usa la tabla de enrutado de arriba).
6. Si un paso depende del resultado de otro, ejecútalos en secuencia: inicia el subagente, espera su informe y luego inicia el siguiente.
"""


def _parse_skill(text: str) -> tuple[str, str, str]:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
        meta: dict[str, str] = {}
        for line in lines[1:end]:
            if ":" in line:
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip()
        body = "\n".join(lines[end + 1:]).strip()
        return meta.get("name", ""), meta.get("description", ""), body
    return "", "", text.strip()


def load_skills() -> dict[str, tuple[str, str]]:
    skills: dict[str, tuple[str, str]] = {}
    for skill_file in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        name, description, body = _parse_skill(skill_file.read_text(encoding="utf-8"))
        skills[name] = (description, body)
    return skills


def build_subagents(skills: dict[str, tuple[str, str]]) -> list:
    subagents = []
    for name, (description, body) in skills.items():
        if name == DIRECTOR_SKILL:
            continue
        subagents.append(
            agents.Subagent(
                name=name,
                description=description,
                instructions=body,
                builtins=agents.Builtins(subagents=False),
            )
        )
    return subagents


def build_director():
    skills = load_skills()
    _description, body = skills[DIRECTOR_SKILL]
    return agents.Agent(
        model=MODEL,
        name=DIRECTOR_SKILL,
        instructions=body + ORCHESTRATION_RULES,
        subagents=build_subagents(skills),
    )
