from juggle_fest import const
from juggle_fest.file import read_input_file, write_results_to_file
from juggle_fest.logic import scatter_jugglers_to_circuits
from juggle_fest.utils import sum_juggler_names


circuits, jugglers = read_input_file(const.FILE_NAME_INPUT)
scatter_jugglers_to_circuits(jugglers, circuits)
write_results_to_file(circuits, const.FILE_NAME_OUTPUT)

circuit = "C1970"
if circuit in circuits:
    sum_jugglers = sum_juggler_names(circuits[circuit].jugglers)
    print("Sum of the names of the jugglers for circuit %s is %d." % (circuit, sum_jugglers))
