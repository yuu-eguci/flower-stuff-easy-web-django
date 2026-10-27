import importlib

from django.test import SimpleTestCase, override_settings
from django.urls import clear_url_caches

import config.urls


@override_settings(DEBUG=True)
class DebugUrlsTests(SimpleTestCase):

    def setUp(self):
        importlib.reload(config.urls)
        clear_url_caches()
        self.addCleanup(clear_url_caches)
        self.addCleanup(importlib.reload, config.urls)

    def test_project_files_are_not_served(self):
        for path in ['/manage.py', '/config/settings/base.py', '/Pipfile']:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 404)
