#! /usr/bin/python3
# -*- coding: utf-8 -*-
import cgitb; cgitb.enable()
import os
from xmlrpc import client
from datetime import datetime
import time
from urllib.parse import parse_qs
from html import escape

actions = ("doorup", "doordown", "innerlighton", "innerlightoff", "outerlighton", "outerlightoff")

def main():
    query_string = os.environ.get("QUERY_STRING", "")
    fields = parse_qs(query_string)
    action = fields.get("action", ["",])[0].lower()

    if not action in actions:
        print('<div class="error">Ungültige Aktion &quot;%s&quot;</div>' % (escape(action),))
        return

    proxy = client.ServerProxy('http://localhost:8010')

    if action in ("doorup", "doordown"):
        meth = proxy.OpenDoor if action == "doorup" else proxy.CloseDoor
        try:
            result = meth()
        except Exception:
            print('<div class="error">Kontrollserver nicht erreichbar!</div>')
        else:
            is_open = proxy.IsDoorOpen()
            print(
                "<span>Kommando %s, T&uuml;r ist %s.</span>" % (
                    "erfolgreich" if result else "fehlgeschlagen",
                    "offen" if is_open else "geschlossen"
                )
            )
    else:
        is_inner = action.startswith("inner")
        meth = proxy.SwitchIndoorLight if is_inner else proxy.SwitchOutdoorLight
        what = action.endswith("on")
        try:
            result = meth(what)
        except Exception:
            print('<div class="error">Kontrollserver nicht erreichbar!</div>')
        else:
            meth = proxy.IsIndoorLightOn if is_inner else proxy.IsOutdoorLightOn
            is_on = meth()
            print(
                "<span>Kommando erfolgreich, %slicht ist %s.</span>" % (
                    "Innen" if is_inner else "Au&szlig;en",
                    "an" if is_on else "aus"
                )
            )


if __name__ == '__main__':
    main()