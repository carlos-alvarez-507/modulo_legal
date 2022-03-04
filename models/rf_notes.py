import string
from odoo import models, fields, api

from datetime import datetime, date, timedelta

import dateutil.parser
# b = "2015-10-28 16:09:59"
# d = dateutil.parser.parse(b).date()


class Notas(models.Model):

    _name = 'rf.notes'

    _rec_name = 'id'

    _order = 'creacion_fecha desc'

    # libro_fecha = fields.Date(default=fields.Date.today, string='FECHA: ')

    # ..............................................................................................................................Demanda ID
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

    # ..............................................................................................................................Cuenta Cliente

    def _get_cntacliente_from_rfdemanda(self):
        demandas_model = self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntacliente

    cntacliente = fields.Char()  # TODO:
    # cntacliente = fields.Char(compute='_get_cntacliente_from_rfdemanda')

    # ..............................................................................................................................Notes
    notes = fields.Html(string='OBERVACIONES: ')

    # ..............................................................................................................................Fecha Registro y tiempo de creacion
    @api.depends('abogado_logger_name')
    def _create_date_compute(self):
        return fields.Datetime.today() #- timedelta(days=2)
        # for item in self:
        # resto 7 dias a la fecha de creacion solo para test
        # item.creacion_fecha = fields.Datetime.today() - timedelta(days=2)
        # item.creacion_fecha =  fields.Date.today() #  Fecha correcta de creacion de la nota
        # item.creacion_fecha =  self.create_date.date() - timedelta(days=7) #  tomamos la fecha de creacion del campo create_date y restamos 7 dias
        # item.creacion_fecha =  self.create_date.date() #  tomamos la fecha de creacion del campo create_date sin restarle 7 dias.

    creacion_fecha = fields.Datetime() #TODO:
    # creacion_fecha = fields.Datetime(default=_create_date_compute, store=True)  # fecha de creacion


    @api.depends('creacion_fecha')
    def _create_age_of_creation(self):
        for item in self:
            if item.creacion_fecha:
                item.age_of_creation = (
                    fields.Datetime.today() - self.creacion_fecha).days
            else:
                item.age_of_creation = 0

    age_of_creation = fields.Integer() #TODO:
    # age_of_creation = fields.Integer(compute=_create_age_of_creation, store=True)  # dias de creacion

    # ......................................................................................................................Usuario

    def _get_user_name(self):
        return self.env.user.name

    def _get_user_id(self):
        return self.env.user.id

    # abogado_logger_name = fields.Char() #TODO:
    abogado_logger_name = fields.Char(default=_get_user_name)

    # abogado_logger_uid = fields.Char() #TODO:
    abogado_logger_uid = fields.Char(default=_get_user_id)

    # ..........................................................................................................................Cuenta del prestamo
    # cntaprestamo = fields.Char()

    def _get_cntaprestamo_from_rfdemanda(self):
        demandas_model = self.env['rf.demandas']
        parent_id = self.env.context.get('parent_id')
        demanda_activa = demandas_model.search([('id', '=', parent_id)])
        self.cntacliente = demanda_activa.cntaprestamo

    # TODO: Este campo debe ser computado tomando la cuenta prestamos directamente de la columna de cntaprestamo de la tabla de rf_demandas.
    cntaprestamo = fields.Char()
    # cntaprestamo = fields.Char(compute='_get_cntaprestamo_from_rfdemanda')

    # .......................................................................................................................... Code Tab
    codtab = fields.Char()

    # .......................................................................................................................... State -> Update de status of the notes so that it can be editable or not by users.
    # TODO: Recordar confirmar el tiempo exacto en el cual las notas pasan a ser no editables para actualiarlo en esta condicion

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

    tcli = fields.Char() #TODO:
    # tcli = fields.Char(compute='_get_tcli')  # TODO: Para import la data, es necesario utilizar el campo como fields.Char() y luego comentarlo y descomentarr la el campo como fields.Char(compute=''). Esto es xq necesitamos tenerlo como compute para poder computar los valores a la hora de crear los records pero como los campos computes no nos permiten importar data entonces necestimos compentarlo y utilizar la opcion no computada a la hora de importar la data.

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

    tcli_desc = fields.Char()  # TODO:
    # tcli_desc = fields.Char(compute='_compute_tcli_desc')

    # .......................................................................................................................... sist
    sist = fields.Char()

    # .......................................................................................................................... cia
    cia = fields.Char()

    # .......................................................................................................................... codtran
    codtran = fields.Char()

    # .......................................................................................................................... clave
    clave = fields.Char()
