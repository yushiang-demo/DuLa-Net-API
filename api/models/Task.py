from flask_restx import fields
from api.app import api

layoutPoint = api.model('LayoutPoint',{
    'id': fields.Integer,
    'coords': fields.List(fields.Float),
    'xyz': fields.List(fields.Float),
})

layoutPoints = api.model('LayoutPoints', {
    'num': fields.Integer,
    'points': fields.List(fields.Nested(layoutPoint))
})

Layout = api.model('Layout',{
    'cameraHeight': fields.Float,
    'layoutHeight': fields.Float,
    'layoutPoints': fields.Nested(layoutPoints),
})

Images = api.model('Images',{
    'aligned': fields.String,
    'layout': fields.String,
})

Output = api.model('Output',{   
    'images': fields.Nested(Images),
    'layout': fields.Nested(Layout),
})

Task = api.model('Task', {
    'uuid':  fields.String(attribute='_id'),
    'status': fields.String,
    'input': fields.String,
    'output': fields.Nested(Output),
})