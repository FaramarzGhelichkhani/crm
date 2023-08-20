import pytest
from apps.EmdadUser.models import CustomUser, Technician


@pytest.fixture
def user_data():
    return {
        'phone': '+989123456789',
        'email': 'user@example.com',
        'password': 'password',

    }


@pytest.mark.django_db
def test_custom_user_creation(user_data):
    user = CustomUser.objects.create(**user_data)

    assert CustomUser.objects.count() == 1
    assert user.phone == user_data['phone']
    assert user.email == user_data['email']
    assert user.is_authenticated is True
    # assert user.check_password(user_data['password'])


@pytest.fixture
def technician_data(user_data):
    return {
        'user': CustomUser.objects.create(**user_data),
        'id_card': '1234567890',
        'address': 'Test Address',
        'commission': 0.2,
        'balance': 100,
        'time_shift': 'Day Shift',
        'activation_status': 1,
        'avatar': None
    }


@pytest.mark.django_db
def test_technician_creation(technician_data):
    technician = Technician.objects.create(**technician_data)

    assert Technician.objects.count() == 1
    assert technician.user.phone == technician_data['user'].phone
    assert technician.id_card == technician_data['id_card']
    assert technician.address == technician_data['address']
    assert technician.commission == technician_data['commission']
    assert technician.balance == technician_data['balance']
    assert technician.time_shift == technician_data['time_shift']
    assert technician.activation_status == technician_data['activation_status']
    assert technician.avatar == technician_data['avatar']
