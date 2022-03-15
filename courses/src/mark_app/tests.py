from django.urls import reverse

from base_app.tests import BaseTestCase


class MarkEndPointTestCase(BaseTestCase):
    def test_add_mark_to_task(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 9,
        }
        url = reverse(
            'mark-list',
            kwargs={
                'course_pk': course_id,
                'lecture_pk': lecture_id,
                'task_statement_pk': task_statement_id,
                'task_pk': task_id,
            }
        )
        resp, resp_data = self.post(url, data, jwt)

        assert resp.status_code == 201
        assert resp_data['mark_value'] == data['mark_value']
        assert self.users['qqq']['id'] == resp_data['author']['id']

    def test_add_mark_to_task_more_than_10(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 20,
        }
        url = reverse(
            'mark-list',
            kwargs={
                'course_pk': course_id,
                'lecture_pk': lecture_id,
                'task_statement_pk': task_statement_id,
                'task_pk': task_id,
            }
        )

        resp, resp_data = self.post(url, data, jwt)
        assert resp.status_code == 400
        assert 'ensure' in resp_data['mark_value'][0].lower()

    def test_get_mark_as_student(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 9,
        }
        url = reverse(
            'mark-list',
            kwargs={
                'course_pk': course_id,
                'lecture_pk': lecture_id,
                'task_statement_pk': task_statement_id,
                'task_pk': task_id,
            }
        )
        resp, resp_data = self.post(url, data, jwt)

        jwt = self.auth('new_student_2')
        url = reverse(
            'mark-detail',
            kwargs={
                'course_pk': course_id,
                'lecture_pk': lecture_id,
                'task_statement_pk': task_statement_id,
                'task_pk': task_id,
                'pk': resp_data["id"],
            }
        )
        resp, resp_data = self.get(url, data, jwt)

        assert resp.status_code == 200
        assert resp_data['mark_value'] == data['mark_value']
        assert self.users['qqq']['id'] == resp_data['author']['id']
