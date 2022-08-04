from typing import Literal, Protocol

RawString = str
Flavors = Literal['generic', 'moodle']


class Definition(Protocol):
    ANSWER: RawString
    OPTION: RawString
    SENTENCE: RawString
    STATEMENT: RawString


class GenericDefinition:
    # TODO make that second spec of option no matches a digit/letter + marker sentence
    ANSWER = r' *(?P<answer>(\([^()\n]+\))|(^[^\d][^(\s][^()\n]+))'
    # NOTE other possible re r' *[^\W\d_] *[\t.,_\-:)]+ *(?P<option>[^\W\d_].+?(?=( [^\W\d_][._\-:)])|\n))'
    OPTION = r'^ *[^\W_][\t .,_\-:)]+(?P<option>[^\W\d_].+)'
    SENTENCE = r'^ *\d\w?[\t .,_\-:)]+(?P<sentence>[^\W\d_].+)'
    STATEMENT = SENTENCE + \
        r'\s*\n(?P<options>('+OPTION+r'\s*)+)\s*(?P<answers>('+ANSWER+r' *)*)?'


class MoodleDefinition:
    ANSWER = r'^( |\t)*respuesta.+\s+la respuesta correcta es:(?P<answer>.+)'
    OPTION = GenericDefinition.OPTION
    SENTENCE = r'^( |\t)*(?P<sentence>[^\W_].+)\s+seleccione.+'
    STATEMENT = SENTENCE + \
        r'\s*\n(?P<options>('+OPTION+r'\s*)+)\s*(?P<answers>('+ANSWER+r' *)*)?'


definitions: dict[Flavors, Definition] = {
    'generic': GenericDefinition,
    'moodle': MoodleDefinition
}
