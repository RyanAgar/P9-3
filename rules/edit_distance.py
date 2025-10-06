import difflib
from typing import Set

# -------------------------------------------------------------------
# ⚠️ IMPORT: Get the master domain list from whitelist.py
from .whitelist import SAFE_DOMAINS 
# -------------------------------------------------------------------

# --- Helper Function (Replicated for self-contained module logic) ---
def _get_root_domain(host: str) -> str:
    """
    Extracts the eTLD+1 (the root domain, e.g., mail.google.com -> google.com).
    This handles common multi-part TLDs like co.uk or com.sg.
    """
    parts = host.split(".")
    if len(parts) < 2:
        return host
    # Handle common two-part TLDs like co.uk or com.sg
    if len(parts) >= 3 and parts[-2] + "." + parts[-1] in {"co.uk", "com.sg", "com.au", "com.my"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])

#This function checks whether the sender's domain is suspiciously similar to a known legitimate domain — even if it's not an exact match
def domain_similarity(sender: str) -> int:
    """
    Performs a similarity check (typosquatting detection) focused on the 
    root domain against the master SAFE_DOMAINS list.
    
    Returns: 0 (safe) or 2 (suspiciously similar).
    """
    #Extracts the domain part of the sender's email 
    if "@" not in sender:
        return 0 # Cannot process

    domain = sender.split("@")[-1].lower().strip()
    
    # 1. Get the ROOT domain to check for similarity (e.g., mail.micros0ft.com -> micros0ft.com)
    root_domain = _get_root_domain(domain)
    
    # 2. Skip if domain is too short or is ALREADY EXACTLY whitelisted
    if len(root_domain) < 5 or root_domain in SAFE_DOMAINS:
        return 0

    # 3. Checks similarity ratio against all target domains
    # We check the suspicious ROOT domain against the SAFE_DOMAINS list
    for target in SAFE_DOMAINS: 
        s = difflib.SequenceMatcher(None, root_domain, target)
        
        # If similarity is high (0.8 or greater), it's a strong indicator of spoofing
        if s.ratio() >= 0.8: 
            return 2 # High-risk score added (for typosquatting like 'micros0ft.com')
            
    return 0 # No significant similarity detected