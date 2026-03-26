import pytest
from django.urls import reverse
from rest_framework import status
from students.models import Course, Student


@pytest.mark.django_db
class TestCoursesAPI:

    def test_retrieve_course(self, api_client, course_factory):
        """Проверка получения первого курса"""
        course = course_factory(name="Python разработка")

        url = reverse('courses-detail', args=[course.id])
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == course.id
        assert response.data['name'] == course.name

    def test_list_courses(self, api_client, course_factory):
        """Проверка получения списка курсов"""
        courses = course_factory(_quantity=3)

        url = reverse('courses-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

        response_ids = [course['id'] for course in response.data]
        for course in courses:
            assert course.id in response_ids

    def test_filter_courses_by_id(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по id"""
        courses = course_factory(_quantity=5)
        target_course = courses[2]

        url = reverse('courses-list')
        response = api_client.get(url, {'id': target_course.id})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id'] == target_course.id
        assert response.data[0]['name'] == target_course.name

    def test_filter_courses_by_name(self, api_client, course_factory):
        """Проверка фильтрации списка курсов по name"""
        course_factory(name="Python для начинающих")
        course_factory(name="Python продвинутый")
        course_factory(name="Java для начинающих")

        url = reverse('courses-list')
        response = api_client.get(url, {'name': 'Python'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2

        for course in response.data:
            assert 'Python' in course['name']

    def test_create_course_success(self, api_client):
        """Тест успешного создания курса"""
        course_data = {
            'name': 'Django разработка'
        }

        url = reverse('courses-list')
        response = api_client.post(url, course_data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == course_data['name']

        assert Course.objects.count() == 1
        course = Course.objects.first()
        assert course.name == course_data['name']

    def test_update_course_success(self, api_client, course_factory):
        """Тест успешного обновления курса"""
        course = course_factory(name="Старое название")

        updated_data = {
            'name': 'Новое название курса'
        }

        url = reverse('courses-detail', args=[course.id])
        response = api_client.put(url, updated_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == updated_data['name']

        course.refresh_from_db()
        assert course.name == updated_data['name']

    def test_delete_course_success(self, api_client, course_factory):
        """Тест успешного удаления курса"""
        course = course_factory()
        course_id = course.id

        url = reverse('courses-detail', args=[course_id])
        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(Course.DoesNotExist):
            Course.objects.get(id=course_id)


@pytest.mark.django_db
class TestCourseValidations:
    """Тест для валидации курсов"""

    def test_max_students_per_course_success(self, api_client, course_factory, student_factory, settings):
        """Тест успешного добавления 20 студентов в курс"""
        settings.MAX_STUDENTS_PER_COURSE = 20

        course = course_factory()
        url = reverse('courses-detail', args=[course.id])

        students = student_factory(_quantity=20)

        update_data = {'students': [s.id for s in students]}
        response = api_client.patch(url, update_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['students']) == 20

        course.refresh_from_db()
        assert course.students.count() == 20

    def test_max_students_per_course_failure(self, api_client, course_factory, student_factory, settings):
        """Тест неудачного добавления 21-го студента"""
        settings.MAX_STUDENTS_PER_COURSE = 20

        course = course_factory()
        url = reverse('courses-detail', args=[course.id])

        students = student_factory(_quantity=20)
        update_data = {'students': [s.id for s in students]}
        response = api_client.patch(url, update_data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['students']) == 20

        extra_student = student_factory()
        update_data = {'students': [s.id for s in students] + [extra_student.id]}
        response = api_client.patch(url, update_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        course.refresh_from_db()
        assert course.students.count() == 20

    @pytest.mark.parametrize('max_students, students_count, expected_status', [
        (5, 3, status.HTTP_200_OK),
        (5, 5, status.HTTP_200_OK),
        (5, 6, status.HTTP_400_BAD_REQUEST),
    ])
    def test_max_students_parametrized(self, api_client, course_factory, student_factory,
                                       settings, max_students, students_count, expected_status):
        """Параметризованный тест для проверки лимита студентов"""
        settings.MAX_STUDENTS_PER_COURSE = max_students

        course = course_factory()
        students = student_factory(_quantity=students_count)

        url = reverse('courses-detail', args=[course.id])
        update_data = {'students': [s.id for s in students]}

        response = api_client.patch(url, update_data, format='json')

        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            course.refresh_from_db()
            assert course.students.count() == students_count
        else:
            course.refresh_from_db()
            assert course.students.count() == 0