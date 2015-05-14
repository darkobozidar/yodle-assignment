from unittest import TestCase

from test import const as const_t
from test import utils as utils_t
from juggle_fest import const as const_j
from juggle_fest.file import read_input_file, write_results_to_file
from juggle_fest.logic import scatter_jugglers_to_circuits
from juggle_fest.classes import Circuit, Juggler


class TestReadInputFile(TestCase):
    def setUp(self):
        self._num_circuits, self._num_jugglers, self._num_preferred_circuits = 200, 1200, 3

    def tearDown(self):
        utils_t.remove_file(const_t.FILE_NAME)

    def test_reads_circuits_correctly(self):
        circuit_0 = Circuit("C0", [1, 2, 3])
        circuit_1 = Circuit("C1", [4, 5, 6])

        with open(const_t.FILE_NAME, "w") as file:
            print(circuit_0.input_file_format, file=file)
            print(circuit_1.input_file_format, file=file)

        circuits, _ = read_input_file(const_t.FILE_NAME)
        circuit_file_0, circuit_file_1 = circuits[circuit_0.name], circuits[circuit_1.name]

        self.assertEqual(circuit_0.name, circuit_file_0.name)
        self.assertEqual(circuit_0.skill_ratings, circuit_file_0.skill_ratings)

        self.assertEqual(circuit_1.name, circuit_file_1.name)
        self.assertEqual(circuit_1.skill_ratings, circuit_file_1.skill_ratings)

    def test_reads_jugglers_correctly(self):
        circuit = Circuit("C0", [1, 2, 3])
        juggler_0 = Juggler("J0", [1, 2, 3], ["C0"])
        juggler_1 = Juggler("J1", [4, 5, 6], ["C1"])

        with open(const_t.FILE_NAME, "w") as file:
            # At least one circuit has to be located before jugglers
            print(circuit.input_file_format, file=file)
            print(juggler_0.input_file_format, file=file)
            print(juggler_1.input_file_format, file=file)

        _, jugglers = read_input_file(const_t.FILE_NAME)
        juggler_file_0, juggler_file_1 = jugglers[0], jugglers[1]

        self.assertEqual(juggler_0.name, juggler_file_0.name)
        self.assertEqual(juggler_0.skill_ratings, juggler_file_0.skill_ratings)
        self.assertEqual(juggler_0._preferred_circuits, juggler_file_0._preferred_circuits)

        self.assertEqual(juggler_1.name, juggler_file_1.name)
        self.assertEqual(juggler_1.skill_ratings, juggler_file_1.skill_ratings)
        self.assertEqual(juggler_1._preferred_circuits, juggler_file_1._preferred_circuits)

    def test_raises_exception_if_no_circuits_are_located_in_file(self):
        juggler = utils_t.gen_rand_juggler(0, ["C0"], 1)

        with open(const_t.FILE_NAME, "w") as file:
            print(juggler.input_file_format, file=file)

        with self.assertRaises(Exception) as e:
            read_input_file(const_t.FILE_NAME)
        self.assertEqual(str(e.exception), const_j.MSG_CIRCUIT_BEFORE_JUGGLER)

    def test_raises_exception_if_jugglers_are_located_before_circuits_in_file(self):
        circuit = utils_t.gen_rand_circuit(0)
        juggler = utils_t.gen_rand_juggler(0, [circuit.name], 1)

        with open(const_t.FILE_NAME, "w") as file:
            print(juggler.input_file_format, file=file)
            print(file=file)
            print(circuit.input_file_format, file=file)

        with self.assertRaises(Exception) as e:
            read_input_file(const_t.FILE_NAME)
        self.assertEqual(str(e.exception), const_j.MSG_CIRCUIT_BEFORE_JUGGLER)

    def test_raises_exception_if_duplicate_circuit_is_located_in_file(self):
        circuit = Circuit("C0", [1, 2, 3])

        with open(const_t.FILE_NAME, "w") as file:
            print(circuit.input_file_format, file=file)
            print(circuit.input_file_format, file=file)

        with self.assertRaises(Exception) as e:
            read_input_file(const_t.FILE_NAME)
        self.assertEqual(str(e.exception), const_j.MSG_DUPLICATE_CIRCUIT % circuit.name)

    def test_raises_exception_if_duplicate_juggler_is_located_in_file(self):
        circuit = Circuit("C0", [1, 2, 3])
        juggler = Juggler("J0", [1, 2, 3], ["C0"])

        with open(const_t.FILE_NAME, "w") as file:
            # At least one circuit has to be located before jugglers
            print(circuit.input_file_format, file=file)
            print(juggler.input_file_format, file=file)
            print(juggler.input_file_format, file=file)

        with self.assertRaises(Exception) as e:
            read_input_file(const_t.FILE_NAME)
        self.assertEqual(str(e.exception), const_j.MSG_DUPLICATE_JUGGLER % juggler.name)

    def test_raises_exception_if_line_doesnt_begin_with_expected_letter(self):
        utils_t.circuits_and_jugglers_to_file(
            self._num_circuits, self._num_jugglers, self._num_preferred_circuits
        )

        with open(const_t.FILE_NAME, "a") as file:
            print("Not expected", file=file)

        with self.assertRaises(Exception) as e:
            read_input_file(const_t.FILE_NAME)
        self.assertEqual(str(e.exception), const_j.MSG_LINE_BEGINNING)


class TestWriteOutputFile(TestCase):
    def setUp(self):
        self._num_circuits, self._num_jugglers, self._num_preferred_circuits = 2, 2, 1
        self._circuits, self._jugglers = utils_t.gen_rand_circuits_and_jugglers(
            self._num_circuits, self._num_jugglers, self._num_preferred_circuits
        )
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)
        write_results_to_file(self._circuits, const_t.FILE_NAME)

    def tearDown(self):
        utils_t.remove_file(const_t.FILE_NAME)

    def test_writes_results_to_file(self):
        circuits = [c for c in self._circuits.values()]

        # Output format is tested in class tests
        with open(const_t.FILE_NAME) as file:
            content = file.read()

        self.assertIn(circuits[0].name, content)
        self.assertIn(circuits[1].name, content)

    def test_orders_circuits_in_descending_order(self):
        # In example output of the task circuits are ordered in reversed order
        circuit_names = [c.name for c in self._circuits.values()]
        circuit_names.sort(reverse=True)

        with open(const_t.FILE_NAME) as file:
            content = file.readlines()

        self.assertIn(circuit_names[0], content[0])
        self.assertIn(circuit_names[1], content[1])

    def test_doesnt_add_new_line_at_the_end_of_the_file(self):
        # Task demands that there is one line per circuit assignment in output file
        with open(const_t.FILE_NAME) as file:
            content = file.readlines()

        self.assertEqual(len(self._circuits), len(content))
