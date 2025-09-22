import re
from urllib.parse import urlparse

def suspicious_url_score(urls):
    score = 0
    for url in urls:
        try:
            parsed = urlparse(url)
            if re.match(r'\d+\.\d+\.\d+\.\d+', parsed.netloc):
                score += 3  # IP address in URL
            elif parsed.netloc and "." not in parsed.netloc:
                score += 2
        except ValueError as e:  #if URL is not a IP Address, skip
            print(f"Skipped malformed URL: {url} ({e})")
            continue
    return score
