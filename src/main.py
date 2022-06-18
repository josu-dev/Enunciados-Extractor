import const
import utils

from processors import multiple_choice, multiple_choice_moodle

def main() -> None:
    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        with open(path, mode='r', encoding='utf-8') as file:
            content = ''.join(file.readlines())
        parsers = [
            multiple_choice.parse,
            multiple_choice_moodle.parse
        ]
        for index, parse in enumerate(parsers):
            result = parse(content)
            if not result:
                continue
            path = utils.join_path(const.PATH_OUTPUT, '_'.join(file_name.split('.')[0].split()) + f'_{index}.json')
            utils.save_json(path, result, True)

if __name__ == '__main__':
    main()