#!/usr/bin/env python

import warnings
from datetime import datetime

from crewai import Crew, Process

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():

    team = EngineeringTeam()

    inputs = {
        "user_query": input("Enter your requirement: "),
        "current_year": str(datetime.now().year),
    }

    # ----------------------------------------------------
    # Step 1 : Product Requirement Analysis
    # ----------------------------------------------------

    print("\n========== PRODUCT MANAGER ==========\n")

    prs_result = Crew(
        agents=[team.product_manager()],
        tasks=[team.product_requirement_analysis()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(inputs=inputs)

    # ----------------------------------------------------
    # Step 2 : AI Assessment
    # ----------------------------------------------------

    print("\n========== AI ENGINEER ==========\n")

    ai_result = Crew(
        agents=[team.ai_engineer()],
        tasks=[team.ai_assessment()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(
        inputs={
            "product_specification": prs_result.pydantic
        }
    )

    # ----------------------------------------------------
    # Step 3 : Engineering Planning
    # ----------------------------------------------------

    print("\n========== ENGINEERING MANAGER ==========\n")

    engineering_plan = Crew(
        agents=[team.engineering_manager()],
        tasks=[team.engineering_planning()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(
        inputs={
            "product_specification": prs_result.pydantic,
            "ai_assessment": ai_result.pydantic,
        }
    )

    # ----------------------------------------------------
    # Step 4 : Innovation
    # ----------------------------------------------------

    print("\n========== INNOVATION ENGINEER ==========\n")

    innovation_report = Crew(
        agents=[team.innovation_engineer()],
        tasks=[team.innovation_research()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(
        inputs={
            "engineering_plan": engineering_plan.pydantic
        }
    )

    # ----------------------------------------------------
    # Step 5 : Implementation
    # ----------------------------------------------------

    print("\n========== SENIOR SOFTWARE ENGINEER ==========\n")

    implementation = Crew(
        agents=[team.senior_software_engineer()],
        tasks=[team.implementation()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(
        inputs={
            "engineering_plan": engineering_plan.pydantic,
            "innovation_report": innovation_report.pydantic,
        }
    )

    # ----------------------------------------------------
    # Step 6 : QA
    # ----------------------------------------------------

    print("\n========== QA ==========\n")

    qa_report = Crew(
        agents=[team.qa_engineer()],
        tasks=[team.qa_review()],
        process=Process.sequential,
        verbose=True,
    ).kickoff(
        inputs={
            "implementation": implementation.pydantic
        }
    )

    print("\n========== FINAL RESULT ==========\n")
    print(qa_report)