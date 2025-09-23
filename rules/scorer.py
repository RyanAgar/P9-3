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
    if whitelist_check(sender) == 0:
        score *= 0.5  # reduce score by half for trusted senders

    label = "Phishing" if score >= 5 else "Safe"
    return label, min(score, 10)  # Cap score at 10

