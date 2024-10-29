import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from bot.models import ChatSession, Message
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def chat_session(user):
    return ChatSession.objects.create(user=user, topic="Test Session")


@pytest.fixture
def message(chat_session):
    return Message.objects.create(
        session=chat_session, role="user", content="Test message", temperature=0.5
    )


@pytest.mark.django_db
def test_list_all_sessions(auth_client, chat_session):
    url = reverse("sessions-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_session(auth_client, chat_session):
    url = reverse("sessions-detail", args=[chat_session.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["topic"] == chat_session.topic


@pytest.mark.django_db
def test_create_session(auth_client, user):
    url = reverse("sessions-create")
    data = {"user": user, "topic": "New Session"}
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["topic"] == "New Session"


@pytest.mark.django_db
def test_create_question(auth_client, chat_session):
    url = reverse("message-create")
    data = {
        "session": chat_session.id,
        "role": "user",
        "content": "New question",
        "temperature": 0.5,
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["content"] == "New question"
