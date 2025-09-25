from .whitelist import whitelist_check
from .keyword_check import keyword_score
from .edit_distance import domain_similarity
from .url_check import suspicious_url_score


#This function pulls together the outputs from all rule modules and produces a final risk label and score
def final_score(sender, subject, body, urls): #Main function that takes parsed email fields
    
    score = 0 #Initializes the total score
    score += whitelist_check(sender) #Adds 0 if sender domain is whitelisted, Adds 1 if not → mild penalty
    score += keyword_score(subject, body) #Adds a percentage score from keyword_check.py
    score += domain_similarity(sender) #Adds 2 if sender domain is similar to a legit domain but not exact, helps catch spoofed domains
    score += suspicious_url_score(urls) #Adds 2–3 points for suspicious URLs: IP addresses, Missing dots, Malformed links
    if whitelist_check(sender) == 0: #If sender is whitelisted, reduce total score by 50%
        score *= 0.5  

    label = "Phishing" if score >= 5 else "Safe" #Threshold: score ≥ 5 → flagged as phishing
    return label, min(score, 10)  # Cap score at 10, returns both label and score

