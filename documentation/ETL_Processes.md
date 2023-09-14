
---

# ETL Процеси використовуючи Apache Airflow | ETL Processes using Apache Airflow

Apache Airflow - це інструмент для програмування, планування та моніторингу великомасштабних ETL процесів.
*Apache Airflow is a tool for programming, scheduling, and monitoring large-scale ETL processes.*

В контексті нашого проекту, ми використовували Airflow для координації наступних процесів:
*In the context of our project, we used Airflow to coordinate the following processes:*

## PostgreSQL OLTP до PostgreSQL DWH | PostgreSQL OLTP to PostgreSQL DWH

### 1.1 Інкрементне завантаження | Incremental Loading

Враховуючи вимогу оптимізації завантаження даних, я обрав інкрементний підхід.
*Considering the requirement to optimize data loading, I chose an incremental approach.*

### 1.2 Таблиця для відслідковування інкрементів | Table for Tracking Increments

Було створено додаткову таблицю в PostgreSQL DWH.
*An additional table was created in PostgreSQL DWH.*

  ```
CREATE TABLE etl_metadata (
    table_name VARCHAR(255) PRIMARY KEY,
    last_updated TIMESTAMP
);
  ```

## PostgreSQL DWH до Hive | PostgreSQL DWH to Hive

### 2.1 Щоденне завантаження | Daily Loading

Кожної півночі ми запускаємо ETL процес.
*Every midnight we run the ETL process.*

## Стратегія зберігання даних та оптимізації | Data Storage and Optimization Strategy

### 3.1 Стратегія зберігання | Storage Strategy

На меті зберігати дані в PostgreSQL DWH протягом місяця.
*The goal is to store data in PostgreSQL DWH for a month.*

### 3.2 Оптимізація PostgreSQL DWH | PostgreSQL DWH Optimization

- **Ретенція (Retention Policy):** Автоматично видаляти записи, які старіше одного місяця.
- **Retention Policy:** Automatically delete records older than one month.
  
- **Vacuum:** Запускати процес `VACUUM`.
- **Vacuum:** Run the `VACUUM` process.
  
- **Reindexing:** Регулярно виконувати переіндексацію.
- **Reindexing:** Regularly perform re-indexing.

### 3.3 Зберігання в Hive | Storing in Hive

Hive буде використовуватися як "холодне" сховище для даних.
*Hive will be used as a "cold" storage for data.*

---