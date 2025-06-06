# 📫 automyx

**automyx** is an automation tool designed to significantly reduce manual effort involved in the following tasks:
- Scraping **Merchant IDs (MIDs)** from email trails
- Creating corresponding **JIRA tickets**
- Creating **Pull Requests (PRs)** on Bitbucket

---

## 🚀 Features

- Parses trailing email content to extract MIDs
- Automatically creates corresponding JIRA tickets
- Initializes Git branches and creates PRs on Bitbucket based on extracted data
- Minimizes context switching and saves developer time

---

## 🔧 Prerequisites

Before using **automyx**, ensure you have:

- A **Gmail account** with IMAP access enabled
- A **JIRA account** with API token
- Access to your **Bitbucket repository**
- Required credentials and access tokens

---

## 🔑 Required Environment Variables

Create a `.env` file in the root directory and add the following keys with their corresponding values:

| Variable Name     | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `EMAIL_USER`     | Your Gmail address used to fetch mail. E.g. `samarth.srivastava@easebuzz.in` |
| `EMAIL_IMAP_PASS`| Your Gmail App Password. Create one from [Google App Passwords](https://myaccount.google.com/apppasswords) |
| `JIRA_API_TOKEN` | Your JIRA API token. Create one from [JIRA API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens) |
| `USER_NAME`      | Your full name. E.g. `Samarth Srivastava`                                   |
| `BB_USERNAME`    | Your Bitbucket username                                                      |
| `BB_PASS`        | Your Bitbucket App Password (Token). Use the same token you use for git pulls |
| `REPO_PATH`        | Your Bitbucket App Password (Token). Use the same token you use for git pulls |
| `JIRA_OPENAPI_URL`        | Organization's Atlassian URL E.g: https://<your-org-name>.atlassian.net/rest/api/3/issue |
| `PR_REVIEWERS`        | List of UUID's of users you want to review your PR |

### Example `.env` file

```env
EMAIL_USER=samarth.srivastava@easebuzz.in
EMAIL_IMAP_PASS=your_gmail_app_password
JIRA_API_TOKEN=your_jira_api_token
USER_NAME=Samarth Srivastava
BB_USERNAME=your_bitbucket_username
BB_PASS=your_bitbucket_app_password
REPO_PATH=your_local_directory_path
JIRA_OPENAPI_URL=https://<your-org>.atlassian.net/rest/api/3/issue
PR_REVIEWERS=[]
```

---

## 🛠️ Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://your-repo-link.git
   cd automyx
   ```

2. **Install Dependencies**
   ```bash
   pip install gitpython requests python-dotenv 
   ```

3. **Configure Environment**

- Create a .env file in the project root.
- Add the following variables with your credentials:
```bash
EMAIL_USER=samarth.srivastava@easebuzz.in
EMAIL_IMAP_PASS=your_gmail_app_password
JIRA_API_TOKEN=your_jira_api_token
USER_NAME=Samarth Srivastava
BB_USERNAME=your_bitbucket_username
BB_PASS=your_bitbucket_app_password
REPO_PATH=your_local_directory_path
JIRA_OPENAPI_URL=https://<your-org>.atlassian.net/rest/api/3/issue
PR_REVIEWERS=[]
```
- Make sure IMAP access is enabled for your Gmail account.

---

## 🧪 Running the Automation

Once setup is complete, run the script using:
```bash
python main.py
```
Ensure you are connected to the internet and have access to Gmail, Bitbucket, and JIRA.

---

## 📌 Notes

- **Security Tip:** Do not commit your .env file to version control.
Add it to your .gitignore to keep credentials safe.

- Use App Passwords and API Tokens instead of storing raw passwords directly.