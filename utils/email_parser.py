import re
from email import message_from_string

def parse_email(raw_email):
    message = message_from_string(raw_email)
    sender = message.get("From","")
    subject = message.get("Subject","")
    
    #Get body (check if email is multipart -> get body from text/plain type)
    body = ""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")

    else:
        body = message.get_payload(decode=True).decode(errors="ignore")
    
    urls = re.findall(r'(https?://\S+)', body)
    return sender, subject, body, urls

def extract_sender_domain(email):
    match = re.search(r'From:.*?@([\w\.-]+)', email)
    return match.group(1) if match else 'unknown'
