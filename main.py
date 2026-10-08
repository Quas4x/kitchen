from cli import KitchenCLI
from cookbook import Cookbook
from data import DISHES, INGREDIENTS


def main():
    cookbook = Cookbook(
        name="Базовая",
        dishes=DISHES[0:3]
    )
    cli = KitchenCLI(cookbook, INGREDIENTS)
    
    cli.run()

if __name__ == "__main__":
    main()
