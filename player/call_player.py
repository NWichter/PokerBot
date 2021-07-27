import numpy as np
from pypokerengine.players import BasePokerPlayer

# weitere Informationen siehe __init__.py
# dieser Algorithmus führt nur die Aktion call aus


class CallBot(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        actions = [item for item in valid_actions if item['action'] in ['call']]
        # print(valid_actions)
        return list(np.random.choice(actions).values())

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return CallBot()
