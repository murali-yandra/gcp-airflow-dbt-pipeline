# Cloud-Native End-to-End Data Engineering Pipeline

## 📖 Project Overview
This project demonstrates a production-grade, automated ELT (Extract, Load, Transform) pipeline orchestrated via Apache Airflow. It extracts raw local data, stages it in a Google Cloud Storage (GCS) Data Lake, performs an atomic bulk-load into Google BigQuery, and executes a container-isolated dbt (data build tool) project for analytical transformations and data quality testing.

## 🏗️ Architecture
```text
Local CSV -> GCS (Data Lake) -> BigQuery (Data Warehouse) -> dbt (Transformation) -> BI/Dashboards

🛠️ Technology Stack
Orchestration: Apache Airflow (Dockerized)

Cloud Infrastructure: Google Cloud Platform (GCS, BigQuery, IAM)

Transformation & Testing: dbt (data build tool)

Language: Python, SQL, Jinja, Bash

Version Control: Git & GitHub

🚀 Key Engineering Features
Containerized Orchestration: Deployed Airflow within a Docker container, managing host-to-container volume mounts for credential and DAG injection.

Idempotent Execution: Engineered custom bash logic within the BashOperator to dynamically handle transient dependencies. The script intelligently caches dbt binaries within the Airflow user space, preventing redundant PyPI network calls and ensuring failure-proof, idempotent restarts.

Decoupled Data Modeling: Utilized dbt's sources.yml abstraction layer to decouple physical cloud infrastructure from the SQL transformation logic, enabling seamless environment promotion (Dev -> Prod).

Automated Data Quality Gates: Enforced strict schema testing via dbt (dbt build). The pipeline automatically validates primary key uniqueness, null constraints, and categorical adherence before finalizing dimension tables.

Secure Cloud Authentication: Implemented GCP Service Accounts utilizing the Principle of Least Privilege (Storage Admin + BigQuery Admin), completely isolating environment credentials via .gitignore.

📂 Project Structure
Plaintext
📦 gcp-airflow-dbt-pipeline
 ┣ 📂 dags
 ┃ ┣ 📂 faang_analytics (dbt project)
 ┃ ┃ ┣ 📂 models
 ┃ ┃ ┃ ┣ 📜 dim_products.sql (Core business logic)
 ┃ ┃ ┃ ┣ 📜 schema.yml (Data quality tests)
 ┃ ┃ ┃ ┗ 📜 sources.yml (Source abstraction graph)
 ┃ ┃ ┣ 📜 dbt_project.yml
 ┃ ┃ ┗ 📜 profiles.yml (GCP connection target)
 ┃ ┣ 📜 gcp_warehouse_orchestration.py (Airflow DAG)
 ┃ ┗ 📜 sample_products.csv (Raw source data)
 ┣ 📜 .gitignore
 ┗ 📜 README.md