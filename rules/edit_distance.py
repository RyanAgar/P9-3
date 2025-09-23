import difflib

LEGIT_DOMAINS = ["microsoft.com",
    "google.com",
    "paypal.com",
    "apple.com",
    "amazon.com",
    "github.com",
    "linkedin.com",
    "dropbox.com",
    "zoom.us",
    "outlook.com",
    "stripe.com",
    "bankofamerica.com",
    "chase.com",
    "hsbc.com",
    "citibank.com",
    "ocbc.com",
    "dbs.com",
    "uob.com.sg",
    "gov.sg",
    "ntu.edu.sg",
    "nus.edu.sg",
    "safeguard.com",
    "adobe.com",
    "cloudflare.com",
    "intel.com",
    "samsung.com",
    "netflix.com",
    "spotify.com",
    "slack.com",
    "airbnb.com",
    "uber.com",
    "grab.com",
    "lazada.sg",
    "shopee.sg"
]

def domain_similarity(sender):
    domain = sender.split("@")[-1].lower()
    max_ratio = max(difflib.SequenceMatcher(None, domain, legit).ratio() for legit in LEGIT_DOMAINS)
    return 2 if max_ratio > 0.8 and domain not in LEGIT_DOMAINS else 0