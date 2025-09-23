from utils.dataset_loader import download_spamassassin, load_dataset
from utils.email_parser import parse_email
from rules.scorer import final_score

def evaluate(path):
    emails, labels = load_dataset(path)
    correct = 0
    total = len(emails)

    for email, label in zip(emails, labels):
        sender, subject, body, urls = parse_email(email)
        prediction = final_score(sender, subject, body, urls)
        predicted_label, score = final_score(sender, subject, body, urls)
        predicted_label = predicted_label.lower()
        true_label = "spam" if label == "spam" else "safe"

        if predicted_label == true_label:
            correct += 1

    accuracy = correct / total
    print(f"Accuracy: {accuracy:.2f} ({correct}/{total})")

if __name__ == "__main__":
    path = download_spamassassin()
    evaluate(path)
