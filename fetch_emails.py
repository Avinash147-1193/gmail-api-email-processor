import os
import sqlite3
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import Request
from utils import initialize_database, save_emails_to_db

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_with_gmail():
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            credentials = flow.run_local_server(port=8020)  # Specified port 8020
        with open('token.json', 'w') as token_file:
            token_file.write(credentials.to_json())
    return credentials

def fetch_inbox_emails(service):
    email_list = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=100).execute().get('messages', [])
    emails = []
    
    for email in email_list:
        email_data = service.users().messages().get(userId='me', id=email['id']).execute()
        email_payload = email_data['payload']
        email_headers = email_payload['headers']
        email_info = {
            'id': email['id'],
            'snippet': email_data['snippet'],
            'sender': '',
            'subject': '',
            'timestamp': email_data['internalDate']
        }
        for header in email_headers:
            if header['name'] == 'From':
                email_info['sender'] = header['value']
            if header['name'] == 'Subject':
                email_info['subject'] = header['value']
        emails.append(email_info)
    return emails

def main():
    credentials = authenticate_with_gmail()
    gmail_service = build('gmail', 'v1', credentials=credentials)
    inbox_emails = fetch_inbox_emails(gmail_service)
    database_connection = initialize_database('emails.db')
    save_emails_to_db(database_connection, inbox_emails)
    database_connection.close()

if __name__ == '__main__':
    main()
