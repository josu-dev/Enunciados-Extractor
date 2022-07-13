import re
from dataclasses import dataclass


@dataclass
class Statement:
    sentence: str
    options: list[tuple[str, str]]
    answers: list[str]


FLAGS = re.IGNORECASE | re.MULTILINE | re.UNICODE
R_UNICODELETTERS = r'[^\W\d_]'
R_MARKER = r'[\t .,_\-:)]'

# TODO make that second spec of option no matches a digit/letter + marker sentence
R_ANSWER = r' *(?P<answer>(\([^()\n]+\))|(^[^\d][^(\s][^()\n]+))'


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
    for match in re.finditer(R_ANSWER, text, FLAGS):
        answer = normalize_answer(match['answer'])
        if not answer:
            continue
        answers.append(answer)
    return answers


# other possible re r' *[^\W\d_] *[\t.,_\-:)]+ *(?P<option>[^\W\d_].+?(?=( [^\W\d_][._\-:)])|\n))'
R_OPTION = r'^ *[^\W_][\t .,_\-:)]+(?P<option>[^\W\d_].+)'


def parse_options(text: str) -> list[tuple[str, str]]:
    options: list[tuple[str, str]] = []
    for index, match in enumerate(re.finditer(R_OPTION, text, FLAGS)):
        options.append(
            (chr(97 + index), match['option'].strip(' .'))
        )
    return options


R_SENTENCE = r'^ *\d\w?[\t .,_\-:)]+(?P<sentence>[^\W\d_].+)'


def parse_sentence(text: str) -> str:
    sentence = ''
    match = re.match(R_SENTENCE, text, FLAGS)
    if match:
        sentence = match['sentence'].strip()
        sentence = sentence[0].upper() + sentence[1:]
    return sentence


def normalize_sentence(text: str) -> str:
    text = text.strip()
    if text and (text[-1] not in ('?', ':')):
        text = text + ':'
    return text[0].upper() + text[1:] if text else text


R_STATEMENT = R_SENTENCE + \
    r'\s*\n(?P<options>('+R_OPTION+r'\s*)+)\s*(?P<answers>('+R_ANSWER+r' *)*)?'


def parse_statement(text: str) -> Statement:
    match = re.match(R_STATEMENT, text, FLAGS)
    if match is None:
        return Statement('', [], [])

    return Statement(
        normalize_sentence(match['sentence']),
        parse_options(match['options']),
        parse_answers(match['answers'])
    )


def parse_enumerated(text: str) -> list[tuple[int, Statement]]:
    result: list[tuple[int, Statement]] = []
    for index, match in enumerate(re.finditer(R_STATEMENT, text, FLAGS)):
        result.append(
            (index, parse_statement(match.group()))
        )
    return result


def parse(text: str) -> list[Statement]:
    result = [
        parse_statement(match.group())
        for match in re.finditer(R_STATEMENT, text, FLAGS)
    ]
    return result
