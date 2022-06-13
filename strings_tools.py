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