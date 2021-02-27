from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Item
from django.views.generic.list import ListView
from django.utils import timezone
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from core.models import Codice,SocialCodice
import pyqrcode
from django.utils import timezone
import os
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Orders
import requests
import json
import uuid

stripe.api_key = 'sk_test_51H5YU9KvsILJhwe0uUmZLDnIH0lQMu5hYHEgT7BO6ImuRvnSUGHR2qxJwnB60QEW8Vc6lWZK5emkRgV6KDa3Ajfl00MLcZvOw1'

# Create your views here.
def viewProdotto(request,pk):
    prodotto = get_object_or_404(Item,pk=pk)
    if request.method == 'POST':
        date_creation = timezone.now()
        data = 'https://127.0.0.1:8000/'
        if prodotto.name == 'Tas-Shirt':
            validate = URLValidator()
            try:
                validate(data)
                Codice.objects.create(user=request.user,redirect=data,date_creation=date_creation)
                codice = Codice.objects.get(user=request.user,redirect=data, date_creation=date_creation)
                qr = pyqrcode.create(codice.get_view())
                qr.svg(f'media-serve/qr_{codice.uuid}.svg',scale=10)
                codice.image_qr = f'qr_{codice.uuid}.svg'
                codice.save()
                return redirect('payment_page',pk=prodotto.pk,uuid=codice.uuid) #to change
            except ValidationError:
                messages.error(request,"L'URL inserito non è valido")
                return redirect('prodottoview',pk=prodotto.pk)
        elif prodotto.name == 'Tansta-Shirt':
            validate = URLValidator()
            try:
                validate('http://www.instagram.com/' + data)
                SocialCodice.objects.create(user=request.user,social_slug=data,date_creation=date_creation)
                codice = SocialCodice.objects.get(user=request.user,social_slug=data, date_creation=date_creation)
                qr = pyqrcode.create(codice.get_view())
                qr.svg(f'media-serve/qr_{codice.uuid}.svg',scale=10)
                codice.image_qr = f'qr_{codice.uuid}.svg'
                codice.save()
                return redirect('payment_page',pk=prodotto.pk,uuid=codice.uuid) #to change
            except ValidationError:
                messages.error(request,"Questo profilo non è esistente. Inseriscine uno nuovo")
                return redirect('prodottoview',pk=prodotto.pk)
        else:
            pass
    else:
        context = {'prodotto':prodotto}
        return render(request,'prodottoview.html',context)

class TShirtView(ListView):
    model = Item
    context_object_name = 'lista_prodotti'
    template_name = 'tshirtlistview.html'

def charge(request):
    pass

#temporary
def payment_page(request,pk,uuid):
    if SocialCodice.objects.filter(uuid=uuid).exists():
        codice = SocialCodice.objects.get(uuid=uuid)
    elif Codice.objects.filter(uuid=uuid).exists():
        codice = Codice.objects.get(uuid=uuid)
    else:
        print("Il codice non esiste")
        return redirect('prodottoview',pk=prodotto.pk)

    prodotto = get_object_or_404(Item,pk=pk)
    context = {'prodotto':prodotto,'code':codice}
    return render(request,'payment_page.html',context)

def payment_redirect(request,pk,uuid):
    prodotto = get_object_or_404(Item,pk=pk)
    if SocialCodice.objects.filter(uuid=uuid).exists():
        codice = SocialCodice.objects.get(uuid=uuid)
    elif Codice.objects.filter(uuid=uuid).exists():
        codice = Codice.objects.get(uuid=uuid)
    else:
        print("Il codice non esiste")
        return redirect('prodottoview',pk=prodotto.pk)

    context = {'prodotto':prodotto, 'code':codice}
    return render(request,'payment_redirect.html',context)

