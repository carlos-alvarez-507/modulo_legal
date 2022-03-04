import string

from odoo import models, fields, api

from datetime import datetime, date, timedelta

class Provincias(models.Model):
    
    _name = 'rf.provincias'

    _rec_name = 'descrip'

    cia = fields.Char()
    tipo = fields.Integer()
    codigo = fields.Integer()
    descrip = fields.Char()
    tags = fields.Char()
    p0 = fields.Integer()
    p1 = fields.Integer()
    p2 = fields.Integer()
    p3 = fields.Integer()
    ubi = fields.Integer()