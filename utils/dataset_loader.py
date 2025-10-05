import os
import kagglehub


def download_spamassassin():
    raw_path = kagglehub.dataset_download("beatoa/spamassassin-public-corpus")
    print("Downloaded dataset to:", raw_path)

    # Look for the parent folder that contains easy_ham, hard_ham, spam
    for root, dirs, files in os.walk(raw_path):
        if all(d in dirs for d in ["easy_ham", "hard_ham", "spam"]):
            print("Found dataset root:", root)
            return root

    raise FileNotFoundError("Could not locate top-level 'easy_ham', 'hard_ham', and 'spam' folders")


def load_dataset(path):
    emails = []
    labels = []

    def load_email(file_path):
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()
        except Exception as e:
            print(f"Skipped {file_path}: {e}")
            return None

    ham_dirs = ["easy_ham", "easy_ham_2", "ham"]
    spam_dirs = ["spam", "spam_2"]

    for d in ham_dirs:
        dir_path = os.path.join(path, d)
        if not os.path.exists(dir_path):
            continue
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                email = load_email(file_path)
                if email:
                    emails.append(email)
                    labels.append("ham")

    for d in spam_dirs:
        dir_path = os.path.join(path, d)
        if not os.path.exists(dir_path):
            continue
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                email = load_email(file_path)
                if email:
                    emails.append(email)
                    labels.append("phishing")

    from collections import Counter
    print("Label distribution:", Counter(labels))

    return emails, labels
if __name__ == "__main__":
    path = download_spamassassin()
    emails, labels = load_dataset(path)
    print(f"Loaded {len(emails)} emails")
    print("First email preview:")
    print(emails[0][:500])