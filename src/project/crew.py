from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from project.custom_tool import PerfTool, FileWriterTool, SmartValidatorTool
from crewai_tools import FileReadTool

@CrewBase
class project:
    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def perf_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['perf_analyzer'],
            tools=[PerfTool()],
            verbose=True
        )

    @agent
    def energy_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['energy_optimizer'],
            tools=[FileReadTool()],
            verbose=True
        )

    @agent
    def code_saver(self) -> Agent:
        return Agent(
            config=self.agents_config['code_saver'],
            tools=[FileWriterTool()],
            verbose=True
        )

    @agent
    def validator(self) -> Agent:
        return Agent(
            config=self.agents_config['validator'],
            tools=[SmartValidatorTool()],
            verbose=True
        )

    @agent
    def summary_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['summary_evaluator'],
            tools=[FileWriterTool()],
            verbose=True
        )

    @task
    def perf_task(self) -> Task:
        return Task(
            config=self.tasks_config["perf_task"],
            input={"command": "perf stat -e power/energy-pkg/ python retrieved_code.py"},
            output_variable="perf_output"
        )

    @task
    def optimize_task(self) -> Task:
        return Task(
            config=self.tasks_config["optimize_task"],
            output_variable="optimized_code"
        )

    @task
    def save_optimized_code(self) -> Task:
        return Task(
        config=self.tasks_config["save_optimized_code"],
        input={"optimized_code": "{optimized_code}"},
        output_variable="save_status"
    )


    @task
    def validate_functionality(self) -> Task:
        return Task(
            config=self.tasks_config["validate_functionality"],
            input={"command": "python optimized_code.py"},
            output_variable="execution_output"
        )

    @task
    def rerun_perf_task(self) -> Task:
        return Task(
            config=self.tasks_config["rerun_perf_task"],
            input={"command": "perf stat -e power/energy-pkg/ python optimized_code.py"},
            output_variable="optimized_perf_output"
        )

    @task
    def summarize_results(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_results"],
            input={
                "perf_output": "{perf_output}",
                "optimized_perf_output": "{optimized_perf_output}",
                "execution_output": "{execution_output}",
                "filename": "summary_report.txt",
                "content": "{summary_report}"
            },
            output_variable="summary_report"
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=[
                self.perf_task(),
                self.optimize_task(),
                self.save_optimized_code(),
                self.validate_functionality(),
                self.rerun_perf_task(),
                self.summarize_results()
            ],
            process=Process.sequential,
            verbose=True
        )
