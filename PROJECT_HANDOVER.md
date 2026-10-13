Project Handover — Retail Demand Forecasting & Inventory Optimization

1. Project Overview

This project uses retail sales data, machine learning, BigQuery, dbt, and Streamlit to analyze sales trends and support demand forecasting and inventory planning.

2. Technologies Used

- Python
- Pandas
- Prophet and LightGBM
- Google BigQuery
- dbt
- Streamlit

3. How to Run the Dashboard

1. Activate the Python virtual environment.
2. Install dependencies using "pip install -r requirements.txt".
3. Configure Google Cloud authentication for BigQuery access.
4. Run "streamlit run app.py".
5. Open the local URL shown in the terminal.

4. Final Code Review

- Confirm that project files are organized correctly.
- Check that required dependencies are listed in "requirements.txt".
- Verify that BigQuery connection settings are configured.
- Ensure credentials and secret keys are not committed to GitHub.
- Check that the dashboard displays available forecast data.

5. Access Control and Security

- Use Google Cloud IAM to grant only the permissions required for BigQuery access.
- Do not share service-account keys, passwords, or other credentials in the repository.
- Keep sensitive configuration in environment variables or an appropriate secrets manager.
- Verify access permissions before sharing the project.

6. Known Limitations

The dashboard uses the forecast results currently stored in BigQuery. Future-demand predictions should be generated and validated separately before being presented as genuine future forecasts. Price-change scenarios are estimates based on assumed price elasticity.

7. Handover

The repository contains the dashboard, forecasting code, data transformation models, and project documentation. Before deployment, verify dependencies, permissions, forecast validity, and the dashboard's behavior in the target environment.