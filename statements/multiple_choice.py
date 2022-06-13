import re
from dataclasses import dataclass
from typing import Any


@dataclass
class SubSection:
    sentence: str
    options: list[tuple[str, str]]
    anwers: list[str]


@dataclass
class Section:
    name: str
    sub_sections: list[tuple[int, SubSection]]


R_ANSWER = r'(?P<answer>\([^()]+\))'
R_OPTION = r'[A-Za-z0-9]\s*[._\-)]?\s*(?P<option>.+)'
R_SENTENCE = r'[0-9]+\s*[._\-)]?\s*(?P<sentence>.+)'
R_TEXT_LINE = r'(?P<text_line>.+)\n'


def parse(text: str) -> Any:
    result: list[SubSection] = []
    sentence = r'[0-9]+\s*[-.)\|]*(?P<sentence>.+)\n(?P<options>([A-Za-z]\s*[.\-)]*\s*.+\n)+)\s*(?P<answers>(\(.+\)\s*)*)'
    r_options = r'[A-Za-z]\s*[.\-)]*\s*(?P<option>.+)\n'
    r_answers = r'\s*(?P<answer>\([^()]+\))\s*'
    captured: list[re.Match[str]] = list(re.finditer(sentence, text))
    for match in captured:
        groups = match.groupdict()
        sentence = groups['sentence']
        options = list(re.finditer(r_options, groups['options']))
        options_list: list[tuple[str, str]] = []
        start_chr = 97
        for option in options:
            options_list.append((chr(start_chr), option['option']))
            start_chr += 1
        answers_list: list[str] = []
        answers = list(re.finditer(r_answers, groups['answers']))
        for answer in answers:
            answers_list.append(answer['answer'])
        result.append(SubSection(sentence, options_list, answers_list))
    return result
