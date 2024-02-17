import os
import io
import base64
from celery import Celery

BROKER_URL = os.environ.get('WORKER_BROKER_URL')
BACKEND_URL = os.environ.get('WORKER_BACKEND_URL')
APP_NAME = os.environ.get('WORKER_APP_NAME')
TASK_NAME = os.environ.get('WORKER_TASK_NAME')
CALLBACK_URL = os.environ.get('WORKER_CALLBACK_URL')
app = Celery(APP_NAME, broker=BROKER_URL, backend=BACKEND_URL)

def inference_from_file(pil_image, id, callback_url=CALLBACK_URL):
    img_bytes = io.BytesIO()
    pil_image.save(img_bytes, format='JPEG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode()
    app.send_task(TASK_NAME, args=[img_base64, id, callback_url])