def create_order(request,pk):
    if request.method == "POST":
        prodotto = get_object_or_404(Item,pk=pk)

        #COLLECTING DATA FROM POST FORM
        name = request.POST.get('name') + ", " + request.POST.get('color')
        address = request.POST.get('address')
        postal_code = request.POST.get('postal_code')
        house_number = request.POST.get('house_number')
        city = request.POST.get('city')
        country = request.POST.get('country')
        telephone = request.POST.get('telephone')
        email = request.POST.get('email')
        order_number = request.POST.get('uuid')

        #API COMMUNICATION PARAMETERS
        SC_PUBLIC_KEY = "db4d7ba1ed80480b83c8f1e759ad2c9e"
        SC_SECRET_KEY = "386677d4d07b401d8c0d244af9c92769"

        headers = {}
        headers['Content-Type'] = 'application/json'

        #NEW ORDER DICT
        new_order = {
            "parcel": {
                "name": name,
                "company_name": prodotto.name,
                "address": address,
                "postal_code": postal_code,
                "house_number": house_number,
                "city": city,
                "country": country,
                "telephone": telephone,
                "email": email,
                "order_number": order_number,
            }
        }

        #SUBMITTING NEW ORDER
        response = requests.post(
            headers=headers,
            url="https://panel.sendcloud.sc/api/v2/parcels",
            data=json.dumps(new_order),
            auth=(SC_PUBLIC_KEY,SC_SECRET_KEY)
        )

        if response.status_code != 200:
            response.raise_for_status()
            return HttpResponse(status=400)

        else:
            order_number = json.loads(response.text)['parcel']['order_number']
            print("\nL'ordine è stato inserito nell'api con successo")

            #CREATING AN ORDER INSTANCE IN DATABASE
            Orders.objects.create(
                item=prodotto,
                name=name,
                address=address,
                postal_code=postal_code,
                house_number=house_number,
                city=city,
                country=country,
                telephone=telephone,
                email=email,
                id=order_number
            )

            print("\nL'ordine è stato inserito nel database con successo")
            return redirect("payment_redirect",pk=prodotto.pk,uuid=order_number)


def thanks(request,pk):
    prodotto = get_object_or_404(Item,pk=pk)

    if prodotto.name == 'Tas-Shirt':
        queryset = Codice.objects.filter(user=request.user).order_by('-date_creation')
        print(queryset)
        last_code = queryset[0]
        last_code.bought = True
        print(last_code.bought)
        last_code.save()
    #aggiungere eventuali elif in presenza di nuovi items
    else:
        queryset = SocialCodice.objects.filter(user=request.user).order_by('-date_creation')
        print(queryset)
        last_code = queryset[0]
        last_code.bought = True
        print(last_code.bought)
        last_code.save()

    context = {'prodotto':prodotto}
    return render(request,'thanks.html',context)

@csrf_exempt
def checkout(request,pk,uuid):
    prodotto = get_object_or_404(Item,pk=pk)

    if SocialCodice.objects.filter(uuid=uuid).exists():
        codice = SocialCodice.objects.get(uuid=uuid)
    elif Codice.objects.filter(uuid=uuid).exists():
        codice = Codice.objects.get(uuid=uuid)
    else:
        print("Il codice non esiste")
        return redirect('prodottoview',pk=prodotto.pk)

    session = stripe.checkout.Session.create(
      payment_method_types=['card'],
      line_items=[{
        'price': prodotto.stripe_payment_id,
        'quantity': 1,
      }],
      mode='payment',
      success_url=request.build_absolute_uri(reverse('thanks',kwargs={'pk':prodotto.pk})) + '?session_id={CHECKOUT_SESSION_ID}',
      cancel_url=request.build_absolute_uri(reverse('payment_page',kwargs={'pk':prodotto.pk,'uuid':codice.uuid})),
    )

    return JsonResponse({
    'session_id':session.id,
    'stripe_public_key':settings.STRIPE_PUBLIC_KEY,
    })

@csrf_exempt
def stripe_webhook(request):
    # Set your secret key. Remember to switch to your live secret key in production!
    # See your keys here: https://dashboard.stripe.com/account/apikeys
    # If you are testing your webhook locally with the Stripe CLI you
    # can find the endpoint's secret by running `stripe listen`
    # Otherwise, find your endpoint's secret in your webhook settings in the Developer Dashboard
    endpoint_secret = 'whsec_QPWnA7eeLI3so0iL8smKkfGnvqceGqXd'

    # Using Django

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
          payload, sig_header, endpoint_secret
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        print('PaymentIntent was successful!')
    elif event.type == 'payment_method.attached':
        payment_method = event.data.object # contains a stripe.PaymentMethod
        print('PaymentMethod was attached to a Customer!')
    # ... handle other event types
    else:
    # Unexpected event type
        return HttpResponse(status=400)

    return HttpResponse(status=200)
