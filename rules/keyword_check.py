import re
from typing import List, Pattern, Tuple

# --- Configuration ---
_EARLY_WINDOW = 200 # Character count for the "early bonus"
_PATTERN_CACHE: dict = {}

# --- 1. THE SUSPICIOUS KEYWORD LIST (SG Focus) ---
SUSPICIOUS_KEYWORDS: List[str] = [
    # Urgency and Threat
    "URGENT", "FINAL NOTICE", "immediately", "4 hours", "24 hours", "forfeiture", 
    "warning", "security alert", "suspended", "locked", "deactivated", "cancel",
    
    # Financial and Authentication
    "unauthorized login", "re-activate", "verify", "authenticate", "credentials", 
    "bank account", "transaction", "payment", "invoice", "wire transfer", 
    "secure login", "password", 
    
    # Regional / Government (High Risk)
    "CPF contribution", "SingPass", "HDB", "ICA", 
    
    # Institution Names
    "DBS", "PayLah!", "OCBC", "UOB", "MAS", "SquireT"
]

# --- 2. HELPER FUNCTIONS ---

def _get_pattern(word: str) -> Pattern[str]:
    """Caches compiled regex patterns for speed."""
    if word not in _PATTERN_CACHE:
        # Compiles the word to match as a whole word, case-insensitive
        _PATTERN_CACHE[word] = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    return _PATTERN_CACHE[word]

def _subject_points(subject: str, kw_pat: Pattern[str]) -> float:
    """Adds 5 points for a keyword hit in the subject (high impact)."""
    if kw_pat.search(subject):
        return 5.0
    return 0.0

def _body_points(body: str, kw_pat: Pattern[str]) -> Tuple[float, float]:
    """Adds 2 points for a body hit, plus an early bonus."""
    points = 0.0
    bonus = 0.0
    match = kw_pat.search(body)
    
    if match:
        points = 2.0
        # Check for early bonus (appears in the first 200 characters)
        if match.start() < _EARLY_WINDOW:
            bonus = 1.0
            
    return points, bonus

# --- 3. MAIN SCORING FUNCTION ---

# Maximum points are calculated based on the number of keywords and the maximum points per keyword.
MAX_POINTS = len(SUSPICIOUS_KEYWORDS) * 5.0 

def keyword_score(subject: str, body: str) -> float:
    """
    Calculates overall keyword risk and normalizes the final score to a 0.0–10.0 scale.
    """
    subject = subject or ""
    body = body or ""
    total_score = 0.0

    global MAX_POINTS 
    if MAX_POINTS == 0:
        return 0.0

    for kw in SUSPICIOUS_KEYWORDS:
        kw_pat = _get_pattern(kw)
        
        total_score += _subject_points(subject, kw_pat)
        body_points, early_bonus = _body_points(body, kw_pat)
        total_score += body_points + early_bonus

    # CRITICAL FIX: Normalize the calculated total to the 0.0 - 10.0 scale.
    final_score_normalized = (total_score / MAX_POINTS) * 10.0
    
    return min(final_score_normalized, 10.0)