from base_app.tests import BaseTestCase


class TaskEndPointTestCase(BaseTestCase):
    def test_create_task_statement(self):
        course_id, lecture_id = self.create_lecture()
        jwt = self.auth('qqq')
        data = {
            'title': 'task statement1',
            'text': 'you should do it fast!',
        }
        resp, resp_data = self.post(f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/', data, jwt)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['text'], resp_data['text'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])

    def test_get_task_statement_as_not_studying(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        jwt = self.auth('new_student_2')
        resp, resp_data = self.get(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/',
            {},
            jwt
        )

        self.assertEqual(resp.status_code, 404)

    def test_get_task_statements_as_studying(self):
        course_id, lecture_id, task_statement_id = self.create_task_statement()
        self.add_student_to_course(course_id, 'new_student_2')

        jwt = self.auth('new_student_2')
        resp, resp_data = self.get(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/',
            {},
            jwt
        )

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
        resp, resp_data = self.post(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/',
            data,
            jwt
        )

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
        resp, resp_data = self.post(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/',
            data,
            jwt
        )

        jwt = self.auth('qqq')
        resp, resp_data = self.get(
            f'/api/v1/course/{course_id}/lecture/{lecture_id}/task_statement/{task_statement_id}/task/',
            data,
            jwt
        )
        print(resp_data)
        self.assertEqual(len(resp_data), 1)
        self.assertEqual(resp.status_code, 200)
