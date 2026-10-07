from models import Dish


class DishAlreadyExistsError(ValueError):
    """Блюдо с таким названием уже есть в книге."""


class DishNotFoundError(LookupError):
    """Блюда с таким названием нет в книге."""


class Cookbook:
    """Хранит блюда и управляет ими. Ничего не печатает и не спрашивает у пользователя."""

    def __init__(self, name: str, dishes=None):
        if not isinstance(name, str):
            raise TypeError(f"Название книги должно быть строкой, получено {type(name).__name__}")
        if not name.strip():
            raise ValueError("Название книги не может быть пустым")

        self.name = name
        self._dishes = {}   # {нормализованное название: Dish}

        # Начальные блюда добавляем через тот же метод add,
        # чтобы на них распространялись те же проверки
        if dishes is not None:
            for dish in dishes:
                self.add(dish)

    @staticmethod
    def _key(name: str) -> str:
        """Приводит название к единому виду: 'Борщ ' и 'борщ' - одно и то же блюдо."""
        return name.strip().lower()

    def add(self, dish: Dish) -> None:
        if not isinstance(dish, Dish):
            raise TypeError(f"В книгу можно добавить только объект Dish, получено '{dish}'")

        key = self._key(dish.name)
        if key in self._dishes:
            raise DishAlreadyExistsError(f"Блюдо '{dish.name}' уже есть в книге '{self.name}'")

        self._dishes[key] = dish

    def remove(self, name: str) -> Dish:
        """Удаляет блюдо и возвращает его (например, чтобы CLI мог написать, что именно удалено)."""
        key = self._key(name)
        if key not in self._dishes:
            raise DishNotFoundError(f"Блюда '{name}' нет в книге '{self.name}'")

        return self._dishes.pop(key)

    def get(self, name: str) -> Dish:
        key = self._key(name)
        if key not in self._dishes:
            raise DishNotFoundError(f"Блюда '{name}' нет в книге '{self.name}'")

        return self._dishes[key]

    def __contains__(self, name: str) -> bool:
        """Позволяет писать: if "Борщ" in cookbook"""
        return self._key(name) in self._dishes

    def get_all(self) -> list:
        """Возвращает копию списка блюд, чтобы снаружи нельзя было случайно испортить хранилище."""
        return list(self._dishes.values())