from extensions import db
from sqlalchemy import asc, desc, or_, text
from . import Util

class AreaModel(db.Model):
    __tablename__ = 'area'

    id_area = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(300), nullable=False, )
    descripcion_completa = db.Column(db.String(300), nullable=False, )
    activo = db.Column(db.Boolean(), default=True)

    @classmethod
    def get_by_id(cls, id_area):
        return cls.query.filter_by(id_area=id_area).first()

    @classmethod
    def get_by_descripcion(cls, descripcion):
        return cls.query.filter_by(descripcion=descripcion, activo=True).first()

    @classmethod
    def get_or_filters(self, q):
        keyword = '%{keyword}%'.format(keyword=q)
        lst_condicion = []

        lst_condicion.append(AreaModel.descripcion.ilike(keyword))
        lst_condicion.append(AreaModel.descripcion_completa.ilike(keyword))

        return or_(*lst_condicion)

    @classmethod
    def get_all(cls, filters, q, page, per_page, sort, order, mode):
         
        sort_logic = Util.get_sort_condition(cls, sort, order)

        obj_qry = cls.query
        if filters:
            obj_qry = obj_qry.filter_by(**filters)

        if q:
            criterion = cls.get_or_filters(q)
            obj_qry = obj_qry.filter(criterion)

        if mode == 'paginated':
            return obj_qry.order_by(sort_logic).paginate(page=page, per_page=per_page)
        else:
            return obj_qry.order_by(sort_logic)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def delete_by_list(cls, lst_areas):
        for area in lst_areas:
            db.session.delete(area)
        db.session.commit()
