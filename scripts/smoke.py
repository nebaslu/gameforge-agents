import main

EXPECTED_SUBAGENTS = 16


def main_check() -> None:
    agent = main.agent
    assert agent.name == "gameforge-director", agent.name
    assert agent.model == "mistral-large-4", agent.model

    subs = agent.subagents
    assert len(subs) == EXPECTED_SUBAGENTS, f"expected {EXPECTED_SUBAGENTS} subagents, got {len(subs)}"
    names = {s.name for s in subs}
    assert "gameforge-director" not in names, "director must not be its own subagent"
    for s in subs:
        assert s.description, f"{s.name}: empty description"
        assert s.instructions, f"{s.name}: empty instructions"

    instructions = agent.instructions
    assert "Tabla de enrutado" in instructions
    assert "Orquestación automática con subagentes" in instructions

    print(f"OK: director '{agent.name}' with {len(subs)} subagents: {', '.join(sorted(names))}")


if __name__ == "__main__":
    main_check()
