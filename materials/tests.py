from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group

from users.models import User
from materials.models import Course, Lesson, Subscribe


class LessonCRUDTestCase(APITestCase):
    def setUp(self):
        # Создаем группы прав
        self.moder_group = Group.objects.create(name='moders')

        # Создаем тестовых пользователей
        self.owner = User.objects.create(
            email='owner@test.com',
            password='testpass123',
            is_active=True
        )
        self.moderator = User.objects.create(
            email='moder@test.com',
            password='testpass123',
            is_active=True
        )
        self.moderator.groups.add(self.moder_group)
        self.other_user = User.objects.create(
            email='other@test.com',
            password='testpass123',
            is_active=True
        )

        # Создаем тестовый курс
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.owner
        )

        # Создаем тестовый урок
        self.lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            video_url='https://www.youtube.com/test',
            owner=self.owner
        )

        # URL для уроков
        self.lessons_list_url = reverse('materials:lessons-list')
        self.lesson_detail_url = reverse('materials:lessons-detail', args=[self.lesson.id])

    def test_lesson_create_by_owner(self):
        """Тест создания урока владельцем"""
        self.client.force_authenticate(user=self.owner)
        data = {
            'name': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/new'
        }
        response = self.client.post(self.lessons_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().owner, self.owner)

    def test_lesson_create_by_moderator(self):
        """Тест что модератор не может создать урок"""
        self.client.force_authenticate(user=self.moderator)
        data = {
            'name': 'New Lesson',
            'description': 'New Description',
            'course': self.course.id,
            'video_url': 'https://www.youtube.com/new'
        }
        response = self.client.post(self.lessons_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update_by_owner(self):
        """Тест обновления урока владельцем"""
        self.client.force_authenticate(user=self.owner)
        data = {'name': 'Updated Lesson'}
        response = self.client.patch(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_lesson_update_by_moderator(self):
        """Тест обновления урока модератором"""
        self.client.force_authenticate(user=self.moderator)
        data = {'name': 'Updated by Moder'}
        response = self.client.patch(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated by Moder')

    def test_lesson_update_by_other_user(self):
        """Тест что другой пользователь не может обновить урок"""
        self.client.force_authenticate(user=self.other_user)
        data = {'name': 'Updated by Other'}
        response = self.client.patch(self.lesson_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_by_owner(self):
        """Тест удаления урока владельцем"""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_by_moderator(self):
        """Тест что модератор не может удалить урок"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_by_other_user(self):
        """Тест что другой пользователь не может удалить урок"""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create(
            email='user1@test.com',
            password='testpass123',
            is_active=True
        )
        self.user2 = User.objects.create(
            email='user2@test.com',
            password='testpass123',
            is_active=True
        )

        # Создаем тестовый курс
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.user1
        )

        # URL для подписок
        self.subscribe_url = reverse('materials:course-subscribe', kwargs={'course_id': self.course.id})

    def test_subscribe(self):
        """Тест подписки на курс"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscribe.objects.filter(user=self.user1, course=self.course).exists())

    def test_double_subscribe(self):
        """Тест двойной подписки на курс"""
        self.client.force_authenticate(user=self.user1)
        # Первая подписка
        self.client.post(self.subscribe_url)
        # Вторая попытка подписки
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsubscribe(self):
        """Тест отписки от курса"""
        self.client.force_authenticate(user=self.user1)
        # Сначала подписываемся
        Subscribe.objects.create(user=self.user1, course=self.course)
        # Затем отписываемся
        response = self.client.delete(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscribe.objects.filter(user=self.user1, course=self.course).exists())

    def test_unsubscribe_without_subscription(self):
        """Тест отписки без существующей подписки"""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_with_subscription_flag(self):
        """Тест что курс возвращает флаг подписки"""
        # URL для получения курса
        course_detail_url = reverse('materials:courses-detail', args=[self.course.id])

        # Проверяем для неподписанного пользователя
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])

        # Создаем подписку
        Subscribe.objects.create(user=self.user1, course=self.course)

        # Проверяем для подписанного пользователя
        response = self.client.get(course_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])