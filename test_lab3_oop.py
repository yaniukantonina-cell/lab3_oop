import functools
import pytest
from lab3_oop import Cosmetics, compare_logic, find_identical, print_array


# ─────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────

@pytest.fixture
def sample_array():
    """Базовий масив із 8 косметичних продуктів (такий самий, як у main)."""
    return [
        Cosmetics("Крем для обличчя",  "L'Oréal",      320.00, 50, 4.5),
        Cosmetics("Тональний засіб",   "Maybelline",    280.00, 30, 4.2),
        Cosmetics("Сироватка",         "The Ordinary",  450.00, 30, 4.8),
        Cosmetics("Помада",            "MAC",           280.00, 10, 4.7),
        Cosmetics("Туш для вій",       "Essence",       120.00, 12, 3.9),
        Cosmetics("Пудра",             "NYX",           320.00, 15, 4.1),
        Cosmetics("Консилер",          "Rimmel",        199.00,  8, 4.3),
        Cosmetics("Масло для губ",     "Essence",       120.00, 10, 4.6),
    ]


# ─────────────────────────────────────────────
# Cosmetics.__init__ / поля
# ─────────────────────────────────────────────

class TestCosmeticsInit:
    def test_fields_are_set_correctly(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert c.name      == "Помада"
        assert c.brand     == "MAC"
        assert c.price     == 280.00
        assert c.volume_ml == 10
        assert c.rating    == 4.7

    def test_zero_price_is_stored(self):
        """Клас сам не валідує ціну — перевіряємо, що зберігає як є."""
        c = Cosmetics("Test", "Brand", 0.0, 50, 3.0)
        assert c.price == 0.0

    def test_float_price_precision(self):
        c = Cosmetics("Test", "Brand", 99.99, 100, 5.0)
        assert c.price == pytest.approx(99.99)


# ─────────────────────────────────────────────
# Cosmetics.__eq__
# ─────────────────────────────────────────────

class TestCosmeticsEq:
    def test_equal_objects(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        b = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert a == b

    def test_different_name(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        b = Cosmetics("Тіні",   "MAC", 280.00, 10, 4.7)
        assert a != b

    def test_different_brand(self):
        a = Cosmetics("Помада", "MAC",       280.00, 10, 4.7)
        b = Cosmetics("Помада", "Maybelline", 280.00, 10, 4.7)
        assert a != b

    def test_different_price(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        b = Cosmetics("Помада", "MAC", 300.00, 10, 4.7)
        assert a != b

    def test_different_volume(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        b = Cosmetics("Помада", "MAC", 280.00, 20, 4.7)
        assert a != b

    def test_different_rating(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        b = Cosmetics("Помада", "MAC", 280.00, 10, 4.0)
        assert a != b

    def test_not_equal_to_non_cosmetics(self):
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert a != "Помада"
        assert a != 42
        assert a != None


# ─────────────────────────────────────────────
# Cosmetics.__repr__
# ─────────────────────────────────────────────

class TestCosmeticsRepr:
    def test_repr_contains_name(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert "Помада" in repr(c)

    def test_repr_contains_brand(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert "MAC" in repr(c)

    def test_repr_contains_price_formatted(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert "280.00" in repr(c)

    def test_repr_contains_volume(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert "10" in repr(c)

    def test_repr_contains_rating(self):
        c = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert "4.7" in repr(c)


# ─────────────────────────────────────────────
# compare_logic
# ─────────────────────────────────────────────

class TestCompareLogic:
    def test_lower_price_comes_first(self):
        a = Cosmetics("A", "X", 100.00, 10, 4.0)
        b = Cosmetics("B", "X", 200.00, 10, 4.0)
        assert compare_logic(a, b) < 0

    def test_higher_price_comes_last(self):
        a = Cosmetics("A", "X", 500.00, 10, 4.0)
        b = Cosmetics("B", "X", 100.00, 10, 4.0)
        assert compare_logic(a, b) > 0

    def test_same_price_higher_rating_comes_first(self):
        a = Cosmetics("A", "X", 280.00, 10, 4.7)
        b = Cosmetics("B", "X", 280.00, 10, 4.2)
        # a має вищий рейтинг → повинна стояти раніше → compare < 0
        assert compare_logic(a, b) < 0

    def test_same_price_lower_rating_comes_last(self):
        a = Cosmetics("A", "X", 280.00, 10, 3.5)
        b = Cosmetics("B", "X", 280.00, 10, 4.9)
        assert compare_logic(a, b) > 0

    def test_same_price_same_rating_returns_zero(self):
        a = Cosmetics("A", "X", 280.00, 10, 4.5)
        b = Cosmetics("B", "Y", 280.00, 20, 4.5)
        assert compare_logic(a, b) == 0

    def test_sorting_order_price_ascending(self, sample_array):
        sorted_arr = sorted(sample_array, key=functools.cmp_to_key(compare_logic))
        prices = [c.price for c in sorted_arr]
        assert prices == sorted(prices)

    def test_sorting_tie_break_rating_descending(self):
        """Продукти з однаковою ціною мають стояти за спаданням рейтингу."""
        items = [
            Cosmetics("A", "X", 280.00, 10, 4.2),
            Cosmetics("B", "X", 280.00, 10, 4.7),
            Cosmetics("C", "X", 280.00, 10, 4.0),
        ]
        sorted_items = sorted(items, key=functools.cmp_to_key(compare_logic))
        ratings = [c.rating for c in sorted_items]
        assert ratings == sorted(ratings, reverse=True)

    def test_full_sort_first_element_cheapest(self, sample_array):
        sorted_arr = sorted(sample_array, key=functools.cmp_to_key(compare_logic))
        assert sorted_arr[0].price == min(c.price for c in sample_array)

    def test_full_sort_last_element_most_expensive(self, sample_array):
        sorted_arr = sorted(sample_array, key=functools.cmp_to_key(compare_logic))
        assert sorted_arr[-1].price == max(c.price for c in sample_array)


# ─────────────────────────────────────────────
# find_identical
# ─────────────────────────────────────────────

class TestFindIdentical:
    def test_finds_existing_object(self, sample_array):
        target = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        idx = find_identical(sample_array, target)
        assert idx is not None
        assert sample_array[idx] == target

    def test_returns_none_when_not_found(self, sample_array):
        target = Cosmetics("Невідомий продукт", "NoName", 999.00, 999, 1.0)
        assert find_identical(sample_array, target) is None

    def test_finds_first_occurrence(self):
        """Якщо є дублікати — повертає індекс першого."""
        a = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        arr = [
            Cosmetics("Крем", "L'Oréal", 100.00, 50, 4.0),
            Cosmetics("Помада", "MAC", 280.00, 10, 4.7),
            Cosmetics("Помада", "MAC", 280.00, 10, 4.7),
        ]
        assert find_identical(arr, a) == 1

    def test_empty_array_returns_none(self):
        target = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        assert find_identical([], target) is None

    def test_single_element_match(self):
        c = Cosmetics("Сироватка", "The Ordinary", 450.00, 30, 4.8)
        assert find_identical([c], c) == 0

    def test_single_element_no_match(self):
        c = Cosmetics("Сироватка", "The Ordinary", 450.00, 30, 4.8)
        other = Cosmetics("Крем", "L'Oréal", 320.00, 50, 4.5)
        assert find_identical([c], other) is None

    def test_finds_in_sorted_array(self, sample_array):
        """Пошук після сортування — основний сценарій з main()."""
        sorted_arr = sorted(sample_array, key=functools.cmp_to_key(compare_logic))
        target = Cosmetics("Помада", "MAC", 280.00, 10, 4.7)
        idx = find_identical(sorted_arr, target)
        assert idx is not None
        assert sorted_arr[idx] == target

    def test_partial_match_is_not_found(self, sample_array):
        """Об'єкт із зміненою лише ціною не вважається ідентичним."""
        target = Cosmetics("Помада", "MAC", 999.00, 10, 4.7)
        assert find_identical(sample_array, target) is None


# ─────────────────────────────────────────────
# print_array (smoke-test через capsys)
# ─────────────────────────────────────────────

class TestPrintArray:
    def test_label_appears_in_output(self, capsys, sample_array):
        print_array("ТЕСТ ВИВОДУ", sample_array)
        captured = capsys.readouterr()
        assert "ТЕСТ ВИВОДУ" in captured.out

    def test_all_items_appear_in_output(self, capsys, sample_array):
        print_array("МАСИВ", sample_array)
        captured = capsys.readouterr()
        for item in sample_array:
            assert item.name in captured.out

    def test_indices_shown(self, capsys, sample_array):
        print_array("МАСИВ", sample_array)
        captured = capsys.readouterr()
        assert "[0]" in captured.out
        assert f"[{len(sample_array) - 1}]" in captured.out

    def test_empty_array_no_crash(self, capsys):
        print_array("ПОРОЖНІЙ", [])
        captured = capsys.readouterr()
        assert "ПОРОЖНІЙ" in captured.out