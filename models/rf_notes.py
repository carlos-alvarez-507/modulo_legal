import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta

import dateutil.parser

class Notas(models.Model):

    _name = 'rf.notes'

    _rec_name = 'id'

    _order = 'creacion_fecha desc'

    # ..............................................................................................................................Demanda ID
    def _get_demanda_id_from_context(self):
        parent_id = self.env.context.get('parent_id')
        parent_model = self.env.context.get('parent_model')

        if parent_id and parent_model:
            default_value = parent_id  # ... use the parent
            return default_value
        return None
    demanda_id = fields.Char(default='_get_demanda_id_from_context')

    # ..............................................................................................................................Cuenta Cliente

    def _get_cntacliente_from_rfdemanda(self):
        demandas_model = self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntacliente

    cntacliente = fields.Char()  # TODO: Utilizamos este campo para importar los archivos solamente. Luego de importar los archivos entonces comentamos este campo y descomentamos el campo que es computado.
    # cntacliente = fields.Char(compute='_get_cntacliente_from_rfdemanda')

    # ..............................................................................................................................Notes
    notes = fields.Html(string='OBERVACIONES: ')

    # ..............................................................................................................................Fecha Registro y tiempo de creacion
    @api.depends('abogado_logger_name')
    def _create_date_compute(self):
        for item in self:
            item.creacion_fecha =  fields.Date.today()

    creacion_fecha = fields.Datetime() #TODO: Utilizamos este campo para importar los archivos solamente.. Luego de imporat los archivos entonces comentamos este campo y descomentamos el campo que es computado.
    # creacion_fecha = fields.Datetime(compute=_create_date_compute, store=True)  # fecha de creacion



    # ..............................................................................................................................Tiempo de creacion de la nota
    @api.depends('creacion_fecha')
    def _create_age_of_creation(self):
        for item in self:
            if item.creacion_fecha:
                item.age_of_creation = (
                    fields.Datetime.today() - self.creacion_fecha).days
            else:
                item.age_of_creation = 0

    age_of_creation = fields.Integer() #TODO: utilizamos este campo para importar los archivos solamente. Luego de importar los archivos entonces comentamos este campo y descomentamos el campo que es computado.
    # age_of_creation = fields.Integer(compute=_create_age_of_creation, store=True)  # dias de creacion

    # ......................................................................................................................Usuario
    def _get_user_name(self):
        return self.env.user.name

    def _get_user_id(self):
        return self.env.user.id

    abogado_logger_name = fields.Char(default=_get_user_name)
    
    abogado_logger_uid = fields.Char(default=_get_user_id)

    # ..........................................................................................................................Cuenta del prestamo    
    def _get_cntaprestamo_from_rfdemanda(self):
        demandas_model = self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntaprestamo
   
    cntaprestamo = fields.Char() #TODO: La cuenta normalmente es ingresada por el usuario desde la UI. Pero tambien podemos computarla halando de la tabla de prestamos (Esto puede ser implementado a futuro).
    # cntaprestamo = fields.Char(compute='_get_cntaprestamo_from_rfdemanda')

    # .......................................................................................................................... Code Tab
    codtab = fields.Char()

    # .......................................................................................................................... State: este campo depende de la cantidad de dias de la creacion de la nota. Indica si el campo puede ser editable o no. 
    # TODO: state indicara el valor editable para la nota hasta los 30 dias. Despues de los 30 dias, state tendra el valor no_editable impidiento que la nota sea editable por el usuario. en el archivo xml la propiedad readonly de la nota depende del campo state.

    @api.depends('age_of_creation')
    def _update_status(self):
        for item in self:
            # confirmar cuantos dias son los aprovados hasta que una nota pueda ser editable.
            if item.age_of_creation <= 30:
                item.state = 'editable'
            else:
                item.state = 'no_editable'

    state = fields.Selection([('editable', 'Editable'), ('no_editable',
                             'No Editable')], compute='_update_status', default='editable')

    # .......................................................................................................................... TCLI
    def _get_tcli(self):
        demandas_model = self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        # demandas_all = demandas_model.search([])
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.tcli = demanda_activa.tcli

    tcli = fields.Char() #TODO: # ESte campo es utilizado al momento de importar los logs. Luego de importar los logs entonces lo comentamos y utilizamos el campo computado.
    # tcli = fields.Char(compute='_get_tcli')  

    # .......................................................................................................................... TCLI DESCRIPCION

    @api.depends('tcli')
    def _compute_tcli_desc(self):
        for item in self:
            if item.tcli == 'P':
                item.tcli_desc = 'NATURAL'
            elif item.tcli == 'F':
                item.tcli_desc = 'JURÍDICA'
            else:
                item.tcli_desc = 'CLIENTE ' + str(item.tcli)

    tcli_desc = fields.Char()  # TODO: Este campo es utilizado al momento de importar los logs. Luego de importar los logs entonces lo comentamo y utilizamos el campo computado.
    # tcli_desc = fields.Char(compute='_compute_tcli_desc')

    # .......................................................................................................................... sist
    sist = fields.Char()

    # .......................................................................................................................... cia
    cia = fields.Char()

    # .......................................................................................................................... codtran
    codtran = fields.Char()

    # .......................................................................................................................... clave
    clave = fields.Char()
