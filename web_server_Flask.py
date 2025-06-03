from flask import Flask
from resources import Entry
from pathlib import Path
from resources import EntryManager

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


FOLDER = Path('/Users/ikartashov/Python/toDoList')


@app.route('/api/entries/')
def get_entries():
    entries_list_of_json = []
    new_entries = EntryManager(FOLDER)
    new_entries.load()
    for item in new_entries.entries:
        entries_list_of_json.append(item.json())
    return entries_list_of_json


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
