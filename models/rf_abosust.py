import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta


class AbogadosSustitutos(models.Model):
    
    _name = 'rf.abosust'

    _rec_name = 'id'
    
    demanda_id = fields.Char(default='_get_context_demanda_id')
    

    cntacliente = fields.Char() # TODO: Este campo es utilizado solamente al momento de importar los logs. Luego de importar los logs comentamos este campo y utilizamos el campo computado.
    # cntacliente = fields.Char(compute='_get_cta_cliente')



    abogado_descripcion = fields.Many2one('rf.abogados', string='Abogado: ')

    desde = fields.Date(string='DESDE: ')

    hasta = fields.Date(string='HASTA: ')


    renglon = fields.Integer()
    clave = fields.Char()

    tcli = fields.Char()  # TODO: Utilizamos este campo, solamente para imporat los logs. luego de importar los logs comentamos este campo y utilizamos el campo computado.
    # tcli = fields.Char(compute='_get_tcli')


    cia = fields.Char(default='')
    codtran = fields.Char(default='*L')    

    ea = fields.Boolean() #status del abogado. 1 si esta activo o con el poder de una demanda. 0 si ya ha pasado el periodo en el cual el fue responsable por esta demanda.

    def _get_context_demanda_id(self):
        parent_id = self.env.context.get('parent_id')
        parent_model = self.env.context.get('parent_model')

        if parent_id and parent_model:
            default_value = parent_id 
            return default_value
        return None


    def _get_cta_cliente(self):          
        demandas_model =  self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')        
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntacliente
    
    def _get_tcli(self):
        demandas_model =  self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')        
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.tcli = demanda_activa.tcli