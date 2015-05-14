import os
import random

from . import const as const_t
from juggle_fest import const as const_j
from juggle_fest.classes import Circuit, Juggler


def gen_rand_skill_ratings(max_skill_val=const_t.MAX_SKILL_VAL):
    """Generates random skill ratings."""

    return [random.randint(1, max_skill_val) for _ in range(len(const_j.JUGGLING_SKILLS))]


def gen_rand_circuit(circuit_id, max_size=0, max_skill_val=const_t.MAX_SKILL_VAL):
    """Generates circuit with random values."""

    name = "%s%d" % (const_j.CIRCUIT, circuit_id)
    skill_ratings = gen_rand_skill_ratings(max_skill_val)

    return Circuit(name, skill_ratings, max_size)


def gen_rand_juggler(juggler_id, circuits_names, num_preferred_circuits,
                     max_skill_val=const_t.MAX_SKILL_VAL):
    """Generates juggler with random values."""

    name = "%s%d" % (const_j.JUGGLER, juggler_id)
    skill_ratings = gen_rand_skill_ratings(max_skill_val)
    circuits_len = len(circuits_names)

    # Generates unique list of preferred circuits
    preferred_circuits, curr_circuit = [], 0
    while curr_circuit < num_preferred_circuits:
        new_circuit = circuits_names[random.randint(0, circuits_len - 1)]

        if new_circuit not in preferred_circuits:
            preferred_circuits.append(new_circuit)
            curr_circuit += 1

    return Juggler(name, skill_ratings, preferred_circuits)


def gen_rand_circuits_and_jugglers(num_circuits, num_jugglers, num_preferred_circuits):
    """Generates specified number of circuits and jugglers."""

    circuits = {}
    for circuit_id in range(num_circuits):
        circuit_new = gen_rand_circuit(circuit_id)
        circuits[circuit_new.name] = circuit_new

    circuit_names = [c for c in circuits.keys()]
    jugglers = [
        gen_rand_juggler(j, circuit_names, num_preferred_circuits) for j in range(num_jugglers)
    ]

    return circuits, jugglers


def circuits_and_jugglers_to_file(num_circuits, num_jugglers, num_preferred_circuits,
                                  file_name=const_t.FILE_NAME):
    """Generates specified number of circuit and jugglers and saves them to file."""

    circuits, jugglers = gen_rand_circuits_and_jugglers(
        num_circuits, num_jugglers, num_preferred_circuits
    )

    with open(file_name, "w") as file:
        for _, circuit in circuits.items():
            print(circuit.input_file_format, file=file)

        print(file=file)

        for juggler in jugglers:
            print(juggler.input_file_format, file=file)

    return circuits, jugglers


def remove_file(file_name):
    """Removes file if it exist."""

    try:
        os.remove(file_name)
    except OSError:
        pass
