import base64
import binascii
import io
import os
import tempfile
from pathlib import Path
from unittest import mock

import tensorflow

from django.test import SimpleTestCase, override_settings
from PIL import Image

from app.utils import prediction_utils

LEGACY_MODEL_PATH = Path(__file__).resolve().parent / 'fixtures' / 'legacy_model.h5'


def make_base64_png(size=(40, 30)):
    buffer = io.BytesIO()
    Image.new('RGB', size, (200, 180, 20)).save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


class TrimBase64HeaderTests(SimpleTestCase):

    def test_removes_data_url_header(self):
        self.assertEqual(prediction_utils.trim_base64_header('data:image/png;base64,AAAA'), 'AAAA')

    def test_keeps_string_without_header(self):
        self.assertEqual(prediction_utils.trim_base64_header('AAAA'), 'AAAA')


@override_settings(APP_HDF5_PATH_IN_APP=str(LEGACY_MODEL_PATH))
class PredictBase64ImageTests(SimpleTestCase):

    def assert_legacy_model_prediction(self, prediction):
        self.assertEqual([name for name, _ in prediction], ['Sunflower', 'Tulip', 'Daisy'])
        confidences = [float(confidence) for _, confidence in prediction]
        self.assertAlmostEqual(confidences[0], 0.7927, places=3)
        self.assertGreater(confidences[1], confidences[2])

    def test_predicts_with_model_saved_by_tensorflow_2_6(self):
        self.assert_legacy_model_prediction(prediction_utils.predict_base64image(make_base64_png()))

    def test_accepts_data_url(self):
        data_url = 'data:image/png;base64,' + make_base64_png()
        self.assert_legacy_model_prediction(prediction_utils.predict_base64image(data_url))

    def test_does_not_leave_files_in_working_directory_on_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            cwd = os.getcwd()
            os.chdir(tmp)
            self.addCleanup(os.chdir, cwd)
            with self.assertRaises(Exception):
                prediction_utils.predict_base64image(base64.b64encode(b'not an image').decode())
            self.assertEqual(os.listdir(tmp), [])

    def test_rejects_invalid_base64(self):
        with self.assertRaises(binascii.Error):
            prediction_utils.predict_base64image('not base64!')

    def test_loads_model_only_once(self):
        load_model = mock.Mock(wraps=tensorflow.keras.models.load_model)
        with mock.patch('tensorflow.keras.models.load_model', load_model):
            prediction_utils.load_model.cache_clear()
            self.addCleanup(prediction_utils.load_model.cache_clear)
            prediction_utils.predict_base64image(make_base64_png())
            prediction_utils.predict_base64image(make_base64_png())
        load_model.assert_called_once_with(str(LEGACY_MODEL_PATH))
