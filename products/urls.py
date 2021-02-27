from django.urls import path
from .views import viewProdotto,TShirtView,payment_page,payment_redirect,thanks,checkout,stripe_webhook,create_order


urlpatterns = [
    path('<int:pk>/',viewProdotto,name='prodottoview'),
    path('t-shirts/',TShirtView.as_view(),name='tshirtlist'),
    path('payment-page/<int:pk>/<uuid:uuid>',payment_page,name='payment_page'),
    path('payment-redirect/<int:pk>/<uuid:uuid>',payment_redirect,name='payment_redirect'),
    path('thanks/<int:pk>',thanks,name='thanks'),
    path('checkout/<int:pk>/<uuid:uuid>',checkout,name='checkout'),
    path('webhook/',stripe_webhook,name='webhook'),
    path('create_order/<int:pk>',create_order,name='create_order')
]
