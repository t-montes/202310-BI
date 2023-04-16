"""Ejemplo de cómo utilizar el modelo Joblib para nuevos datos."""

# La librería utils.py debe estar en el mismo directorio que este script
# Esta librería es necesaria porque importa todos los módulos necesarios para correr el modelo .joblib
from utils import *

""" Ejemplo 1, con un CSV de MovieReviews.csv """
"""
path = 'data/MovieReviews.csv' # Modificar el path de acuerdo a la ubicación del archivo .csv con los datos a predeci


data = pd.read_csv(path)

pipeline = joblib.load('best_model.joblib')
y_pred = pipeline.predict(data['review_es'])

data['predicted_sentimiento'] = y_pred
data['predicted_sentimiento'] = data['predicted_sentimiento'].replace({0: 'negativo', 1: 'positivo'})

# Se guarda el archivo con el nombre original + _predicted.csv
new_filename = path.split('.')[0] + '_predicted.csv'
data.to_csv(new_filename, index=False)
"""
""" Ejemplo 2, con un simple texto (str) """

texts = [
    'Terrible película, no la recomiendo.',
    'Excelente película, la recomiendo.'
    ]

# convert text to pandas dataframe
text = pd.DataFrame(texts, columns=['review_es'])

pipeline = joblib.load('best_model.joblib')
y_pred = pipeline.predict(text['review_es'])

print(y_pred)
