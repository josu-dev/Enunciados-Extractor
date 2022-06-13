import helpers
from statements import multiple_choice

SOURCE_FOLDER = 'pdfs'
OUTPUT_FOLDER = helpers.join_path(helpers.dirname(__file__), 'jsons')

for file_name, path in helpers.scan_dir(SOURCE_FOLDER, '.text'):
    with open(path, mode='r', encoding='utf-8') as file:
        content = ''.join(file.readlines())
    result = multiple_choice.parse(content)
    path = helpers.join_path(OUTPUT_FOLDER, file_name.split('.')[0] + '.json')
    helpers.save_json(path, result, True)