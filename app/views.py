from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import joblib
import pandas as pd

usage_count = 0
pipeline = joblib.load('best_model.joblib')

def feel_extractor(texts, include_texts):
    global pipeline
    df = pd.DataFrame(texts, columns=['texto'])
    df['sentimiento'] = pipeline.predict(df['texto'])
    df['sentimiento'] = df['sentimiento'].replace({1: 'positivo', 0: 'negativo'})
    return df.to_dict('records') if include_texts else df['sentimiento'].to_list()
    

@csrf_exempt
def main_endpoint(request):
    global usage_count
    if request.method == 'POST':
        data = json.loads(request.body)
        texts = data['textos']
        include_texts = data['incluir_textos'] if 'incluir_textos' in data else False
        feelings = feel_extractor(texts, include_texts)
        response_data = {'sentimiento': feelings}
        usage_count += 1
        return JsonResponse(response_data)
    elif request.method == 'GET':
        return render(request, 'index.html')
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

