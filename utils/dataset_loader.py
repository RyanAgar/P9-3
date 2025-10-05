import os
import kagglehub


def download_spamassassin():
    raw_path = kagglehub.dataset_download("beatoa/spamassassin-public-corpus")
    print("Downloaded dataset to:", raw_path)

    # Look for the parent folder that contains easy_ham, hard_ham, spam_2
    for root, dirs, files in os.walk(raw_path):
        if all(d in dirs for d in ["easy_ham", "hard_ham", "spam_2"]):
            print("Found dataset root:", root)
            return root

    raise FileNotFoundError("Could not locate top-level 'easy_ham', 'hard_ham', and 'spam_2' folders")


def load_dataset(path):
    emails = []
    labels = []

    def load_folder(folder_path, label):
        for filename in os.listdir(folder_path):
            if filename.startswith("__MACOSX"):
                continue  # Skip system folders

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
    spam_folder = os.path.join(path, "spam_2", "spam_2")
    load_folder(spam_folder, "spam")


    # Load ham variants
    for ham_type in ["easy_ham", "hard_ham"]:
        ham_folder = os.path.join(path, ham_type, ham_type)
    if os.path.exists(ham_folder):
        load_folder(ham_folder, "ham")


    return emails, labels

if __name__ == "__main__":
    path = download_spamassassin()
    emails, labels = load_dataset(path)
    print(f"Loaded {len(emails)} emails")
    print("First email preview:")
    print(emails[0][:500])