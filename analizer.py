import re

from typing import Any, Iterable

from PyPDF2 import PdfReader


def remove_bad_whitespace(contents : Iterable[str]) -> str:
    full_text = ''
    for content in contents:
        bad_whitespaces = list(re.finditer(r'(\s|\n){2,}', content))
        bad_whitespaces.reverse()
        new = content[:]
        for match in bad_whitespaces:
            union = ''
            matched = match[0]
            if matched.count(' ') == len(matched):
                union = ' '
            elif matched.count('\n') > 0:
                union = '\n'
            new = new[:match.start()] + union + new[match.end():]
        full_text += new

    return full_text

def recompose_text(text: str) -> str:
    result = ''
    sentences = list(re.finditer(r'',text))

    return result


def main() -> None:
    PDF_PATH = './pdfs/fod_largo.pdf'
    MAX_SIZE = 5

    pdf_reader = PdfReader(PDF_PATH)
    count = -1
    def my_func(_:Any) -> bool:
        nonlocal count
        count += 1
        return count < MAX_SIZE
    limited_pages = filter(my_func,pdf_reader.pages)
    result = remove_bad_whitespace(map(lambda page: page.extract_text(), limited_pages))
    print(result)
    result = recompose_text(result)
    print(result)
    

if __name__ == '__main__':
    main()