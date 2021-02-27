from django.urls import path
from .views import homepage,registrationView,view_code,ProfileView,add_help_request,RequestsView,save_requests,remove_request,\
new_code_by_passkey

urlpatterns = [
    path('',homepage,name='home'),
    path('accounts/registration/',registrationView,name='registration'),
    path('codes/<uuid:uuid>/',view_code,name='codeview'),
    path('accounts/profileview/<user>',ProfileView.as_view(),name='profileview'),
    path('help-request/',add_help_request,name='help_request'),
    path('requests/',RequestsView.as_view(),name='requests'),
    path('save-requests/',save_requests,name='save_requests'),
    path('remove-request/<int:pk>/',remove_request,name='remove_request'),
    path('new-code-by-passkey/',new_code_by_passkey,name="new_code_by_passkey"),
]
