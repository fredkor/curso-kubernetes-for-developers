from flask import url_for
from marshmallow import Schema, fields, ValidationError

from schemas.pagination import PaginationSchema

class AreaSchema(Schema):
    class Meta:
        ordered = True

    id_area = fields.Int(dump_only=True)
    descripcion = fields.String(required=True)
    descripcion_completa = fields.String(required=True)
    activo = fields.Boolean(required=True)

class AreaPaginationSchema(PaginationSchema):
    data = fields.Nested(AreaSchema, attribute='items', many=True)
