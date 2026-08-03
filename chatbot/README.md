# Chatbot Crew

Welcome to the Chatbot Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/chatbot/config/agents.yaml` to define your agents
- Modify `src/chatbot/config/tasks.yaml` to define your tasks
- Modify `src/chatbot/crew.py` to add your own logic, tools and specific args
- Modify `src/chatbot/main.py` to add custom inputs for your agents and tasks

## Running the Project

To run a single, one-off message through the crew:

```bash
$ crewai run
```

To start an interactive chat session in the terminal:

```bash
$ uv run chat
```

## Understanding Your Crew

The chatbot Crew is a single conversational `assistant` agent that responds to `{user_message}`, defined in `config/agents.yaml` and `config/tasks.yaml`.

## Memory (`memory=True`)

`src/chatbot/crew.py` sets `memory=True` on the `Crew`. This turns on CrewAI's
short-term (ChromaDB), long-term (SQLite) and entity memory. Each turn in
`chat()` is its own `crew.kickoff()` call with no chat history in the
prompt — memory is what lets the agent recall facts from earlier turns.

To see it working, run `uv run chat` and try:

```
You: Hi, my name is Alex and I love hiking.
You: What's my name and what do I like?
```

The second reply should reference your name and hobby from the first turn.
Short-term memory persists for the lifetime of the crew instance (i.e. across
turns within one `chat()` session); long-term/entity memory is written to
disk (`.crewai` storage by default) and can persist across separate runs too.
Reset it anytime with:

```bash
crewai reset-memories -a
```

## Support

For support, questions, or feedback regarding the Chatbot Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
