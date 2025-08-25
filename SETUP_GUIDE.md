# Nigerian Audit AI: Comprehensive Setup and Training Guide

This guide provides detailed, step-by-step instructions for setting up the Nigerian Audit AI project, collecting data, training models, and running the API. It also includes a troubleshooting section for common errors and an FAQ.

## 1. Prerequisites

Before you begin, ensure you have the following installed on your system:

-   **Python 3.10+:** You can download it from the [official Python website](https://www.python.org/).
-   **Poetry:** A dependency management tool. Install it by following the instructions on the [Poetry website](https://python-poetry.org/docs/).
-   **Git:** For version control.
-   **Docker:** (Optional, for containerized deployment)
-   **Access to a PostgreSQL Database and a Redis Instance:** These can be running locally or in the cloud.

## 2. Environment Setup

This section covers setting up your local development environment.

### Step 2.1: Clone the Repository

```bash
git clone https://github.com/TechGirlNerd900/nigerian-audit-ai.git
cd nigerian-audit-ai
```

### Step 2.2: Install Dependencies

This project uses Poetry to manage dependencies. Run the following command to create a virtual environment and install all required packages from `pyproject.toml`:

```bash
poetry install
```

### Step 2.3: Configure Environment Variables

The application requires a `.env` file for configuration.

1.  **Create the `.env` file:**
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file** and provide the following values:

    -   `DATABASE_URL`: Your full PostgreSQL connection string.
        -   *Example:* `postgresql://user:password@host:port/dbname`
    -   `REDIS_URL`: Your Redis connection string.
        -   *Example:* `redis://localhost:6379`
    -   `GOOGLE_CLOUD_PROJECT_ID`: Your GCP Project ID.
    -   `GOOGLE_APPLICATION_CREDENTIALS`: The **absolute path** to your GCP service account JSON key file.
    -   `GCS_BUCKET`: The name of your Google Cloud Storage bucket for storing models and data.
    -   `FIRS_API_KEY`: Your API key for the Federal Inland Revenue Service.
    -   `JWT_SECRET`: A long, random string for signing JWTs. Generate one with `openssl rand -hex 32`.
    -   `API_KEY`: A secret key for securing access to your API. Generate one with `openssl rand -hex 32`.

## 3. Database and Data Pipeline

### Step 3.1: Initialize the Database

Run the database setup script to create the necessary tables:

```bash
poetry run python scripts/setup_database.py
```

### Step 3.2: Collect Data

Run the data collection script to execute the scrapers and gather data for training:

```bash
poetry run python scripts/collect_data.py
```
This will populate the `data/raw/` directory.

## 4. Model Training

With the data collected, you can now train the machine learning models.

```bash
poetry run python scripts/train_models.py
```
This script will process the raw data, train the models defined in `src/training/`, and save the trained artifacts to the `models/saved_models/` directory.

## 5. Running the API

Once the models are trained, you can start the FastAPI server.

```bash
poetry run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Your API is now live and accessible at `http://localhost:8000`. You can explore the interactive API documentation at `http://localhost:8000/docs`.

---

##  Troubleshooting Common Errors

-   **Error:** `ModuleNotFoundError: No module named '...`
    -   **Cause:** Dependencies are not installed correctly or you are not in the Poetry virtual environment.
    -   **Solution:** Make sure you have run `poetry install`. To activate the virtual environment shell directly, run `poetry shell`.

 -   **Error:** `Poetry... Error: The current project could not be installed: No file/folder found for package...`
    -   **Cause:** This happens when Poetry tries to install the project as a package but cannot find the source code directory. This is common for application layouts where code is in a `src` folder.
    -   **Solution:** You need to tell Poetry not to package the project. Add the line `package-mode = false` to the `[tool.poetry]` section of your `pyproject.toml` file.

-   **Error:** `psycopg2.OperationalError: connection to server failed`
    -   **Cause:** The `DATABASE_URL` in your `.env` file is incorrect, or the PostgreSQL server is not running.
    -   **Solution:** Verify your database connection string. Ensure your database server is active and accessible from your machine.

-   **Error:** `google.auth.exceptions.DefaultCredentialsError`
    -   **Cause:** The application cannot find your GCP credentials.
    -   **Solution:** Ensure the `GOOGLE_APPLICATION_CREDENTIALS` variable in your `.env` file points to the **correct and absolute path** of your service account JSON key.

-   **Error:** `uvicorn: command not found`
    -   **Cause:** You are trying to run `uvicorn` outside of the Poetry-managed environment.
    -   **Solution:** Always prefix your commands with `poetry run` (e.g., `poetry run uvicorn ...`). This ensures you are using the packages installed in the project's virtual environment.

-   **Scraping Failures:**
    -   **Cause:** The websites of regulatory bodies (FIRS, CAC, etc.) may have changed their structure, or your IP might be blocked.
    -   **Solution:** The scrapers in `src/scrapers/` may need to be updated to reflect the new website structure. Check the logs for specific error messages.

-   **Dependency Resolution Errors:**
    -   **Cause:** Sometimes Poetry may struggle to find a compatible set of package versions, as seen with the `google-cloud-sql-connector` issue.
    -   **Solution:** If you encounter a "version solving failed" error, please report it. I can adjust the version constraints in `pyproject.toml` to resolve the conflict.

---

## Frequently Asked Questions (FAQ)

**Q1: How can I add a new machine learning model?**
-   **A:**
    1.  Create your model training logic in a new file within the `src/training/` directory.
    2.  Add your model class to the `src/models/` directory.
    3.  Update `scripts/train_models.py` to include your new training script.
    4.  Integrate the model into `src/api/main.py` by initializing it in the `lifespan` function and creating a new endpoint for it.

**Q2: How do I use the report generation with the Gemini model?**
-   **A:** You need a valid `GOOGLE_APPLICATION_CREDENTIALS` key for a GCP project that has the "Vertex AI API" enabled. The `ReportGenerator` model will automatically use this key to authenticate and interact with the Gemini API.

**Q3: Can I train a single model instead of all of them?**
-   **A:** Yes. The `scripts/train_models.py` script can be modified to accept an argument specifying which model to train. For example: `poetry run python scripts/train_models.py --model financial_analyzer`. (Note: This functionality would need to be added to the script).

**Q4: Where is the data stored?**
-   **A:**
    -   **Raw Data:** Collected by scrapers, stored in `data/raw/`.
    -   **Processed Data:** Cleaned and transformed data ready for training, stored in `data/processed/`.
    -   **Trained Models:** Saved model artifacts are stored in `models/saved_models/`.
    -   **Database:** Structured data, user info, and logs are stored in the PostgreSQL database.

**Q5: How do I deploy this application to production?**
-   **A:** The `README.md` file contains instructions for deploying the application to Google Cloud Run using Docker and Terraform, which is the recommended path for production.
