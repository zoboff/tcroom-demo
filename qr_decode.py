from PIL import Image
from pyzbar.pyzbar import decode

data = decode(Image.open('qr2.png'))
print(data)
