import pyqrcode
from core.models import SocialCodice, Codice
from django.utils import timezone
from shutil import copyfile
import os

with_dirs = bool(input("With dirs? (True/False)"))

if not os.path.isdir("red"):
    os.mkdir("red")
    os.mkdir("blue")

data = "https://127.0.0.1:8000/" #to change in production

for i in range(24):
    codice = Codice.objects.create(social_slug="tasqr_moda",date_creation=timezone.now(),bought=False)
    qr = pyqrcode.create(codice.get_view())
    qr.svg(f'media-serve/qr_{codice.uuid}.svg', scale=10)
    codice.image_qr = f'qr_{codice.uuid}.svg'
    if with_dirs:
        if i < 12:
            copyfile(f'media-serve/qr_{codice.uuid}.svg',f'red/qr_{codice.uuid}.svg')
        else:
            copyfile(f'media-serve/qr_{codice.uuid}.svg',f'blue/qr_{codice.uuid}.svg')
    codice.save()


print("Everything was done successfully!")
