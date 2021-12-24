from base_app.tests import BaseTestCase


class MarkEndPointTestCase(BaseTestCase):
    def test_add_mark_to_task(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 9,
        }
        resp, resp_data = self.post(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/{task_id}/mark/',
            data,
            jwt
        )

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_data['mark_value'], data['mark_value'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])

    def test_add_mark_to_task_more_than_10(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 20,
        }
        resp, resp_data = self.post(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/{task_id}/mark/',
            data,
            jwt
        )
        self.assertEqual(resp.status_code, 400)
        self.assertTrue('ensure' in resp_data['mark_value'][0].lower())

    def test_get_mark_as_student(self):
        course_id, lecture_id, task_statement_id, task_id = self.create_task()
        jwt = self.auth('qqq')
        data = {
            'mark_value': 9,
        }
        resp, resp_data = self.post(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/{task_id}/mark/',
            data,
            jwt
        )

        jwt = self.auth('new_student_2')
        resp, resp_data = self.get(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/{task_id}/mark/{resp_data["id"]}/',
            data,
            jwt
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_data['mark_value'], data['mark_value'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])
