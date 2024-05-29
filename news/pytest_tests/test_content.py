import pytest
from django.conf import settings


@pytest.mark.django_db
def test_news_count(extra_eleven_news, url_news_home, client):
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(extra_eleven_news, url_news_home, client, news):
    response = client.get(url_news_home)
    object_list = response.context['object_list']
    all_date = [news.date for news in object_list]
    sorted_date = sorted(all_date, reverse=True)
    assert all_date == sorted_date


@pytest.mark.django_db
def test_comments_order(news_with_ten_comments, url_news_detail, client):
    response = client.get(url_news_detail)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    for i in range(all_comments.count() - 1):
        if all_comments[i].created > all_comments[i + 1].created:
            assert False, 'Комментарии отсортированы не правильно'


@pytest.mark.django_db
def test_authorized_client_has_form(url_news_detail, author_client):
    response = author_client.get(url_news_detail)
    assert 'form' in response.context
    assert type(response.context['form']).__name__ == 'CommentForm'


@pytest.mark.django_db
def test_anonymous_client_hasnt_form(url_news_detail, client):
    response = client.get(url_news_detail)
    assert 'form' not in response.context
