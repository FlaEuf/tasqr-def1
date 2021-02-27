from django.contrib import admin
from .models import Codice, SocialCodice, RichiestaAiuto
import os
from django.conf import settings

# Register your models here.

class SocialCodiceAdmin(admin.ModelAdmin):
    fields = ()
    actions = ["delete_model"]

    def delete_model(self, request, obj):
        filename = f"qr_{obj.uuid}.svg"
        os.remove(os.path.join(settings.BASE_DIR, f"media-serve/{filename}"))
        print("Qr deleted correctly!")
        obj.delete()
        print("Object deleted correctly!")

class CodiceAdmin(admin.ModelAdmin):
    fields = ()
    actions = ["delete_model"]

    def delete_model(self, request, obj):
        filename = f"qr_{obj.uuid}.svg"
        os.remove(os.path.join(settings.BASE_DIR, f"media-serve/{filename}"))
        print("Qr deleted correctly!")
        obj.delete()
        print("Object deleted correctly!")




admin.site.register(Codice, CodiceAdmin)
admin.site.register(SocialCodice, SocialCodiceAdmin)
admin.site.register(RichiestaAiuto)
