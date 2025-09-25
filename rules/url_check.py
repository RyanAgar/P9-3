#Analyze each URL extracted from the email body
#Assign a risk score based on patterns often used in phishing
#Return a cumulative score to be used in scorer.py
import re #-re: used for regex matching (e.g., IP addresses)
from urllib.parse import urlparse #urlparse: breaks a URL into components like scheme, netloc, path

#Main function that takes a list of URLs
def suspicious_url_score(urls):
    score = 0 #Initializes the total score
    for url in urls: #Loops through each URL
        try:
            parsed = urlparse(url) #Uses urlparse() to extract parts like netloc (domain), path, etc.
            if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc): #If the domain (netloc) is an IP address like 192.168.0.1
                score += 3  #Adds 3 points — this is a strong phishing signal
            elif parsed.netloc and "." not in parsed.netloc: #If the domain has no dot (e.g., login, secure)
                score += 2 #Adds 2 points — likely a malformed or deceptive URL
        except ValueError as e:  #If urlparse() fails, skip the URL and log the error
            print(f"Skipped malformed URL: {url} ({e})")
            continue #Prevents crashes from malformed input
    return score #Returns the total score across all URLs

