# rules/whitelist.py
# Simple domain whitelist check

SAFE_DOMAINS = {
    # Tech giants
    "microsoft.com",
    "google.com",
    "apple.com",
    "amazon.com",
    "facebook.com", "meta.com",
    
    # Finance & payments
    "paypal.com",
    "chase.com", "bankofamerica.com", "wellsfargo.com",
    "hsbc.com", "dbs.com", "ocbc.com", "uobgroup.com",
    
    # Shopping / services
    "ebay.com",
    "alibaba.com", "aliexpress.com",
    "netflix.com",
    "spotify.com",
    
    # Travel & logistics
    "dhl.com", "fedex.com", "ups.com",
    "booking.com", "expedia.com",
    
    # Government / orgs (common in phishing spoofs)
    "irs.gov",
    "singpass.gov.sg",
    "gov.uk"
}

def whitelist_check(sender: str) -> int:
    """
    Check if the sender’s email is from a trusted (safe) company.
    
    Args:
        sender (str): full email address (example: user@paypal.com)
    
    Returns:
        int: 
          - 0 → safe (in whitelist)
          - 1 → suspicious (not in whitelist or malformed email)
    """
    if not sender or "@" not in sender:
        return 1  # suspicious if email is broken or missing
    
    domain = sender.split("@")[-1].lower().strip()
    return 0 if domain in SAFE_DOMAINS else 1