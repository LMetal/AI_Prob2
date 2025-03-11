import pysmile
import pysmile_license

TIME_STEPS = 5


def init_net():
    net.read_file("Problema2_unrolled.xdsl")
    net.clear_all_evidence()
    net.update_beliefs()


def check_right_timesteps():
    try:
        net.get_node_value(f"Sensore_Posizione_{TIME_STEPS-1}")
    except:
        print("TIME STEP ERRATO : troppo grande")
        return False

    try:
        net.get_node_value(f"Sensore_Posizione_{TIME_STEPS}")
    except:
        return True

    print("TIME STEP ERRATO : troppo piccolo")
    return False


def sensor_read(i):
    if i == 0:
        sensor_name = "Sensore_Posizione"
    else:
        sensor_name = f"Sensore_Posizione_{i}"

    print(sensor_name)

    values = list(range(len(net.get_node_value(sensor_name))))  # Lista degli indici
    probabilities = net.get_node_value(sensor_name)  # Probabilità associate
    state_names = net.get_outcome_ids(sensor_name)

    if probabilities.count(1) == 1:  # se c'è solo una possibilità
        net.set_evidence(sensor_name, probabilities.index(1))
    else:
        print("\n\nImpostare risultato nodo " + sensor_name)
        print("N\tState")
        print("--------------------")
        for n, state, prob in zip(values, state_names, probabilities):
            if prob == 0:
                continue
            print(f"{n}\t{state}")  # print(f"{n}\t{state}\t\t{prob:.2f}")
        n = int(input("Quale N? : "))
        net.set_evidence(sensor_name, n)

    print(sensor_name, " settato a  ", net.get_evidence_id(sensor_name))
    net.update_beliefs()


def action(i):
    if i == 0:
        action_name = "Azione"
    else:
        action_name = f"Azione_{i}"

    print("\n\nEffettuare ", action_name, "? [c, d, s]")

    value = net.get_node_value(action_name)
    print("Scelta\t\t\t:\tUtilità")
    print("---------------------------")
    print(f"n (nulla)\t\t:\t{value[0]:.2f}")
    print(f"d (destra)\t\t:\t{value[1]:.2f}")
    print(f"s (sinistra)\t:\t{value[2]:.2f}")

    azione = input("Scelta: ")
    if azione == "c":
        net.set_evidence(action_name, "Nulla")
    elif azione == "d":
        net.set_evidence(action_name, "Destra")
    elif azione == "s":
        net.set_evidence(action_name, "Sinistra")
    else:
        print("ERRORE INSERIMENTO")

    net.update_beliefs()


def problema2():
    for i in range(TIME_STEPS):
        sensor_read(i)
        action(i)


if __name__ == "__main__":
    net = pysmile.Network()
    init_net()

    if not check_right_timesteps():
        exit()

    problema2()
