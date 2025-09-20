import re 
from urllib.parse import urlparse

def suspicious_url_score(urls):
    score = 0
    for url in urls:
        parsed = urlparse(url)
        if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):  # check for IP address in URL 
            score += 3 
        elif parsed.netloc and "." not in parsed.netloc:
            score += 2 
    return score