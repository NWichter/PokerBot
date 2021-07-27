import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

def create_graphs():
    player = ["p1: MCCFRBot1", "p2: MCCFRBot2",
            "p3: MonteCarloBot", "p4: HonestBot", "p5: Callbot"]

    files = ["results/evaluation_100_p1.pkl", "results/evaluation_100_p2.pkl",
            "results/evaluation_100_p3.pkl", "results/evaluation_100_p4.pkl", "results/evaluation_100_p5.pkl"]
    # Auswertung aller Datenpunkte (Durchschnitt)

    all_avgstack = []

    for file in files:

        result = pd.read_pickle(file)
        # print(result)
        avgstack = []
        for c in range(1, len(result)+1):
            avgstack.append(int(np.mean(result[0:c])))
        all_avgstack.append(avgstack)

    for avgstack in all_avgstack:
        # print(avgstack)
        plt.plot(range(1, len(avgstack)+1), avgstack)

    plt.title(f"Ergebnisse")
    plt.xlabel('Iterationen')
    plt.ylabel('Durchschnittliche Stacksgröße')


    plt.axhline(y=100, color="black", label="Anfangsstack")
    plt.legend(player, loc='best')

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    fig.savefig('./results/average_stacks', dpi=100)
    plt.close()

    # Auswertung der letzten 20 Datenpunkte (Durchschnitt)

    all_avgstack20 = []
    for file in files:

        result = pd.read_pickle(file)
        # print(result)
        avgstack = []
        for c in range(21, len(result)+1):
            avgstack.append(int(np.mean(result[c-21:c])))
        all_avgstack20.append(avgstack)

    for avgstack in all_avgstack20:
        # print(avgstack)
        plt.plot(range(1, len(avgstack)+1), avgstack)

    plt.title(f"Ergebnisse")
    plt.xlabel('Iterationen')
    plt.ylabel('Durchschnittliche Stackgröße')


    plt.axhline(y=100, color="black", label="Anfangsstack")
    plt.legend(player, loc='best')

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)

    fig.savefig('./results/average20_stacks', dpi=100)
    plt.close()

if __name__ == '__main__':
    create_graphs()