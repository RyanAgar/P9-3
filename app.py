from flask import Flask, request, render_template
from utils.email_parser import parse_email
from rules.scorer import final_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        raw_email = request.form["email_content"]
        sender, subject, body, urls = parse_email(raw_email)
        result = final_score(sender, subject, body, urls)
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)