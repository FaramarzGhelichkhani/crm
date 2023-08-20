import pytest
from apps.Transaction.models import Transaction
from apps.EmdadUser.models import CustomUser, Technician
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


@pytest.fixture
def user_data():
    return {
        'phone': '+989123456789',
        'email': 'user@example.com',
        'password': 'password',

    }


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


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_user_detail_view(technician_data, client: APIClient):
    technician = Technician.objects.create(**technician_data)
    Transaction.objects.create(technician=technician, amount=100000)

    token, _ = Token.objects.get_or_create(user=technician.user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    url = reverse('transaction:transactions-list_app')
    response = client.get(url, format='json')
    print(response.data[0]['amount'])
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]['amount'] == 100000
    assert response.data[0]['technician'] == technician.id
