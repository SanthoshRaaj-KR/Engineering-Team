from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Chatbot():
    """Chatbot crew - a conversational assistant with memory enabled
    across turns, so it recalls facts you mention earlier in the chat."""

    agents: list[BaseAgent]
    tasks: list[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def chat_task(self) -> Task:
        return Task(
            config=self.tasks_config['chat_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Chatbot crew"""
        # memory=True turns on CrewAI's short-term (ChromaDB), long-term
        # (SQLite) and entity memory, so each new kickoff() call can recall
        # relevant facts from earlier turns even though every kickoff is a
        # fresh task execution with no chat history in the prompt.
        # https://docs.crewai.com/concepts/memory
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            memory=True,
        )
