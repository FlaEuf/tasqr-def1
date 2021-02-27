from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = User
        fields = ['username','email','password1','password2']

    def save(self,commit=True):
        user = super(UserCreationForm,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    # def save(self,commit=True):
    #     email = self.cleaned_data['email']
    #     password = self.cleaned_data['password1']
    #     username = self.cleaned_data['username']
    #     user = CustomUser.objects.create(email=email,username=username,password=password)
