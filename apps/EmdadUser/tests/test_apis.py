from django.urls import reverse
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.mark.django_db
def test_validate_credentials(client):
    url = '/en/crm/motor/agents/credentials/'
    user = User.objects.create_user(phone='testuser', password='testpassword')

    data = {'phone': 'testuser', 'password': 'testpassword'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'token' in response.data


@pytest.mark.django_db
def test_invalid_credentials(client):
    url = '/en/crm/motor/agents/credentials/'
    data = {'phone': 'invaliduser', 'password': 'invalidpassword'}
    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'error' in response.data


@pytest.mark.django_db
def test_user_detail_view(client):
    user = User.objects.create_user(phone='testuser', password='testpassword')

    token, _ = Token.objects.get_or_create(user=user)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('agents:user-info')
    response = client.get(url, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data['phone'] == 'testuser'
