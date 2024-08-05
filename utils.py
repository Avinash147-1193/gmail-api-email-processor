import sqlite3
import json
from datetime import datetime

def initialize_database(database_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails
                      (id TEXT PRIMARY KEY, snippet TEXT, sender TEXT, subject TEXT, timestamp INTEGER)''')
    connection.commit()
    return connection

def save_emails_to_db(connection, emails):
    cursor = connection.cursor()
    for email in emails:
        cursor.execute('INSERT OR REPLACE INTO emails (id, snippet, sender, subject, timestamp) VALUES (?, ?, ?, ?, ?)',
                       (email['id'], email['snippet'], email['sender'], email['subject'], email['timestamp']))
    connection.commit()

def load_rules_from_file(file_path):
    with open(file_path) as rules_file:
        rules = json.load(rules_file)
    return rules

def retrieve_emails_from_db(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM emails')
    emails = cursor.fetchall()
    return emails

def evaluate_rule_conditions(rule, email, overall_predicate):
    if overall_predicate == 'All':
        return all(evaluate_condition(condition, email) for condition in rule['conditions'])
    elif overall_predicate == 'Any':
        return any(evaluate_condition(condition, email) for condition in rule['conditions'])

def evaluate_condition(condition, email):
    field = condition['field']
    predicate = condition['predicate']
    value = condition['value']

    email_value = {
        'From': email[2],
        'Subject': email[3],
        'Received': email[4]
    }.get(field, '')

    if field == 'Received':
        email_value = datetime.fromtimestamp(int(email_value) / 1000)
        value = datetime.strptime(value, '%Y-%m-%d')
        if predicate == 'Less than':
            return email_value < value
        elif predicate == 'Greater than':
            return email_value > value
    else:
        if predicate == 'Contains':
            return value in email_value
        elif predicate == 'Does not Contain':
            return value not in email_value
        elif predicate == 'Equals':
            return value == email_value
        elif predicate == 'Does not equal':
            return value != email_value

def execute_rule_actions(actions, email, gmail_service):
    for action in actions:
        if action == 'Mark as read':
            gmail_service.users().messages().modify(userId='me', id=email[0], body={'removeLabelIds': ['UNREAD']}).execute()
        elif action == 'Mark as unread':
            gmail_service.users().messages().modify(userId='me', id=email[0], body={'addLabelIds': ['UNREAD']}).execute()
        elif action == 'Move Message':
            pass
