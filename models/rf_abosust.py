import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta


class AbogadosSustitutos(models.Model):
    
    _name = 'rf.abosust'

    _rec_name = 'id'
    
    demanda_id = fields.Char(default='_get_context_demanda_id')
    

    cntacliente = fields.Char() # TODO:
    # cntacliente = fields.Char(compute='_get_cta_cliente')



    abogado_descripcion = fields.Many2one('rf.abogados')

    desde = fields.Date('DESDE: ')

    hasta = fields.Date('HASTA: ')


    renglon = fields.Integer()
    clave = fields.Char()

    tcli = fields.Char()  # TODO:
    # tcli = fields.Char(compute='_get_tcli') #TODO: Para import la data, es necesario utilizar el campo como fields.Char() y luego comentarlo y descomentarr la el campo como fields.Char(compute=''). Esto es xq necesitamos tenerlo como compute para poder computar los valores a la hora de crear los records pero como los campos computes no nos permiten importar data entonces necestimos compentarlo y utilizar la opcion no computada a la hora de importar la data.


    cia = fields.Char(default='')
    codtran = fields.Char(default='*L')


    # abogado_nombre = fields.Char(related='abogado_id.nombre')

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
        # demandas_all = demandas_model.search([])
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntacliente
    
    def _get_tcli(self):
        demandas_model =  self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        # demandas_all = demandas_model.search([])
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.tcli = demanda_activa.tcli