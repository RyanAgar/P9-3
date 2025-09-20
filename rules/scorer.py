from .whitelist import whitelist_check
from .keyword_check import keyword_score
from .edit_distance import domain_similarity
from .url_check import suspicious_url_score

def final_score(sender, subject, body, urls):
    score = 0 
    score += whitelist_check(sender)
    score += keyword_score(subject, body)
    score += domain_similarity(sender)
    score += suspicious_url_score(urls)
    return "Phishing" if score >= 5 else "Safe"