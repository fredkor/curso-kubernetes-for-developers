import os

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from http import HTTPStatus

from webargs import fields
from webargs.flaskparser import use_kwargs

from models.AreaModel import AreaModel
from models import Util

from schemas.AreaSchema import AreaSchema, AreaPaginationSchema

area_schema = AreaSchema()
area_lst_schema = AreaSchema(many=True)
area_pagination_schema = AreaPaginationSchema()

class AreaListResource(Resource):

    def get(self):
        q = request.args.get('q', '')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        sort = request.args.get('sort', 'descripcion')
        order = request.args.get('order', 'asc')
        mode = request.args.get('mode', 'catalog')

        if sort not in ['descripcion', 'descripcion_completa', 'activo']:
            sort = 'descripcion'

        if order not in ['asc', 'desc']:
            order = 'asc'

        filters = Util.get_filter_from_request(request)
        paginated_areas = AreaModel.get_all(filters, q, page, per_page, sort, order, mode)

        if mode == 'paginated':
            return area_pagination_schema.dump(paginated_areas), HTTPStatus.OK
        else:
            return area_lst_schema.dump(paginated_areas), HTTPStatus.OK

    def post(self):
        json_data = request.get_json()

        try:
            data = area_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, HTTPStatus.BAD_REQUEST

        area = AreaModel(
            descripcion=data.get('descripcion'),
            descripcion_completa=data.get('descripcion_completa'),
            activo=data.get('activo'))
        area.save()

        return area_schema.dump(area), HTTPStatus.CREATED

    @use_kwargs({'ids': fields.Str(missing='')})
    def delete(self, ids):

        lst_ids = ids.split(',')
        if ids == '' or len(lst_ids) == 0:
            return {'message': 'Se requieren la lista de ids'}, HTTPStatus.BAD_REQUEST

        lst_areas = []
        for id in lst_ids:
            area = AreaModel.get_by_id(id)

            if area is None:
                return {'message': 'Area no encontrada'}, HTTPStatus.NOT_FOUND

            lst_areas.append(area)

        AreaModel.delete_by_list(lst_areas)

        return {}, HTTPStatus.NO_CONTENT

class AreaResource(Resource):

    def get(self, id_area):
        area = AreaModel.get_by_id(id_area=id_area)

        if area is None:
            return {'message': 'Area no encontrada'}, HTTPStatus.NOT_FOUND

        return area_schema.dump(area), HTTPStatus.OK

    def put(self, id_area):
        json_data = request.get_json()

        if json_data is None:
            return {'message': 'Se requieren datos del area'}, HTTPStatus.BAD_REQUEST

        try:
            data = area_schema.load(json_data)
        except ValidationError as err:
            return {'message': 'Validation errors', 'errors': err.messages}, HTTPStatus.BAD_REQUEST

        area = AreaModel.get_by_id(id_area)
        area.descripcion = data.get('descripcion') or area.descripcion
        area.descripcion_completa = data.get('descripcion_completa') or area.descripcion_completa
        area.activo = data.get('activo')
        area.save()

        return area_schema.dump(area), HTTPStatus.OK

    def delete(self, id_area):
        area = AreaModel.get_by_id(id_area)

        if area is None:
            return {'message': 'Area no encontrado'}, HTTPStatus.NOT_FOUND

        area.delete()

        return {}, HTTPStatus.NO_CONTENT
