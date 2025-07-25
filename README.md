# AI-Powered Resume Optimizer

An AI-driven Streamlit application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). This tool analyzes your resume against a job description, calculates a match score, and suggests keywords to improve your chances.

## 🚀 Features

-   **Secure User Authentication**: Login and signup system using MySQL and bcrypt for password hashing.
-   **Resume Parsing**: Supports both PDF and DOCX file uploads.
-   **ATS Score Analysis**: Compares your resume to a job description and provides a percentage score.
-   **Keyword Suggestions**: Highlights matched keywords and shows which crucial keywords are missing.
-   **Automated Resume Editing**: Automatically generates an updated DOCX resume with the missing keywords added to the "Skills" section.
-   **Downloadable Results**: Allows you to download the optimized resume.
-   **Deployment-Ready**: Configured for easy deployment on Render.

## 💻 Tech Stack

-   **Frontend**: Streamlit
-   **Backend**: Python
-   **Database**: MySQL
-   **Authentication**: bcrypt for password hashing
-   **File Handling**: PyMuPDF (for PDF), python-docx (for DOCX)
-   **Visualization**: Matplotlib
-   **Deployment**: Render

## ⚙️ Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd ai-resume-app
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up MySQL:**
    -   Install and run a local MySQL server.
    -   Create a database (e.g., `resume_app_db`).

4.  **Configure Environment Variables:**
    -   Streamlit now recommends using `secrets.toml` for local development. Create a file `.streamlit/secrets.toml` with your database credentials:
    ```toml
    # .streamlit/secrets.toml
    [mysql]
    host = "localhost"
    user = "your_mysql_user"
    password = "your_mysql_password"
    database = "resume_app_db"
    ```

5.  **Initialize the database and run the app:**
    -   First, run the `init_db` script from your terminal to create the `users` table:
        ```bash
        python -c "from auth.db import init_db; init_db()"
        ```
    -   Then, run the Streamlit application:
        ```bash
        streamlit run app.py
        ```

## ☁️ Deployment on Render

This project is configured for deployment on Render using the `render.yaml` file.

1.  **Push to GitHub:**
    -   Create a new repository on GitHub and push the project code.

2.  **Create a New Blueprint on Render:**
    -   Go to your Render Dashboard and click **New > Blueprint**.
    -   Connect the GitHub repository you just created.
    -   Render will automatically detect the `render.yaml` file and configure the services.

3.  **Configure Environment Variables:**
    -   The `render.yaml` file references a secret group named `mysql-credentials`.
    -   On Render, go to **Environment** and create a **New Secret Group**.
    -   Name it `mysql-credentials`.
    -   Add the following keys. The values will be automatically provided by the Render MySQL database instance once it's created.
        -   `host`: The internal hostname of your Render MySQL service (e.g., `mysql-db`).
        -   `user`: The user from your Render MySQL instance.
        -   `password`: The password from your Render MySQL instance.
        -   `database`: The database name from your Render MySQL instance.

4.  **Deploy:**
    -   Click **Create** or **Apply Changes**. Render will build and deploy both the web service and the MySQL database. The `buildCommand` in `render.yaml` will automatically initialize the database table on the first deploy.