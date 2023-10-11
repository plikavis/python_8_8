"""
Протестируйте классы из модуля homework/models.py
"""
import pytest
from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity)
        assert product.check_quantity(product.quantity-1)
        assert not product.check_quantity(product.quantity+1)

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        count = 111
        assert product.quantity - count == product.buy(count) == product.quantity

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            count = product.quantity + 10
            return product.buy(count)


@pytest.fixture
def cart_empty():
    return Cart()


@pytest.fixture
def cart(product):
    cart = Cart()
    cart.products = {product: 3}
    return cart


@pytest.fixture
def cart_new():
    cart_new = Cart()
    cart_new.products = {Product("magazine", 10, "This is a magazine", 500): 1}
    return cart_new


@pytest.fixture
def cart_over_quantity(product):
    cart_over_quantity = Cart()
    cart_over_quantity.products = {product: product.quantity * 2}
    return cart_over_quantity


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_check_add_product_empty_cart(self, product, cart_empty):
        # Добавление в пустую корзину
        cart_empty.add_product(product)
        assert cart_empty.products == {product: 1}

    def test_cart_check_add_product_not_empty_cart(self, product, cart):
        # если в корзине уже есть сколько-то таких продуктов
        old_count = cart.products[product]
        old_products = len(cart.products)
        cart.add_product(product)
        assert old_count + 1 == cart.products[product]
        assert old_products == len(cart.products)

    def test_cart_check_add_product_not_empty_cart_new_product(self, product, cart_new):
        # корзина не пуста, добавляем новый продукт
        old_products = len(cart_new.products)
        cart_new.add_product(product)
        assert old_products + 1 == len(cart_new.products)
        assert product in cart_new.products.keys()

    def test_cart_remove_product(self, product, cart):
        """
        Удаляем единственный продукт в корзине, не указываем количество
        """
        cart.remove_product(product)
        assert cart.products == {}

    def test_card_remove_product_count(self, product, cart):
        """
        Удаляем 1 штуку, когда в корзине больше 1 шт этого продукта
        """
        old_count = cart.products[product]
        cart.remove_product(product, 1)
        assert old_count - 1 == cart.products[product]

    def test_card_remove_product_count_more_then_have(self, product, cart):
        """
        Удаляем на 1 шт продуктa больше чем есть в корзине. ОР: удаляется вся позиция
        """
        count = cart.products[product]
        cart.remove_product(product, count + 1)
        assert product not in cart.products.keys()

    def test_card_clear(self, cart):
        """
        Чистим корзину
        """
        cart.clear()
        assert cart.products == {}

    def test_card_get_total_price(self, cart):
        keys = cart.products.keys()
        price = 0.0
        for product in keys:
            price += product.price * cart.products[product]
        assert cart.get_total_price() == price

    def test_card_buy(self, cart, product):
        """
        Покупка продуктов в корзине. ОР: корзина пуста, на складе стало меньше
        """
        old_quantity = product.quantity
        value_in_cart = cart.products[product]
        cart.buy()
        assert cart.products == {}
        assert product.quantity == old_quantity - value_in_cart

    def test_card_buy_value_error(self, cart_over_quantity, product):
        """
        Если товаров не хватате на складе
        """
        with pytest.raises(ValueError):
            cart_over_quantity.buy()
