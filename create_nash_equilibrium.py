import pandas as pd
from pypokerengine.utils.card_utils import gen_deck

deck = []
full_deck = gen_deck()
for x in range(52):
    deck.append(str(full_deck.draw_card()))

print(deck)  # Alle Karten
print(len(deck))  # Anzahl aller Karten


hole_cards = []  # Liste für alle Kartenkombinationen (2 Handkarten)
hole_cards_c3 = []
hole_cards_c4 = []
hole_cards_c5 = []

second_deck = deck[:]
third_deck = deck[:]
fourth_deck = deck[:]
fifth_deck = deck[:]
sixth_deck = deck[:]
seventh_deck = deck[:]

for first_card in deck:
    second_deck.remove(first_card)

    for second_card in second_deck:

        hole_cards.append(str([first_card, second_card]))
        # Ausblenden nicht benötigter Komponenten (Zu hohe Rechenanforderungen)
        continue
        third_deck = second_deck[:]
        third_deck.remove(second_card)

        for third_card in third_deck:

            fourth_deck = third_deck[:]
            fourth_deck.remove(third_card)

            for fourth_card in fourth_deck:

                fifth_deck = fourth_deck[:]
                fifth_deck.remove(fourth_card)

                for fifth_card in fifth_deck:

                    hole_cards_c3.append(
                        str([[first_card, second_card], [third_card, fourth_card, fifth_card]]))
                    continue
                    sixth_deck = fifth_deck[:]
                    sixth_deck.remove(fifth_card)

                    for sixth_card in sixth_deck:

                        hole_cards_c4.append(str([[first_card, second_card], [
                                             third_card, fourth_card, fifth_card, sixth_card]]))

                        seventh_deck = sixth_deck[:]
                        seventh_deck.remove(sixth_card)

                        for seventh_card in seventh_deck:

                            hole_cards_c5.append(str([[first_card, second_card], [
                                                 third_card, fourth_card, fifth_card, sixth_card, seventh_card]]))

hole_cards_len = len(hole_cards)
hole_cards_c3_len = len(hole_cards_c3)
hole_cards_c4_len = len(hole_cards_c4)
hole_cards_c5_len = len(hole_cards_c5)

# 2 Handkarten
print("Länge hole_cards:", hole_cards_len)
# 2 Handkarten + 3 Gemeinschaftskarten
print("Länge hole_cards_c3", hole_cards_c3_len)
# 2 Handkarten + 4 Gemeinschaftskarten
print("Länge hole_cards_c4", hole_cards_c4_len)
# 2 Handkarten + 5 Gemeinschaftskarten
print("Länge hole_cards_c5", hole_cards_c5_len)

columns = ["call", "fold", "raise", "counter"]

# Erstellen und Speichern der Datei für das Nash Equilibrium (2 Handkarten)
df = pd.DataFrame(index=hole_cards, columns=columns)

df["call"] = [1 for x in range(hole_cards_len)]
df["fold"] = [0 for x in range(hole_cards_len)]
df["raise"] = [0 for x in range(hole_cards_len)]
df["counter"] = [0 for x in range(hole_cards_len)]

df[['call', 'fold', 'raise']] = df[['call', 'fold', 'raise']].astype(float)
# Ausblenden um Datei nicht auf Werkeinstellungen zurück zu setzen
# df.to_pickle("nash_equilibrium/nash2cards.pkl")

if hole_cards_c3_len:  # Aus Speichergründen nicht möglich
    # Erstellen und Speichern der Datei für Nash Equilibrium (2 Handkarten + 3 Gemeinschaftskarten)
    df = pd.DataFrame(index=hole_cards_c3, columns=columns)

    df["call"] = [1 for x in range(hole_cards_c3_len)]
    df["fold"] = [0 for x in range(hole_cards_c3_len)]
    df["raise"] = [0 for x in range(hole_cards_c3_len)]
    df["counter"] = [0 for x in range(hole_cards_c3_len)]

    df[['call', 'fold', 'raise']] = df[['call', 'fold', 'raise']].astype(float)
    df.to_pickle("nash_equilibrium/nash5cards.pkl")

    exit()
    # Erstellen und Speichern der Datei für Nash Equilibrium (2 Handkarten + 4 Gemeinschaftskarten)
    df = pd.DataFrame(index=hole_cards_c4, columns=columns)

    df["call"] = [1 for x in range(hole_cards_c4_len)]
    df["fold"] = [0 for x in range(hole_cards_c4_len)]
    df["raise"] = [0 for x in range(hole_cards_c4_len)]
    df["counter"] = [0 for x in range(hole_cards_c4_len)]

    df[['call', 'fold', 'raise']] = df[['call', 'fold', 'raise']].astype(float)
    df.to_pickle("nash_equilibrium/nash6cards.pkl")

    # Erstellen und Speichern der Datei für Nash Equilibrium (2 Handkarten + 5 Gemeinschaftskarten)
    df = pd.DataFrame(index=hole_cards_c5, columns=columns)

    df["call"] = [1 for x in range(hole_cards_c5_len)]
    df["fold"] = [0 for x in range(hole_cards_c5_len)]
    df["raise"] = [0 for x in range(hole_cards_c5_len)]
    df["counter"] = [0 for x in range(hole_cards_c5_len)]

    df[['call', 'fold', 'raise']] = df[['call', 'fold', 'raise']].astype(float)
    df.to_pickle("nash_equilibrium/nash7cards.pkl")
