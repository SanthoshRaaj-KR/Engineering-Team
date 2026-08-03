#!/usr/bin/env python
import sys
import warnings

from chatbot.crew import Chatbot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew once, prompting the user in the terminal for a message.
    """
    user_message = input("You: ").strip()
    inputs = {'user_message': user_message}

    try:
        Chatbot().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def chat():
    """
    Run an interactive chat session in the terminal.

    Each turn is its own crew.kickoff() call - there is no chat history in
    the prompt. Since memory=True is set on the Crew (see crew.py), the
    crew's short-term/long-term/entity memory is what lets it recall facts
    from earlier turns. Try this to see it in action:

        You: Hi, my name is Alex and I love hiking.
        You: What's my name and what do I like?

    Type 'exit' or 'quit' to end the session.
    """
    print("Chatbot ready (memory=True). Type 'exit' to quit.\n")

    # Reuse the same crew instance across turns.
    chatbot_crew = Chatbot().crew()

    while True:
        user_message = input("You: ").strip()
        if user_message.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        if not user_message:
            continue

        try:
            result = chatbot_crew.kickoff(inputs={"user_message": user_message})
        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")

        print(f"\nAssistant: {result.raw}\n")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'user_message': "Hi, my name is Alex and I'm interested in AI agents."
    }
    try:
        Chatbot().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Chatbot().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'user_message': "Hi, my name is Alex and I'm interested in AI agents."
    }

    try:
        Chatbot().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "user_message": "",
    }

    try:
        result = Chatbot().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
