from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split

class IntentPredictor:
    """
    ML classifier used to predict user intent from input
    """
    def __init__(self):
        self.model = Pipeline([
            ('tfidf', CountVectorizer()),
            ('clf', SVC())
        ])

    def fit(self, X, y):
        self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)


    def prepare_for_exercise(self):
        dataset = pd.read_csv('data/dialog_acts.dat', header=None)
        X = [" ".join(line.split()[1:]) for line in dataset[0]]
        y = [line.split()[0] for line in dataset[0]]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=42)

        model = IntentPredictor()
        model.fit(X_train, y_train)
        return model

