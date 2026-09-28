"""Pruebas principales de SauceDemo.

Cada prueba abre su propio navegador y no usa el estado de otra.
"""

import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.login
def test_login_con_usuario_valido_muestra_inventario(driver, base_url, credentials):
    """Con los datos correctos se entra al inventario."""
    LoginPage(driver).open(base_url).login(credentials["username"], credentials["password"])

    inventory = InventoryPage(driver).wait_until_loaded()
    assert "/inventory.html" in driver.current_url
    assert inventory.product_names()


@pytest.mark.catalog
def test_catalogo_muestra_lista_nombre_y_precio(logged_driver):
    """Cada producto tiene nombre y precio."""
    inventory = InventoryPage(logged_driver).wait_until_loaded()
    names = inventory.product_names()
    prices = inventory.product_prices()

    assert len(names) >= 1
    assert len(names) == len(prices)
    assert all(name.strip() for name in names)
    assert all(price.startswith("$") for price in prices)


@pytest.mark.catalog
def test_catalogo_contiene_productos_esperados(logged_driver):
    """Se revisan dos productos que tienen que estar en la lista."""
    inventory = InventoryPage(logged_driver).wait_until_loaded()
    names = inventory.product_names()

    assert "Sauce Labs Backpack" in names
    assert "Sauce Labs Bike Light" in names


@pytest.mark.cart
def test_agregar_producto_muestra_el_item_correcto_en_carrito(logged_driver):
    """El producto agregado aparece en el carrito."""
    product = "Sauce Labs Backpack"
    InventoryPage(logged_driver).wait_until_loaded().add_product(product).cart()

    cart = CartPage(logged_driver).wait_until_loaded()
    assert cart.product_names() == [product]
    assert len(cart.product_prices()) == 1
    assert cart.product_prices()[0].startswith("$")
