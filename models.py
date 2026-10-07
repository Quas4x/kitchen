def is_number(value) -> bool:
    """Проверяет, что значение - int или float, но не bool."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class Ingredient:
    """Ингредиент: название, КБЖУ и цена (все значения на 100 г)."""

    # Явный список полей, которые пересчитываются пропорционально массе
    NUMERIC_PARAMS = ("calories", "proteins", "fats", "carbohydrats", "price")

    def __init__(
            self,
            name: str,
            calories: float,
            proteins: float,
            fats: float,
            carbohydrats: float,
            price: float,
    ):
        self.name = name
        self.calories = calories
        self.proteins = proteins
        self.fats = fats
        self.carbohydrats = carbohydrats
        self.price = price

        self.__validate()

    def __validate(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Название ингредиента должно быть строкой, получено {type(self.name).__name__}")
        if not self.name.strip():
            raise ValueError("Название ингредиента не может быть пустым")

        for param in self.NUMERIC_PARAMS:
            value = getattr(self, param)
            if not is_number(value):
                raise TypeError(
                    f"Поле {param} ингредиента '{self.name}' должно быть числом, получено {value!r}"
                )
            if value < 0:
                raise ValueError(
                    f"Поле {param} ингредиента '{self.name}' не может быть отрицательным, получено {value}"
                )

    def count_param_for_proportions(self, weight: float) -> dict:
        """Считает все параметры ингредиента пропорционально его массе (масса в кг)."""
        count_of_element = {}
        for param in self.NUMERIC_PARAMS:
            # Значения заданы на 100 г, масса в кг: 1 кг = 10 * 100 г
            count_of_element[param] = getattr(self, param) * 10 * weight

        return count_of_element


class Dish:
    def __init__(
            self,
            name: str,
            ingredients: dict,
            preparation_method: str,
            difficulty: int
    ):
        self.name = name
        self.ingredients = ingredients      # {Ingredient: масса в кг}
        self.preparation_method = preparation_method
        self.difficulty = difficulty        # Сложность приготовления от 1 до 10

        self.__validate()

    def __validate(self):
        if not isinstance(self.name, str):
            raise TypeError(f"Название блюда должно быть строкой, получено {type(self.name).__name__}")
        if not self.name.strip():
            raise ValueError("Название блюда не может быть пустым")

        if not isinstance(self.preparation_method, str):
            raise TypeError(
                f"Способ приготовления блюда '{self.name}' должен быть строкой, "
                f"получено {type(self.preparation_method).__name__}"
            )

        if isinstance(self.difficulty, bool) or not isinstance(self.difficulty, int):
            raise TypeError(f"Сложность блюда '{self.name}' должна быть целым числом, получено {self.difficulty!r}")
        if not 1 <= self.difficulty <= 10:
            raise ValueError(f"Сложность блюда '{self.name}' должна быть от 1 до 10, получено {self.difficulty}")

        if not isinstance(self.ingredients, dict):
            raise TypeError(
                f"Ингредиенты блюда '{self.name}' должны быть словарём, "
                f"получено {type(self.ingredients).__name__}"
            )
        if not self.ingredients:
            raise ValueError(f"В блюде '{self.name}' должен быть хотя бы один ингредиент")

        for ingredient, weight in self.ingredients.items():
            if not isinstance(ingredient, Ingredient):
                raise TypeError(
                    f"Ключами в ингредиентах блюда '{self.name}' должны быть объекты Ingredient, получено {ingredient!r}"
                )
            if not is_number(weight):
                raise TypeError(
                    f"Вес ингредиента '{ingredient.name}' в блюде '{self.name}' должен быть числом, получено {weight!r}"
                )
            if weight <= 0:
                raise ValueError(
                    f"Вес ингредиента '{ingredient.name}' в блюде '{self.name}' должен быть больше нуля, получено {weight}"
                )

    def count_dish_from_ingridients(self) -> dict:
        """Суммирует параметры всех ингредиентов блюда с учётом их массы."""
        count_of_dish = {}
        for ingredient, weight in self.ingredients.items():
            count_of_ingredient = ingredient.count_param_for_proportions(weight)
            for param, value in count_of_ingredient.items():
                count_of_dish[param] = count_of_dish.get(param, 0) + value

        return count_of_dish