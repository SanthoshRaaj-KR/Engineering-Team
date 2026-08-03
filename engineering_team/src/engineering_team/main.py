#!/usr/bin/env python

import sys
import warnings

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def _inputs() -> dict:
    return {
        "user_query": input("Enter your requirement: "),
    }


def run():
    team = EngineeringTeam()

    qa_report = team.crew().kickoff(inputs=_inputs())

    print("\n========== FINAL RESULT ==========\n")
    print(qa_report)


def train():
    """Train the crew for a given number of iterations."""
    try:
        EngineeringTeam().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=_inputs(),
        )
    except Exception as exc:
        raise Exception(f"An error occurred while training the crew: {exc}") from exc


def replay():
    """Replay the crew execution from a given task id."""
    try:
        EngineeringTeam().crew().replay(task_id=sys.argv[1])
    except Exception as exc:
        raise Exception(f"An error occurred while replaying the crew: {exc}") from exc


def test():
    """Test the crew execution and return the results."""
    try:
        EngineeringTeam().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2],
            inputs=_inputs(),
        )
    except Exception as exc:
        raise Exception(f"An error occurred while testing the crew: {exc}") from exc
