from base_app.tests import BaseTestCase
from django.urls import reverse


class LectureEndPointTestCase(BaseTestCase):
    def test_create_lecture(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title lecture',
            'text': 'texllllllllllll',
        }
        course_id = self.create_course()
        resp, resp_data = self.post(reverse('lecture-list', kwargs={'course_pk': course_id}), data, jwt)

        assert resp.status_code == 201
        assert data['text'] == resp_data['text']
        assert self.users['qqq']['id'] == resp_data['author']['id']

    def test_get_lecture_not_studying_course(self):
        course_id, lecture_id = self.create_lecture()

        jwt = self.auth('new_student_2')

        resp, resp_data = self.get(
            reverse('lecture-detail', kwargs={'course_pk': course_id, 'pk': lecture_id}),
            {},
            jwt
        )
        assert resp.status_code == 403

        jwt = self.auth('qqq')
        resp, resp_data = self.get(
            reverse('lecture-detail', kwargs={'course_pk': course_id, 'pk': lecture_id}),
            {},
            jwt
        )
        assert resp.status_code == 200

    def test_get_lecture_teaching_course(self):
        course_id, lecture_id = self.create_lecture()

        jwt = self.auth('qqq')
        resp, resp_data = self.get(
            reverse('lecture-detail', kwargs={'course_pk': course_id, 'pk': lecture_id}),
            {},
            jwt
        )
        assert resp.status_code == 200
