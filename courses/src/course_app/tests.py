import pytest
from django.urls import reverse

from base_app.tests import BaseTestCase


class CourseEndPointTestCase(BaseTestCase):
    def test_create_course_start_date_in_the_past(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2012-02-27',
            'ends_at': '2022-12-13',
        }
        resp, resp_data = self.post(reverse('course-list'), data, jwt)
        assert resp.status_code == 400
        assert 'starts_at' in resp_data

    def test_create_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2022-02-27',
            'ends_at': '2022-12-13',
        }
        resp, resp_data = self.post(reverse('course-list'), data, jwt)

        assert resp.status_code == 201
        assert data['title'] == resp_data['title']
        assert resp_data['teachers'][0]['id'] == resp_data['author']['id']

    def test_update_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2022-02-27',
            'ends_at': '2022-12-13',
        }
        resp, resp_data = self.post(reverse('course-list'), data, jwt)

        assert resp.status_code == 201

        data = {
            'title': 'this is test title',
            'starts_at': '2022-02-27',
            'ends_at': '2022-12-13',
            'status': 'Open',
            'students': [self.users['new_student_1']['id']],
            'teachers': [self.users['qqq']['id'], self.users['new_teacher_1']['id']],
        }

        resp, resp_data = self.put(reverse('course-detail', args=[resp_data["id"]]), data, jwt)

        assert resp.status_code == 200

    def test_add_student_to_course(self):
        jwt = self.auth('qqq')
        data = {
            'title': 'this is test title',
            'starts_at': '2022-02-27',
            'ends_at': '2022-12-13',
        }
        resp, resp_data = self.post(reverse('course-list'), data, jwt)

        self.add_student_to_course(resp_data['id'], 'new_student_1')

        jwt = self.auth('new_student_1')
        resp, resp_data = self.get(reverse('course-detail', args=[resp_data["id"]]), data, jwt)

        assert resp_data['title'] == data['title']
        assert len(resp_data['students']) == 1
