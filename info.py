#! /usr/bin/python3
# -*- coding: utf-8 -*-

from xmlrpc import client
from datetime import datetime
import time

DOOR_OPEN = 4

light_text = [
    (200, "Dunkel"),
    (150, "D&auml;mmerung"),
    (100, "Bew&ouml;lkt"),
    (0, "Sonnig"),
]


def GetNextActionText(state):
    now = datetime.now()
    for dt, action in state.get("next_actions", []):
        if now < dt:
            dt = datetime.fromtimestamp(time.mktime(dt.timetuple())).strftime('%H:%M')
            return "{0} um {1} Uhr".format(
                "&Ouml;ffnen" if action == DOOR_OPEN else "Schlie&szlig;en",
                dt
            )
    return "FEHLER"

def page():
    proxy = client.ServerProxy('http://localhost:8010')

    try:
        state = proxy.GetBoardState()
    except Exception:
        print ('<div class="error">Failed to get board info, control server not available.</div>')
    else:
        door_states = {
            0: "FEHLER",
            1: "&Ouml;ffnet gerade",
            2: "Schlie&szlig;t gerade",
            4: "Offen",
            8: "Geschlossen"
        }

        light_states = {
            True: "An",
            False: "Aus",
        }
        
        print("<table>")

        print("  <tr>")
        print("    <td>Zeit</td>")
        print("    <td>%s</td>" % (datetime.now().strftime('%d.%m.%Y %H:%M:%S'),))
        print("  <tr>")

        print("  </tr>")
        print("    <td>N&auml;chste Aktion</td>")
        print("    <td>%s</td>" % (GetNextActionText(state),))
        print("  </tr>")

        autostate = state['automatic']
        if autostate == 1:
            autotext = "An"
        elif autostate == -1:
            autotext = "Dauerhaft deaktiviert"
        else:
            enable_time = state["automatic_enable_time"]
            autotext = "Deaktiviert bis %s" % (datetime.fromtimestamp(enable_time).strftime("%H:%M"),)

        print("  </tr>")
        print("    <td>Automatik</td>")
        print("    <td>%s</td>" % (autotext,))
        print("  </tr>")

        print("  </tr>")
        print("    <td>T&uuml;r</td>")
        print("    <td>%s</td>" % (door_states.get(state["door"], 0)))
        print("  </tr>")

        print("  </tr>")
        print("    <td>Licht innen</td>")
        print("    <td>%s</td>" % (light_states[state["indoor_light"]],))
        print("  </tr>")

        print("  </tr>")
        print("    <td>Licht au&szlig;en</td>")
        print("    <td>%s</td>" % (light_states[state["outdoor_light"]],))
        print("  </tr>")

        light_sensor_text = "Ung&uuml;ltig"
        light_sensor = state["light_sensor"]
        for boundary, text in light_text:
            if light_sensor > boundary:
                light_sensor_text = text
                break

        print("  </tr>")
        print("    <td>Helligkeitssensor</td>")
        print("    <td>%s</td>" % (light_sensor_text,))
        print("  </tr>")

        # print("  </tr>")
        # print("    <td>Temperatursensor</td>")
        # print("    <td>%.2f</td>" % (state["temperature"],))
        # print("  </tr>")

        print("</table>")

if __name__ == '__main__':
    page()