from unittest import TestCase

from test import utils as utils_t
from juggle_fest import utils as utils_j


class TestUtils(TestCase):
    def test_str_skills_to_numbers(self):
        skill_ratings = utils_j.str_skills_to_numbers(["H:1", "E:2", "P:3"])
        self.assertEqual([1, 2, 3], skill_ratings)

    def test_skills_to_file_format(self):
        str_skills = utils_j.skills_to_file_format([1, 2, 3])
        self.assertEqual("H:1 E:2 P:3", str_skills)

    def test_calc_similarity(self):
        similarity = utils_j.calc_similarity([1, 1, 1], [1, 2, 3])
        self.assertEqual(6, similarity)

    def test_sum_juggler_names(self):
        jugglers = [utils_t.gen_rand_juggler(j, [], 0) for j in range(3)]
        jugglers[0].name = "J0"
        jugglers[1].name = "J1"
        jugglers[2].name = "J10"

        sum_names = utils_j.sum_juggler_names(jugglers)
        self.assertEqual(11, sum_names)
