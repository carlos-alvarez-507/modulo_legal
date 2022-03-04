import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta


class Abogados(models.Model):
    _name = 'rf.abogados'

    _rec_name = 'descripcion'

    codigo = fields.Integer()
    usuario_id = fields.Many2one('res.users', 'user_id') #varios perfiles de abogados podrian ser vinculados a un solo perfil de usuario.
    partner_id = fields.Many2one('res.partner', 'partner_id')
    nombre = fields.Char(related='partner_id.name')
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

    # Omitidas porque no se utilizan
    # h1era = fields.Datetime()
    # h2da = fields.Datetime()