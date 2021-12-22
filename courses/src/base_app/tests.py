from django.contrib.auth import get_user_model
from django.test import TestCase


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
