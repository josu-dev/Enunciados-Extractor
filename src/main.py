import const
import utils

from processors import multiple_choice, multiple_choice_moodle

def main() -> None:
    parsers = [
        multiple_choice.parse,
        multiple_choice_moodle.parse
    ]

    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        file_name = utils.normalize_name(file_name.split('.')[0])
        
        with open(path, mode='r', encoding='utf-8') as file:
            content = ''.join(file.readlines())

        for index, parse in enumerate(parsers):
            result = parse(content)
            if not result:
                continue
            new_file_name = file_name + f'_{index}.json'
            path = utils.join_path(const.PATH_OUTPUT, new_file_name)
            utils.save_json(path, result, True)

if __name__ == '__main__':
    main()