from base_app.tests import BaseTestCase
from django.urls import reverse


class TaskEndPointTestCase(BaseTestCase):
    def test_create_task_statement(self):
        course_id, lecture_id = self.create_lecture()
        jwt = self.auth('qqq')
        data = {
            'title': 'task statement1',
            'text': 'you should do it fast!',
        }
        url = reverse('task_statement-list', kwargs={'course_pk': course_id, 'lecture_pk': lecture_id})
        print(url)
        resp, resp_data = self.post(url, data, jwt)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['text'], resp_data['text'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])

    def test_get_task_statement_as_not_studying(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        jwt = self.auth('new_student_2')
        url = reverse(
            'task_statement-detail',
            kwargs={'course_pk': course_id, 'lecture_pk': lecture_id, 'pk': task_statement_id}
        )
        resp, resp_data = self.get(url, {}, jwt)

        self.assertEqual(resp.status_code, 404)

    def test_get_task_statements_as_studying(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        self.add_student_to_course(course_id, 'new_student_2')

        jwt = self.auth('new_student_2')
        url = reverse('task_statement-list', kwargs={'course_pk': course_id, 'lecture_pk': lecture_id})
        resp, resp_data = self.get(url, {}, jwt)

        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp.status_code, 200)

    def test_send_task_to_task_statement(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        self.add_student_to_course(course_id, 'new_student_2')

        jwt = self.auth('new_student_2')
        data = {
            'text': 'ooooooo moya oborona',
            'link': 'https://github.com/yuramorozov01/courses_system',
        }
        url = reverse(
            'task-list',
            kwargs={'course_pk': course_id, 'lecture_pk': lecture_id, 'task_statement_pk': task_statement_id}
        )
        resp, resp_data = self.post(url, data, jwt)

        self.assertEqual(resp_data['text'], data['text'])
        self.assertEqual(resp_data['author']['id'], self.users['new_student_2']['id'])
        self.assertEqual(resp.status_code, 201)

    def test_get_task_from_task_statement_as_teacher(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        self.add_student_to_course(course_id, 'new_student_2')

        jwt = self.auth('new_student_2')
        data = {
            'text': 'ooooooo moya oborona',
            'link': 'https://github.com/yuramorozov01/courses_system',
        }
        url = reverse(
            'task-list',
            kwargs={'course_pk': course_id, 'lecture_pk': lecture_id, 'task_statement_pk': task_statement_id}
        )
        resp, resp_data = self.post(url, data, jwt)

        jwt = self.auth('qqq')
        url = reverse(
            'task-list',
            kwargs={'course_pk': course_id, 'lecture_pk': lecture_id, 'task_statement_pk': task_statement_id}
        )
        resp, resp_data = self.get(url, {}, jwt)

        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp.status_code, 200)
