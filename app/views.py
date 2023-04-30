from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import joblib
import pandas as pd
from io import StringIO

analytics = {
    'usage': 0,
    'reviews': 0,
    'unexpected_errors': [] # maximum 10
}

pipeline = joblib.load('best_model.joblib')
pipeline.predict(pd.Series(['']))

def add_error(request, e):
    global analytics
    if len(analytics['unexpected_errors']) < 10:
        analytics['unexpected_errors'].append((
            # GET /endpoint
            request.method + ' ' + request.path,
            e.__class__.__name__,
            str(e)
        ))

def feel_extractor(texts, include_texts=False):
    global pipeline, analytics
    # si no es un DF, lo convierto a uno
    if not isinstance(texts, pd.DataFrame):
        df = pd.DataFrame(texts, columns=['texto'])
    else:
        df = texts.copy()
        df = df[['texto']]
    df['sentimiento'] = pipeline.predict(df['texto'])
    df['sentimiento'] = df['sentimiento'].replace({1: 'positivo', 0: 'negativo'})
    #cts = df['sentimiento'].value_counts().to_dict()
    # find the percentage of each class * 100
    analytics['usage'] += 1
    analytics['reviews'] += df.shape[0]
    cts = df['sentimiento'].value_counts(normalize=True).mul(100).round(2).to_dict()
    return df.to_dict('records') if include_texts else df['sentimiento'].to_list(), cts
    

@csrf_exempt
def main_endpoint(request):
    try:
        if request.method == 'POST':
            texts = request.POST.getlist('textos[]')
            #include_texts = data['incluir_textos'] if 'incluir_textos' in data else False
            feelings, cts = feel_extractor(texts, False)
            response_data = {'sentimiento': feelings, 'conteo': cts}
            return JsonResponse(response_data)
        elif request.method == 'GET':
            return render(request, 'index.html')
        else:
            return JsonResponse({'error': 'POST or GET request required'})
    except Exception as e:
        add_error(request, e)
        return JsonResponse({'error': str(e)})


@csrf_exempt
def main_endpoint_json(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            texts = data['textos']
            include_texts = data['incluir_textos'] if 'incluir_textos' in data else False
            feelings, cts = feel_extractor(texts, include_texts)
            response_data = {'sentimiento': feelings, 'conteo': cts}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'POST request required'})
    except Exception as e:
        add_error(request, e)
        return JsonResponse({'error': str(e)})
        

@csrf_exempt
def main_endpoint_csvtext(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            texts = data['textos'] # raw text "col1,col2,col3\n1,2,3\n4,5,6"
            sep = data['separador'] if 'separador' in data else ','
            col_name = data['nombre_columna'] if 'nombre_columna' in data else 'texto'
            include_texts = data['incluir_textos'] if 'incluir_textos' in data else False

            df = pd.read_csv(StringIO(texts), sep=sep)

            if col_name not in df.columns:
                return JsonResponse({'error': f'Column name "{col_name}" not found in CSV file'})
            df.rename(columns={col_name: 'texto'}, inplace=True)

            feelings, cts = feel_extractor(df, include_texts)
            response_data = {'sentimiento': feelings, 'conteo': cts}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'error': 'POST request required'})
    except pd.errors.ParserError:
        return JsonResponse({'error': 'Check CSV column separator'})
    except Exception as e:
        add_error(request, e)
        return JsonResponse({'error': str(e)})


@csrf_exempt
def analytics_endpoint(request):
    global analytics
    if request.method == 'GET':
        return JsonResponse(analytics)
    else:
        return JsonResponse({'error': 'GET request required'})
