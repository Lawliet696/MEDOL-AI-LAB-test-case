import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app

t_login = 'TestUser'
t_password = 'password'

#Первичная регистрация
@pytest.mark.asyncio
async def test_registration():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post(
            "/register",
            json={"username": t_login, "password": t_password}
        )
        assert response.status_code == 201

#Аутентификация
@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post(
            "/login",
            json={"username": t_login, "password": t_password}
        )
        assert response == 200

#Регистрация уже существующего пользователя
@pytest.mark.asyncio
async def test_registration_repeat():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        response = await ac.post(
            "/register",
            json={"username": t_login, "password": t_password}
        )
        assert response.status_code == 400
