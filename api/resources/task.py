import os
import io
import uuid
from PIL import Image
from worker_helper import inference_from_file
from api.constant import TASK_STATUS

from api.app import api, db

from flask import request, jsonify
from flask_restx import Resource, abort
from api.models import Request, Task
from helpers.storage import save_input

postReq = Request()
postReq.addFile(name='file',required=True)

putReq = Request()
putReq.addFile(name='file',required=True)
putReq.addString(name="id",required=True)

getReq = Request()
getReq.addString(name="id",required=True)

delReq = Request()
delReq.addString(name="id",required=True)

class Task(Resource):

    @api.expect(delReq.parser)
    @api.marshal_with(Task)
    def delete(self):
        args = getReq.parser.parse_args()
        id = args.id
        success = db.updateTask(id, {
            'status': TASK_STATUS.REMOVED,
        })
        
        if success:
            return db.getTask(id), 200
        else:
            abort(400,message=f'Task {id} not found')

    @api.expect(getReq.parser)
    @api.marshal_with(Task, code=200)
    def get(self):
        args = getReq.parser.parse_args()
        id = args.id
        task = db.getTask(id)
        if task :
            if task['status'] == TASK_STATUS.DONE:
                return task, 200
            else:
                return abort(400, message=f'Task {id} is not ready.')
        else:
            abort(400, message=f'Task {id} not found')

    @api.expect(putReq.parser)
    @api.marshal_with(Task)
    def put(self):
        args = putReq.parser.parse_args()
        file = args.file
        id = args.id

        task = db.getTask(id)

        if task:
            isReady = db.updateTask(id, {
                'status': TASK_STATUS.PROCESSING,
            })
            if isReady:                
                pil_image = Image.open(io.BytesIO(file.read()))
                image_path = save_input(pil_image, id)
                db.updateTask(id, {
                    'input': image_path,
                    'output': None
                })
                
                inference_from_file(pil_image, id)

                return db.getTask(id), 200
            else:
                return abort(400, message=f'Task {id} is not ready.')
        else:
            abort(400, message=f'Task {id} not found')

    @api.expect(postReq.parser)
    @api.marshal_with(Task)
    def post(self):
        args = postReq.parser.parse_args()
        file = args.file
        if file:
            id = db.createTask()
            
            pil_image = Image.open(io.BytesIO(file.read()))
            image_path = save_input(pil_image, id)
            db.updateTask(id, {
                'input': image_path,
            })

            inference_from_file(pil_image, id)

            return db.getTask(id), 200
        else:
            return {}, 400