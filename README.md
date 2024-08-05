# Gmail API integration with rules

1. Clone the below github repository.

    https://github.com/Avinash147-1193/gmail-api-email-processor.git
    cd gmail-api-email-processor
    

2. We have to create a python virtual env and activate it.
    
    python3 -m venv venv
    source venv/bin/activate  # For Windows: `venv\Scripts\activate`
    

3. Now we have to install all dependencies in requirements.txt file using below command.
    
    pip install -r requirements.txt
    
 #below instructions are copied staright from google documentation#
4. Follow below steps to setup Gmail API credentials.
    - Follow [this guide](https://developers.google.com/gmail/api/quickstart/python) to create `credentials.json` and place it in the root directory.
    - Add the localhost URL `http://localhost:8020/` to the list of authorized redirect URIs in Google Cloud Console.
    - We have to ensure the scope to be `https://www.googleapis.com/auth/gmail.modify` as we need to have permission for modify.

5. Run the script using below command, which runs `fetch_emails.py` to fetch emails and store them in the sqlite db.
    
    python fetch_emails.py
    

6. Run the `process_emails.py` script to process the emails based on the rules defined in `rules.json`.
    
    python process_emails.py
    

## Demo Video

- [Link to demo video: https://www.loom.com/share/d973e29666e7450fba92c9a52b57d59a?sid=e714a05d-d5da-419c-a073-73525f57f197](#)
