import helpers
from processors import multiple_choice

SOURCE_FOLDER = 'input'
OUTPUT_FOLDER = helpers.join_path(helpers.dirname(__file__), 'jsons')

for file_name, path in helpers.scan_dir(SOURCE_FOLDER, '.txt'):
    with open(path, mode='r', encoding='utf-8') as file:
        content = ''.join(file.readlines())
    result = multiple_choice.parse(content)
    path = helpers.join_path(OUTPUT_FOLDER, file_name.split('.')[0] + '.json')
    helpers.save_json(path, result, True)