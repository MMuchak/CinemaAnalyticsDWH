
---

# Методології Структури Бази Даних | Database Structure Methodologies

_Є багато різних методологій, які широко використовуються для розробки структури баз данних._
*There are many different methodologies widely used for database structure development.*

## 1. Kimball:
   - **Focus**: Центровано на процесах бізнесу. | Centered on business processes.
   - **Usage**: В основному використовується для розробки системи бізнес-аналітики (BI). | Primarily used for business intelligence (BI) system development.
   - **Structure**: Використовує "зіркову схему", де основна таблиця оточена додатковими таблицями. | Uses a "star schema" where the central table is surrounded by auxiliary tables.

## 2. Inmon:
   - **Focus**: Центровано на предметних областях. | Centered on subject areas.
   - **Usage**: Створює централізоване сховище даних для всієї організації. | Creates a centralized data warehouse for the entire organization.
   - **Structure**: Використовує "схему сніжинки", де таблиці можуть мати багато зв'язків з іншими таблицями. | Uses a "snowflake schema" where tables can have multiple relations with other tables.

## 3. Snowflake (Схема Сніжинки):
   - **Extension**: Це розширення "зіркової схеми". | It is an extension of the "star schema".
   - **Normalization**: Додаткові таблиці можуть бути нормалізовані. | Auxiliary tables can be normalized, leading to the creation of additional relations between tables.

## 4. Data Vault:
   - **Focus**: Збереженні історії даних з різних джерел у сховище. | Preserving the history of data from various sources in storage.
   - **Idea**: Створення гнучкого, скальованого та адаптивного сховища даних. | Creation of a flexible, scalable, and adaptive data repository.
   - **Structure**: Основні таблиці (Hubs), посилальні таблиці (Satellites) та зв'язуючі таблиці (Links). | Main tables (Hubs), reference tables (Satellites), and linking tables (Links).

## 5. Anchor Modeling:
   - **Focus**: Адаптивності сховища даних до змін. | Adaptability of data storage to changes.
   - **Idea**: Розділення дійсності на стабільні та змінювані частини. | Dividing reality into stable and changeable parts.
   - **Structure**: Якірні таблиці представляють основні об'єкти, атрибути та історія змін зберігаються в окремих таблицях. | Anchor tables represent the main objects, attributes and history of changes are stored in separate tables.

## 6. Agile Data Warehousing:
   - **Focus**: Швидка адаптація до вимог бізнесу. | Rapid adaptation to business requirements.
   - **Idea**: Максимальна гнучкість з мінімальними втратами часу. | Maximum flexibility with minimal time loss.
   - **Approach**: Ітераційний підхід з постійною взаємодією з бізнес-замовниками. | Iterative approach with constant interaction with business customers.

## 7. Federated Data Warehousing:
   - **Focus**: Інтеграція автономних сховищ даних. | Integration of autonomous data repositories.
   - **Idea**: Об'єднання даних з різних сховищ. | Combining data from different repositories.
   - **Structure**: Автономні сховища з інтеграційними шарами. | Autonomous repositories with integration layers.

## 8. Lambda and Kappa Architectures:
   - **Focus**: Обробка великих даних в реальному часі. | Processing big data in real-time.
   - **Idea**: Lambda комбінує потокову та пакетну обробку, Kappa виключно потокову. | Lambda combines stream and batch processing, Kappa focuses solely on streaming.
   - **Structure**: Побудова на основі потокової обробки в масштабах. | Built on the basis of stream processing at scale.



## Обрана методологія: Kimball. | Chosen Methodology: Kimball.

**Причини вибору**: | **Reasons for choice**:
- Швидка відповідь на запити аналітики. | - Quick response to analytical queries.
- Ефективність для кінотеатру при аналізі продажів квитків. | - Efficiency for a cinema when analyzing ticket sales.

# Обгрунтування вибору методології | Justification for Methodology Choice

Ця структура бази даних орієнтована на швидке виконання аналітичних запитів і забезпечує гнучкість для додавання нових даних без зміни схеми. | This database structure focuses on fast execution of analytical queries and provides flexibility for adding new data without schema changes.

## Чому не підхід Inmon: | Why not Inmon's approach:
1. Наш сценарій головним чином зосереджений на кінотематиці. Створення цілого EDW, як це пропонується Inmon, може бути надмірним. Підхід Kimball пропонує швидші результати, менш витратний з точки зору розробки, та краще відповідає вимогам цього конкретного бізнес-випадку. | Our scenario mainly focuses on cinema-related themes. Creating a whole EDW as proposed by Inmon might be overkill. Kimball's approach offers faster results, is less costly in terms of development, and better meets the requirements of this specific business case.

## Чому не підхід Snowflake: | Why not Snowflake's approach:
1. Наш сценарій вимагає простих та швидких аналітичних запитів. Введення більше таблиць та з'єднань, як це в схемі Snowflake, може сповільнити наші запити. | Our scenario requires simple and fast analytical queries. Introducing more tables and connections, as in the Snowflake schema, might slow down our queries.

2. Підхід Kimball, використовуючи зіркову схему, простіший за конструкцією та легший для розуміння для BI-розробників та інших зацікавлених сторін. У такій сфері, як кіно, де структура даних не є надто складною, простота та переваги в продуктивності зіркової схеми можуть переважити переваги нормалізації схеми Snowflake. | Kimball's approach, using a star schema, is simpler in design and easier for BI developers and other stakeholders to understand. In an area like cinema, where the data structure isn't overly complex, the simplicity and performance advantages of the star schema might outweigh the normalization benefits of the Snowflake schema.

## Чому не підхід Data Vault: | Why not Data Vault's approach:
1. Схема Data Vault може бути занадто складною для ваших потреб. Кінотеатр не має такої кількості різноманітних джерел даних, щоб виправдати використання цієї методології. | The Data Vault schema might be overly complex for your needs. A cinema doesn't have such a variety of different data sources to justify using this methodology.

## Чому не підхід Anchor Modeling: | Why not Anchor Modeling's approach:
1. Цей підхід може бути занадто гнучким для сценарію кінотеатру. Він призначений для дуже змінюваних джерел даних, чого, як правило, не виникає в кінобізнесі. | This approach might be overly flexible for the cinema scenario. It's intended for highly changeable data sources, which typically don't arise in the movie business.

## Чому не підхід Agile Data Warehousing: | Why not Agile Data Warehousing's approach:
1. Хоча гнучкість є ключем до успіху в багатьох проектах, ви, можливо, не зіткнетесь з постійно змінюваними вимогами в сценарії кінотеатру. | Although flexibility is key to success in many projects, you might not face constantly changing requirements in a cinema scenario.

## Чому не підхід Federated Data Warehousing: | Why not Federated Data Warehousing's approach:
1. Для кінотеатру, який не має багатьох розподілених сховищ даних, цей підхід може бути зайвим. | For a cinema that doesn't have multiple distributed data warehouses, this approach might be excessive.

## Чому не підхід Lambda and Kappa Architectures: | Why not Lambda and Kappa Architectures' approach:
1. Ці архітектури призначені для реального часу та великих даних. Кінотеатр, як правило, не потребує такої обробки даних в режимі реального часу, яка передбачена цими підходами. | These architectures are designed for real-time and big data processing. A cinema typically doesn't require the real-time data processing anticipated by these approaches.

--- 
