from project.crew import project

def run():
    # Kick off the CrewAI workflow — no need for manual file reading anymore
    project().crew().kickoff()

if __name__ == "__main__":
    run()
