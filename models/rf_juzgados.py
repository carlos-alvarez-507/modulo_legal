import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta


class Juzgados(models.Model):
    _name = 'rf.juzgados'
    _rec_name = 'descripcion'

    codigo = fields.Integer()
    descripcion = fields.Char()
    tipo = fields.Integer()
    ckpb = fields.Integer()
    monto = fields.Integer()
    ctacont = fields.Integer()
    cia = fields.Char()
    letra = fields.Char()
    deta0 = fields.Integer()
    deta1 = fields.Integer()
    deta2 = fields.Integer()
    p1era = fields.Integer()
    p2da = fields.Integer()