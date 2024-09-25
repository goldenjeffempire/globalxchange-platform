# globalxchange/stripe_views.py

import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def create_checkout_session(request):
    YOUR_DOMAIN = "http://localhost:8000"
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'T-shirt',
                    },
                    'unit_amount': 2000,
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=YOUR_DOMAIN + '/success/',
        cancel_url=YOUR_DOMAIN + '/cancel/',
    )
    return JsonResponse({
        'id': checkout_session.id
    })

@csrf_exempt
def success(request):
    return render(request, 'success.html')

@csrf_exempt
def cancel(request):
    return render(request, 'cancel.html')
