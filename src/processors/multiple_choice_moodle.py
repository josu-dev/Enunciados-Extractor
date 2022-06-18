import re

import multiple_choice as mc


R_ANSWER = r'^( |\t)*respuesta.+\s+la respuesta correcta es:(?P<answer>.+)'

R_SENTENCE = r'^( |\t)*(?P<sentence>[^\W_].+)\s+seleccione.+'

R_STATEMENT = R_SENTENCE + \
    r'\s*\n(?P<options>('+mc.R_OPTION+r'\s*)+)\s*'+R_ANSWER


def parse_statement(text: str) -> mc.Statement:
    match = re.match(R_STATEMENT, text, mc.FLAGS)
    if match is None:
        return mc.Statement('', [], [])

    return mc.Statement(
        match['sentence'].strip(),
        mc.parse_options(match['options']),
        [match['answer'].strip()]
    )


def parse(text: str) -> list[tuple[int, mc.Statement]]:
    result: list[tuple[int, mc.Statement]] = []
    for index, match in enumerate(re.finditer(R_STATEMENT, text, mc.FLAGS)):
        result.append(
            (index, parse_statement(match.group()))
        )
    return result
