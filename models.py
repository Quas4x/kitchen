class Dish:
    def __init__(self, name: str, ingridients: list, preparation_method: str, difficulty: int):
        self.name = name
        self.ingridients = ingridients      # Ингридиенты, их кол-во, кбжу и цена каждого
        self.preparation_method = preparation_method
        self.difficulty = difficulty        # Сложность приготоволения от 1 до 10

    def sum_of_cpfc(self):
        cpfc_sum = 0
        for i in self.ingridients:
            



class Ingridient:
    def __init__(self, name: str, cpfc: dict, price: int):
        self.name = name
        self.cpfc = cpfc
        self.price = price


# Разделить cpfc!
