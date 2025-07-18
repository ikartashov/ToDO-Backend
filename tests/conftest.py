import pytest

from resources import EntryManager, Entry

@pytest.fixture()
def entry():
    return Entry('Test Title')

@pytest.fixture()
def json_data():
    json_data = {
        "title": "Root",
        "entries": [
            {
                "title": "Child1",
                "entries": []
            },
            {
                "title": "Child2",
                "entries": [
                    {"title": "Grandchild", "entries": []}
                ]
            }
        ]
    }
    return json_data

@pytest.fixture()
def nested_entry():
    root = Entry("Root")
    # Создаем дочерние узлы
    child1 = Entry("Child1")
    child2 = Entry("Child2")
    # Создаем внука
    grandchild = Entry("Grandchild")
    # Собираем структуру
    child2.add_entry(grandchild)
    root.add_entry(child1)
    root.add_entry(child2)
    return root

@pytest.fixture()
def entry_data():
    entry_data = {
        "title": "Root",
        "entries": [
            {"title": "Child", "entries": []}
        ]
    }
    return entry_data

@pytest.fixture()
def entry_in_manager(tmp_path):
    entry_in_manager = EntryManager(str(tmp_path))
    entry_in_manager.add_entry('Test entry')
    return entry_in_manager
