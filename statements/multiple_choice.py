import re
from dataclasses import dataclass


@dataclass
class SubSection:
    sentence: str
    options: list[tuple[str, str]]
    anwers: list[str]


@dataclass
class Section:
    name: str
    sub_sections: list[tuple[int, SubSection]]


R_ANSWER = r'\([^()]+\)'
RC_ANSWER = r'(?P<answer>\([^()]+\))'
R_OPTION = r'[A-Za-z]\s*[._\-)]?\s*.+'
RC_OPTION = r'[A-Za-z]\s*[._\-)]?\s*(?P<option>.+)'
R_SENTENCE = r'[0-9]+\s*[._\-)]?\s*.+'
RC_SENTENCE = r'[0-9]+\s*[._\-)]?\s*(?P<sentence>.+)'
R_TITLE = r'[A-Za-zñÑ][A-Za-zñÑ ]*[A-Za-zñÑ]'
RC_TITLE = r'(?P<title>[A-Za-zñÑ][A-Za-zñÑ ]*[A-Za-zñÑ])'


def parse_options(text: str) -> list[tuple[str, str]]:
    options: list[tuple[str, str]] = []
    for index, match in enumerate(re.finditer(RC_OPTION, text)):
        options.append((chr(97 + index), match['option']))
    return options


def parse_answers(text: str) -> list[str]:
    answers: list[str] = []
    for match in re.finditer(RC_ANSWER, text):
        answers.append(match['answer'])
    return answers


def parse_subsections(text: str) -> list[tuple[int, SubSection]]:
    subsections: list[tuple[int, SubSection]] = []
    r_subsection = fr'{RC_SENTENCE}\n(?P<options>({R_OPTION}\s*)+)(?P<answers>({R_ANSWER}\s*)*)'
    for index, match in enumerate(re.finditer(r_subsection, text)):
        subsection = SubSection(
            match['sentence'],
            parse_options(match['options']),
            parse_answers(match['answers'])
        )
        subsections.append((index, subsection))
    return subsections


def parse(text: str) -> list[Section]:
    sections: list[Section] = []
    r_subsection = fr'{RC_SENTENCE}\n(?P<options>({R_OPTION}\s*)+)(?P<answers>({R_ANSWER}\s*)*)'
    r_section = fr'{RC_TITLE}?\s*(?P<subsections>({r_subsection}\s*)+)'
    for match in re.finditer(r_section, text):
        section = Section(
            match['title'] if match['title'] else '',
            parse_subsections(match['subsections'])
        )
        sections.append(section)
    return sections
