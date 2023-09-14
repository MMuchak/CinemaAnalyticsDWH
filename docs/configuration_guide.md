---

# 🛠 Configuration Guide for Airflow DAGs

Set up your Airflow DAGs seamlessly with this step-by-step guide. Make sure to follow each section meticulously for a smooth setup.

---

# 🛠 Configuration Guide for Airflow DAGs | 🛠 Керівництво з налаштування для Airflow DAGs

Set up your Airflow DAGs seamlessly with this step-by-step guide. Make sure to follow each section meticulously for a smooth setup.

*(Українська)*: Налаштуйте свої Airflow DAGs без проблем з цим покроковим керівництвом. Переконайтеся, що ви уважно слідкуєте за кожним розділом для гладкого налаштування.

## 📝 Table of Contents | 📝 Зміст

1. [Prerequisites | Передумови](#1-prerequisites)
2. [Airflow Setup | Налаштування Airflow](#2-airflow-setup)
3. [DAG Configuration | Налаштування DAG](#3-dag-configuration)
4. [Dependencies Installation | Встановлення залежностей](#4-dependencies-installation)
5. [Database Connections | Підключення баз даних](#5-database-connections)
6. [Email Notifications | Повідомлення по e-mail](#6-email-notifications)
7. [Running the DAGs | Запуск DAGs](#7-running-the-dags)
8. [Troubleshooting | Усунення неполадок](#8-troubleshooting)
9. [Maintenance | Обслуговування](#9-maintenance)
10. [Software & Version Info | Інформація про програмне забезпечення та версії](#10-software--version-info)

---

## 1. Prerequisites | Передумови 📋

- Python 3.8+ 🐍
- Installed version of Apache Airflow.
- Access to PostgreSQL and Hive databases.
- SMTP server or email service for notifications.

*(Українська)*:
- Python 3.8+ 🐍
- Встановлена версія Apache Airflow.
- Доступ до баз даних PostgreSQL та Hive.
- SMTP-сервер або служба електронної пошти для повідомлень.

---

## 2. Airflow Setup | Налаштування Airflow 🌬

1. **Initialize Airflow Database**: `airflow db init`
2. **Start Airflow Webserver**: `airflow webserver -p 8080`
3. **Start Airflow Scheduler**: `airflow scheduler`

*(Українська)*:
1. **Ініціалізація бази даних Airflow**: `airflow db init`
2. **Запуск Airflow Webserver**: `airflow webserver -p 8080`
3. **Запуск Airflow Scheduler**: `airflow scheduler`

---

## 3. DAG Configuration | Налаштування DAG 🗂

- Copy the DAG `.py` files into the Airflow DAGs directory (`$AIRFLOW_HOME/dags`).
- Verify the DAGs' appearance in the Airflow Web UI.

*(Українська)*:
- Скопіюйте файли DAG `.py` в директорію DAGs Airflow (`$AIRFLOW_HOME/dags`).
- Перевірте зовнішній вигляд DAGs у веб-інтерфейсі Airflow.

---


## 4. Dependencies Installation 📦

```bash
pip install apache-airflow-providers-postgres apache-airflow-providers-apache-hive pandas
```
*(Українська)*:
Встановіть необхідні залежності за допомогою команди наведеної вище.
---

## 5. Database Connections | Підключення баз даних 🗄

1. **PostgreSQL Connection**: Set up via the Airflow Web UI under `Admin` > `Connections`.
2. **Hive Connection**: Add a connection with Conn Id `hive_default`.
3. **HTTP Connection (For Mock Requests)**: 
    - Add a new connection with Conn Type as `HTTP`.
    - Set Conn Id as `http_default` (or any other relevant name).
    - Provide the base URL for the mock service or endpoint.

*(Українська)*:
1. **PostgreSQL Connection | Підключення до PostgreSQL**: Налаштуйте через веб-інтерфейс Airflow у розділі `Admin` > `Connections`.
2. **Hive Connection | Підключення до Hive**: Додайте з'єднання з Conn Id `hive_default`.
3. **HTTP Connection (For Mock Requests) | HTTP підключення (для тестових запитів)**: 
    - Додайте нове з'єднання з Conn Type як `HTTP`.
    - Встановіть Conn Id як `http_default` (або будь-яке інше відповідне ім'я).
    - Вкажіть базовий URL для тестового сервісу або кінцевої точки.
---

## 6. Email Notifications | Повідомлення по e-mail 📧

- Configure the SMTP settings in `$AIRFLOW_HOME/airflow.cfg`.
- Replace placeholder emails in the DAGs.

*(Українська)*:
- Налаштуйте параметри SMTP у `$AIRFLOW_HOME/airflow.cfg`.
- Замініть тимчасові електронні адреси у DAGs.

---

## 7. Running the DAGs | Запуск DAGs ▶️

Activate and trigger DAGs via the Airflow Web UI.

*(Українська)*:
- Активуйте та запустіть DAGs через веб-інтерфейс Airflow.

---

## 8. Troubleshooting | Усунення неполадок 🚫

Common issues:
- DAGs not appearing
- Database connection errors
- Data transfer mismatches
- Emails not being sent

*(Українська)*:
Загальні проблеми:
- DAGs не відображаються
- Помилки підключення до бази даних
- Невідповідності при передачі даних
- Електронні листи не надсилаються

---

## 9. Maintenance | Обслуговування 🧹

- Regularly review Airflow logs.
- Keep DAGs updated.
- Monitor resource usage.

*(Українська)*:
- Регулярно переглядайте журнали Airflow.
- Тримайте DAGs оновленими.
- Слідкуйте за використанням ресурсів.


---

## 10. Software & Version Info | Інформація про програмне забезпечення та версії ℹ️

- **Python**: 3.8+
- **PostgreSQL**: 13.3
  - 📘 [PostgreSQL documentation](https://www.postgresql.org/docs/13/index.html)
- **Apache Hive**: 3.1.2 
  - 📘 [Hive documentation](https://cwiki.apache.org/confluence/display/Hive/Home)

---

*Happy Data Pipelining!* | *Щасливої роботи з даними!*

---
