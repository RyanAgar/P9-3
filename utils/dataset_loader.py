import os
import kagglehub


def download_spamassassin():
    raw_path = kagglehub.dataset_download("beatoa/spamassassin-public-corpus")
    print("Downloaded dataset to:", raw_path)

    # Search for folder containing 'spam' and 'easy_ham'
    for root, dirs, files in os.walk(raw_path):
        if "spam" in dirs and ("easy_ham" in dirs or "ham" in dirs or "hard_ham" in dirs):
            print("Found dataset root:", root)
            return root

    raise FileNotFoundError("Could not locate 'spam' and 'ham' folders in downloaded dataset")


def load_dataset(path):
    emails = []
    labels = []

    def load_folder(folder_path, label):
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if not os.path.isfile(file_path):
                continue  # Skip directories or non-files
            try:
                with open(file_path, "r", encoding="latin-1") as f:
                    emails.append(f.read())
                    labels.append(label)
            except Exception as e:
                print(f"Skipped {filename}: {e}")

    # Load spam
    spam_folder = os.path.join(path, "spam")
    load_folder(spam_folder, "spam")

    # Load ham variants
    for ham_type in ["easy_ham", "hard_ham", "ham"]:
        ham_folder = os.path.join(path, ham_type)
        if os.path.exists(ham_folder):
            load_folder(ham_folder, "ham")

    return emails, labels

if __name__ == "__main__":
    path = download_spamassassin()
    emails, labels = load_dataset(path)
    print(f"Loaded {len(emails)} emails")
    print("First email preview:")
    print(emails[0][:500])