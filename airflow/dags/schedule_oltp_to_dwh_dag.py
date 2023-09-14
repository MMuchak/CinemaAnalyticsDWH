from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.email import send_email_smtp
from datetime import datetime, timedelta
import logging

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag_schedule = DAG(
    'etl_schedule_oltp_to_dwh',
    default_args=default_args,
    description='Incremental ETL job from OLTP Schedule database to DWH using last_updated metadata',
    schedule_interval=timedelta(days=7),
    start_date=datetime(2023, 9, 13),
    catchup=False
)

extract_sessions = PostgresOperator(
    task_id='extract_sessions',
    sql='''
    INSERT INTO dwh.SessionDim(session_id, date, start_time, end_time, hall_status, available_seats)
           SELECT s.session_id, s.date, s.start_time, s.end_time, h.status, h.available_seats
           FROM schedule_db.sessions s
           JOIN schedule_db.halls h ON s.hall_id = h.hall_id
           WHERE s.date > (SELECT COALESCE(MAX(last_updated), '2000-01-01') FROM dwh.etl_metadata WHERE table_name = 'sessions')
           ON CONFLICT (session_id)
           DO UPDATE SET date=EXCLUDED.date, start_time=EXCLUDED.start_time, 
               end_time=EXCLUDED.end_time, hall_status=EXCLUDED.hall_status, 
               available_seats=EXCLUDED.available_seats;

           -- Update metadata
           INSERT INTO dwh.etl_metadata(table_name, last_updated) VALUES ('sessions', NOW())
           ON CONFLICT (table_name)
           DO UPDATE SET last_updated = NOW();
    ''',
    postgres_conn_id='oltp_postgres',
    dag=dag_schedule
)

check_duplicates_sessions_sql = """
SELECT COUNT(*) = COUNT(DISTINCT session_id) AS is_unique FROM dwh.SessionDim WHERE date > '{{ prev_execution_date }}';
"""

check_null_values_sessions_sql = """
SELECT COUNT(*) AS null_count FROM dwh.SessionDim WHERE session_id IS NULL OR date IS NULL OR start_time IS NULL OR end_time IS NULL;
"""

check_negative_seats_sql = """
SELECT COUNT(*) FROM dwh.SessionDim WHERE available_seats < 0;
"""

def send_email(to, subject, html_content):
    send_email_smtp(
        to=to,
        subject=subject,
        html_content=html_content
    )

def evaluate_schedule_quality_checks(**kwargs):
    ti = kwargs['ti']
    postgres_hook = PostgresHook(postgres_conn_id='oltp_postgres')
    
    is_unique = postgres_hook.get_first(check_duplicates_sessions_sql)[0]
    null_count = postgres_hook.get_first(check_null_values_sessions_sql)[0]
    negative_seats = postgres_hook.get_first(check_negative_seats_sql)[0]
    
    error_messages = []
    
    if not is_unique:
        error_messages.append("Duplicate session records exist in SessionDim table")
    if null_count > 0:
        error_messages.append(f"{null_count} null values found in critical columns of SessionDim table")
    if negative_seats > 0:
        error_messages.append(f"{negative_seats} records have negative available seats")
        
    if error_messages:
        error_text = "Data Quality Checks Failed: " + " | ".join(error_messages)
        logging.error(error_text)
        
        send_email(
            to=['your_email@example.com'],
            subject='Data Quality Checks Failed for Schedule ETL',
            html_content=error_text
        )
        raise ValueError(error_text)
    else:
        logging.info("Data Quality Checks Passed Successfully for Schedule ETL")

quality_check_task = PythonOperator(
    task_id='data_quality_check',
    python_callable=evaluate_schedule_quality_checks,
    provide_context=True,
    dag=dag_schedule
)

extract_sessions >> quality_check_task
