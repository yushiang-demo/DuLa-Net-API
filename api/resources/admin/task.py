import os
from flask import request
from flask_restx import Resource

from api.constant import TASK_STATUS
from api.app import api
from mongodb.app import db

import base64
from PIL import Image
from io import BytesIO

STORAGE_FOLDER = os.environ.get('STORAGE_FOLDER')
STORAGE_BASE_URL = os.environ.get('STORAGE_BASE_URL')
def base64_to_pil(base64_str):
    image_data = base64.b64decode(base64_str)
    img_buffer = BytesIO(image_data)
    pil_image = Image.open(img_buffer)
    return pil_image

class Task(Resource):
    def put(self):
        '''
        callback endpoints for worker.
        '''
        data = request.json
        input_img = base64_to_pil(data['images']['input'])
        aligned_img = base64_to_pil(data['images']['aligned'])
        layout_img = base64_to_pil(data['images']['layout'])
        layout = data['layout']
        id = data['id']
        
        output = os.path.join(STORAGE_FOLDER,id)
        os.makedirs(output, exist_ok=True)

        input_img.save(os.path.join(output,"input.jpg"))
        aligned_img.save(os.path.join(output,"aligned.jpg"))
        layout_img.save(os.path.join(output,"layout.jpg"))

        db.updateTask(id, {
            'images': {
                'input': f'{STORAGE_BASE_URL}/{id}/input.jpg',
                'aligned': f'{STORAGE_BASE_URL}/{id}/aligned.jpg',
                'layout': f'{STORAGE_BASE_URL}/{id}/layout.jpg',
            },
            'layout': layout
        })
        if db.getTask(id):
            db.updateTask(id, {
                'status': TASK_STATUS.DONE,
            })

        return { "tasks": data }, 200