import re
from typing import Tuple, Set

# -------------------------------------------------------------------
# THE MASTER LIST: Comprehensive list of ALL trusted domains,
# using a Python set {} for maximum lookup speed (O(1)).
# -------------------------------------------------------------------

SAFE_DOMAINS: Set[str] = {
    # 1. SINGAPORE GOVERNMENT & PUBLIC SERVICES 🇸🇬
    "gov.sg", "singpass.gov.sg", "iras.gov.sg", "ica.gov.sg", 
    "moh.gov.sg", "cpf.gov.sg", "hdb.gov.sg", "mom.gov.sg",
    "police.gov.sg", "squiret.sg", 
    
    # 2. SINGAPORE & REGIONAL BANKING / FINANCE
    "dbs.com", "dbs.com.sg", "posb.com.sg", "ocbc.com", "ocbc.com.sg", 
    "uob.com.sg", "maybank2u.com.sg", 
    "standardchartered.com", "hsbc.com.sg", "citi.com.sg", 
    "mas.gov.sg", "sgx.com", 
    
    # 3. ESSENTIAL GLOBAL TECH & SERVICES
    "microsoft.com", "google.com", "apple.com", "amazon.com", 
    "paypal.com", "stripe.com",
    
    # 4. Other
    "singaporeair.com", "grab.com", "shopee.sg",
}


# --- Helper Functions ---

def _get_root_domain(host: str) -> str:
    """
    Extracts the eTLD+1 (the root domain, e.g., mail.google.com -> google.com).
    """
    parts = host.split(".")
    if len(parts) < 2:
        return host
    # Handle common two-part TLDs like co.uk or com.sg
    if len(parts) >= 3 and parts[-2] + "." + parts[-1] in {"co.uk", "com.sg", "com.au", "com.my"}:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])

def _has_homoglyph_chars(domain: str) -> bool:
    """
    Checks for non-ASCII characters that can be used for homoglyph attacks.
    """
    return any(ord(char) > 127 for char in domain)

# --- Primary Check Function ---

def whitelist_check(sender: str) -> Tuple[float, float, str]:
    """
    Evaluates the sender's domain against multiple trust criteria including 
    Punycode, Subdomain Trust, and Base Listing.
    
    Returns: 
        Tuple[risk_score (0.0–4.0), confidence (0–1.0), category (str)]
    """
    # Malformed sender defaults to mild penalty
    if not sender or "@" not in sender:
        return (1.0, 0.5, "malformed_sender")

    domain = sender.split("@")[-1].lower().strip()
    
    # --- CRITERION 1: Exact Match / Trusted Subdomain Check (TRUSTED) ---
    root_domain = _get_root_domain(domain)
    
    # Check if the root domain is on the safe list OR if it's a subdomain 
    if root_domain in SAFE_DOMAINS or any(domain.endswith("." + safe_root) for safe_root in SAFE_DOMAINS):
        # Trusted domain: 0 risk, 1.0 confidence
        return (0.0, 1.0, "trusted_root") 

    # --- CRITERION 2: Punycode/Homoglyph Check (MAX RISK) ---
    if domain.startswith("xn--"):
        # High-risk score for Punycode
        return (4.0, 0.2, "punycode_attack")

    if _has_homoglyph_chars(domain):
        # High-risk score for Homoglyph attempt
        return (4.0, 0.3, "homoglyph_attempt")

    # --- CRITERION 3: General Unlisted Domain (STRICT RISK) ---
    # Stricter penalty for any domain not explicitly whitelisted
    return (2.0, 0.4, "unlisted_domain")