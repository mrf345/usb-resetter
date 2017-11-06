# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
import usb.core
from os import path
import sys


class find_class(object):
    def __init__(self, class_):
        self._class = class_

    def __call__(self, device):
        # first, let's check the device
        if device.bDeviceClass == self._class:
            return True
        # ok, transverse all devices to find an
        # interface that matches our class
        for cfg in device:
            # find_descriptor: what's it?
            intf = usb.util.find_descriptor(cfg, bInterfaceClass=self._class)
            if intf is not None:
                return True

        return False


def listd(tp=None, gui=None):
    vl = []
    ftp = []
    if tp is not None:
        for ttp in tp:
            ftp.append(usb.core.find(find_all=True,
                                     custom_match=find_class(ttp)))
    else:
        ftp = [usb.core.find(find_all=True)]
    for f in ftp:
        for ll in f:
            if gui:
                d = None
                try:
                    d = usb.util.get_string(ll, ll.iProduct)
                except:
                    pass
                if d is None:
                    dl = [0, 1, 2, 3, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19]
                    dld = ["Unspecified", "Audio", "Network card",
                           "Human interface", "Printer", "Mass storage",
                           "Hub", "Network", "Smart card", "Content security",
                           "Video device", "Audio or Video", "Billboard",
                           "USB Type-C", "Wireless"]
                    d = "Unknown"
                    for desc in ll:
                        for dd in dl:
                            if usb.util.find_descriptor(desc,
                                                        bInterfaceClass=dd
                                                        ):
                                d = dld[dl.index(dd)]
                                break
                vl.append(
                    str(d) + "," + str(
                        hex(ll.idVendor)) + "," + str(
                            hex(ll.idProduct)))
            else:
                vl.append([hex(ll.idVendor), hex(ll.idProduct)])
    return vl


def resetit(dstr):
    s = dstr.split(',')
    try:
        ud = usb.core.find(idVendor=int(s[1], 16), idProduct=int(s[2], 16))
        if ud is not None:
            ud.reset()
            return True
        else:
            return False
    except:
        return False


def r_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")

    return path.join(base_path, relative_path)
