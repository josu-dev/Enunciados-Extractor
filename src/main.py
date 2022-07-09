import const
import utils

from processors import multiple_choice, multiple_choice_moodle

def main_old() -> None:
    parsers = [
        multiple_choice.parse,
        multiple_choice_moodle.parse
    ]

    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        file_name = utils.normalize_name(file_name.split('.')[0])
        
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                content = ''.join(file.readlines())
        except:
            continue
        
        for index, parse in enumerate(parsers):
            result = parse(content)
            if not result:
                continue
            
            print(len(result))
            new_file_name = file_name + f'_{index}.json'
            path = utils.join_path(const.PATH_OUTPUT, new_file_name)
            utils.save_json(path, result, True)


def main() -> None:
    parsers = [
        multiple_choice.parse,
        multiple_choice_moodle.parse
    ]

    partial_results:list[list[multiple_choice.Statement]]= []

    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        file_name = utils.normalize_name(file_name.split('.')[0])
        
        try:
            with open(path, mode='r', encoding='utf-8') as file:
                content = ''.join(file.readlines())
        except:
            continue
        
        for parse in parsers:
            result = parse(content)
            if not result:
                continue
            partial_results.append(result)

    result = [
        statement
        for l_statements in partial_results
        for statement in l_statements
    ]
    
    file_name = 'extracted_multiple_choices.json'
    path = utils.join_path(const.PATH_OUTPUT, file_name)
    utils.save_json(path, result, True)

if __name__ == '__main__':
    main()