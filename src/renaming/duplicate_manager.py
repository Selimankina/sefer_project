class DuplicateManager:
    """
    Генерирует уникальные имена файлов, избегая дубликатов.

    Если имя уже используется, добавляет суффикс _1, _2 и т.д.
    """
    def __init__(self, existing_names=None):
        self.counts = {}
        self.used_names = set(existing_names or [])

    def get_unique_name(self, base_name: str) -> str:
        if base_name not in self.used_names:
            self.used_names.add(base_name)
            self.counts[base_name] = 1
            return base_name

        index = self.counts.get(base_name, 1)

        while True:
            new_name = f"{base_name}_{index}"
            if new_name not in self.used_names:
                self.used_names.add(new_name)
                self.counts[base_name] = index + 1
                return new_name
            index += 1