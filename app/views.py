from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import joblib
import pandas as pd
from io import StringIO

usage_count = 0
pipeline = joblib.load('best_model.joblib')
pipeline.predict(pd.Series(['']))

def feel_extractor(texts, include_texts=False):
    global pipeline
    # si no es un DF, lo convierto a uno
    if not isinstance(texts, pd.DataFrame):
        df = pd.DataFrame(texts, columns=['texto'])
    else:
        df = texts.copy()
        df = df[['texto']]
    df['sentimiento'] = pipeline.predict(df['texto'])
    df['sentimiento'] = df['sentimiento'].replace({1: 'positivo', 0: 'negativo'})
    return df.to_dict('records') if include_texts else df['sentimiento'].to_list()
    

@csrf_exempt
def main_endpoint(request):
    global usage_count
    if request.method == 'POST':
        texts = request.POST.getlist('textos[]')
        #include_texts = data['incluir_textos'] if 'incluir_textos' in data else False
        feelings = feel_extractor(texts, False)
        response_data = {'sentimiento': feelings}
        usage_count += 1
        return JsonResponse(response_data)
    elif request.method == 'GET':
        return render(request, 'index.html')
    else:
        return JsonResponse({'error': 'POST request required'})

@csrf_exempt
def main_endpoint_json(request):
    global usage_count
    if request.method == 'POST':
        data = json.loads(request.body)
        texts = data['textos']
        include_texts = data['incluir_textos'] if 'incluir_textos' in data else False
        feelings = feel_extractor(texts, include_texts)
        response_data = {'sentimiento': feelings}
        usage_count += 1
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'POST request required'})

@csrf_exempt
def main_endpoint_csvtext(request):
    global usage_count
    if request.method == 'POST':
        data = json.loads(request.body)
        texts = data['textos'] # raw text "col1,col2,col3\n1,2,3\n4,5,6"
        sep = data['separador'] if 'separador' in data else ','
        col_name = data['nombre_columna'] if 'nombre_columna' in data else 'texto'
        include_texts = data['incluir_textos'] if 'incluir_textos' in data else False

        df = pd.read_csv(StringIO(texts), sep=sep)
        print(df)

        if col_name not in df.columns:
            return JsonResponse({'error': f'Columna {col_name} no encontrada'})
        df.rename(columns={col_name: 'texto'}, inplace=True)

        feelings = feel_extractor(df, include_texts)
        response_data = {'sentimiento': feelings}
        usage_count += 1
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'POST request required'})


@csrf_exempt
def usage_endpoint(request):
    global usage_count
    if request.method == 'GET':
        response_data = {'usage_count': usage_count}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'GET request required'})

