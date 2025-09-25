import difflib

#List of whitelisted domains
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

#This function checks whether the sender's domain is suspiciously similar to a known legitimate domain — even if it's not an exact match
def domain_similarity(sender):
    #Extracts the domain part of the sender's email (e.g., support@micros0ft.com → micros0ft.com) and then converts it to lowercase
    #for consistent comparison
    domain = sender.split("@")[-1].lower()  
    #Compares the sender's domain to every white listed domain, using difflib.SequenceMatcher to compute a similarity ratio (0 to 1)
    #Finds the highest similarity score among all legit domains
    max_ratio = max(difflib.SequenceMatcher(None, domain, legit).ratio() for legit in LEGIT_DOMAINS) 
    #If the domain is not in the legit list, but is very similar to one eg. (similarity > 0.8), it returns a score of 2
    #Otherwise, it returns 0
    return 2 if max_ratio > 0.8 and domain not in LEGIT_DOMAINS else 0