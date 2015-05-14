from unittest import TestCase

from test import utils
from juggle_fest import const as const_j
from juggle_fest.classes import Circuit, Juggler
from juggle_fest.utils import calc_similarity


class TestCircuit(TestCase):
    def setUp(self):
        self._max_size = 2
        self._circuit = utils.gen_rand_circuit(0, self._max_size)

    def test_property_is_full(self):
        self.assertFalse(self._circuit.is_full)

        self._circuit.add_juggler(utils.gen_rand_juggler(0, [self._circuit.name], 1))
        self.assertFalse(self._circuit.is_full)

        self._circuit.add_juggler(utils.gen_rand_juggler(1, [self._circuit.name], 1))
        self.assertTrue(self._circuit.is_full)

    def test_property_num_free_places(self):
        self.assertEqual(2, self._circuit.num_free_places)

        self._circuit.add_juggler(utils.gen_rand_juggler(0, [self._circuit.name], 1))
        self.assertEqual(1, self._circuit.num_free_places)

        self._circuit.add_juggler(utils.gen_rand_juggler(1, [self._circuit.name], 1))
        self.assertEqual(0, self._circuit.num_free_places)

    def test_property_min_rating(self):
        self.assertEqual(0, self._circuit.min_rating)

        juggler_0 = utils.gen_rand_juggler(0, [self._circuit.name], 1)
        juggler_0.rating_curr_circuit = 20
        self._circuit.jugglers.append(juggler_0)
        self.assertEqual(20, self._circuit.min_rating)

        juggler_1 = utils.gen_rand_juggler(0, [self._circuit.name], 1)
        juggler_1.rating_curr_circuit = 10
        self._circuit.jugglers.append(juggler_1)
        self.assertEqual(10, self._circuit.min_rating)

    def test_property_input_file_format(self):
        circuit = Circuit("C0", [1, 2, 3])

        self.assertEqual("C C0 H:1 E:2 P:3", circuit.input_file_format)

    def test_output_file_format(self):
        circuit = Circuit("C0", [0, 0, 0])
        circuit.jugglers.append(Juggler("J0", [0, 0, 0], [circuit.name]))
        circuit.jugglers.append(Juggler("J1", [0, 0, 0], [circuit.name]))

        circuits_dict = {circuit.name: circuit}

        self.assertEqual("C0 J0 C0:0, J1 C0:0", circuit.output_file_format(circuits_dict))

    def test_adds_new_juggler(self):
        self._circuit.add_juggler(utils.gen_rand_juggler(0, [self._circuit.name], 1))
        self.assertEqual(1, len(self._circuit.jugglers))

        self._circuit.add_juggler(utils.gen_rand_juggler(1, [self._circuit.name], 1))
        self.assertEqual(2, len(self._circuit.jugglers))

    def test_sorts_jugglers_according_to_similarity_to_circuit(self):
        self._circuit.max_size = 3

        self._circuit.add_juggler(Juggler("J0", [1, 1, 1], [self._circuit.name]))
        self._circuit.add_juggler(Juggler("J1", [0, 0, 0], [self._circuit.name]))
        self._circuit.add_juggler(Juggler("J2", [9, 9, 9], [self._circuit.name]))

        self.assertEqual("J2", self._circuit.jugglers[0].name)
        self.assertEqual("J0", self._circuit.jugglers[1].name)
        self.assertEqual("J1", self._circuit.jugglers[2].name)

    def test_sets_provided_rating_if_specified(self):
        juggler = Juggler("J0", [1, 1, 1], [self._circuit.name])
        self._circuit.add_juggler(juggler, 100)

        self.assertEqual(100, juggler.rating_curr_circuit)

    def test_raises_exception_when_adding_juggler_if_juggler_list_is_full(self):
        self._circuit.add_juggler(utils.gen_rand_juggler(0, [self._circuit.name], 1))
        self._circuit.add_juggler(utils.gen_rand_juggler(1, [self._circuit.name], 1))

        with self.assertRaises(Exception) as e:
            self._circuit.add_juggler(utils.gen_rand_juggler(2, [self._circuit.name], 1))
        self.assertEqual(const_j.MSG_CIRCUIT_FULL, str(e.exception))


class TestJuggler(TestCase):
    def setUp(self):
        self._circuit_max_size = 2
        self._circuit_0 = utils.gen_rand_circuit(0, self._circuit_max_size)
        self._circuit_1 = utils.gen_rand_circuit(1, self._circuit_max_size)

        self._circuits = {
            self._circuit_0.name: self._circuit_0,
            self._circuit_1.name: self._circuit_1,
        }
        self._circuit_names = [c for c in self._circuits.keys()]
        self._circuit_names.sort()

        self._juggler = Juggler("J0", [1, 1, 1], self._circuit_names)

    def test_property_input_file_format(self):
        juggler = Juggler("J0", [1, 2, 3], ["C0", "C1"])
        self.assertEqual("J J0 H:1 E:2 P:3 C0,C1", juggler.input_file_format)

    def test_generator_next_circuit_and_sim(self):
        self._circuit_0.skill_ratings = [0, 0, 0]
        self._circuit_1.skill_ratings = [1, 1, 1]
        self._juggler.skill_ratings = [1, 1, 1]
        generator = self._juggler.all_circuits_and_sim(self._circuits)

        c_name, rating = next(generator)
        similarity = calc_similarity(self._circuit_0.skill_ratings, self._juggler.skill_ratings)
        self.assertEqual(self._circuit_0.name, c_name)
        self.assertEqual(similarity, rating)

        # Generator should continue to iterate from last generated circuit
        c_name, rating = next(generator)
        similarity = calc_similarity(self._circuit_1.skill_ratings, self._juggler.skill_ratings)
        self.assertEqual(self._circuit_1.name, c_name)
        self.assertEqual(similarity, rating)

    def test_generator_next_circuit_and_sim_if_provided_circuit_index(self):
        for _ in self._juggler.next_circuit_and_sim(self._circuits):
            break

        # Generator should start from the beginning, because index 0 is specified
        for c_name, rating in self._juggler.next_circuit_and_sim(self._circuits, 0):
            self.assertEqual(self._circuit_0.name, c_name)
            break

    def test_generator_all_circuits_and_sim(self):
        self._juggler._curr_circuit = 1
        generator = self._juggler.all_circuits_and_sim(self._circuits)

        c_name, rating = next(generator)
        self.assertEqual(self._circuit_0.name, c_name)

        c_name, rating = next(generator)
        self.assertEqual(self._circuit_1.name, c_name)

    def test_reset_circuit_index(self):
        self._juggler._curr_circuit = 1
        self._juggler.reset_circuits_index()
        self.assertEqual(0, self._juggler._curr_circuit)
