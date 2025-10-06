import re
from email import message_from_string

def parse_email(raw_email: str) -> tuple[str, str, str, list[str]]:
    """
    Parse a raw email string and return sender, subject, body, and extracted URLs.

    Returns: 
    tuple[str, str, str, list[str]]: (sender, subject, body, urls)
    - sender: value of the From header
    - subject: value of the Subject header
    - body: value of body (only text/plain)
    - urls: list of URLs
    """
    message = message_from_string(raw_email)

    sender = message.get("From","")
    subject = message.get("Subject","")
    
    #Get body (check if email is multipart -> get body contents from text/plain type)
    body = ""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = message.get_payload(decode=True).decode(errors="ignore")
    urls = re.findall(r'(https?://\S+)', body)

    return sender, subject, body, urls

def extract_sender_domain(raw_email: str) -> str:
    """
    Extract domain from a "From" header, will default to 'unknown' if not found.
    """    
    match = re.search(r'From:.*?@([\w\.-]+)', raw_email)
    return match.group(1).lower() if match else 'unknown'
