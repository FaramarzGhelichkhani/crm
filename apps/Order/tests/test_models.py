import pytest
from apps.EmdadUser.models import Technician, CustomUser
from apps.Emdad.models import Service, Motor
from apps.Order.models import Order, Followup


@pytest.fixture
def service():
    return Service.objects.create(name="Service 1")


@pytest.fixture
def motor():
    return Motor.objects.create(brand="Motor 1")


@pytest.fixture
def customer():
    return CustomUser.objects.create(phone="+989126736308", password='password')


@pytest.fixture
def technician(customer):
    tech_data = {
        'user': customer,
        'id_card': '1234567890',
        'address': 'Test Address',
        'commission': 0.2,
        'balance': 100,
        'time_shift': 'Day Shift',
        'activation_status': 1,
        'avatar': None
    }
    return Technician.objects.create(**tech_data)


@pytest.fixture
def order(technician):
    return Order.objects.create(
        address="Test Address",
        customer_phone="1234567890",
        customer_full_name="Test Customer",
        technician=technician,
        wage=100,
        comment="Test Comment"
    )


@pytest.mark.django_db
def test_order_creation(order, service, motor, technician):
    order.services.add(service)
    order.motors.add(motor)

    assert Order.objects.count() == 1
    assert order.services.count() == 1
    assert order.motors.count() == 1
    assert order.customer_full_name == "Test Customer"
    assert order.technician == technician
    assert order.wage == 100


@pytest.mark.django_db
def test_followup_creation(order, customer):
    followup = Followup.objects.create(
        order=order,
        user=customer,
        total_price_cusotmer=200,
        total_wage_agent=50,
        grade=4
    )

    assert Followup.objects.count() == 1
    assert followup.order == order
    assert followup.user == customer
    assert followup.total_price_cusotmer == 200
    assert followup.total_wage_agent == 50
    assert followup.grade == 4
