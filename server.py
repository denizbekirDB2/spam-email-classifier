from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import pickle
import data_cleaner

app = Flask(__name__)
CORS(app)

naivebayes_model = pickle.load(open("naivebayes_classifier.pkl", "rb"))
logistcreg_model = pickle.load(open("logisticreg_classifier.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/classification", methods=["POST"])
def classification():
    email = request.get_json()["email"]

    email_cleaned = data_cleaner.pipeline(email)
    mail_vectorized = vectorizer.transform([email_cleaned])

    nb_preds = naivebayes_model.predict(mail_vectorized)
    lr_preds = logistcreg_model.predict(mail_vectorized)

    if nb_preds == lr_preds and nb_preds == 1:
        return jsonify({"data": "Spam"}),200
    if nb_preds == lr_preds and nb_preds == 0:
        return jsonify({"data": "Not Spam"}),200

    return jsonify({"data": "Unsure"}), 200

if __name__ == '__main__':

    app.run(debug=True)