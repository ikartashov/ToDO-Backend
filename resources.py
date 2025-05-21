import json
import os


def print_with_indent(value, indent=0):
    indention = '\t' * indent
    print(indention + str(value))


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def add_entry(self, title: str):
        self.entries.append(Entry(title))

    def save(self):
        for item in self.entries:
            item.save(self.data_path)

    def load(self):
        if not os.path.isdir(self.data_path):
            os.makedirs(self.data_path)
        else:
            for item in os.listdir(self.data_path):
                if item.endswith('json'):
                    entry = Entry.load(os.path.join(self.data_path, item))
                    self.entries.append(entry)
        return self


class Entry:
    def __init__(self, title, entries=None, parent=None):
        if entries is None:
            entries = []
        self.title = title
        self.entries = entries
        self.parent = parent

    @classmethod
    def from_json(cls, value: dict):
        new_entry = cls(value['title'])
        for item in value.get('entries', []):
            new_entry.add_entry(cls.from_json(item))
        return new_entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            content = json.load(file)
            return cls.from_json(content)

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        filename = os.path.join(path, self.title)
        content = self.json()
        with open(f'{filename}.json', 'w', encoding='utf-8') as file:
            json.dump(content, file)

    def __str__(self):
        return self.title
