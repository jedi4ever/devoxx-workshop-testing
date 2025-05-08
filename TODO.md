- Finish examples mcp & agents

- Custom tool, solver, scorer, agent

- Add context - RAG
- Langchain ?

- Templated examples uitwerken

- Shortcut to run cmd-enter
- inspect view correct directory

- agent as scorer ? works as solver

    using await agent.run()

    from inspect_ai.agent import run

    state = await run(
        web_surfer(), "What were the 3 most popular movies of 2020?"
    )
    print(f"The most popular movies were: {state.output.completion}")

- temp API keys - OpenAI
