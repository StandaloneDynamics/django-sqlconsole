from django.test import TestCase, Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import QueryLog


class ConsoleTestCase(TestCase):
    def setUp(self) -> None:
        self.admin = User.objects.create(username='admin', password='admin',
                                    is_staff=True, is_superuser=True)
        self.staff = User.objects.create(username='staff', password='staff', is_staff=True)

        ct = ContentType.objects.get_for_model(QueryLog)
        self.perm = Permission.objects.get(
            codename='can_execute_query',
            content_type=ct
        )

    def test_permissions(self):
        url = reverse('admin:console')

        admin_user = Client()
        admin_user.force_login(self.admin)
        resp = admin_user.get(url)
        self.assertEqual(resp.status_code, 200)

        # staff user does not have correct permissions
        staff_user = Client()
        staff_user.force_login(self.staff)
        resp = staff_user.get(url)
        self.assertEqual(resp.status_code, 403)

        # grant staff user permission
        self.staff.user_permissions.add(self.perm)
        self.staff.save()
        self.assertTrue(self.staff.has_perm('sqlconsole.can_execute_query'))

        staff_user = Client()
        staff_user.force_login(self.staff)
        resp = staff_user.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_error_query_log(self):
        url = reverse('admin:console')

        admin_user = Client()
        admin_user.force_login(self.admin)
        resp = admin_user.post(url,
                               {'query': 'select count(*) from query_log',
                                '_save': 'Submit'
                                })
        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(resp.context['message']), 'no such table: query_log')
        self.assertEqual(QueryLog.objects.count(), 1)

    def test_success_query_log(self):
        url = reverse('admin:console')

        admin_user = Client()
        admin_user.force_login(self.admin)
        resp = admin_user.post(url,
                               {'query': 'select count(*) from sqlconsole_querylog',
                                '_save': 'Submit'
                                })
        self.assertEqual(resp.status_code, 200)
        self.assertIn(str(resp.context['message']), '')
        self.assertEqual(resp.context['columns'][0], 'count(*)')
        self.assertEqual(resp.context['results'][0], (0,))
        self.assertEqual(QueryLog.objects.count(), 1)
















