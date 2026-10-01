class Dish:
    def __init__(
            self,
            name: str,
            ingredients: dict,
            preparation_method: str,
            difficulty: int
    ):
        self.name = name
        self.ingredients = ingredients      # Ингридиенты, их кол-во, кбжу и цена каждого
        self.preparation_method = preparation_method
        self.difficulty = difficulty        # Сложность приготоволения от 1 до 10

    def count_param_for_proportions(self, element: str):
        count_of_element = 0
        for i in self.ingredients:
            count_of_element += getattr(i, element) * (self.ingredients[i] / 100 ) # Умножаем параметр ингридиента на его массу (в кг) в данном блюде

        return count_of_element


class Ingredient:
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
