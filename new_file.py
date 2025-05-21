import os

from resources import Entry


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





