import re
from utils.email_parser import extract_sender_domain 
#Extracts the domain from the sender’s email address (e.g., paypal.com).


#Counts number of URLs in the email body
#Phishing emails often contain suspicious links. More links → higher risk.
def count_links(email): 
    return len(re.findall(r'https?://', email)) #Count occurrences of http/https links

    #Calculates the ratio of phishing-related keywords to total words.
    #Why it matters: Phishing emails often use urgent or manipulative language. 
    #Higher density → higher risk.
def keyword_density(email, keywords=None): 

    if keywords is None:
        keywords = [# Urgency
    "urgent", "immediately", "important", "attention", "asap",
    # Verification / Login
    "verify", "update", "login", "sign in", "authenticate",
    # Account / Security
    "account", "password", "credentials", "secure", "suspended", "locked",
    # Financial / Payment
    "payment", "invoice", "transaction", "credit card", "bank",
    # Links
    "click", "link", "http", "https",
    # Security & Account Threats
    "account suspended",
    "unauthorized login",
    "verify your identity",
    "your account has been locked",
    "security alert",
    "unusual activity detected",
    "confirm your password",
    "update billing information",
    "login required",
    "secure your account",
    # Financial Bait & Urgency
    "claim your prize",
    "you’ve won",
    "limited-time offer",
    "urgent action required",
    "act now",
    "act fast",
    "reward",
    "cash bonus",
    "exclusive deal",
    "click here to claim",
    "final notice",
    # Social Engineering & Impersonation
    "important message from HR",
    "invoice attached",
    "payment overdue",
    "reset your credentials",
    "document review required",
    "confidential message",
    "internal memo",
    "IT department request",
    "CEO request",
    "wire transfer",
    # Suspicious Link Language
    "login here",
    "verify now",
    "secure portal",
    "click to unlock",
    "access your account",
    "update now",
    "download attachment",
    "open document"] #Common phishing keywords
    total_words = len(email.split()) #Total word count
    keyword_hits = sum(email.lower().count(k) for k in keywords) #Count of keywords found
    return keyword_hits / total_words if total_words else 0 #Avoid division by zero


#Combines all the above into a dictionary, used for hybrid_scorer.py
def extract_features(email): 
    return {
        "sender_domain": extract_sender_domain(email),
        "link_count": count_links(email),
        "keyword_score": keyword_density(email)
    }