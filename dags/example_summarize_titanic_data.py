"""
example_summarize_titanic_data
DAG auto-generated by Astro Cloud IDE.
"""

from airflow.decorators import dag
from astro import sql as aql
from astro.table import Table, Metadata
import pandas as pd
import pendulum


"""
This pipeline demonstrates how to use the Astro Cloud IDE. It loads the Titanic dataset, filters out passengers under 18, and aggregates the data by survival and class.

The pipeline is composed of four cells:

`load`: Loads the Titanic dataset from Seaborn's GitHub repository.

`over_18`: Filters out passengers under 18.

`aggregate_sql`: Aggregates the data by survival and class, using SQL.

`aggregate_python`: Aggregates the data by survival and class, using Python.

Note that each cell returns a value that can be referenced in subsequent cells using the `{{cell_name}}` syntax in SQL and `cell_name` syntax in Python.
"""

@aql.dataframe(task_id="load")
def load_func():
    import pandas as pd
    
    # use pandas to load the titanic dataset from github
    return pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv')

@aql.run_raw_sql(conn_id="duckdb_default", task_id="over_18", results_format="pandas_dataframe")
def over_18_func(load: Table):
    return """
    -- use SQL to filter out passengers under 18
    -- note that we can reference the output of the load cell using the {{load}} syntax
    select sex as no_male_servivial, sex as female from
    (SELECT *
    FROM {{load}}
    where  sex = 1)
    
    
    
    """

@aql.run_raw_sql(conn_id="duckdb_default", task_id="aggregate_sql", results_format="pandas_dataframe")
def aggregate_sql_func(over_18: Table):
    return """
    -- use SQL to calculate the average age and count of passengers by survival and class
    SELECT
        alive,
        class,
        avg(age) as avg_age,
        count(*) as count
    FROM {{over_18}}
    GROUP BY alive, class
    """

@aql.dataframe(task_id="aggregate_python")
def aggregate_python_func(over_18: pd.DataFrame):
    import pandas as pd
    
    # use pandas to calculate the average age and count of passengers by survival and class
    # notice that we can reference the output of the over_18 cell using the over_18 variable
    return over_18.groupby(['alive', 'class']).agg({'age': ['mean', 'count']}).reset_index()

@aql.run_raw_sql(conn_id="duckdb_default", task_id="sql_1", results_format="pandas_dataframe")
def sql_1_func():
    return """
    
    """

@aql.transform(conn_id="", task_id="warehouse_sql_1")
def warehouse_sql_1_func():
    return """
    
    """

default_args={
    "owner": "ifiok@engineer.com,Open in Cloud IDE",
}

@dag(
    default_args=default_args,
    schedule=None,
    start_date=pendulum.from_format("2024-07-25", "YYYY-MM-DD"),
    catchup=False,
    owner_links={
        "ifiok@engineer.com": "mailto:ifiok@engineer.com",
        "Open in Cloud IDE": "https://cloud.astronomer.io/clz1m3alx08ny01kxmed8ns4a/cloud-ide/clz1m4emy08o901kx1kdxs5pe/clz1m4ewy08zr01jyxl9qbmnv",
    },
)
def example_summarize_titanic_data():
    load = load_func()

    over_18 = over_18_func(
        load,
    )

    aggregate_sql = aggregate_sql_func(
        over_18,
    )

    aggregate_python = aggregate_python_func(
        over_18,
    )

    sql_1 = sql_1_func()

    warehouse_sql_1 = warehouse_sql_1_func()

dag_obj = example_summarize_titanic_data()
