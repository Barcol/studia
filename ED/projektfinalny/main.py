"""Simple Machine Learning project on Bike Sharing Dataset"""
import pandas as pd
import sklearn.linear_model
import sklearn.tree
import sklearn.model_selection

# Regresja liniowa
dataset = pd.read_csv(r"./day.csv")  # odczyt zbioru danych Bike Sharing
y = dataset.iloc[:, -1]  # utworzenie macierzy obserwacji oraz odpowiedzi
X = dataset.iloc[:, 10:13]  # wybranie temperatury, wilgotnosci oraz predkosci wiatru jako zmiennych (Hipoteza 1)
mnk = sklearn.linear_model.LinearRegression()
mnk.fit(X, y)  # dopasowanie modelu regresji liniowej
print(mnk.intercept_)
print(mnk.coef_)


# Drzewo decyzyjne
def fit_classifier(alg, X_ucz, X_test, y_ucz, y_test):
    alg.fit(X_ucz, y_ucz)
    y_pred = alg.predict(X_test)
    return {
        "ACC":  sklearn.metrics.accuracy_score(y_pred, y_test),
        "P":    sklearn.metrics.precision_score(y_pred, y_test, average="micro"),
        "R":    sklearn.metrics.recall_score(y_pred, y_test, average="micro"),
        "F1":   sklearn.metrics.f1_score(y_pred, y_test, average="micro")
    }


X_ucz, X_test, y_ucz, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.2, random_state=12345)
modrzew = sklearn.tree.DecisionTreeClassifier()
modrzew.fit(X_ucz, y_ucz)
print(pd.Series(modrzew.feature_importances_))
