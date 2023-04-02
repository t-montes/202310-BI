"""Ejemplo de cómo importar el modelo Joblib para nuevos datos."""

from utils import *

data = pd.read_csv('data/MovieReviews.csv')

pipeline = joblib.load('best_model.joblib')

y_true = data['sentimiento'].replace({'negativo': 0, 'positivo': 1})
y_pred = pipeline.predict(data['review_es'])

classif_report = classification_report(y_true, y_pred, output_dict=True)
print(classif_report)