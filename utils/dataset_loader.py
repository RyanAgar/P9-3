import os
import kagglehub

def download_spamassassin():
    path = kagglehub.dataset_download("beatoa/spamassassin-public-corpus")
    print("Downloaded dataset to:", path)
    return path

def load_dataset(path):
    emails = []
    labels = []
    for label in ["spam", "ham"]: # Loops through "spam" and "ham" folders
        folder = os.path.join(path, label)
        for filename in os.listdir(folder): #Read each file in the folder
            with open(os.path.join(folder, filename), "r", encoding="latin-1") as f:
                emails.append(f.read()) # Add email content to list
                labels.append(label) # Add corresponding label
    return emails, labels