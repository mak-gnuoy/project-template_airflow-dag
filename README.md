
### run
$ python ./dags/example.py 

### useful commands
```
# initialize the database tables
$ airflow db init

# print the list of active DAGs
$ airflow dags list

# prints the list of tasks in the "example" DAG
$ airflow tasks list example

# prints the hierarchy of tasks in the "example" DAG
$ airflow tasks list example --tree

# testing a dag with ariflow test run
$ airflow dags test example 2015-06-01

# testing a task with ariflow test run
$ airflow tasks test example transform 2015-06-01

# start a web server in debug mode in the background
$ airflow webserver --debug &
