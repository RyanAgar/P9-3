import difflib

LEGIT_DOMAINS = ["microsoft.com", "google.com", "paypal.com"]

def domain_similarity(sender):
    domain = sender.split("@")[-1].lower()
    max_ratio = max(difflib.SequenceMatcher(None, domain, legit).ratio() for legit in LEGIT_DOMAINS)
    return 2 if max_ratio > 0.8 and domain not in LEGIT_DOMAINS else 0