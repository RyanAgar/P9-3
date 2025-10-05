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
        keywords = ['urgent', 'click', 'verify', 'account', 'login'] #Common phishing keywords
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