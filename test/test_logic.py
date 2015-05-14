from unittest import TestCase

from test.utils import gen_rand_circuits_and_jugglers
from juggle_fest import const as const_j
from juggle_fest.logic import scatter_jugglers_to_circuits
from juggle_fest.utils import calc_similarity


class TestLogic(TestCase):
    def setUp(self):
        self._num_circuits, self._num_jugglers, self._num_preferred_circuits = 200, 1200, 3
        self._circuits, self._jugglers = gen_rand_circuits_and_jugglers(
            self._num_circuits, self._num_jugglers, self._num_preferred_circuits
        )

    def _check_no_jugglers_can_be_moved_to_another_team(self, circuits):
        for c_name, circuit in circuits.items():
            for juggler in circuit.jugglers:
                juggler.reset_circuits_index()
                for preferred_circuit_name, _ in juggler.next_circuit_and_sim(circuits):
                    # Juggler is located in his preferred circuit
                    if preferred_circuit_name == c_name:
                        break

                    # Similarity between juggler and his current preferred circuit
                    preferred_circuit = circuits[preferred_circuit_name]
                    skill_rating_curr = calc_similarity(
                        juggler.skill_ratings, preferred_circuit.skill_ratings
                    )

                    # Similarity between last juggler in preferred circuit and preferred circuit
                    skill_rating_other = calc_similarity(
                        preferred_circuit.jugglers[-1].skill_ratings,
                        preferred_circuit.skill_ratings
                    )

                    self.assertLessEqual(skill_rating_curr, skill_rating_other)

    def _set_all_jugglers_prefer_same_team(self):
        for juggler in self._jugglers:
            juggler._preferred_circuits = ["%s%d" % (const_j.CIRCUIT, 0)]

    def _set_all_jugglers_prefer_no_team(self):
        for juggler in self._jugglers:
            juggler._preferred_circuits = []

    def test_all_teams_contain_unique_jugglers(self):
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)
        seen_jugglers = {}

        for _, circuit in self._circuits.items():
            for juggler in circuit.jugglers:
                self.assertNotIn(juggler, seen_jugglers)
                seen_jugglers[juggler.name] = True

    def test_all_teams_have_equal_size(self):
        expected_size = self._num_jugglers // self._num_circuits
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)

        for _, circuit in self._circuits.items():
            self.assertEqual(expected_size, len(circuit.jugglers))

    def test_all_teams_have_equal_size_if_all_jugglers_prefer_same_team(self):
        expected_size = self._num_jugglers // self._num_circuits
        self._set_all_jugglers_prefer_same_team()
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)

        for _, circuit in self._circuits.items():
            self.assertEqual(expected_size, len(circuit.jugglers))

    def test_all_teams_have_equal_size_if_none_of_the_jugglers_prefer_any_team(self):
        expected_size = self._num_jugglers // self._num_circuits
        self._set_all_jugglers_prefer_no_team()
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)

        for _, circuit in self._circuits.items():
            self.assertEqual(expected_size, len(circuit.jugglers))

    def test_no_juggler_can_be_moved_to_another_team(self):
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)
        self._check_no_jugglers_can_be_moved_to_another_team(self._circuits)

    def test_no_juggler_can_be_moved_to_another_team_if_all_jugglers_prefer_same_team(self):
        self._set_all_jugglers_prefer_same_team()
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)
        self._check_no_jugglers_can_be_moved_to_another_team(self._circuits)

    def test_no_juggler_can_be_moved_to_another_team_if_none_of_the_jugglers_prefer_any_team(self):
        self._set_all_jugglers_prefer_no_team()
        scatter_jugglers_to_circuits(self._jugglers, self._circuits)
        self._check_no_jugglers_can_be_moved_to_another_team(self._circuits)

    def test_orders_jugglers_by_similarity_to_their_corresponding_circuit(self):
        for c_name, circuit in self._circuits.items():
            for j1, j2 in zip(circuit.jugglers[:-1], circuit.jugglers[1:]):
                self.assertGreaterEqual(j1.rating_curr, j2.rating_curr)

    def test_correctly_calculates_similarity_between_circuits_and_jugglers(self):
        for c_name, circuit in self._circuits.items():
            for juggler in circuit.jugglers:
                similarity = calc_similarity(juggler.rating_curr_circuit, circuit.skill_ratings)
                self.assertEqual(similarity, juggler.rating_curr)

    def test_raises_exception_if_no_circuits_provided(self):
        with self.assertRaises(Exception) as e:
            scatter_jugglers_to_circuits(self._jugglers, {})
        self.assertEqual(str(e.exception), const_j.MSG_NO_CIRCUITS)

    def test_doesnt_raise_exception_if_no_jugglers_provided(self):
        # No exceptions should be raised
        scatter_jugglers_to_circuits({}, self._circuits)

    def test_raises_exception_if_number_of_jugglers_is_not_divisible_by_number_of_circuits(self):
        with self.assertRaises(Exception) as e:
            scatter_jugglers_to_circuits(self._jugglers[:555], self._circuits)
        self.assertEqual(str(e.exception), const_j.MSG_DIVISIBILITY)
