import math

from cookbook import Cookbook, DishAlreadyExistsError
from models import Dish


# Как показывать параметры пользователю
PARAM_LABELS = {
    "calories": "Калории, ккал.",
    "proteins": "Белки, г.",
    "fats": "Жиры, г.",
    "carbohydrats": "Углеводы, г.",
    "price": "Цена, у.е.",
}


class KitchenCLI:
    """Консольный интерфейс: общается с пользователем и передаёт запросы в Cookbook"""

    def __init__(self, cookbook: Cookbook, ingredients: list):
        self.cookbook = cookbook
        # Каталог для поиска ингредиента по названию без учёта регистра:
        self.ingredients = {ing.name.strip().lower(): ing for ing in ingredients}
        self.running = True
        self.commands = {
            "1": ("Показать все блюда", self.show_all_dishes),
            "2": ("Подробнее о блюде", self.show_dish),
            "3": ("Добавить блюдо", self.add_dish),
            "4": ("Удалить блюдо", self.remove_dish),
            "5": ("Показать ингредиенты", self.show_ingredients),
            "0": ("Выход", self.exit),
        }

    # ---------- Главный цикл ----------

    def run(self):
        try:
            while self.running:
                self.print_menu()
                choice = input("Выберите команду: ").strip()
                command = self.commands.get(choice)
                if command is None:
                    print("Нет такой команды\n")
                    continue

                _, action = command
                try:
                    action()
                except (ValueError, LookupError) as e:
                    print(f"Ошибка: {e}")
                print()
        except (KeyboardInterrupt, EOFError):
            # Выходим без трейсбека
            print("\nДо свидания!")

    def print_menu(self):
        print(f"=== {self.cookbook.name} ===")
        for key, (description, _) in self.commands.items():
            print(f"{key}. {description}")

    # ---------- Команды ----------

    def show_all_dishes(self):
        dishes = self.cookbook.get_all()
        if not dishes:
            print("В книге пока нет блюд")
            return
        for i, dish in enumerate(dishes, start=1):
            print(f"{i}. {dish.name} (сложность {dish.difficulty}/10)")

    def show_dish(self):
        name = input("Название блюда: ")
        dish = self.cookbook.get(name)   # если блюда нет - DishNotFoundError

        print(f"\n--- {dish.name} ---")
        print(f"Сложность: {dish.difficulty}/10")

        print("Ингредиенты:")
        for ingredient, weight in dish.ingredients.items():
            print(f"  - {ingredient.name}: {round(weight * 1000)} г")

        print("Всего в блюде:")
        for param, value in dish.count_dish_from_ingridients().items():
            label = PARAM_LABELS.get(param, param)
            print(f"  {label}: {value:.1f}")

        print(f"Способ приготовления:\n  {dish.preparation_method}")import math

from cookbook import Cookbook, DishAlreadyExistsError
from models import Dish


# Как показывать параметры пользователю
PARAM_LABELS = {
    "calories": "Калории, ккал.",
    "proteins": "Белки, г.",
    "fats": "Жиры, г.",
    "carbohydrats": "Углеводы, г.",
    "price": "Цена, у.е.",
}


