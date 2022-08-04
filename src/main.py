import const
import utils
from processors import multiple_choice


def main() -> None:
    stats: dict[str, list[int]] = {
        'statements': [],
        'options': [],
        'answers': []
    }

    partial_results: list[list[multiple_choice.parser.Statement]] = []

    for file_name, path in utils.scan_dir(const.PATH_INPUT, '.txt'):
        file_name = utils.normalize_file_name(file_name.split('.')[0])

        try:
            with open(path, mode='r', encoding='utf-8') as file:
                content = file.read()
        except FileNotFoundError:
            continue

        result = multiple_choice.parser.parse(content, 'all')
        if not result:
            continue

        partial_results.append(result)

        for r in result:
            stats['answers'].append(len(r.answers))
            stats['options'].append(len(r.options))
            stats['statements'].append(1)

    print('Extraction results:')
    for key in stats:
        print(f' - Total {key}: {sum(stats[key])}')

    result = [
        statement
        for l_statements in partial_results
        for statement in l_statements
    ]

    file_name = 'extracted_multiple_choices.json'
    path = utils.join_path(const.PATH_OUTPUT, file_name)
    utils.save_json(path, result, is_custom_class=True, prettify=True)


if __name__ == '__main__':
    main()
