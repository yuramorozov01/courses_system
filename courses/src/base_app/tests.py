from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class BaseTestCase(TestCase):
    def setUp(self):
        self.users = {
            'qqq': {
                'username': 'qqq',
                'password': 'qqwwee112233',
            },
            'new_student_1': {
                'username': 'new_student_1',
                'password': 'qqwwee112233',
            },
            'new_student_2': {
                'username': 'new_student_2',
                'password': 'qqwwee112233',
            },
            'new_teacher_1': {
                'username': 'new_teacher_1',
                'password': 'qqwwee112233',
            },
            'new_teacher_2': {
                'username': 'new_teacher_2',
                'password': 'qqwwee112233',
            }
        }
        for user, data in self.users.items():
            user_inst = get_user_model().objects.create_user(username=data['username'], password=data['password'])
            data['id'] = user_inst.pk
            user_inst.save()

    def auth(self, username):
        login_resp = self.client.post('/auth/jwt/create/', {'username': username, 'password': self.users[username]['password']})
        jwt = login_resp.json()['access']
        return jwt

    def post(self, url, data, jwt):
        resp = self.client.post(url, data, HTTP_AUTHORIZATION='JWT ' + jwt, content_type='application/json')
        return resp, resp.json()

    def get(self, url, data, jwt):
        resp = self.client.get(url, data, HTTP_AUTHORIZATION='JWT ' + jwt, content_type='application/json')
        return resp, resp.json()

    def put(self, url, data, jwt):
        resp = self.client.put(url, data, HTTP_AUTHORIZATION='JWT ' + jwt, content_type='application/json')
        return resp, resp.json()

    def patch(self, url, data, jwt):
        resp = self.client.patch(url, data, HTTP_AUTHORIZATION='JWT ' + jwt, content_type='application/json')
        return resp, resp.json()

    def delete(self, url, data, jwt):
        resp = self.client.delete(url, data, HTTP_AUTHORIZATION='JWT ' + jwt, content_type='application/json')
        return resp, resp.json()

    def create_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post(reverse('course-list'), data, jwt)
        return resp_data['id']

    def create_lecture(self):
        course_id = self.create_course()
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title lecture',
            'text': 'texllllllllllll',
        }
        resp, resp_data = self.post(reverse('lecture-list', kwargs={'course_pk': course_id}), data, jwt)
        return course_id, resp_data['id']

    def create_task_statement(self):
        course_id, lecture_id = self.create_lecture()
        jwt = self.auth('qqq')
        data = {
            'title': 'task statement1',
            'text': 'you should do it fast!',
        }

        resp, resp_data = self.post(
            reverse('task_statement-list', kwargs={'course_pk': course_id, 'lecture_pk': lecture_id}),
            data,
            jwt
        )
        return course_id, lecture_id, resp_data['id']

    def create_task(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        self.add_student_to_course(course_id, 'new_student_2')

        jwt = self.auth('new_student_2')
        data = {
            'text': 'ooooooo moya oborona',
            'link': 'https://github.com/yuramorozov01/courses_system',
        }
        resp, resp_data = self.post(
            reverse('task-list', kwargs={'course_pk': course_id, 'lecture_pk': lecture_id, 'task_statement_pk': task_statement_id}),
            data,
            jwt
        )
        return course_id, lecture_id, task_statement_id, resp_data['id']

    def add_student_to_course(self, course_id, student_username):
        jwt = self.auth('qqq')
        resp, resp_data = self.get(reverse('course-detail', args=[course_id]), {}, jwt)
        students = [student['id'] for student in resp_data['students']]
        students.append(self.users[student_username]['id'])
        teachers = [teacher['id'] for teacher in resp_data['teachers']]
        data = {
            'students': students,
            'teachers': teachers,
        }
        resp, resp_data = self.patch(reverse('course-detail', args=[course_id]), data, jwt)
