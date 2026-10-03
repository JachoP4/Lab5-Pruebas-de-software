from shop import Order
from shop import OrderService
from shop import CONFIG
import pytest

@pytest.mark.sys
def test_order_normal():
    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        },
        {
            "name": "Mouse",
            "price": 300,
            "quantity": 1
        }
    ]

    order = Order(products)
    service = OrderService(CONFIG)
    #order_processed = service.process_order(order)
    result = service.calculate_total(order)
    #assert order_processed['payment']['status'] == 'approved'
    assert result["subtotal"] == 1100
    assert result["discount"] == 110
    assert result["tax"] == 158.4
    assert result["total"] == 1148.4

@pytest.mark.sys
def test_order_normal_monkey_patch_setattr(monkeypatch):
    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]

    class SusPaymentGateway:
            def charge(self, amount):
                return  {
                    "status": "approved",
                    "transaction_id": "FAKE-001",
                    "amount": amount
                    }

    order = Order(products)
    service = OrderService(CONFIG)
    monkeypatch.setattr(service, 'payment_gateway', SusPaymentGateway())
    order_processed = service.process_order(order)
    assert order_processed['payment']['status'] == 'approved'

@pytest.mark.fix
def test_order_normal_monkey_patch_setitem(monkeypatch):
    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]

    order = Order(products)
    service = OrderService(CONFIG)
    monkeypatch.setitem(CONFIG, 'tax_rate', 0.2)
    order_processed = service.process_order(order)
    result= service.calculate_total(order)
    assert result["subtotal"] == 800
    assert result["discount"] == 40
    assert result["tax"] == 152
    assert result["total"] == 912

@pytest.mark.wip
def test_order_normal_monkey_patch_delattr(monkeypatch):
    products = [
        {
            "name": "Teclado",
            "price": 800,
            "quantity": 1
        }
    ]

    order = Order(products)
    service = OrderService(CONFIG)
    monkeypatch.delattr(service, 'discount_service')
    order_processed = service.process_order(order)
    result= service.calculate_total(order)
    assert order_processed['payment']['status'] == 'approved'
    assert result["subtotal"] == 800
    assert result["discount"] == 0
    assert result["tax"] == 128
    assert result["total"] == 928