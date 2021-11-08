import pytest
from django.urls import reverse


# проверка получения 1го курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data['id'] == course.id


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses_list(client, course_factory):
    course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


# проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_filtered_course_by_id(client, course_factory):
    course = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url, data={'id': course[1].id})
    assert response.status_code == 200
    assert response.data[0]['id'] == course[1].id
    assert len(response.data) == 1


# проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_filtered_course_by_name(client, course_factory):
    course = course_factory(_quantity=5)
    url = reverse('courses-list')
    response = client.get(url, data={'name': course[1].name})
    assert response.status_code == 200
    assert response.data[0]['name'] == course[1].name
    assert len(response.data) == 1


# тест успешного создания курса
@pytest.mark.django_db
def test_create_a_course(client):
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'basic'})
    assert response.status_code == 201


# тест успешного обновления курса
@pytest.mark.django_db
def test_update_a_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = client.put(url, data={'name': 'simple course'})
    assert response.status_code == 200
    assert response.data["name"] == 'simple course'


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_a_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-detail', args=[course.id])
    response = client.delete(url)
    assert response.status_code == 204