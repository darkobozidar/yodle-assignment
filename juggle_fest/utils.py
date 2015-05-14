from . import const


def str_skills_to_numbers(skills):
    """Converts string with skills read from a file to integers. List has format: [H, E, P]."""

    return [int(d.split(const.SEPARATOR_SKILL)[1]) for d in skills]


def skills_to_file_format(skills):
    """Converts list of skills to file format."""

    format_skill = lambda j, s: "%s%s%d" % (j, const.SEPARATOR_SKILL, s)
    str_skills = const.SEPARATOR_DATA.join(
        format_skill(j, s) for j, s in zip(const.JUGGLING_SKILLS, skills)
    )

    return str_skills


def calc_similarity(skills_1, skills_2):
    """Calculated similarity between two list of skill ratings."""

    return sum(s1 * s2 for s1, s2 in zip(skills_1, skills_2))


def sum_juggler_names(jugglers):
    """Sums the names of the jugglers excluding letter 'J'."""

    return sum(int(j.name[1:]) for j in jugglers)
