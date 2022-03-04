from odoo import fields, models

class DemoCliente(models.Model):
    _name = 'demo.clientes'
    _description = 'Clientes'

    # _order = "name desc"

    _rec_name ="ruced"

    # _inherit = ["mail.thread", 'mail.activity.mixin']



    cia = fields.Char()
    ctacliente = fields.Char()
    tipo	= fields.Char()
    nombre = fields.Char()
    ruced = fields.Char()
    