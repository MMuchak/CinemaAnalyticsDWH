from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email_smtp
from datetime import datetime, timedelta
import logging

# Setting default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG definition for Users Database ETL process
dag_users = DAG(
    'etl_users_oltp_to_dwh',
    default_args=default_args,
    description='Incremental ETL job from OLTP Users database to DWH using last_updated metadata',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2023, 9, 13),
    catchup=False
)

# SQL task to extract users data from OLTP and insert/update into DWH
extract_users = PostgresOperator(
    task_id='extract_users',
    sql='''
    INSERT INTO dwh.UserDim(user_id, phone_number, email, is_verified)
           SELECT u.user_id, u.phone_number, u.email, u.is_verified
           FROM users_db.users u
           WHERE u.user_id > (SELECT COALESCE(MAX(last_updated), '0') FROM dwh.etl_metadata WHERE table_name = 'users')
           ON CONFLICT (user_id)
           DO UPDATE SET phone_number=EXCLUDED.phone_number, email=EXCLUDED.email, 
               is_verified=EXCLUDED.is_verified;

           -- Update the metadata table with the latest ETL timestamp
           INSERT INTO dwh.etl_metadata(table_name, last_updated) VALUES ('users', NOW())
           ON CONFLICT (table_name)
           DO UPDATE SET last_updated = NOW();
    ''',
    postgres_conn_id='oltp_postgres',
    dag=dag_users
)

# SQL statements for data validation checks
check_duplicates_users_sql = """
SELECT COUNT(*) = COUNT(DISTINCT user_id) AS is_unique FROM dwh.UserDim WHERE user_id > '{{ prev_execution_date }}';
"""
check_null_values_users_sql = """
SELECT COUNT(*) AS null_count FROM dwh.UserDim WHERE user_id IS NULL OR phone_number IS NULL OR email IS NULL;
"""

# Function to send email notifications
def send_email(to, subject, html_content):
    send_email_smtp(
        to=to,
        subject=subject,
        html_content=html_content
    )

# Function to evaluate data quality checks for Users ETL process
def evaluate_users_quality_checks(**kwargs):
    ti = kwargs['ti']
    postgres_hook = PostgresHook(postgres_conn_id='oltp_postgres')
    
    is_unique = postgres_hook.get_first(check_duplicates_users_sql)[0]
    null_count = postgres_hook.get_first(check_null_values_users_sql)[0]
    
    error_messages = []
    
    # Checking for duplicate records and null values in critical columns
    if not is_unique:
        error_messages.append("Duplicate user records exist in UserDim table")
    if null_count > 0:
        error_messages.append(f"{null_count} null values found in critical columns of UserDim table")
        
    # If errors are found, send an email notification and raise an exception
    if error_messages:
        error_text = "Data Quality Checks Failed: " + " | ".join(error_messages)
        logging.error(error_text)
        
        send_email(
            to=['your_email@example.com'],
            subject='Data Quality Checks Failed for Users ETL',
            html_content=error_text
        )
        raise ValueError(error_text)
    else:
        logging.info("Data Quality Checks Passed Successfully for Users ETL")

# Task to perform data quality checks after the extraction
quality_check_task = PythonOperator(
    task_id='data_quality_check',
    python_callable=evaluate_users_quality_checks,
    provide_context=True,
    dag=dag_users
)

# Defining task sequence in the DAG
extract_users >> quality_check_task
