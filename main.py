import imaplib
import email
import re
import time
import os
import subprocess
from datetime import datetime, timedelta
import requests
from requests.auth import HTTPBasicAuth
import json
from git import Repo
from dotenv import load_dotenv
from jira_ticket_config import CREATE_TICKET_CONFIG

# Load environment variables from .env file
load_dotenv()
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_IMAP_PASS = os.getenv('EMAIL_IMAP_PASS')
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
USER_NAME = os.getenv('USER_NAME')
LOCAL_REPO_PATH = os.getenv('REPO_PATH')
JIRA_OPEN_API_URL = os.getenv('JIRA_OPENAPI_URL')
REVIEWERS_LIST = os.getenv('PR_REVIEWERS')
GOOGLE_SPACES_WEBHOOK_URL = os.getenv('GOOGLE_SPACES_WEBHOOK_URL')

def get_time_frame():
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    since = yesterday.strftime("%d-%b-%Y")  # e.g., '05-Jun-2025'
    until = tomorrow.strftime("%d-%b-%Y")  # e.g., '06-Jun-2025'
    return since, until

def fetch_target_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_USER, EMAIL_IMAP_PASS)
    mail.select("inbox")

    since, before = get_time_frame()

    # Search for subjects that contain both "Enable" and "bulk refund"
    result, data = mail.search(
        None, f'(SINCE "{since}" BEFORE "{before}")')
    if result != "OK":
        print("No messages found.")
        return []

    matched_emails = []
    for num in data[0].split():
        result, msg_data = mail.fetch(num, "(RFC822)")
        if result != "OK":
            continue

        msg = email.message_from_bytes(msg_data[0][1])
        subject = msg["subject"] or ""

        if "enable" in subject.lower() and "bulk refund" in subject.lower():
            # Get full plain-text body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        charset = part.get_content_charset() or 'utf-8'
                        body += part.get_payload(decode=True).decode(charset, errors="replace")
            else:
                charset = msg.get_content_charset() or 'utf-8'
                body = msg.get_payload(decode=True).decode(charset, errors="replace")

            mids = extract_merchant_ids(body)
            matched_emails.append({
                "subject": subject,
                "body": body,
                "mids": mids
            })
    return matched_emails

def extract_merchant_ids(text):
    return re.findall(r'\b\d{5,6}\b', text)

def create_jira_ticket(mids_found):
    print("Creating JIRA ticket...")
    auth = HTTPBasicAuth(EMAIL_USER, JIRA_API_TOKEN)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    todays_date = datetime.now().strftime("%Y-%m-%d")
    payload = CREATE_TICKET_CONFIG
    # Update the payload with the subject and body
    payload['fields']['description']["content"][0]["content"][0]["text"] = f"Enabling Bulk Refund Feature for MIDs: {mids_found}"
    payload['fields']['customfield_10147']["content"][0]["content"][0]["text"] = f'Support of Bulk Refund for MID - {mids_found}'
    payload['fields']['summary'] = f"Addition of Bullk Refund MID - {mids_found}"
    payload['fields']['customfield_10127'] = todays_date
    payload['fields']['customfield_10167'] = todays_date
    payload['fields']['customfield_10171'] = todays_date
    response = requests.request(
        "POST",
        JIRA_OPEN_API_URL,
        data=json.dumps(payload),
        headers=headers,
        auth=auth
    )
    try:
        ticket_id = response.json()['key']
    except Exception:
        raise ValueError("Creation of JIRA Ticket failed with following exception: ", response.json())

    ticket_url = f"https://easebuzz.atlassian.net/browse/{ticket_id}"
    print(f"JIRA Ticket Link: {ticket_url}")
    return ticket_id, ticket_url

def handle_git_branch(ticket_id):
    repo = Repo(LOCAL_REPO_PATH)
    git = repo.git
    os.chdir(LOCAL_REPO_PATH)

    # Stash any local changes
    git.stash('save')

    # Checkout master and pull latest
    git.checkout('master')
    git.pull()

    # Create and checkout new branch
    new_branch = ticket_id
    git.checkout('-b', new_branch)

    # Push the new branch to remote
    git.push('--set-upstream', 'origin', new_branch)
    return new_branch

def open_vscode():
    subprocess.Popen(["code", LOCAL_REPO_PATH])

def create_bitbucket_pr(
    repo_slug,
    branch_name,
    target_branch="master",
    jira_id="PG-123456"
):
    url = f"https://api.bitbucket.org/2.0/repositories/easebuzz1/{repo_slug}/pullrequests"
    headers = {"Content-Type": "application/json"}
    data = {
        "title": f"{jira_id}: Enable bulk refund for merchant(s)",
        "source": {"branch": {"name": branch_name}},
        "destination": {"branch": {"name": target_branch}},
        "description": f"Automated PR created for {jira_id}",
        # "reviewers": REVIEWERS_LIST,  # Add reviewer UUIDs if required
        "close_source_branch": True
    }

    response = requests.post(url, auth=(os.getenv("BB_USERNAME"), os.getenv("BB_PASS")), json=data, headers=headers)
    print(response.__dict__)
    repo_link = response.json().get('links').get('html').get('href')
    if response.status_code in [200, 201]:
        print(f"✅ Pull Request created: {repo_link}")
    else:
        print("❌ Failed to create PR:", response.text)
    return repo_link

def main():
    matched_mails = fetch_target_email()
    if not matched_mails:
        print("No relevant email found.")
        return

    duplicate_mail_subject = []
    for mail in matched_mails:
        subject, mids_found = mail['subject'], mail['mids']
        print(f"Processing email: {subject}")

        mids_found = list(set(mids_found))
        print(f"Merchant IDs: {', '.join(mids_found)}")

        #* Exclude certain subject lines
        # if subject in set([]):
        #     print(f"Skipping email with subject: {subject}")
        #     continue

        # Discard duplicate emails based on subject
        if subject in duplicate_mail_subject: 
            continue
        duplicate_mail_subject.append(subject)

        # Check if any Merchant IDs were found
        if not mids_found:
            print(f"No Merchant IDs found in email: {subject}")
            continue

        # Create JIRA Ticket
        ticket_id, ticket_url = create_jira_ticket(', '.join(mids_found))
        print(f"Created JIRA Ticket: {ticket_id}")

        # Open VSCode
        open_vscode()

        # Create and push a new branch
        new_branch = handle_git_branch(ticket_id)
        print(f"Switched to new Git branch: {new_branch}")

        time.sleep(7)

        # Raise a PR to merge on master
        pr_url = create_bitbucket_pr(
            repo_slug="dashboard",
            branch_name=ticket_id,
            jira_id=ticket_id
        )

        # Send update on Google Chat
        message = {"text": f"SUCCESS for Bulk-Refund Automation: \n Tix: {ticket_url} \n BE PR: {pr_url}"}
        requests.post(GOOGLE_SPACES_WEBHOOK_URL, data=json.dumps(message), headers={'Content-Type': 'application/json'})

if __name__ == "__main__":
    main()