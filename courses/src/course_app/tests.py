from base_app.tests import BaseTestCase


class CourseEndPointTestCase(BaseTestCase):
    def test_create_course_start_date_in_the_past(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-11-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post('/api/v1/course/', data, jwt)

        self.assertEqual(resp.status_code, 400)
        self.assertTrue('starts_at' in resp_data)

    def test_create_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post('/api/v1/course/', data, jwt)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['title'], resp_data['title'])
        self.assertEqual(resp_data['teachers'][0]['id'], resp_data['author']['id'])

    def test_update_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post('/api/v1/course/', data, jwt)

        self.assertEqual(resp.status_code, 201)

        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
            'status': 'Open',
            'students': [self.users['new_student_1']['id']],
            'teachers': [self.users['qqq']['id'], self.users['new_teacher_1']['id']],
        }
        resp, resp_data = self.put(f'/api/v1/course/{resp_data["id"]}/', data, jwt)

        self.assertEqual(resp.status_code, 200)

    def test_add_student_to_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post('/api/v1/course/', data, jwt)

        self.add_student_to_course(resp_data['id'], 'new_student_1')

        jwt = self.auth('new_student_1')
        resp, resp_data = self.get(f'/api/v1/course/{resp_data["id"]}/', data, jwt)
        self.assertEqual(resp_data['title'], data['title'])
        self.assertEqual(len(resp_data['students']), 1)
