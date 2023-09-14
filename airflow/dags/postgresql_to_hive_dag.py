from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.apache.hive.hooks.hive import HiveCliHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email
import pandas as pd
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'postgresql_to_hive_incremental',
    default_args=default_args,
    description='Incremental transfer of data from PostgreSQL DWH to Hive',
    schedule_interval='0 0 * * *',
    start_date=datetime(2023, 9, 13),
    catchup=False
)

def transfer_table(table_name, **kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='dwh_postgres')
    hive_hook = HiveCliHook(hive_cli_conn_id="hive_default")

    # Fetch last_updated for the table from Hive
    last_updated_query = f"SELECT last_updated FROM etl_metadata WHERE table_name = '{table_name}'"
    last_updated = hive_hook.get_first(last_updated_query)

    # Determine the extraction SQL based on the last_updated timestamp
    if last_updated:
        last_updated_date = last_updated[0].strftime('%Y-%m-%d')
        extract_sql = f"SELECT * FROM {table_name} WHERE data_date > '{last_updated_date}'"
    else:
        extract_sql = f"SELECT * FROM {table_name}"

    # Extract data from PostgreSQL
    df = postgres_hook.get_pandas_df(extract_sql)

    # Transform data if necessary
    if table_name in ["SessionDim", "SalesFact", "TicketsFact"]:
        date_col = 'date' if table_name == "SessionDim" else 'transaction_date' if table_name == "SalesFact" else 'purchase_date'
        df['year'] = pd.to_datetime(df[date_col]).dt.year
        df['month'] = pd.to_datetime(df[date_col]).dt.month
        df[date_col] = df[date_col].astype(str)

    # Saving DataFrame to CSV
    file_path = f"/tmp/{table_name}.csv"
    df.to_csv(file_path, sep='\t', index=False)

    # Load data into Hive
    hive_hook.load_file(
        file_path=file_path,
        table=f"{table_name}",
        create=False,
        partition={'year': df['year'].iloc[0], 'month': df['month'].iloc[0]} if table_name in ["SessionDim", "SalesFact", "TicketsFact"] else None,
        delimiter='\t'
    )

    # Update etl_metadata in Hive after successful transfer
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp_table_name = f"temp_etl_metadata_{table_name}"
    hive_hook.run(f"CREATE TABLE IF NOT EXISTS {temp_table_name} AS SELECT '{table_name}' AS table_name, '{current_time}' AS last_updated")
    overwrite_sql = f"""
    INSERT OVERWRITE TABLE etl_metadata 
    SELECT * FROM etl_metadata WHERE table_name != '{table_name}'
    UNION ALL
    SELECT * FROM {temp_table_name};
    """
    hive_hook.run(overwrite_sql)
    hive_hook.run(f"DROP TABLE IF EXISTS {temp_table_name}")

    # Check count between PostgreSQL and Hive
    postgres_count = postgres_hook.get_first(f"SELECT COUNT(*) FROM {table_name} WHERE data_date > '{last_updated_date}' if last_updated else ''")[0]
    hive_count = hive_hook.get_first(f"SELECT COUNT(*) FROM {table_name}")[0]
    
    if postgres_count != hive_count:
        error_msg = f"Discrepancy in record counts for {table_name}. PostgreSQL: {postgres_count}, Hive: {hive_count}."
        logging.error(error_msg)
        send_email(
            to=['your_email@example.com'],
            subject=f'Discrepancy in {table_name}',
            html_content=f'<p>{error_msg}</p>'
        )
        raise ValueError(error_msg)

tables = ['UserDim', 'CinemaDim', 'FilmDim', 'SessionDim', 'SalesFact', 'TicketsFact']

for table in tables:
    transfer_task = PythonOperator(
        task_id=f'transfer_{table}',
        python_callable=transfer_table,
        op_args=[table],
        provide_context=True,
        dag=dag,
    )

    transfer_task

# Handling Errors
def on_failure_callback(context):
    error_msg = str(context['exception'])
    send_email(
        to=['your_email@example.com'],
        subject='Airflow Task Failed',
        html_content=f'<p>{error_msg}</p>'
    )

for task in dag.tasks:
    task.on_failure_callback = on_failure_callback
