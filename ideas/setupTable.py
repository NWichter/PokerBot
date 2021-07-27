from player.call_player import CallBot
from player.honest_player import HonestBot
from player.monte_carlo_player import MonteCarloBot

#Erweiterungsmöglichkeit für beliebige Spieler an einem Tisch (Der Hauptalgorithmus ist immer am Tisch)
#Einstellungen für verschiedene Spieler an einem Tisch
#C = Callbot
#M = MonteCarloBot
#H = HonestBot


def setupTable(player="CM"):

    table = []
    playercount = len(player)+1

    if playercount > 8:
        raise ValueError("Zu viele Spieler max. 8 Spieler möglich")
    if playercount < 2:
        raise ValueError("Zu wenige Spieler min. 2 Spieler notwendig")

    # Umwandlung des Strings in eine Liste mit den verknüpften Algorithmen
    for c in player:
        if c == "C":
            table.append(CallBot())

        elif c == "H":
            table.append(HonestBot())

        elif c == "M":
            table.append(MonteCarloBot())

        else:
            raise ValueError(
                c, "Fehlerhafter Wert bei 'player' erlaubte Werte: 'C','M'")

    return table, player