class Dish:
    def __init__(
            self,
            name: str,
            ingredients: dict,
            preparation_method: str,
            difficulty: int
    ):
        self.name = name
        self.ingredients = ingredients      # Ингридиенты и их кол-во
        self.preparation_method = preparation_method
        self.difficulty = difficulty        # Сложность приготоволения от 1 до 10

    def count_dish_from_ingridients(self):
        count_of_dish = {}
        for ingridient, weight in self.ingredients.items():
            count_of_ingridient = ingridient.count_param_for_proportions(weight)
            for param, value in count_of_ingridient.items():
                count_of_dish[param] = count_of_dish.get(param, 0) + value

        return count_of_dish


class Ingredient:
    "Ингридиенты - их названия, кбжу и цена каждого (расчет на 100г)"
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

    def count_param_for_proportions(self, weight: float):
        "Считаем все параметры ингредиента пропорционально его массе в блюде (масса в кг)"
        count_of_element = {}
        for param, value in vars(self).items():
            if isinstance(value, (int, float)):
                # Значения заданы на 100 г, масса в кг: 1 кг = 10 * 100 г
                count_of_element[param] = value * 10 * weight

        return count_of_element
