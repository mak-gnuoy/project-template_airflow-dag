
import json
import pendulum

from airflow.decorators import dag, task
from airflow.providers.docker.operators.docker import DockerOperator

@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)
def example():
    # docker operator task running with command 
    extract = DockerOperator(
        task_id='extract',
        image="python",
        command=["ls", "-alh"],
        mount_tmp_dir=False,
        auto_remove='success'
    )

    # docker decorator task running with python code
    @task.docker(
        image="python",
        mount_tmp_dir=False,
        multiple_outputs=True,
        auto_remove='success'
    )
    def transform(files: str):
        file_list = files.split("\n")
        file_list.pop(0)
        file_list.pop(0)
        file_list.pop(0)

        import re
        pattern = re.compile(r"[^\s]+")
        file_names = []
        for file_row in file_list:
            matches = pattern.findall(file_row)
            file_names.append(matches[8])

        return { "filenames": file_names}

    # basic task
    @task
    def load(filenames: dict):
        print(f"{filenames}")

    files = extract.output
    filenames = transform(files)
    load(filenames)

example_dag = example()

if __name__ == '__main__':
    example_dag.test()