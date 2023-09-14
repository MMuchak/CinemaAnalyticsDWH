from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email_smtp
from datetime import datetime, timedelta
import logging

# Default configuration parameters for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG definition for Films Database ETL process
dag_films = DAG(
    'etl_films_oltp_to_dwh',
    default_args=default_args,
    description='Incremental ETL job from OLTP Films database to DWH',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2023, 9, 13),
    catchup=False
)

# SQL task to extract films data from OLTP and insert/update into DWH
extract_films = PostgresOperator(
    task_id='extract_films',
    sql='''
    INSERT INTO dwh.FilmDim(film_id, duration, technology_name, genre_name, category_name)
           SELECT f.film_id, f.duration, t.technology_name, g.genre_name, c.category_name
           FROM movies_db.films f
           LEFT JOIN movies_db.technologies t ON f.technology_id = t.technology_id
           LEFT JOIN movies_db.genres g ON f.genre_id = g.genre_id
           LEFT JOIN movies_db.categories c ON f.category_id = c.category_id
           ON CONFLICT (film_id)
           DO UPDATE SET duration=EXCLUDED.duration, technology_name=EXCLUDED.technology_name,
               genre_name=EXCLUDED.genre_name, category_name=EXCLUDED.category_name;

    ''',
    postgres_conn_id='oltp_postgres',
    dag=dag_films
)

# SQL statements for data validation checks
check_duplicates_films_sql = """
SELECT COUNT(*) = COUNT(DISTINCT film_id) AS is_unique FROM dwh.FilmDim WHERE film_id > '{{ prev_execution_date }}';
"""
check_null_values_films_sql = """
SELECT COUNT(*) AS null_count FROM dwh.FilmDim WHERE film_id IS NULL OR duration IS NULL;
"""

# Function to send email notifications
def send_email(to, subject, html_content):
    send_email_smtp(
        to=to,
        subject=subject,
        html_content=html_content
    )

# Function to evaluate data quality checks for Films ETL process
def evaluate_films_quality_checks(**kwargs):
    ti = kwargs['ti']
    postgres_hook = PostgresHook(postgres_conn_id='oltp_postgres')
    
    is_unique = postgres_hook.get_first(check_duplicates_films_sql)[0]
    null_count = postgres_hook.get_first(check_null_values_films_sql)[0]
    
    error_messages = []
    
    # Checking for duplicate records and null values in critical columns
    if not is_unique:
        error_messages.append("Duplicate film records exist in FilmDim table")
    if null_count > 0:
        error_messages.append(f"{null_count} null values found in critical columns of FilmDim table")
        
    # If errors are found, send an email notification and raise an exception
    if error_messages:
        error_text = "Data Quality Checks Failed for Films ETL: " + " | ".join(error_messages)
        logging.error(error_text)
        
        send_email(
            to=['your_email@example.com'],
            subject='Data Quality Checks Failed for Films ETL',
            html_content=error_text
        )
        raise ValueError(error_text)
    else:
        logging.info("Data Quality Checks Passed Successfully for Films ETL")

# Task to perform data quality checks after the extraction
quality_check_task = PythonOperator(
    task_id='data_quality_check',
    python_callable=evaluate_films_quality_checks,
    provide_context=True,
    dag=dag_films
)

# Defining task sequence in the DAG
extract_films >> quality_check_task
