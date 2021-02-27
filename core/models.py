from django.db import models
from django.conf import settings
import uuid
from django.core.validators import FileExtensionValidator
from django.shortcuts import reverse
from django.contrib.auth.models import User


class Codice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='qrs',blank=True,null=True)
    redirect = models.CharField(max_length=150)
    image_qr = models.FileField(upload_to='static/img',validators=[FileExtensionValidator(['svg'])])
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_creation = models.DateTimeField(blank=True,null=True)
    bought = models.BooleanField(blank=True,default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'codice'
        verbose_name_plural = 'codici'

    def __str__(self):
        try:
            return self.user.username + ', ' + self.redirect
        except:
            return "No user, " + self.redirect

    def get_view(self):
        return 'http://127.0.0.1:8000' + reverse('codeview',kwargs={'uuid':self.uuid})


class SocialCodice(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='social_qrs',blank=True,null=True)
    image_qr = models.FileField(upload_to='static/img',validators=[FileExtensionValidator(['svg'])])
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_slug = models.CharField(max_length=60)
    date_creation = models.DateTimeField(blank=True,null=True)
    bought = models.BooleanField(blank=True,default=False)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'SocialCodice'
        verbose_name_plural = 'SocialCodici'

    def __str__(self):
        try:
            return self.user.username + ', ' + self.social_slug
        except:
            return "No user, " + self.social_slug

    def get_view(self):
        return 'http://127.0.0.1:8000' + reverse('codeview',kwargs={'uuid':self.uuid})

class RichiestaAiuto(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='help_requests',default=None)
    message = models.TextField(max_length=700)
    solved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ', ' + self.message[:40] + '...'

    class Meta:
        verbose_name = 'RichiestaAiuto'
        verbose_name_plural = 'RichiesteAiuto'
