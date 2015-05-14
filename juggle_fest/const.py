# Name of the input file, where jugglers and circuits are stored
FILE_NAME_INPUT = "../data/jugglefest.txt"
# Output file, where results are saved
FILE_NAME_OUTPUT = "../data/output.txt"

# Character used to separate data about circuit or juggler
SEPARATOR_DATA = " "
# Character used to separate skills for circuits and jugglers
SEPARATOR_SKILL = ":"
# Character used to separate juggler's preferred circuits
SEPARATOR_PREFERENCES = ","

# Denotes circuit in a file
CIRCUIT = "C"
# Denotes juggler in a file
JUGGLER = "J"

# Juggling skills: eye coordination (H), endurance (E) and pizzazz (P)
JUGGLING_SKILLS = ["H", "E", "P"]

# Error message if duplicate circuit with the same name is found in input file
MSG_DUPLICATE_CIRCUIT = "Duplicate circuit in input file: '%s'"
# Error message if duplicate juggler with the same name is found in input file
MSG_DUPLICATE_JUGGLER = "Duplicate juggler in input file: '%s'"
# Error message if line of the input file doesn't begin with correct letter
MSG_LINE_BEGINNING = "Line in file has to begin with '%s' or '%s'." % (CIRCUIT, JUGGLER)
# Error message in case jugglers are located before circuits in file
MSG_CIRCUIT_BEFORE_JUGGLER = "Circuits have to be located before jugglers in file."

# Error message if no circuits are provided. In that case jugglers cannot be scattered.
MSG_NO_CIRCUITS = "No circuits provided - cannot scatter jugglers."
# Error message if number of jugglers is not divisible with number of circuits
MSG_DIVISIBILITY = "Number of jugglers not divisible with number of circuits."
# Error message if scattering is performed incorrectly
MSG_SCATTERING = "Error in algorithm for scattering remaining jugglers."

# Error message if trying to insert a juggler in full circuit
MSG_CIRCUIT_FULL = "Cannot insert juggler. Circuit is full."
