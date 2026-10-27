#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

docker compose up --detach --build --wait
trap 'docker compose down' EXIT

docker compose exec -T django python manage.py check
curl --fail --silent --show-error http://127.0.0.1:8000/api/v1/status
echo

# Predict with the tiny test model instead of the real one.
docker compose exec -T django cp app/tests/fixtures/legacy_model.h5 app/hdf5.hdf5
docker compose exec -T django python - <<'PYTHON'
import base64
import io
import json
import urllib.request

from PIL import Image

buffer = io.BytesIO()
Image.new('RGB', (8, 8), (200, 180, 20)).save(buffer, format='PNG')
body = json.dumps({'base64image': base64.b64encode(buffer.getvalue()).decode()}).encode()
request = urllib.request.Request('http://127.0.0.1:8000/api/v1/predict-image', data=body,
                                 headers={'Content-Type': 'application/json'})
result = json.load(urllib.request.urlopen(request))
print(result)
assert result['result'][0]['name'] == 'Sunflower', result
PYTHON

echo "Docker smoke test passed."
