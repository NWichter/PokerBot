import pickle
from pypokerengine.api.game import start_poker, setup_config

from player.call_player import CallBot
from player.honest_player import HonestBot
from player.monte_carlo_player import MonteCarloBot

from mccfr import MCCFRBot
from evaluation import create_graphs

# Grundeinstellungen
settings = {"iterations": 5000,     # Anzahl an Trainingspielen
            "max_round": 10,           # Anzahl der maximalen Runden pro Spiel
            "initial_stack": 100,      # Anfangsbestand an Spielgeld
            "small_blind_amount": 5,   # Wert des Small Blind
            "evaluation": False,       # Aktivieren für die Auswertung
            "showDetails": False}       # Anzeigen von Details während des Lernens

stackp1_log, stackp2_log, stackp3_log, stackp4_log, stackp5_log = [], [], [], [], []


def main():

    p1, p2, p3, p4, p5 = MCCFRBot(), MCCFRBot(), MonteCarloBot(), HonestBot(), CallBot()
    p1.init_bot(True, settings["showDetails"])
    p2.init_bot(False)

    for round in range(1, settings["iterations"]+1):

        # Grundeinstellungen eines Pokerspiels
        config = setup_config(
            max_round=settings["max_round"],
            initial_stack=settings["initial_stack"],
            small_blind_amount=settings["small_blind_amount"])

        # Hinzufügen der verschieden Spieler mit ihrem jeweiligen Algorithmus
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        config.register_player(name="p3", algorithm=p3)
        config.register_player(name="p4", algorithm=p4)
        config.register_player(name="p5", algorithm=p5)

        # Starten des Spielablaufs
        # verbose=0 => keine Spieldetails werden angezeigt
        # verbose=1 => Spieldetails werden angezeigt (nur sinnvoll bei einer geringen Anzahl an Iterationen)
        game_result = start_poker(config, verbose=0)

        # Alle 100 Spiele wird der aktuelle Lernstand gespeichert
        if round % 20 == 0 and round != 0:
            print("Runde:", round, "Lernstand aktualisiert")
            p1.save_data()
            p2.load_data()
        else:
            print("Runde:", round)

        # nur wenn die Einstellung evaluation == True und unter 500 Iterationen
        if settings["evaluation"] and settings["iterations"] < 501:
            # Auswertung eines Spiels

            stackp1_log.append(
                [player['stack'] for player in game_result['players'] if player['uuid'] == p1.uuid])
            stackp2_log.append(
                [player['stack'] for player in game_result['players'] if player['uuid'] == p2.uuid])
            stackp3_log.append(
                [player['stack'] for player in game_result['players'] if player['uuid'] == p3.uuid])
            stackp4_log.append(
                [player['stack'] for player in game_result['players'] if player['uuid'] == p4.uuid])
            stackp5_log.append(
                [player['stack'] for player in game_result['players'] if player['uuid'] == p5.uuid])

            # Ausgabe des durchschnittlichen Pots des ersten Spieler (Algorithmus)
            #print('Avg. stack:', '%d' % (int(np.mean(stackp1_log))))

    if settings["evaluation"] and settings["iterations"] < 501:
        # Speichern einer Spieleauswertung
        file_name = f"results/evaluation_100_p1.pkl"
        with open(file_name, "wb") as f:
            pickle.dump(stackp1_log, f)

        file_name = f"results/evaluation_100_p2.pkl"
        with open(file_name, "wb") as f:
            pickle.dump(stackp2_log, f)

        file_name = f"results/evaluation_100_p3.pkl"
        with open(file_name, "wb") as f:
            pickle.dump(stackp3_log, f)

        file_name = f"results/evaluation_100_p4.pkl"
        with open(file_name, "wb") as f:
            pickle.dump(stackp4_log, f)

        file_name = f"results/evaluation_100_p5.pkl"
        with open(file_name, "wb") as f:
            pickle.dump(stackp5_log, f)

        create_graphs()


if __name__ == '__main__':
    main()
