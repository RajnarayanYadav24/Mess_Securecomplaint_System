from __future__ import print_function
import base64
import os.path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw_message.decode()}

def send_email(to, subject, message_text):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    sender = "me"
    message = create_message(sender, to, subject, message_text)
    sent_message = service.users().messages().send(userId="me", body=message).execute()
    print(f"Email sent to {to}, Message ID: {sent_message['id']}")


def main():
    creds = None
    # token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret_858063691277.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    

if __name__ == '__main__':
    main()
