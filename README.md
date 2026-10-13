# spam-email-classifier

The Complete Preprocessing Pipeline for Multinomial Naive Bayes

For a Multinomial Naive Bayes model using a bag-of-words or TF-IDF vectorizer, execute your text cleaning in this exact, logical order so steps don't accidentally ruin each other:

Step	Action	Why?
1	Convert to Lowercase	Treats "Spam", "SPAM", and "spam" as the exact same feature.
2	Strip HTML/Headers	Cleans out non-human text formatting before splitting words.
3	Replace URLs & Emails	Swaps long web links out for a simple [url] token.
4	Replace/Remove Numbers	Converts digits to [number] tokens (preserving currency context).
5	Strip Punctuation	Removes commas, periods, and brackets to isolate pure words.
6	Filter Stopwords	Drops high-frequency, low-meaning words (e.g., "a", "of").
7	Apply Stemming	Reduces words to their base form (e.g., "win", "winning", "winner" all become "win"). MNB prefers Stemming over Lemmatization because it aggressively collapses vocabulary size.
