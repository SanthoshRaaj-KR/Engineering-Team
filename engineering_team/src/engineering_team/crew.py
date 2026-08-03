from crewai import Agent, Task
from crewai.project import CrewBase, agent, task
from crewai.agents.agent_builder.base_agent import BaseAgent

from models.product import ProductRequirementSpecification
from models.ai import AIAssessment
from models.engineering import EngineeringExecutionPlan
from models.innovation import InnovationReport
from models.implementation import ImplementationReport
from models.qa import QAReport


@CrewBase
class EngineeringTeam:
    """Engineering Team"""

    agents: list[BaseAgent]
    tasks: list[Task]

    # ------------------------------------------------------------------
    # Agents
    # ------------------------------------------------------------------

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["product_manager"],
            verbose=True,
        )

    @agent
    def engineering_manager(self) -> Agent:
        return Agent(
            config=self.agents_config["engineering_manager"],
            verbose=True,
        )

    @agent
    def ai_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["ai_engineer"],
            verbose=True,
        )

    @agent
    def innovation_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["innovation_engineer"],
            verbose=True,
        )

    @agent
    def senior_software_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["senior_software_engineer"],
            verbose=True,
        )

    @agent
    def qa_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["qa_engineer"],
            verbose=True,
        )

    # ------------------------------------------------------------------
    # Tasks
    # ------------------------------------------------------------------

    @task
    def product_requirement_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["product_requirement_analysis"],
            agent=self.product_manager(),
            output_json=ProductRequirementSpecification,
        )

    @task
    def ai_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["ai_assessment"],
            agent=self.ai_engineer(),
            output_json=AIAssessment,
        )

    @task
    def engineering_planning(self) -> Task:
        return Task(
            config=self.tasks_config["engineering_planning"],
            agent=self.engineering_manager(),
            output_json=EngineeringExecutionPlan,
        )

    @task
    def innovation_research(self) -> Task:
        return Task(
            config=self.tasks_config["innovation_research"],
            agent=self.innovation_engineer(),
            output_json=InnovationReport,
        )

    @task
    def implementation(self) -> Task:
        return Task(
            config=self.tasks_config["implementation"],
            agent=self.senior_software_engineer(),
            output_json=ImplementationReport,
        )

    @task
    def qa_review(self) -> Task:
        return Task(
            config=self.tasks_config["qa_review"],
            agent=self.qa_engineer(),
            output_json=QAReport,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EngineeringTeam crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
