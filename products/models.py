from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.contrib.auth.models import User
from core.models import SocialCodice, Codice

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField()
    stripe_payment_id = models.CharField(max_length=50,blank=True)

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        return self.name


class Orders(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE,related_name='ordered_by')
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=10)
    house_number = models.CharField(max_length=20)
    city = models.CharField(max_length=45)
    country = models.CharField(max_length=50)
    telephone = models.CharField(max_length=15)
    email = models.EmailField()
    id = models.CharField(primary_key=True,max_length=70)

    def __str__(self):
        return self.email + "; " + self.address + "," + self.house_number + " (" + self.item.name + ")"


    class Meta:
        verbose_name = "ordine"
        verbose_name_plural = "ordini"