class KitchenCLI:
    """Консольный интерфейс: общается с пользователем и передаёт запросы в Cookbook"""

    def __init__(self, cookbook: Cookbook, ingredients: list):
        self.cookbook = cookbook
        # Каталог для поиска ингредиента по названию без учёта регистра:
        self.ingredients = {ing.name.strip().lower(): ing for ing in ingredients}
        self.running = True
        self.commands = {
            "1": ("Показать все блюда", self.show_all_dishes),
            "2": ("Подробнее о блюде", self.show_dish),
            "3": ("Добавить блюдо", self.add_dish),
            "4": ("Удалить блюдо", self.remove_dish),
            "5": ("Показать ингредиенты", self.show_ingredients),
            "0": ("Выход", self.exit),
        }

    # ---------- Главный цикл ----------

    def run(self):
        try:
            while self.running:
                self.print_menu()
                choice = input("Выберите команду: ").strip()
                command = self.commands.get(choice)
                if command is None:
                    print("Нет такой команды\n")
                    continue

                _, action = command
                try:
                    action()
                except (ValueError, LookupError) as e:
                    print(f"Ошибка: {e}")
                print()
        except (KeyboardInterrupt, EOFError):
            # Выходим без трейсбека
            print("\nДо свидания!")

    def print_menu(self):
        print(f"=== {self.cookbook.name} ===")
        for key, (description, _) in self.commands.items():
            print(f"{key}. {description}")

    # ---------- Команды ----------

    def show_all_dishes(self):
        dishes = self.cookbook.get_all()
        if not dishes:
            print("В книге пока нет блюд")
            return
        for i, dish in enumerate(dishes, start=1):
            print(f"{i}. {dish.name} (сложность {dish.difficulty}/10)")

    def show_dish(self):
        name = input("Название блюда: ")
        dish = self.cookbook.get(name)   # если блюда нет - DishNotFoundError

        print(f"\n--- {dish.name} ---")
        print(f"Сложность: {dish.difficulty}/10")

        print("Ингредиенты:")
        for ingredient, weight in dish.ingredients.items():
            print(f"  - {ingredient.name}: {round(weight * 1000)} г")

        print("Всего в блюде:")
        for param, value in dish.count_dish_from_ingridients().items():
            label = PARAM_LABELS.get(param, param)
            print(f"  {label}: {value:.1f}")

        print(f"Способ приготовления:\n  {dish.preparation_method}")

    def add_dish(self):
        name = input("Название блюда: ").strip()
        # Проверяем сразу, чтобы пользователь не вводил всё зря
        if name in self.cookbook:
            raise DishAlreadyExistsError(f"блюдо '{name}' уже есть в книге")

        ingredients = self._ask_ingredients()
        method = input("Способ приготовления: ").strip()
        difficulty = self._ask_int("Сложность (1-10): ")

        dish = Dish(name, ingredients, method, difficulty)
        self.cookbook.add(dish)
        print(f"Блюдо '{dish.name}' добавлено")

    def remove_dish(self):
        name = input("Название блюда для удаления: ")
        removed = self.cookbook.remove(name)
        print(f"Блюдо '{removed.name}' удалено")

    def show_ingredients(self):
        for ingredient in self.ingredients.values():
            print(f"  - {ingredient.name}")

    def exit(self):
        print("До свидания!")
        self.running = False

    # ---------- Вспомогательные методы ввода ----------

    def _ask_ingredients(self) -> dict:
        """Спрашивает ингредиенты по одному, пока пользователь не введёт пустую строку"""
        print("Вводите ингредиенты по одному. Пустая строка - закончить.")
        print("Доступные: " + ", ".join(ing.name for ing in self.ingredients.values()))

        ingredients = {}
        while True:
            ing_name = input("Ингредиент: ").strip()
            if not ing_name:
                break

            ingredient = self.ingredients.get(ing_name.lower())
            if ingredient is None:
                print(f"  Ингредиента '{ing_name}' нет в каталоге, попробуйте ещё раз")
                continue

            try:
                weight = self._ask_float(f"  Вес '{ingredient.name}' в кг: ")
                if weight <= 0:
                    raise ValueError("вес должен быть больше нуля")
            except ValueError as e:
                print(f"  Ошибка: {e}, попробуйте ещё раз")
                continue

            # Если ингредиент ввели повторно - складываем веса
            ingredients[ingredient] = ingredients.get(ingredient, 0) + weight

        return ingredients

    @staticmethod
    def _ask_float(prompt: str) -> float:
        text = input(prompt).strip().replace(",", ".")   # разрешаем "0,3"
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"'{text}' - не число")
        if not math.isfinite(value):                     # float() принимает "inf" и "nan"
            raise ValueError(f"'{text}' - недопустимое значение")
        return value

    @staticmethod
    def _ask_int(prompt: str) -> int:
        text = input(prompt).strip()
        try:
            return int(text)
        except ValueError:
            raise ValueError(f"'{text}' - не целое число")
        

    def add_dish(self):
        name = input("Название блюда: ").strip()
        # Проверяем сразу, чтобы пользователь не вводил всё зря
        if name in self.cookbook:
            raise DishAlreadyExistsError(f"блюдо '{name}' уже есть в книге")

        ingredients = self._ask_ingredients()
        method = input("Способ приготовления: ").strip()
        difficulty = self._ask_int("Сложность (1-10): ")

        dish = Dish(name, ingredients, method, difficulty)   # здесь сработает валидация Dish
        self.cookbook.add(dish)
        print(f"Блюдо '{dish.name}' добавлено")

    def remove_dish(self):
        name = input("Название блюда для удаления: ")
        removed = self.cookbook.remove(name)
        print(f"Блюдо '{removed.name}' удалено")

    def show_ingredients(self):
        for ingredient in self.ingredients.values():
            print(f"  - {ingredient.name}")

    def exit(self):
        print("До свидания!")
        self.running = False

    # ---------- Вспомогательные методы ввода ----------

    def _ask_ingredients(self) -> dict:
        """Спрашивает ингредиенты по одному, пока пользователь не введёт пустую строку"""
        print("Вводите ингредиенты по одному. Пустая строка - закончить.")
        print("Доступные: " + ", ".join(ing.name for ing in self.ingredients.values()))

        ingredients = {}
        while True:
            ing_name = input("Ингредиент: ").strip()
            if not ing_name:
                break

            ingredient = self.ingredients.get(ing_name.lower())
            if ingredient is None:
                print(f"  Ингредиента '{ing_name}' нет в каталоге, попробуйте ещё раз")
                continue

            try:
                weight = self._ask_float(f"  Вес '{ingredient.name}' в кг: ")
                if weight <= 0:
                    raise ValueError("вес должен быть больше нуля")
            except ValueError as e:
                print(f"  Ошибка: {e}, попробуйте ещё раз")
                continue

            # Если ингредиент ввели повторно - складываем веса
            ingredients[ingredient] = ingredients.get(ingredient, 0) + weight

        return ingredients

    @staticmethod
    def _ask_float(prompt: str) -> float:
        text = input(prompt).strip().replace(",", ".")   # разрешаем "0,3"
        try:
            value = float(text)
        except ValueError:
            raise ValueError(f"'{text}' - не число")
        if not math.isfinite(value):                     # float() принимает "inf" и "nan"
            raise ValueError(f"'{text}' - недопустимое значение")
        return value

    @staticmethod
    def _ask_int(prompt: str) -> int:
        text = input(prompt).strip()
        try:
            return int(text)
        except ValueError:
            raise ValueError(f"'{text}' - не целое число")
        
