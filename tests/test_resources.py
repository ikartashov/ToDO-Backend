import json

from resources import Entry, EntryManager


class TestEntry:
    def test_add_entry(self, entry):
        entry.add_entry(entry)
        assert entry.entries
        assert entry in entry.entries

    def test_print_entries(self, entry, capfd):
        entry.add_entry(Entry('Child'))
        entry.print_entries()
        out, err = capfd.readouterr()
        assert 'Test Title' in out
        assert 'Child' in out

    def test_json(self, entry):
        res = entry.json()
        assert res['title'] == entry.title

    def test_from_json(self, json_data):
        local_entry = Entry.from_json(json_data)
        assert local_entry.title == 'Root'
        assert len(local_entry.entries) == 2
        assert local_entry.entries[1].entries[0].title == 'Grandchild'

    def test_load(self,entry_data,tmp_path):
        file_path = tmp_path/'test-entry.json'
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(entry_data,file)

        loaded_entry = Entry.load(file_path)
        assert isinstance(loaded_entry, Entry)
        assert loaded_entry.title == 'Root'

    def test_save(self, tmp_path, nested_entry):
        nested_entry.save(tmp_path)
        filepath = tmp_path / f"{nested_entry.title}.json"
        with open(filepath, 'r', encoding='utf-8') as f:
            expected_data = json.load(f)

        assert nested_entry.json() == expected_data

class TestEntryManager:
    def test_add_entry_in_entrymanager(self, entry, tmp_path):
        entry_in_manager = EntryManager(str(tmp_path))
        entry_in_manager.add_entry('Test entry')
        assert 'Test entry' == entry_in_manager.entries[0].title
        assert len(entry_in_manager.entries) == 1

    def test_save_entry_in_manager(self,entry_in_manager, tmp_path):
        entry_in_manager.save()
        filepath = tmp_path/'Test entry.json'
        assert filepath.exists(), 'Файл отсутствует'

        with open(tmp_path / 'Test entry.json', 'r', encoding='utf-8') as file:
            entry_in_folder = json.load(file)

        assert entry_in_manager.entries[0].json() == entry_in_folder

    def test_load(self,entry_in_manager,tmp_path):
        entry_in_manager.save()
        loaded_entry_manager = entry_in_manager.load()
        assert isinstance(loaded_entry_manager,EntryManager)
        entry_original = entry_in_manager.entries[0]
        entry_loaded = loaded_entry_manager.entries[0]
        assert entry_loaded == entry_original

    def test_load_if_not(self, tmp_path):
        non_exist_dir = tmp_path/'non_exist_dir'
        assert not non_exist_dir.exists()
        manager = EntryManager(str(non_exist_dir))
        manager.load()
        assert non_exist_dir.exists()
        assert non_exist_dir.is_dir()

















