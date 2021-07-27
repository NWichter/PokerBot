
import pandas as pd
import random

from pypokerengine.players import BasePokerPlayer
from player.monte_carlo_player import estimate_win_rate, montecarlo_simulation


class MCCFRBot(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):

        community_cards = round_state["community_card"]
        #print("c", community_cards)

        if len(community_cards) < 3:
            # print(hole_card)

            try:
                self.hole_cards_str = str([str(x) for x in hole_card])
                # print("hole_cards",self.hole_cards_str)
                self.df.loc[self.hole_cards_str]
                # print(type(self.hole_cards_str))
            except:
                # Umdrehen der Handkarten, da nur eine Reihenfolge gespeichert wird
                hole_card[0], hole_card[1] = hole_card[1], hole_card[0]
                self.hole_cards_str = str([str(x) for x in hole_card])

            actions = {"fold": self.df.loc[self.hole_cards_str]["fold"],
                       "call": self.df.loc[self.hole_cards_str]["call"],
                       "raise": self.df.loc[self.hole_cards_str]["raise"]}

            # verschiedene Varianten zum Bestimmen der Aktion
            # 1. Möglichkeit immer die Aktion mit den meisten Prozenten wird ausgeführt
            """if actions["fold"] > actions["call"] and actions["fold"] > actions["raise"]:
                action = valid_actions[0]
            elif actions["call"] > actions["raise"]:
                action = valid_actions[1]
            else:
                action = valid_actions[2]
                # raise wird immer mit dem doppelten des Small Blind ausgeführt
                action["amount"] = self.small_blind_amount*2"""

            # 2. Möglichkeit Zufällige Auswahl der Aktion basiernd auf den Wahrscheinlichkeiten, welche durch die Werte der Aktionen in der Tabelle gegeben sind
            random_factor = random.random(
            )*(actions["fold"]+actions["call"] + actions["raise"])
            if random_factor < actions["fold"]:
                action = valid_actions[0]
            elif random_factor < actions["fold"] + actions["call"]:
                action = valid_actions[1]
            else:
                action = valid_actions[2]
                # raise wird immer mit dem durschnittlich möglichen Betrag durchgeführt
                raise_amount_options = [
                    item for item in valid_actions if item['action'] == 'raise'][0]['amount']

                action["amount"] = (
                    raise_amount_options['max'] + raise_amount_options['min'])/2

            self.action = action["action"]
            # Ausgabe der Aktion an die Simulation
            return action["action"], action['amount']

        # Wenn Gemeinschaftskarten ausgelegt worden sind basiert die Entscheidung des Algorithmus auf MC
        else:  # Alternative mit zusätzlichen Karten er callt bis zum Schluss oder verwendet MC

            # 1. Möglichkeit einfach bis zum Ende callen (siehe CallBot)
            """action = valid_actions[1]
            return action["action"], action['amount']"""

            # 2. Möglichkeit Verwendung von Monte Carlo (siehe MonteCarloBot)
            # Berechnung der Siegesrate
            win_rate = estimate_win_rate(
                100, self.num_players, hole_card, round_state['community_card'])

            # Überprüfung, ob Call möglich ist
            can_call = len(
                [item for item in valid_actions if item['action'] == 'call']) > 0
            if can_call:
                # Call Betrag bestimmen
                call_amount = [
                    item for item in valid_actions if item['action'] == 'call'][0]['amount']
            else:
                call_amount = 0

            amount = None

            # Wenn die Siegesrate groß genug ist -> raise
            if win_rate > 0.5:
                raise_amount_options = [
                    item for item in valid_actions if item['action'] == 'raise'][0]['amount']
                if win_rate > 0.85:
                    # Wenn die Siegesrate besonders groß -> max raise
                    action = 'raise'
                    amount = raise_amount_options['max']
                elif win_rate > 0.75:
                    # Wenn die Siegesrate groß -> min raise
                    action = 'raise'
                    amount = raise_amount_options['min']
                else:
                    # Wenn überhaupt eine Möglichkeit zum Gewinnen besteht -> call
                    action = 'call'
            else:   # Call falls nichts gesetzt wurde ansonsten -> fold
                action = 'call' if can_call and call_amount == 0 else 'fold'

            # Setzen des Betrags
            if amount is None:
                items = [
                    item for item in valid_actions if item['action'] == action]
                amount = items[0]['amount']

            return action, amount

    # Status zu Beginn des Spiels
    # Enthält alle Einstellungen für den Ablauf eines Spiels

    def receive_game_start_message(self, game_info):

        self.num_players = game_info["player_num"]
        self.max_round = game_info["rule"]["max_round"]
        self.small_blind_amount = game_info["rule"]["small_blind_amount"]
        self.ante_amount = game_info["rule"]["ante"]
        self.blind_structure = game_info["rule"]["blind_structure"]

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    # Nach Beendigung eines Spiels werden die Entscheidungen des Algorithmus bewertet und für die nächsten Spiele gespeichert
    def receive_round_result_message(self, winners, hand_info, round_state):

        #print("winners", winners)
        #print("hand_info", hand_info)
        # print("round_state",round_state)
        # print("uuid",self.uuid)
        # print(winners[0]["uuid"],self.uuid)

        if self.main == True:  # nur der Hauptalgorithmus verändert die erlernten Werte
            # Überprüfung, ob der Algorithmus das aktuelle Spiel gewonnen hat
            if winners[0]["uuid"] != self.uuid:
                fold_action = 0.7
                call_action = 0.3
                raise_action = 0
                # print("ungleich")

            # verstärkt Verhalten bei welchem bereits erhöht wurde
            elif winners[0]["uuid"] == self.uuid and self.action == "raise":
                fold_action = 0
                call_action = 0.2
                raise_action = 0.8
            elif winners[0]["uuid"] == self.uuid:
                # print("gleich")
                fold_action = 0
                call_action = 0.8
                raise_action = 0.2

            counter = self.df.loc[self.hole_cards_str]["counter"]

            fold = self.df.loc[self.hole_cards_str]["fold"]
            call = self.df.loc[self.hole_cards_str]["call"]
            raise_ = self.df.loc[self.hole_cards_str]["raise"]

            if counter > 25:  # Ab dem 25. Spiel bleibt der Anteil der neusten Veränderung konstant bei 5%
                new_fold = fold * 0.96 + 0.04 * fold_action
                new_call = call * 0.96 + 0.04 * call_action
                new_raise = raise_ * 0.96 + 0.04 * raise_action

            elif counter > 3:  # Solange noch keine 20. Spiele erfolgt sind bei dieser Kartenkombination berechnet der Algorithmus einen Durchschnitt aller bisherigen Spiele
                new_fold = (fold * (counter-1) + fold_action)/counter
                new_call = (call * (counter-1) + call_action)/counter
                new_raise = (raise_ * (counter-1) + raise_action)/counter

            else:  # Das ersten 3 Spiele machen 25% Anteil bei der Berechnung aus
                new_fold = fold * 75 + 0.25 * fold_action
                new_call = call * 0.75 + 0.25 * call_action
                new_raise = raise_ * 0.75 + 0.25 * raise_action

            self.df.loc[self.hole_cards_str, 'fold'] = new_fold

            self.df.loc[self.hole_cards_str, 'call'] = new_call

            self.df.loc[self.hole_cards_str, 'raise'] = new_raise

            self.df.loc[self.hole_cards_str, 'counter'] += 1

            if self.showDetails == True:
                print("Anzahl Spiele:", sum(
                    self.df["counter"]), "\tAktion:", self.action, "\tHandkarten:", self.hole_cards_str)

    def init_bot(self, main, showDetails=False):
        self.df = pd.read_pickle("nash_equilibrium/nash2cards.pkl")
        self.showDetails = showDetails
        if main == True:
            self.main = True
        else:
            self.main = False

    def save_data(self):  # Der Hauptalgorithmus speichert alle 20 Spieldurchläufe (200 Spiele) seinen Wissenstand
        if self.main == True:
            self.df.to_pickle("nash_equilibrium/nash2cards.pkl")

    def load_data(self):
        if self.main == False:
            self.df = pd.read_pickle("nash_equilibrium/nash2cards.pkl")


def setup_ai():
    return MCCFRBot()
