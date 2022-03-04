import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta

import dateutil.parser
#b = "2015-10-28 16:09:59"
#d = dateutil.parser.parse(b).date()


class DemoPartner(models.Model):
    _name = 'demo.partner'
    _rec_name = 'cedula'

    nombre = fields.Char()
    numero_registro = fields.Char()
    cedula = fields.Char()

    # nombre = fields.Char()
    # numReg = fields.Char()
    # cip = fields.Char(

