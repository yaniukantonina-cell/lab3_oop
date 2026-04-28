import functools
from typing import Optional

class Cosmetics:
    """
    Клас, що представляє косметичний продукт.

    Поля:
        name (str):        Назва продукту.
        brand (str):       Бренд виробника.
        price (float):     Ціна продукту у гривнях.
        volume_ml (int):   Об'єм продукту у мілілітрах.
        rating (float):    Рейтинг продукту (від 1.0 до 5.0).
    """

    def __init__(self, name: str, brand: str, price: float, volume_ml: int, rating: float):
        """
        Ініціалізує об'єкт Cosmetics із заданими полями.

        Args:
            name (str):        Назва косметичного продукту.
            brand (str):       Назва бренду.
            price (float):     Ціна у гривнях (має бути > 0).
            volume_ml (int):   Об'єм у мілілітрах (має бути > 0).
            rating (float):    Рейтинг від 1.0 до 5.0.
        """
        self.name = name
        self.brand = brand
        self.price = price
        self.volume_ml = volume_ml
        self.rating = rating

    def __eq__(self, other: object):
        """
        Порівнює два об'єкти Cosmetics на повну ідентичність.

        Args:
            other (object): Об'єкт для порівняння.

        Returns:
            bool: True, якщо всі поля обох об'єктів збігаються, інакше False.
        """

        if not isinstance(other, Cosmetics):
            return False
        return (
            self.name == other.name
            and self.brand == other.brand
            and self.price == other.price
            and self.volume_ml == other.volume_ml
            and self.rating == other.rating
        )

    def __repr__(self):
        """
        Повертає рядкове представлення об'єкта для зручного виведення.

        Returns:
            str: Рядок із усіма полями об'єкта.
        """
        return (
            f"Cosmetics("
            f"name='{self.name}', "
            f"brand='{self.brand}', "
            f"price={self.price:.2f} грн, "
            f"volume={self.volume_ml} мл, "
            f"rating={self.rating})"
        )

def compare_logic(a: Cosmetics, b: Cosmetics):
    """
    Компаратор для сортування масиву об'єктів Cosmetics.

    Порівнює за полем "price" за зростанням (перше поле).
    Якщо "price" однакова — порівнює за полем "rating" за спаданням.

    Args:
        a (Cosmetics): Перший об'єкт для порівняння.
        b (Cosmetics): Другий об'єкт для порівняння.

    Returns:
        int: Від'ємне число, якщо a < b; 0, якщо a == b; додатне, якщо a > b.
    """

    if a.price != b.price:
        return -1 if a.price < b.price else 1

    if a.rating != b.rating:
        return -1 if a.rating > b.rating else 1

    return 0

def find_identical(array: list[Cosmetics], target: Cosmetics):
    """
    Шукає в масиві об'єкт, ідентичний заданому ("target").

    Args:
        array (list[Cosmetics]): Масив об'єктів Cosmetics для пошуку.
        target (Cosmetics):      Об'єкт-еталон, який потрібно знайти.

    Returns:
        Optional[int]: Індекс першого знайденого ідентичного об'єкта,
                       або None, якщо такого не знайдено.
    """

    for index, item in enumerate(array):
        if item == target:
            return index
    return None

def print_array(label: str, array: list[Cosmetics]):
    """
    Виводить масив об'єктів Cosmetics з підписом.

    Args:
        label (str):              Підпис для виведення.
        array (list[Cosmetics]):  Масив для виведення.
    """

    print(f" \n{label}\n")
    for i, item in enumerate(array):
        print(f"  [{i}] {item}")


def main():
    """
    Виконавчий метод — точка входу програми.

    Створює масив із 8-и об'єктів класу Cosmetics.
    Сортує масив за ціною (зростання) та рейтингом (спадання).
    Шукає в масиві об'єкт, ідентичний заданому еталону.
    """

    cosmetics_array: list[Cosmetics] = [
        Cosmetics("Крем для обличчя",  "L'Oréal",   320.00, 50,  4.5),
        Cosmetics("Тональний засіб",   "Maybelline", 280.00, 30,  4.2),
        Cosmetics("Сироватка",         "The Ordinary", 450.00, 30, 4.8),
        Cosmetics("Помада",            "MAC",         280.00, 10,  4.7),
        Cosmetics("Туш для вій",      "Essence",     120.00, 12,  3.9),
        Cosmetics("Пудра",             "NYX",         320.00, 15,  4.1),
        Cosmetics("Консилер",          "Rimmel",      199.00,  8,  4.3),
        Cosmetics("Масло для губ",     "Essence",     120.00, 10,  4.6),
    ]

    print_array("ПОЧАТКОВИЙ МАСИВ", cosmetics_array)

    sorted_array: list[Cosmetics] = sorted(
        cosmetics_array,
        key=functools.cmp_to_key(compare_logic),
    )

    print_array("ВІДСОРТОВАНИЙ МАСИВ", sorted_array)

    target: Cosmetics = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)

    print(f"\nПОШУК ІДЕНТИЧНОГО ОБ'ЄКТА")
    print(f"  Еталон: {target}")

    found_index: Optional[int] = find_identical(sorted_array, target)

    if found_index is not None:
        print(f"  Знайдено на індексі [{found_index}]: {sorted_array[found_index]}")
    else:
        print("  Ідентичного об'єкта не знайдено.")

if __name__ == "__main__":
    main()