import re
from dataclasses import dataclass
from typing import Literal

import flavors


@dataclass
class Statement:
    sentence: str
    options: list[tuple[str, str]]
    answers: list[str]


FLAGS = re.IGNORECASE | re.MULTILINE | re.UNICODE
R_UNICODELETTERS = r'[^\W\d_]'
R_MARKER = r'[\t .,_\-:)]'

r_defs: flavors.Definition


def normalize_answer(text: str) -> str:
    text = text.strip(' ().')
    if not text:
        return ''
    if text.isdigit():
        return chr(96 + int(text))
    if len(text) == 1:
        return text.lower()
    return text


def parse_answers(text: str) -> list[str]:
    answers: list[str] = []
    for match in re.finditer(r_defs.ANSWER, text, FLAGS):
        answer = normalize_answer(match['answer'])
        if not answer:
            continue
        answers.append(answer)
    return answers


def parse_options(text: str) -> list[tuple[str, str]]:
    options: list[tuple[str, str]] = []
    for index, match in enumerate(re.finditer(r_defs.OPTION, text, FLAGS)):
        options.append(
            (chr(97 + index), match['option'].strip(' .'))
        )
    return options


def parse_sentence(text: str) -> str:
    sentence = ''
    match = re.match(r_defs.SENTENCE, text, FLAGS)
    if match:
        sentence = match['sentence'].strip()
        sentence = sentence[0].upper() + sentence[1:]
    return sentence


def normalize_sentence(text: str) -> str:
    text = text.strip()
    if text and (text[-1] not in ('?', ':')):
        text = text + ':'
    return text[0].upper() + text[1:] if text else text


def parse_statement(text: str) -> Statement:
    match = re.match(r_defs.STATEMENT, text, FLAGS)
    if match is None:
        return Statement('', [], [])

    return Statement(
        normalize_sentence(match['sentence']),
        parse_options(match['options']),
        parse_answers(match['answers'])
    )


def _parse(text: str, flavor: Literal['generic', 'moodle']) -> list[Statement]:
    global r_defs
    r_defs = flavors.definitions[flavor]
    return [
        parse_statement(match.group())
        for match in re.finditer(r_defs.STATEMENT, text, FLAGS)
    ]


def normalize_option_separetors(text: str) -> str:
    result = text

    for match in re.finditer(r' [a-l1-9][.-]', text, re.I):
        result = result[0:match.start()] + '\n' + result[match.start()+1:]
    return result


def parse(text: str, flavor: Literal[flavors.Flavors, 'all'] = 'all') -> list[Statement]:
    text = normalize_option_separetors(text)
    
    if flavor == 'all':
        return [
            statement
            for flavor_name in flavors.definitions
            for statement in _parse(text, flavor_name)
        ]
    return _parse(text, flavor)
