from odoo import fields, models

class Estados(models.Model):
    _name = 'rf.estados'
    _description = 'Estados'

    # _order = "name desc"

    _rec_name ="estado"

    codigo = fields.Char() #TODO: Utilzo este campo para importar los logs.  Despues de importar utilizo el campo computado
    # codigo = fields.Char(compute='_compute_codigo_estados') 

    estado = fields.Char()

    def _compute_codigo_estados(self):
        for item in self:
            item.codigo = str(item.id)
