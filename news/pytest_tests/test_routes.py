from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_news_home'),
        pytest.lazy_fixture('url_user_signup'),
        pytest.lazy_fixture('url_user_login'),
        pytest.lazy_fixture('url_user_logout'),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, url):
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_page_detail_availability(url_news_detail, client):
    response = client.get(url_news_detail)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_comment_edit'),
        pytest.lazy_fixture('url_comment_delete'),
    ),
)
def test_pages_availability_for_autor(
        parametrized_client, url, expected_status
):
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url',
    (
        pytest.lazy_fixture('url_comment_edit'),
        pytest.lazy_fixture('url_comment_delete'),
    ),
)
@pytest.mark.django_db
def test_redirects(url, url_user_login, client):
    expected_url = f'{url_user_login}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
