import re
from dataclasses import dataclass


@dataclass
class Statement:
    sentence: str
    options: list[tuple[str, str]]
    anwers: list[str]


FLAGS = re.IGNORECASE | re.MULTILINE | re.UNICODE
R_UNICODELETTERS = r'[^\W\d_]'
R_MARKER = r'[\t .,_\-:)]'


R_ANSWER = r' *(?P<answer>(\([^()\n]+\))|([^(\s][^()\n]+))'


def parse_answers(text: str) -> list[str]:
    answers: list[str] = []
    for match in re.finditer(R_ANSWER, text, FLAGS):
        answers.append(match['answer'].strip())
    return answers


R_OPTION = r'^ *[^\W\d_][\t .,_\-:)]+(?P<option>[^\W\d_].+)'


def parse_options(text: str) -> list[tuple[str, str]]:
    options: list[tuple[str, str]] = []
    for index, match in enumerate(re.finditer(R_OPTION, text, FLAGS)):
        options.append(
            (chr(97 + index), match['option'].strip())
        )
    return options


R_SENTENCE = r'^ *\d\w?[\t .,_\-:)]+(?P<sentence>[^\W\d_].+)'


def parse_sentence(text: str) -> str:
    sentence = ''
    match = re.match(R_SENTENCE, text, FLAGS)
    if match:
        sentence = match['sentence'].strip()
    return sentence


R_STATEMENT = R_SENTENCE + \
    r'\s*\n(?P<options>('+R_OPTION+r'\s*)+)\s*(?P<answers>('+R_ANSWER+r' *)*)?'


def parse_statement(text: str) -> Statement:
    match = re.match(R_STATEMENT, text, FLAGS)
    if match is None:
        return Statement('', [], [])

    return Statement(
        match['sentence'].strip(),
        parse_options(match['options']),
        parse_answers(match['answers'])
    )


def parse(text: str) -> list[tuple[int, Statement]]:
    result: list[tuple[int, Statement]] = []
    for index, match in enumerate(re.finditer(R_STATEMENT, text, FLAGS)):
        result.append(
            (index, parse_statement(match.group()))
        )
    return result
