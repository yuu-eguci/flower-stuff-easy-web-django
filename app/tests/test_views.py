import json
import tempfile
from pathlib import Path
from unittest import mock

import numpy
from django.test import SimpleTestCase, override_settings


@override_settings(APP_PINCODE='2468', APP_HDF5_VERSION='test-version')
class ApiTests(SimpleTestCase):

    def post_json(self, path, data):
        return self.client.post(path, data=json.dumps(data), content_type='application/json')

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'top')

    def test_status_is_not_ready_without_model(self):
        with override_settings(APP_HDF5_PATH_IN_APP='/nonexistent/hdf5.hdf5'):
            response = self.client.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'ready': False})

    def test_status_is_ready_with_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            model_path = Path(tmp) / 'hdf5.hdf5'
            model_path.touch()
            with override_settings(APP_HDF5_PATH_IN_APP=str(model_path)):
                response = self.client.get('/api/v1/status')
        self.assertEqual(response.json(), {'ready': True})

    def test_verify_pincode(self):
        response = self.post_json('/api/v1/verify-pincode', {'pincode': '2468'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'verification_succeeded': True})

        response = self.post_json('/api/v1/verify-pincode', {'pincode': '0000'})
        self.assertEqual(response.json(), {'verification_succeeded': False})

    def test_verify_pincode_requires_pincode(self):
        response = self.post_json('/api/v1/verify-pincode', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'pincode is required.'})

    def test_predict_image_requires_base64image(self):
        response = self.post_json('/api/v1/predict-image', {})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'base64image is required.'})

    def test_predict_image(self):
        prediction = [('Sunflower', numpy.float32(0.75)), ('Tulip', numpy.float32(0.25))]
        with mock.patch('app.utils.prediction_utils.predict_base64image', return_value=prediction) as predict:
            response = self.post_json('/api/v1/predict-image', {'base64image': 'data:image/png;base64,AAAA'})
        predict.assert_called_once_with('data:image/png;base64,AAAA')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'hdf5_version': 'test-version',
            'result': [
                {'name': 'Sunflower', 'confidence': '0.75'},
                {'name': 'Tulip', 'confidence': '0.25'},
            ],
        })

    def test_predict_image_returns_message_on_error(self):
        with mock.patch('app.utils.prediction_utils.predict_base64image', side_effect=OSError):
            with self.assertLogs('app.views', level='ERROR'):
                response = self.post_json('/api/v1/predict-image', {'base64image': 'AAAA'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'message': 'Something went wrong.'})
