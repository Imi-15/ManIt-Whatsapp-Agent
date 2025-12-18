"""
run_researcher.py - Simple CLI entry point to use the ResearcherAgent directly.

Usage (from project root, with venv activated):
    python run_researcher.py "Your research question here"

If no argument is provided, you will be prompted to type a topic.
"""

import sys

from agents.researcher import ResearcherAgent


def main() -> None:
    # Get topic from command-line argument or prompt
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter a research topic or question: ").strip()

    if not topic:
        print("No topic provided. Exiting.")
        return

    agent = ResearcherAgent()
    print("\n--- Running ResearcherAgent ---\n")
    try:
        result = agent.research(topic)
        print(result)
    except Exception as e:
        print(f"Error while running ResearcherAgent: {e}")


if __name__ == "__main__":
    main()


