<<<<<<< HEAD
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
=======
# -----------------------------------------------------------
# This file checks for suspicious words in an email.
# Idea:
#   - Certain words like "urgent" or "password" often appear in scams.
#   - If they are in the SUBJECT line, they are extra suspicious.
#   - If they are in the BODY, they still matter, but less.
#   - If they appear right at the START of the body, we treat it as even riskier.
# Each word can give at most 5 points total.
# In the end, we turn the total into a percentage (0–100%).
# -----------------------------------------------------------

import re
from pathlib import Path

#Load keywords.txt into a list
def load_keywords(path: str) -> list[str]:
    seen = set()
    keyword_list = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"): #Skip comments and empty lines
                continue
            keyword = " ".join(line.split())

            if keyword.lower() in seen: #Prevent duplication by checking with set object O(1)
                continue
            seen.add(keyword.lower())

            keyword_list.append(keyword)
    return keyword_list

KEYWORDS_PATH = Path(__file__).parent / "keywords.txt"
SUSPICIOUS_KEYWORDS = load_keywords(KEYWORDS_PATH)

# Scoring rules:
# - Subject hit = 3 points
# - Body hit = 1 point
# - Bonus if word appears in first 200 chars of body = +1 point
# Max = 5 points per keyword -> makes it easy to convert to %
_MAX_PER_KEYWORD = 6
_EARLY_WINDOW = 200  # we call "early" = first 200 characters of the email body
>>>>>>> d3bcb0cb32df29d4436cecf5d2f5814e6d277514

def _get_pattern(word: str) -> Pattern[str]:
    """Caches compiled regex patterns for speed."""
    if word not in _PATTERN_CACHE:
        # Compiles the word to match as a whole word, case-insensitive
        _PATTERN_CACHE[word] = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    return _PATTERN_CACHE[word]

<<<<<<< HEAD
def _subject_points(subject: str, kw_pat: Pattern[str]) -> float:
    """Adds 5 points for a keyword hit in the subject (high impact)."""
    if kw_pat.search(subject):
        return 5.0
    return 0.0

def _body_points(body: str, kw_pat: Pattern[str]) -> Tuple[float, float]:
    """Adds 2 points for a body hit, plus an early bonus."""
    points = 0.0
    bonus = 0.0
=======
def _regex_for_kw(kw: str) -> re.Pattern:
    """
    Build a search pattern for each keyword.
    - If keyword is 'bank', only match the whole word 'bank'
      (not 'banking' or 'snowbank').
    - If keyword is 'sign in', match that full phrase.
    - Ignore upper/lowercase -> 'BANK', 'Bank', 'bank' all match.
    """
    return re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)


def _subject_points(subject: str, kw_pat: re.Pattern) -> int:
    """Return 3 if kw_pat matches subject, else return 0."""
    if not subject:
        return 0
    return 3 if kw_pat.search(subject) else 0


def _body_points(body: str, kw_pat: re.Pattern) -> tuple[int, int]:
    """
    Check if keyword is in the body.
    - Always gives 1 point if found.
    - Gives +1 extra if it shows up very early (first 200 chars).
    - Returns tuple of int (normal_points, early_bonus).
    """
    if not body:
        return 0, 0
>>>>>>> d3bcb0cb32df29d4436cecf5d2f5814e6d277514
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
<<<<<<< HEAD
    Calculates overall keyword risk and normalizes the final score to a 0.0–10.0 scale.
=======
    Calculate overall keyword risk as a percentage (0-100%).
    - Goes through every suspicious word.
    - Adds points from subject + body + early bonus.
    - Normalizes against max possible points for fairness.
>>>>>>> d3bcb0cb32df29d4436cecf5d2f5814e6d277514
    """
    #Ensure subject and body are strings
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

<<<<<<< HEAD
    # CRITICAL FIX: Normalize the calculated total to the 0.0 - 10.0 scale.
    final_score_normalized = (total_score / MAX_POINTS) * 10.0
    
    return min(final_score_normalized, 10.0)
=======
    max_possible = len(SUSPICIOUS_KEYWORDS) * _MAX_PER_KEYWORD
    return round((score / max_possible) * 100, 2) #score in percentage
>>>>>>> d3bcb0cb32df29d4436cecf5d2f5814e6d277514
