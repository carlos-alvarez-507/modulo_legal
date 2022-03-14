import string

from odoo import models, fields, api

from datetime import datetime, date, timedelta

class Galeria(models.Model):
    
    _name = 'rf.galeria'
    
    _rec_name = 'id'

    # _order = 'creacion_fecha desc'

    imagen = fields.Binary()
    desc = fields.Text()

    def _get_demanda_id_from_context(self):
        parent_id = self.env.context.get('parent_id')
        parent_model = self.env.context.get('parent_model')

        if parent_id and parent_model:
            # parent_obj = self.env[parent_model].browse(parent_id)
            # now you have the parent obj to do what you want
            default_value = parent_id  # ... use the parent
            return default_value
        return None
    demanda_id = fields.Char(default='_get_demanda_id_from_context')