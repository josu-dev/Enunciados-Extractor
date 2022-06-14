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

def test(reader: PdfReader) -> None:
    
    for index, page in enumerate(reader.pages):
        print(page.extract_text())
        if index > 3:
            break

def main() -> None:
    PDF_PATH = './input/fod_corto_new2.pdf'
    MAX_SIZE = 5
    file = open(PDF_PATH, mode='rb')
    pdf_reader = PdfReader(file, False)
    test(pdf_reader)
    exit()
    # print(pdf_reader.metadata)
    count = -1
    def my_func(_:Any) -> bool:
        nonlocal count
        count += 1
        return count < MAX_SIZE
    limited_pages = filter(my_func,pdf_reader.pages)
    for page in limited_pages:
        print(page.__dict__)
        if '/Annots' in page:
            annot = page['/Annots']
            print(annot)
        # print(f'{page.extract_text()}')
    # result = remove_bad_whitespace(map(lambda page: page.extract_text(), limited_pages))
    # print(result)
    # result = recompose_text(result)
    # print(result)
    

if __name__ == '__main__':
    main()