import json
import sqlite3
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from utils import load_rules_from_file, retrieve_emails_from_db, evaluate_rule_conditions, execute_rule_actions

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate_with_gmail():
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    return credentials

def main():
    credentials = authenticate_with_gmail()
    gmail_service = build('gmail', 'v1', credentials=credentials)
    rules = load_rules_from_file('rules.json')
    database_connection = sqlite3.connect('emails.db')
    emails = retrieve_emails_from_db(database_connection)
    database_connection.close()
    for rule in rules['rules']:
        for email in emails:
            if evaluate_rule_conditions(rule, email, rules['predicate']):
                execute_rule_actions(rule['actions'], email, gmail_service)

if __name__ == '__main__':
    main()
