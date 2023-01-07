import pytest

from app import app


def test_app_all_posts():
    response = app.test_client().get('/api/posts', follow_redirects=True)
    assert response.status_code == 200, "Статус код запроса всех постов неверный"
    assert type(response.json) == list, "Получен не список"


def test_app_check_keys():
    keys = {"post_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}

    response = app.test_client().get('/api/posts/1', follow_redirects=True)
    first_keys = set(response.json.keys())
    assert keys == first_keys, "Ключи не совпадают"
