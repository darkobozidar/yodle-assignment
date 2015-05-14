from . import const
from .classes import Juggler, Circuit


def add_juggler_to_circuit(juggler, circuits):
    """
    Adds a juggler to the circuit. If the current circuit is full, pops last juggler of the team and
    recursively inserts him to another team according to his preferences.
    If all jugglers preferred circuits are taken, functions returns that juggler.
    """

    for circuit_name, rating in juggler.next_circuit_and_sim(circuits):
        circuit = circuits[circuit_name]

        if circuit.is_full and rating < circuit.min_rating:
            continue

        juggler_removed = circuit.jugglers.pop() if circuit.is_full else None
        circuit.add_juggler(juggler, rating)

        # Recursively adds removed user to another team.
        if juggler_removed:
            return add_juggler_to_circuit(juggler_removed, circuits)
        return None

    return juggler


def scatter_remaining_jugglers(jugglers, circuits):
    """
    Juggler's for which all their preferred circuits are already full, are scattered to remaining
    circuits according to the similarity between them and circuits.
    Trivial examples where this could happen is if all jugglers prefer only one circuit and they all
    prefer the same circuit OR if none of the jugglers prefer any of the circuits.
    """

    # Creates a copy of circuits which are not full in order to ensure, that none of the jugglers,
    # which are already located in their circuits, doesn't get removed from them.
    # When the circuits are copied, their max size is changed and their juggler lists are set to [].
    circuits_not_full = {
        n: Circuit(c.name, c.skill_ratings, c.num_free_places) for n, c in circuits.items()
        if not c.is_full
    }
    circuit_names = [n for n in circuits_not_full.keys()]
    # Creates a copy of jugglers and changes their preferred circuits.
    jugglers_copy = [Juggler(j.name, j.skill_ratings, circuit_names) for j in jugglers]

    # Copied jugglers are first scattered to copied circuits in order not to spoil real circuits.
    for juggler in jugglers_copy:
        juggler_not_inserted = add_juggler_to_circuit(juggler, circuits_not_full)

        if juggler_not_inserted:
            raise Exception(const.MSG_SCATTERING)

    jugglers_dict = {j.name: j for j in jugglers}

    # Scatters jugglers to real circuits
    for c_name, circuit in circuits_not_full.items():
        for juggler in circuit.jugglers:
            # Real juggler and copied juggler have different preferred circuits
            juggler_real = jugglers_dict[juggler.name]
            juggler_real.rating_curr = juggler.rating_curr_circuit
            circuits[c_name].add_juggler(juggler_real)


def scatter_jugglers_to_circuits(jugglers, circuits):
    """
    Scatters jugglers into circuits according to their preferences and similarity with circuits.
    """

    if not circuits:
        raise Exception(const.MSG_NO_CIRCUITS)

    num_circuits, num_jugglers = len(circuits), len(jugglers)
    if num_jugglers % num_circuits != 0:
        raise Exception(const.MSG_DIVISIBILITY)

    circuit_size = num_jugglers // num_circuits

    for _, circuit in circuits.items():
        circuit.max_size = circuit_size

    jugglers_without_circuit = []

    for juggler in jugglers:
        juggler_not_inserted = add_juggler_to_circuit(juggler, circuits)

        if juggler_not_inserted:
            jugglers_without_circuit.append(juggler_not_inserted)

    scatter_remaining_jugglers(jugglers_without_circuit, circuits)

