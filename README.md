---
date: 2024-04-16T14:16:50.602472
author: AutoGPT <info@agpt.co>
---

# aarushi-email-validation-api-2

The task involves developing an endpoint that takes an email address as input and performs several validation checks to determine its legitimacy and validity. The validation process consists of the following steps:

1. **Verifying the Format and Syntax:** The endpoint will utilize Python's regular expression (re) module to ensure the email follows a standard format, such as 'example@domain.com'. A pattern will be defined to match valid email structures.

2. **Checking Domain Existence and MX Records:** The `dns.resolver` module from the `dnspython` package will be employed to query the domain of the email address for MX records. This confirms if the domain is active and set up to receive emails.

3. **Detecting Disposable Email Addresses:** The system will integrate functionality to identify disposable or temporary email addresses through the use of libraries like `validate_email_address` or manually curated lists of known disposable domains. This step helps in filtering out emails that are often used for spam or fraudulent activities.

4. **Identifying Role-Based Email Addresses:** A list of common role-based keywords (e.g., 'info', 'support', 'admin') will be utilized to detect if the email address is associated with a generic role rather than an individual. This is important as role-based emails may not be suitable for personal user accounts due to their shared nature.

5. **Return of Validation Results:** Finally, the endpoint will return a comprehensive validation result, indicating whether the email is valid, and if not, specifying the issues detected (e.g., invalid format, nonexistent domain, disposable email, role-based address).

This system ensures a high level of integrity in user data by verifying email addresses thoroughly before acceptance, enhancing security, and engagement by preventing spam and ensuring communications reach intended recipients.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'aarushi-email-validation-api-2'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
