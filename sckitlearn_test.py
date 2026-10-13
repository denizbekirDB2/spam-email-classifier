import ast
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

df = pd.read_csv('emails_cleaned.csv', sep='\t', index_col=0)

df["data"] = df["data"].apply(ast.literal_eval)

X_text = df["data"]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X_text, y, test_size=0.2, random_state=0)

def identity_tokenizer(text):
    return text

vectorizer = TfidfVectorizer(
    tokenizer=identity_tokenizer,
    preprocessor=identity_tokenizer,
    lowercase=False
)

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