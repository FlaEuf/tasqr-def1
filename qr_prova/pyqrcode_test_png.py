import pyqrcode

qr = pyqrcode.create("https://tas-qr.com")
qr.png("2tasqrcode_test.png", scale=5, module_color=(255,255,255,255), background=(0,0,0,255))
