from . import const
from .utils import skills_to_file_format, calc_similarity


class Circuit():
    """Represents the circuit."""

    def __init__(self, name, skill_ratings, max_size=0):
        # Circuit name
        self.name = name
        # Maximum number of jugglers for this circuit
        self.max_size = max_size
        # List of skills required to execute circuit in order [H, E, P]
        self.skill_ratings = skill_ratings

        # List of jugglers, which will execute this circuit
        self.jugglers = []

    @property
    def is_full(self):
        """Returns true if list of jugglers is full."""

        return len(self.jugglers) >= self.max_size

    @property
    def num_free_places(self):
        """Returns the number of free places in the circuit for the jugglers."""

        return self.max_size - len(self.jugglers)

    @property
    def min_rating(self):
        """Returns minimum circuit rating of all jugglers."""

        return self.jugglers[-1].rating_curr_circuit if self.jugglers else 0

    @property
    def input_file_format(self):
        """Returns a circuit in a string format needed for input file."""

        output = "%(circuit)s%(sep)s%(name)s%(sep)s%(skills)s" % {
            "circuit": const.CIRCUIT,
            "sep": const.SEPARATOR_DATA,
            "name": self.name,
            "skills": skills_to_file_format(self.skill_ratings),
        }

        return output

    def output_file_format(self, circuits):
        """Returns a circuit in a string format needed for output file."""

        format_rating = lambda c, r: "%s%s%d" % (c, const.SEPARATOR_SKILL, r)
        ratings_gen = lambda j: (format_rating(c, r) for c, r in j.all_circuits_and_sim(circuits))
        ratings = lambda j: const.SEPARATOR_DATA.join(ratings_gen(j))
        format_juggler = lambda j: "%s%s%s" % (j.name, const.SEPARATOR_DATA, ratings(j))
        juggler_str = ", ".join((format_juggler(j) for j in self.jugglers))

        output = "%(c_name)s%(sep)s%(jugglers)s" % {
            "c_name": self.name,
            "sep": const.SEPARATOR_DATA,
            "jugglers": juggler_str,
        }

        return output

    def add_juggler(self, juggler_new, rating=None):
        """Adds new juggler, which are ordered by the similarity between them and circuit."""

        if self.is_full:
            raise Exception(const.MSG_CIRCUIT_FULL)

        if rating is None:
            juggler_new.rating_curr_circuit = calc_similarity(
                juggler_new.skill_ratings, self.skill_ratings
            )
        else:
            juggler_new.rating_curr_circuit = rating

        index_juggler = 0
        for juggler in self.jugglers:
            if juggler_new.rating_curr_circuit > juggler.rating_curr_circuit:
                break
            index_juggler += 1

        self.jugglers.insert(index_juggler, juggler_new)


class Juggler():
    """Represents jugglers."""

    def __init__(self, name, skill_ratings, preferred_circuits):
        # Name of the juggler
        self.name = name
        # List of juggler's skills in order [H, E, P]
        self.skill_ratings = skill_ratings
        # List of tuples containing juggler's preferred circuits and corresponding similarities
        self._preferred_circuits = preferred_circuits

        # Index of last juggler's circuit, which has been examined
        self._curr_circuit = 0
        # Juggler's rating for the circuit he is currently assigned to
        self.rating_curr_circuit = 0

    @property
    def input_file_format(self):
        """Returns a juggler in a string format needed for input file."""

        output = "%(juggler)s%(sep)s%(name)s%(sep)s%(skills)s%(sep)s%(preferred_circuits)s" % {
            "juggler": const.JUGGLER,
            "sep": const.SEPARATOR_DATA,
            "name": self.name,
            "skills": skills_to_file_format(self.skill_ratings),
            "preferred_circuits": const.SEPARATOR_PREFERENCES.join(self._preferred_circuits),
        }

        return output

    def next_circuit_and_sim(self, circuits, curr_circuit=None):
        """
        From juggler's preferred circuits generates new circuit and it's similarity with juggler.
        """

        curr_circuit = self._curr_circuit if curr_circuit is None else curr_circuit

        for c_name in self._preferred_circuits[curr_circuit:]:
            self._curr_circuit += 1
            yield c_name, calc_similarity(self.skill_ratings, circuits[c_name].skill_ratings)

    def all_circuits_and_sim(self, circuits):
        """Returns generator with all juggler's pref. circuits and corresponding similarities."""

        for c_name, sim in self.next_circuit_and_sim(circuits, 0):
            yield c_name, sim

    def reset_circuits_index(self):
        """Resets generator of juggler's preferences to first circuit."""

        self._curr_circuit = 0
