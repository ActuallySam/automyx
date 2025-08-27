# 🛠️ automyx

**automyx** is a collection of automation scripts designed to streamline and reduce manual effort in operational and analytical workflows, such as extracting Merchant IDs from emails, automating JIRA ticket creation, Bitbucket PRs, and analyzing Swiggy delivery spends.

---

## 📂 Repository Structure

```
Calculate Delivery Spends on Swiggy/
    spendings.py
Scrape Mails to Automate Operation/
    .gitignore
    jira_ticket_config.py
    main.py
    README.md
README.md
```

---

## 🚀 Features

- **Email Automation:**  
  Scrapes Gmail inbox for emails related to "Enable bulk refund", extracts Merchant IDs, and automates the creation of JIRA tickets and Bitbucket PRs.  
  See [`main.py`](Scrape%20Mails%20to%20Automate%20Operation/main.py) for implementation.

- **Swiggy Spend Analysis:**  
  Analyzes and sums up delivery spends from Swiggy order history for a target city.  
  See [`spendings.py`](Calculate%20Delivery%20Spends%20on%20Swiggy/spendings.py) for implementation.

---

## 🔧 Prerequisites

- Python 3.7+
- [pip](https://pip.pypa.io/en/stable/)
- Gmail account with IMAP enabled
- JIRA and Bitbucket accounts with API tokens

---

## ⚙️ Setup & Installation

1. **Clone the Repository**
    ```bash
    git clone <your-repo-link>
    cd automyx
    ```

2. **Install Dependencies**
    ```bash
    pip install gitpython requests python-dotenv
    ```

3. **Configure Environment Variables**

    - Create a `.env` file in `Scrape Mails to Automate Operation/` with the following keys:

      | Variable Name         | Description                                              |
      |----------------------|----------------------------------------------------------|
      | EMAIL_USER           | Gmail address for fetching emails                        |
      | EMAIL_IMAP_PASS      | Gmail App Password                                       |
      | JIRA_API_TOKEN       | JIRA API token                                           |
      | USER_NAME            | Your full name                                           |
      | BB_USERNAME          | Bitbucket username                                       |
      | BB_PASS              | Bitbucket App Password                                   |
      | REPO_PATH            | Local path to your Bitbucket repo                        |
      | JIRA_OPENAPI_URL     | Atlassian API URL for issue creation                     |
      | PR_REVIEWERS         | List of Bitbucket reviewer UUIDs (as a JSON array)       |
      | GOOGLE_SPACES_WEBHOOK_URL | (Optional) Google Chat webhook for notifications    |
      | REPO_SLUG            | Bitbucket repository slug                                |

    - Example `.env`:
      ```env
      EMAIL_USER=your_email@domain.com
      EMAIL_IMAP_PASS=your_gmail_app_password
      JIRA_API_TOKEN=your_jira_api_token
      USER_NAME=Your Name
      BB_USERNAME=your_bitbucket_username
      BB_PASS=your_bitbucket_app_password
      REPO_PATH=/path/to/your/local/repo
      JIRA_OPENAPI_URL=https://<your-org>.atlassian.net/rest/api/3/issue
      PR_REVIEWERS=[]
      GOOGLE_SPACES_WEBHOOK_URL=https://chat.googleapis.com/v1/spaces/...
      REPO_SLUG=your-repo-slug
      ```

---

## 🧪 Usage

### 1. **Automate Operations (JIRA/PR)**
Navigate to `Scrape Mails to Automate Operation/` and run:
```bash
python main.py
```
- This will process relevant emails, create JIRA tickets, initialize git branches, create Bitbucket PRs, and optionally send notifications.

### 2. **Analyze Swiggy Delivery Spends**
Navigate to `Calculate Delivery Spends on Swiggy/` and run:
```bash
python spendings.py
```
- This will fetch and sum up your Swiggy order spends for the configured city.

---

## 📌 Notes

- **Security:**  
  Never commit your `.env` file or sensitive credentials.  
  The `.gitignore` is already set up to exclude `.env` and other sensitive files.

- **Customization:**  
  Update the configuration in [`jira_ticket_config.py`](Scrape%20Mails%20to%20Automate%20Operation/jira_ticket_config.py) as per your JIRA workflow.

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

MIT