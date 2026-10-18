from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import pandas as pd
import pickle

df = pd.read_csv('emails_cleaned.csv', sep='\t')
 
X = df["data"]
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

vectorizer = TfidfVectorizer()

X_train_tfidf = vectorizer.fit_transform(X_train)

X_test_tfidf = vectorizer.transform(X_test)


mnb = MultinomialNB(alpha=0.1)
y_pred = mnb.fit(X_train_tfidf, y_train).predict(X_test_tfidf)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    pickle.dump(mnb, open("naivebayes_classifier.pkl","wb"))
    pickle.dump(vectorizer, open("tfidf_vectorizer.pkl","wb"))