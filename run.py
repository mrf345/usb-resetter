from app import gui
from sys import exit, exc_info

try:
    gui()
except Exception:
    print(exc_info()[1])
    print('Error runtime: please, help us improve by reporting to us on :')
    print("\n\thttps://usb-resetter.github.io/")
    exit(0)
