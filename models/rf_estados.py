from odoo import fields, models

class Estados(models.Model):
    _name = 'rf.estados'

    _rec_name  = 'desc'

    desc = fields.Char()
