from collections import defaultdict


class DuplicateManager:
    def __init__(self):
        self.counter = defaultdict(int)

    def get_unique_name(self, base_name: str) -> str:
        """
        Добавляет _1, _2 и т.д. если имя уже встречалось.
        """
        name, ext = base_name.rsplit('.', 1)

        count = self.counter[name]

        if count == 0:
            self.counter[name] += 1
            return base_name

        new_name = f"{name}_{count}.{ext}"
        self.counter[name] += 1

        return new_name