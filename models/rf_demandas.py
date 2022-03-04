from email.policy import default
from re import S
import string
from this import d
from odoo import models, fields, api


class Demandas(models.Model):

    _name = 'rf.demandas'
    _description = 'Demandas'
    _rec_name = 'id'

    # _order = 'fecha_demanda desc'

    # .................................................................................................................................... demandas

    # archivo del cual tomamos los datos para consolidar todas los maestros de demandas.
    archivo_origen = fields.Char()



    fecha_reg = fields.Date(string='Fecha de registro ')

    # Cedula es el No. ID
    cedula = fields.Many2one(
        comodel_name='demo.clientes', string='No. ID', store=True
    )

    cip = fields.Char(related='cedula.ruced', store=True)

    @api.depends('codigo_demanda')
    def _compute_title(self):
        for item in self:               
            # item.title = 'Demanda No. ' + str(item.codigo_demanda) + '    -    ' + str(item.cip) + '    -    ' + str(item.cliente_nombre) + '    -    ' + str(item.monto_demanda)
            item.title_demanda = 'Demanda No. ' + str(item.codigo_demanda) + '        '  + str(item.cip) + '        ' + str(item.cliente_nombre) + '        $' + str(item.monto_demanda)

    title_demanda = fields.Char(compute='_compute_title', store=True)

    # tcli = fields.Selection([('P', 'Natural'), ('F', 'Jurídica')], string='CLIENTE') # TODO:
    tcli = fields.Char(related='cedula.tipo', string='Cliente')

    # .......................................................................................................................... TCLI DESCRIPCION   
    @api.depends('tcli')
    def _compute_tcli_desc(self):
        for item in self:
            if item.tcli == 'P':
                item.tcli_desc = 'NATURAL'
            elif item.tcli == 'F':
                item.tcli_desc = 'JURÍDICA'
            else:
                item.tcli_desc = ''
                
    tcli_desc = fields.Char(compute='_compute_tcli_desc', string='Tipo de Cliente')
    

    # codigo_demanda = fields.Char(default='test')
    codigo_demanda = fields.Char(compute='_compute_codigo_demanda', string='Código de Demanda') # el codigo de la demanda es el id
    # id

    cntacliente = fields.Char(
        related='cedula.ctacliente', string='Numero de Regitro'
    )  # La cuenta cliente es lo que aparece como numero de registro, podemos halar esta cuenta de la tabla de clientes.



    cntaprestamo = fields.Char(string='Cuenta de Prestamo') #TODO: trabajar en la relacion de la cuenta prestamo
    # cntaprestamo = fields.Char(compute='_get_cnta_prestamo') #TODO: Crear esta funcion de llegar a ser necesario


    ck_crear = fields.Boolean(string='Mostrar / Crear')

    # ---------------------------------------------------------------COMPUTAR ESTE CAMPO TODO:
    # demanda_nombre = fields.Selection([('demandaa', 'demanda A'), ('demandab', 'demanda B')], 'DEMANDA: ')
    demanda_nombre = fields.Char(compute='_compute_demanda')

    # ------------------------------------------------------------------RELACIONAR ESTE CAMPO CON LA TABLA DE SUCURSALES (ACTUALIZR EL LOG DE DEMANDAS PARA QUE APUNTEN AL CODIGO CORECTO ESTABLECIDO POR ROBINSON)
    # sucursal = fields.Selection([('sucursala', 'sucursal A'), ('sucursalb', 'sucursal B')], 'SUCURSAL: ')
    sucursal = fields.Many2one('res.company', string='Sucursal')
    # sucursal = fields.Char(related='sucursal_name.id', string='SUCURSAL NUMERO: ') # TODO: actualizar este campo para que apunte al campo correct el cual no es id sino numero_empresa   
    

    code_sucursal = fields.Integer(related='sucursal.id')

    abogado = fields.Many2one(comodel_name='rf.abogados', string='Abogado')

    cliente_nombre = fields.Char(
       related='cedula.nombre', string='Nombre del Cliente'
    )

    # --------------------------------------------------------------------RELACIONAR ESTE CAMPO CON LA TABLA DE PROVINCIAS (ACTUALIZR EL LOG DE DEMANDAS PARA QUE APUNTEN AL CODIGO CORECTO ESTABLECIDO POR ROBINSON)
    # provincia = fields.Selection([('provinciaa', 'Provincia A'), ('provinciab', 'Provincia B')], 'PROVINCIA: ')
    # provincia = fields.Many2one('fc.dirprov') #TODO: ESTA LA CORRECTA RELACION DE PROVINCIA. Esta es la tabla que ha creado Robinson del lado del model demografica
    provincia = fields.Many2one(comodel_name='rf.provincias')

    # --------------------------------------------------------------------RELACIONAR ESTE CAMPO CON LA TABLA DE JUZGADOS (ACTUALIZR EL LOG DE DEMANDAS PARA QUE APUNTEN AL CODIGO CORECTO ESTABLECIDO POR ROBINSON Y ACTUALIZAR EL LOG DE JUZGADOS PARA QUE TAMBIEN CONTANGAN EL CODIGO CORRECT ESTABLECIDO POR ROBINSON EN LAS COLUMNAS DE PROVINCIAS, ETC)
    # juzgado = fields.Selection([('juzgadoa', 'Juzgado A'), ('juzgadob', 'Juzgado B')], string='JUSGADO: ')
    # juzgado = fields.Selection([('juzgadoa', 'Juzgado A'), ('juzgadob', 'Juzgado B')], string='JUSGADO: ')
    juzgado = fields.Many2one(comodel_name='rf.juzgados', string='Juzgado')

    # solicitud_sec_visivility = fields.Boolean(
    ck_sol_sec = fields.Boolean(
        string='Solicitud de Secuestro')

    fecha_demanda = fields.Date(string='Fecha de Demanda')

    monto_demanda = fields.Float(string='Monto $')

    admitida = fields.Boolean(string='Admitida')

    admitida_desc = fields.Text(string='Admitida Descripción')

    no_admitida = fields.Boolean(string='No Admitida')

    no_adm_desc = fields.Text(string='No Admitida Descripción')

    # --------------------------------------------- Este campo apunta al id de la file localizada en la tabla rf_abosust la cual este vinculada a la demanda por el demanda_id
    # necesito importar las tabla de abogados sustitutos manteniendo la relacion por el codigo y tambien mantener una relacion por el.
    # Recordar importar las tablas de observaciones/notas para el tab Fin al final.
    abogados_sustitutos_ids = fields.One2many(
        'rf.abosust', 'demanda_id', string='Abogado')

    # .................................................................................................................................... Secuestros

    sec_fianza = fields.Boolean(string='Fianza', )
    sec_fecha_consignacion = fields.Date(string='Consignación')
    sec_fc_visivility = fields.Boolean()
    sec_devolucion_fianza = fields.Boolean(string='Devolución Fianza', )
    sec_devolucion_fianza_fecha = fields.Date(string='Fecha')
    sec_df_visivility = fields.Boolean()
    sec_fianza_monto = fields.Float(string='Monto $')

    sec_fecha_retiro = fields.Date(string='Fecha Retiro')
    sec_fr_visivility = fields.Boolean()

    sec_fecha_auto = fields.Date(string='Fecha Auto')
    sec_fa_visivility = fields.Boolean()
    sec_fecha_oficio = fields.Date(string='Fecha Oficio')
    sec_fo_visivility = fields.Boolean()
    sec_num_auto = fields.Char(string='No. Auto')
    sec_num_oficio = fields.Char(string='No. Oficio')

    sec_costa = fields.Float(string='Costas $')
    sec_total = fields.Float(string='Total $')

    # .................................................................................................................................... Bienes // agregar los campos que yo he definido para poder manejar los radio button campos.

    bienes = fields.Boolean(string='Bienes a Embargar o Secuestrar', )

    bien_finca_prop = fields.Boolean(string='Finca o Propiedades')
    bien_salario = fields.Boolean(string='Salario')
    bien_ambos = fields.Boolean(string='Ambos')

    ckopbien = fields.Integer()

    bien_desc = fields.Text()

    bien_salario_type = fields.Many2one(comodel_name='rf.bienembargable')

    bien_planilla_type = fields.Selection([('planillaa', '(idPlanilla)'), ('planillab', 'Contraloria'), (
        'planillac', 'Caja Seguro Social'), ('planillad', 'Empresa Privada')])

    bien_planilla_id = fields.Char(string='ID Planilla')

    bien_ministerio = fields.Char(string='Ministerio')

    bien_planilla = fields.Char(string='Planilla')

    bien_posicion = fields.Char(string='Posición')

    # .................................................................................................................................... Notificaciones

    notificacion = fields.Boolean(
        string='Notificación', default=False, store=False)
    noti_fecha = fields.Date(string='Fecha')
    noti_nf_visivility = fields.Boolean()

    noti_client = fields.Boolean(string='Cliente')
    noti_emplazamiento = fields.Boolean(string='Emplazamiento')
    noti_abogado = fields.Boolean(string='Abogado')
    ckopnotif = fields.Integer()

    noti_abogado_nombre = fields.Char(string='Nombre')
    noti_transaction = fields.Boolean(string='Transacción')
    noti_transaction_fecha = fields.Date(string='Fecha')
    noti_tf_visivility = fields.Boolean()
    noti_solicitud = fields.Boolean(
        string='Solicitud a Elevar Embargo y Devolución de Fianza')
    noti_solicitud_fecha = fields.Date(string='Fecha')
    noti_sf_visivility = fields.Boolean()
    noti_denuncia_bienes = fields.Boolean(string='Denuncia de Bienes')
    noti_db_fecha = fields.Date(string='Fecha')
    noti_db_visivility = fields.Boolean(string='Fecha')

    # .................................................................................................................................... Embargos

    embargo_visibility = fields.Boolean(
        string='Embargo', default=False, store=False)
    emb_fecha_retiro = fields.Date(string='Fecha Retiro')
    emb_fr_visivility = fields.Boolean()

    emb_fecha_auto = fields.Date(string='Fecha Auto')
    emb_fa_visivility = fields.Boolean()
    emb_num_auto = fields.Char(string='No. Auto')
    emb_fecha_oficio = fields.Date(string='Fecha Oficio')
    emb_fo_visivility = fields.Boolean()
    emb_num_oficio = fields.Char(string='No. Oficio')

    emb_costas = fields.Float(string='Costas $')
    emb_total = fields.Float(string='Total $')

    adj_finca = fields.Boolean(string='Adjudicación de Finca')
    adj_finca_fecha_retiro = fields.Date(string='Fecha Retiro')
    adj_finca_fr_visivility = fields.Boolean()

    adj_emb_fecha_auto_st = fields.Date(string='Fecha Auto')
    adj_emb_fa_visivility_st = fields.Boolean()

    adj_emb_fecha_auto_nd = fields.Date(string='Fecha Auto')
    adj_emb_fa_visivility_nd = fields.Boolean()

    adj_num_auto_st = fields.Char(string='No. Auto')
    adj_num_auto_nd = fields.Char(string='No. Auto')

    adj_costas = fields.Float(string='Costas $')
    adj_total = fields.Float(string='Total $')

    adj_finca_fecha_solic_remate = fields.Date(
        string='Fecha Solicitud Remate')
    adj_finca_fs_visivility = fields.Boolean()
    adj_finca_fecha_remate_juzgado = fields.Date(
        string='Fecha Remate Juzgado')
    adj_finca_rj_visivility = fields.Boolean()
    monto_base_remate = fields.Float(string='Monto Base Remate')

    # .................................................................................................................................... Ampliaciones

    amp_emb = fields.Boolean(string='Ampliación de Embargo', )
    ae_retiro = fields.Date(string='Fecha Retiro')
    ae_retiro_visivility = fields.Boolean()

    ae_fecha_auto = fields.Date(string='Fecha Auto')
    ae_fa_visivility = fields.Boolean()

    ae_fecha_oficio = fields.Date(string='Fecha Oficio')
    ae_fo_visivility = fields.Boolean()

    ae_num_auto = fields.Char(string='No. Auto')
    ae_num_oficio = fields.Char(string='No. Oficio')

    ae_bien_ampliar = fields.Text(string='Bien a Ampliar')

    amp_sec = fields.Boolean(string='Amplicación de Secuestro', )
    as_fr = fields.Date(string='Fecha Retiro')
    as_fr_visivility = fields.Boolean()

    as_fecha_auto = fields.Date(string='Fecha Auto')
    as_fa_visivility = fields.Boolean()

    as_fecha_oficio = fields.Date(string='Fecha Oficio')
    as_fo_visivility = fields.Boolean()

    as_num_auto = fields.Char(string='No. Auto')
    as_num_oficio = fields.Char(string='No. Oficio')

    as_bien_ampliar = fields.Text(string='Bien a Secuestrar')

    # .................................................................................................................................... Fin / En Cierre?

    fin_cerrar_archivar = fields.Boolean(string='Cerrar y Archivar Proceso')

    fin_cancel_deuda = fields.Boolean(string='Por Cancelación Deuda')

    fin_cancelacion = fields.Date(string='Cancelación')

    fin_c_visivility = fields.Boolean()

    # agregar estas columnas al excel.
    fin_efectivo = fields.Boolean(string='Efectivo')
    fin_cheque = fields.Boolean(string='Cheque')
    fin_deposito_judicial = fields.Boolean(string='Deposito Judicial')

    # este campo mantendra el valor de los campos arriba (0, 1, 2)
    optcancel = fields.Integer()

    fin_solic_desistimiento = fields.Date(string='Solicitud Desistimiento')
    fin_sd_visivility = fields.Boolean()
    fin_oficio_desistimiento = fields.Date(string='Oficio Desistimiento')
    fin_of_visivility = fields.Boolean()

    # esta campo junto al campo fin_retira_cliente tambien afectan el campo   optejedesisti
    fin_env_emp = fields.Boolean()
    fin_env_emp_fecha = fields.Date(string='Envia la Empresa')
    fin_env_emp_visibility = fields.Boolean()
    fin_retira_cliente = fields.Boolean(string='Retira Cliente')

    # campo que almacena el valor en la base de datos. el valos depende de si se selecciona fin_env_emp o fin_retira_cliente
    optejedesisti = fields.Integer()

    fin_retiro_dem = fields.Boolean(
        string='Por Retiro de Demanda (Antes de Admisión)')
        
    fin_rdem_solic = fields.Date(string='Solicitud: ')

    fin_rdem_solic_visivility = fields.Boolean()
    fin_entrega_desgl_prueb = fields.Date(string='Entrega Desglose Pruebas: ')
    fin_entrega_desgl_prueb_visivility = fields.Boolean()

    # .................................................................................................................................... Libro

    nota_id = fields.One2many('rf.notes', 'demanda_id', string='Notes: ')

    # .................................................................................................................................... Columnas generales o internas
    codtran = fields.Char()
    status = fields.Char()
    renglon = fields.Char()
    tags = fields.Char()
    clave = fields.Char()
    cambios = fields.Char()


    @api.onchange('admitida')
    def _update_admitida(self):
        if self.admitida:
            self.no_admitida = False
        else:
            self.no_admitida = True
        self.no_adm_desc = ''

    @api.onchange('no_admitida')
    def _update_no_admitida(self):
        if self.no_admitida:
            self.admitida = False
        else:
            self.admitida = True
        self.admitida_desc = ''

    # Bienes a Embargar Checks handlers

    @api.onchange('bien_finca_prop')
    def _bien_finca_prop_onchange_handler(self):
        if self.bien_finca_prop:
            self.bien_salario = False
            self.bien_ambos = False
            self.ckopbien = 0

    @api.onchange('bien_salario')
    def _bien_salario_onchange_handler(self):
        if self.bien_salario:
            self.bien_finca_prop = False
            self.bien_ambos = False
            self.ckopbien = 1

    @api.onchange('bien_ambos')
    def _bien_ambos_onchange_handler(self):
        if self.bien_ambos:
            self.bien_finca_prop = False
            self.bien_salario = False
            self.ckopbien = 2

  # Notificacion Checks handlers

    @api.onchange('noti_client')
    def _noti_client_onchange_handler(self):
        if self.noti_client:
            self.noti_emplazamiento = False
            self.noti_abogado = False

    @api.onchange('noti_emplazamiento')
    def _noti_emplazamiento_onchange_handler(self):
        if self.noti_emplazamiento:
            self.noti_client = False
            self.noti_abogado = False

    @api.onchange('noti_abogado')
    def _noti_abogado_onchange_handler(self):
        if self.noti_abogado:
            self.noti_client = False
            self.noti_emplazamiento = False

    # En Cierra / Fin  Checks handlers

    @api.onchange('fin_cancel_deuda')
    def _fin_cancel_deuda_onchange_handler(self):
        if self.fin_cancel_deuda:
            self.fin_retiro_dem = False
            self.fin_retiro_dem = False
            self.fin_rdem_solic = ''
            self.fin_rdem_solic_visivility = False
            self.fin_entrega_desgl_prueb = ''
            self.fin_entrega_desgl_prueb_visivility = False

    @api.onchange('fin_retiro_dem')
    def _fin_retiro_dem_onchange_handler(self):
        if self.fin_retiro_dem:
            self.fin_cancel_deuda = False
            self.fin_cancelacion = ''
            self.fin_c_visivility = False
            self.fin_efectivo = False
            self.fin_cheque = False
            self.fin_deposito_judicial = False
            self.fin_solic_desistimiento = ''
            self.fin_sd_visivility = False
            self.fin_oficio_desistimiento = ''
            self.fin_of_visivility = False
            self.fin_env_emp = False
            self.fin_env_emp_fecha = ''
            self.fin_env_emp_visibility = False
            self.fin_retira_cliente = False

    @api.onchange('fin_efectivo')
    def _fin_efectivo_onchange_handler(self):
        if self.fin_efectivo:
            self.fin_cheque = False
            self.fin_deposito_judicial = False

    @api.onchange('fin_cheque')
    def _fin_cheque_onchange_handler(self):
        if self.fin_cheque:
            self.fin_efectivo = False
            self.fin_deposito_judicial = False

    @api.onchange('fin_deposito_judicial')
    def _fin_deposito_judicial_onchange_handler(self):
        if self.fin_deposito_judicial:
            self.fin_efectivo = False
            self.fin_cheque = False

    @api.onchange('fin_env_emp')
    def _fin_env_emp_onchange_handler(self):
        if self.fin_env_emp:
            self.fin_retira_cliente = False

    @api.onchange('fin_retira_cliente')
    def _fin_retira_cliente_onchange_handler(self):
        if self.fin_retira_cliente:
            self.fin_env_emp = False
            self.fin_env_emp_fecha = ''
            self.fin_env_emp_visibility = False

    # Compute codigo demanda
    def _compute_codigo_demanda(self):
        for item in self:
            item.codigo_demanda = str(item.id)

    # Compute demanda nombre
    def _compute_demanda(self):
        for item in self:
            item.demanda_nombre = 'Demanda: [' + str(item.fecha_demanda) + '] ' + str(item.monto_demanda) + ' <' + str(item.code_sucursal) + '>' # TODO: Necesito tomar el codigo de la compañia y concatenarlo