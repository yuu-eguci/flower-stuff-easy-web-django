import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AsgiSettingsModuleTests(SimpleTestCase):

    def settings_module_after_importing_asgi(self, extra_env):
        env = {k: v for k, v in os.environ.items() if k not in ('DJANGO_SETTINGS_MODULE', 'WEBSITE_HOSTNAME')}
        env.update(extra_env)
        code = 'import os, config.asgi; print(os.environ["DJANGO_SETTINGS_MODULE"])'
        result = subprocess.run([sys.executable, '-c', code], cwd=BASE_DIR, env=env,
                                capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def test_uses_local_settings_by_default(self):
        self.assertEqual(self.settings_module_after_importing_asgi({}), 'config.settings.local')

    def test_uses_production_settings_on_app_service(self):
        self.assertEqual(self.settings_module_after_importing_asgi({'WEBSITE_HOSTNAME': 'example.com'}),
                         'config.settings.production')
