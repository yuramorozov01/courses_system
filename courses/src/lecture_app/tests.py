from base_app.tests import BaseTestCase


class LectureEndPointTestCase(BaseTestCase):
    def create_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2021-12-27',
            'ends_at': '2022-02-13',
        }
        resp, resp_data = self.post('/api/v1/course/', data, jwt)
        return resp_data['id']

    def test_create_lecture(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title lecture',
            'text': 'texllllllllllll',
        }
        course_id = self.create_course()
        resp, resp_data = self.post(f'/api/v1/course/{course_id}/lecture/', data, jwt)

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(data['text'], resp_data['text'])
        self.assertEqual(self.users['qqq']['id'], resp_data['author']['id'])
