from django.shortcuts import render
import requests
from django.http import JsonResponse


def index(request):
    api_key = '0412daf24d7b649dec9bb29e'

    # Получение данных о курсах валют
    response = requests.get(url=f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD').json()
    currencies = response.get('conversion_rates')
    response_bitcoin = requests.get(url=f'https://api.coindesk.com/v1/bpi/currentprice.json').json()
    usd_bitcoin = response_bitcoin.get('bpi')
    price_bitcoin = float(usd_bitcoin['USD']['rate'].replace(',', ''))
    currencies['Bitcoin'] = 1 / price_bitcoin
    if request.method == 'GET':
        # Возвращаем HTML-шаблон с данными о валютах для обычных запросов
        content = {
            'currencies': currencies,
        }
        return render(request, 'exchange/index.html', content)

    if request.method == 'POST':
        from_amount = request.POST.get('from-amount')
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        # Получение конвертированной суммы
        converted_amount = round((currencies[to_curr] / currencies[from_curr]) * float(from_amount), 2)

        # Возвращаем HTML-шаблон с данными о валютах и конвертированной суммой
        content = {
            'from_amount': from_amount,
            'from_curr': from_curr,
            'to_curr': to_curr,
            'currencies': currencies,
            'converted_amount': converted_amount,
        }
        return render(request, 'exchange/index.html', content)
