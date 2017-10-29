# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from app import gui
from sys import exit, exc_info

try:
    gui()
except Exception:
    print(exc_info()[1])
    print('Error runtime: please, help us improve by reporting to us on :')
    print("\n\thttps://usb-resetter.github.io/")
    exit(0)
