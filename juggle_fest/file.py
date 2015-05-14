from . import const
from .utils import str_skills_to_numbers
from .classes import Circuit, Juggler


def read_input_file(file_name):
    """Reads data from file about circuits and jugglers."""

    circuits, jugglers, jugglers_seen = {}, [], {}

    for line in open(file_name):
        # Separator between circuits and jugglers
        if len(line) <= 1:
            continue

        line = line[:-1] if line.endswith("\n") else line
        data = line.split(const.SEPARATOR_DATA)

        if data[0] == const.CIRCUIT:
            if jugglers:
                raise Exception(const.MSG_CIRCUIT_BEFORE_JUGGLER)

            circuit_name = data[1]
            if circuit_name in circuits:
                raise Exception(const.MSG_DUPLICATE_CIRCUIT % circuit_name)

            circuits[data[1]] = Circuit(data[1], str_skills_to_numbers(data[2:]))
        elif data[0] == const.JUGGLER:
            if not circuits:
                raise Exception(const.MSG_CIRCUIT_BEFORE_JUGGLER)

            juggler_name = data[1]
            if juggler_name in jugglers_seen:
                raise Exception(const.MSG_DUPLICATE_JUGGLER % juggler_name)

            skill_ratings = str_skills_to_numbers(data[2:5])
            preferred_circuits = data[5].split(const.SEPARATOR_PREFERENCES)
            jugglers.append(Juggler(juggler_name, skill_ratings, preferred_circuits))
            jugglers_seen[juggler_name] = True
        else:
            raise Exception(const.MSG_LINE_BEGINNING)

    return circuits, jugglers


def write_results_to_file(circuits, file_output):
    """Writes results to output file."""

    # Output has to be reversed
    circuits_sorted = sorted(circuits.items(), key=lambda t: int(t[0][1:]), reverse=True)
    num_circuits = len(circuits)

    with open(file_output, "w") as file:
        for c_index, (c_name, circuit) in enumerate(circuits_sorted):
            file.write(circuit.output_file_format(circuits))

            # At the end of the file there shouldn't be new line
            if c_index < num_circuits - 1:
                file.write("\n")
