from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import HttpResponse, HttpResponseRedirect
from products.models import Item
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm
from .models import Codice,SocialCodice,RichiestaAiuto
import os
import pyqrcode
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.core.validators import URLValidator
from django.http import HttpResponseForbidden

# Create your views here.

def helloworld(request):
    return HttpResponse('<h1>Hello World!</h1>')

def homepage(request):
    items = Item.objects.all()
    context = {'items':items}
    return render(request,'homepage.html',context)

def registrationView(request):
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return redirect('registration')

    else:
        form = RegistrationForm()
        context = {'form':form}
        return render(request,'registration/registration.html',context)

class ProfileView(ListView):
    context_object_name = 'name'
    template_name = 'registration/profile_view.html'
    queryset = Codice.objects.all()

    def get_context_data(self,*args,**kwargs):
        context = super(ProfileView,self).get_context_data()
        context['codici'] = Codice.objects.filter(user__username=self.kwargs['user'],bought=True)
        context['socialcodici'] = SocialCodice.objects.filter(user__username=self.kwargs['user'],bought=True)
        context['user'] = self.kwargs['user']
        return context

    def get(self,request,*args,**kwargs):
        if str(request.user) != self.kwargs['user']:
            return HttpResponseForbidden('<h1 align=\'center\'>You are not authenticated as \'%s\'<h1>' %self.kwargs['user'])

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self,request,*args,**kwargs):
        for k,i in request.POST.items():
            print('Chiave: ' + k)
            print('\n')
            print('Item: ' + i)
            if '-' in k:
                codice = Codice.objects.filter(uuid=k)
                if not codice.exists():
                    codice = SocialCodice.objects.filter(uuid=k)
                    print('Sembra andare tutto bene, codice social rilevato')
                    codice = codice[0]
                    codice.social_slug = i
                    codice.save()
                    messages.success(request,'Hai modificato il tuo Instagram Username con successo!')
                else:
                    validate = URLValidator()
                    try:
                        validate(i)
                        codice = codice[0]
                        if codice.redirect == i:
                            messages.warning(request,"Questo codice ha già un collegamento con l'URL digitato")
                            return redirect('profileview',self.kwargs['user'])

                        codice.redirect = i
                        codice.save()
                        messages.success(request,'Hai modificato il tuo URL di reindirizzamento con successo!')
                    except:
                        messages.error(request,"L'URL inserito non è valido...")
                        return redirect('profileview',self.kwargs['user'])

        return redirect('profileview',self.kwargs['user'])

def view_code(request,uuid):
    social_code = SocialCodice.objects.filter(uuid=uuid)
    if social_code.exists():
        social_code = SocialCodice.objects.get(uuid=uuid)
        social_code.views += 1
        social_code.save()
        return HttpResponseRedirect('https://www.instagram.com/' + social_code.social_slug)

    else:
        code = Codice.objects.get(uuid=uuid)
        code.views += 1
        code.save()
        return HttpResponseRedirect(code.redirect)

def add_help_request(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            message = request.POST.get('message')
            RichiestaAiuto.objects.create(user=user,message=message)
            messages.success(request,'Hai inviato con successo la tua segnalazione! Ti risponderemo al più presto.')
            return redirect('home')
        else:
            print("L'user non è autenticato")
            messages.error(request,'Devi autenticarti prima di inviare un messaggio privato. Clicca su Login in alto a destra o Registrati se ancora non hai un account...')
            return redirect('home')

class RequestsView(ListView):
    model = RichiestaAiuto
    template_name = 'requests_view.html'
    context_object_name = 'requests'

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseForbidden('<h1 align=\'center\'>Non sei autorizzato ad accedere a questa pagina</h1>')

        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

def save_requests(request):
    if request.method == 'POST':
        print(request.POST)
        for richiesta in RichiestaAiuto.objects.all():

            if request.POST.get(str(richiesta.id)) == 'on':
                richiesta.solved = True
                richiesta.save()

            else:
                richiesta.solved = False
                richiesta.save()
                continue

    return redirect('requests')

def remove_request(request,pk):
    richiesta = get_object_or_404(RichiestaAiuto,pk=pk)
    richiesta.delete()
    messages.success(request,'Richiesta Eliminata')
    return redirect('requests')

def new_code_by_passkey(request):
    if request.method == "POST":
        passkey = request.POST.get("passkey")
        print(passkey)
        try:
            QRcode = SocialCodice.objects.get(uuid=passkey)
            assert QRcode.user == None
            QRcode.user = request.user
            if (QRcode.bought == False):
                QRcode.bought = True
            QRcode.save()
            messages.success(request,"Link al Nuovo Codice creato correttamente!")

        except:
            try:
                QRcode = Codice.objects.get(uuid=passkey)
                assert QRcode.user == None
                QRcode.user = request.user
                if (QRcode.bought == False):
                    QRcode.bought = True
                QRcode.save()
                messages.success(request,"Link al Nuovo Codice creato correttamente!")

            except:
                messages.error(request,"La PassKey inserita non è valida!")

        return redirect("profileview",request.user)
