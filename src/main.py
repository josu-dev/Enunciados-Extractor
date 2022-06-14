from . import const
from . import utils
from .processors import multiple_choice

def main() -> None:
    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        with open(path, mode='r', encoding='utf-8') as file:
            content = ''.join(file.readlines())
        result = multiple_choice.parse(content)
        path = utils.join_path(const.PATH_OUTPUT, file_name.split('.')[0] + '.json')
        utils.save_json(path, result, True)

if __name__ == '__main__':
    main()