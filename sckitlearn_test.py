from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
)
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from functools import reduce
import pandas as pd
import re

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
ps = PorterStemmer()

df = pd.read_csv('emails_cleaned.csv', sep='\t', index_col=0)

X_text = df["data"]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=0)

# def identity_tokenizer(text):
#     return text

# vectorizer = TfidfVectorizer(
#     tokenizer=identity_tokenizer,
#     preprocessor=identity_tokenizer,
#     lowercase=False
# )
vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


mnb = MultinomialNB(alpha=0.1)
y_pred = mnb.fit(X_train_tfidf, y_train).predict(X_test_tfidf)
print(confusion_matrix(y_test, y_pred))
acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy:  {acc}")
print(f"Precision: {prec}")
print(f"Recall:    {rec}")
print(f"F1-Score:  {f1}")

new_input = """**Note:** If this message has been directed to your SPAM or BULK folder due to
your Internet Service Provider’s settings, we urge you to consider it genuine and
respond accordingly."""

new_input2 = """Hi Y3llow St0ne,
Just a heads-up, on Oct 14 (UTC timezone), we'll attempt to automatically top up your "Y3llow St0ne - In The Dark" ad budget with 70 credits using your balance.
If you'd prefer to turn off automatic top ups, you can easily do so by visiting this page.
If you have any questions or need further assistance, feel free to reach out!
- Jason & Tilly"""

line = new_input2

# sub urls for URL
LABEL = r"[a-z0-9_-]+"
DOT   = r"\s*\.\s*"
HOST  = rf"(?:{DOT})*{LABEL}(?:{DOT}+{LABEL})+"
SEG   = r"[^\s/]+"

pattern = re.compile(
    rf"https? *: */ */\s*{HOST}"                     
    rf"(?:\s*/\s*{SEG})*"                            
    rf"(?:\s*/)?",                                  
    re.I,
)

line = re.sub(pattern, "URL ", line)

# sub e-mails for EMail

LOCAL = r"[a-z0-9_%+-]+(?:\s*\.\s*[a-z0-9_%+-]+)*"
LABEL = r"[a-z0-9-]+"
DOMAIN = rf"{LABEL}(?:\s*\.\s*{LABEL})+"             

pattern = re.compile(rf"\b{LOCAL}\s*@\s*{DOMAIN}", re.I)

line = re.sub(pattern, "EMAIL ", line)

# sub currencys for CURRENCY

line = re.sub(r"[\$\€\£\¥]+ *([0-9]+ ?[0-9]?)+", "CURRENCY ", line)

# sub numbers for NUMBER
line = re.sub(r"([0-9]+ *[0-9]?)+", "NUMBER ", line)

# strip punctuation
translator = str.maketrans('', '', string.punctuation)

line = line.translate(translator)

# remove stop words ,single letters and "subject"
tokens = word_tokenize(line)
stop_words = set(stopwords.words('english'))
filtered_tokens = [word for word in tokens if word not in stop_words and len(word) != 1 and word != "subject"]

stemmed_tokens = [ps.stem(word) for word in filtered_tokens]
line = " ".join(stemmed_tokens)

new_input_tfidf = vectorizer.transform([line])
y_pred = mnb.fit(X_train_tfidf, y_train).predict(new_input_tfidf)
print(y_pred)