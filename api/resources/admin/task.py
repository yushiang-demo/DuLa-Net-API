import os
from flask import request
from flask_restx import Resource

from api.constant import TASK_STATUS
from api.app import api
from mongodb.app import db

import base64
from PIL import Image
from io import BytesIO
from helpers.storage import save_input, save_aligned, save_layout

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
        aligned_img = base64_to_pil(data['images']['aligned'])
        layout_img = base64_to_pil(data['images']['layout'])
        layout = data['layout']
        id = data['id']
        aligned_path = save_aligned(aligned_img, id)
        layout_path = save_layout(layout_img, id)

        db.updateTask(id, {
            'output':{
                'images': {
                    'aligned': aligned_path,
                    'layout': layout_path,
                },
                'layout': layout
            }
            
        })
        if db.getTask(id):
            db.updateTask(id, {
                'status': TASK_STATUS.DONE,
            })

        return { "tasks": data }, 200