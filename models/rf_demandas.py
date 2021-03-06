from email.policy import default
from re import S
import string
from this import d
from odoo import models, fields, api


class Demandas(models.Model):

    _name = 'rf.demandas'
    _description = 'Demandas'
    _rec_name = 'id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'fecha_demanda desc'


    # Estados Legales de las demandas
    state = fields.Selection([
                              ('status_0', 'Sin Observación'),
                              ('status_1', 'Por admisión de demanda   '),
                              ('status_3', 'Por consignación de fianza'),
                              ('status_2', 'Por monto de fianza'),
                              ('status_4', 'Por oficio de secuestro'),
                              ('status_5', 'Por solicitar ampliación de secuestro'),
                              ('status_6', 'Por salir oficio de ampliación de secuestro'),
                              ('status_7', 'Por corrección oficio de secuestro'),
                              ('status_8', 'Por notificación cliente'),
                              ('status_9', 'Por envío notificación por ccj'),
                              ('status_10','Por respuesta de ccj'),
                              ('status_11','Por envío de boleta con la policia'),
                              ('status_12','Por respuesta de la policia'),
                              ('status_13','Por envío comisión a otro juzgado'),
                              ('status_14','Por respuesta de comisión enviada'),
                              ('status_15','Por solicitar emplazamiento por edicto'),
                              ('status_16','Por aprobar en juzg. Emplazamiento por edicto'),
                              ('status_17','Por oficio de embargo'),
                              ('status_18','Por corrección oficio de embargo'),
                              ('status_19','Por oficio de entrega de sumas retenidas'),
                              ('status_20','Por solicitar ampliación de embargo'),
                              ('status_21','Por salir oficio de ampliación de embargo'),
                              ('status_22','Por devolución de fianza'),
                              ('status_23','Por corrección devolución de fianza'),
                              ('status_24','Por oficio de embargo y devolución de fianza'),
                              ('status_25','Por solicitud remate finca'),
                              ('status_26','Por realizar avalúo finca'),
                              ('status_27','Por dar fecha de remate finca'),
                              ('status_28','Por solicitar desistimiento'),
                              ('status_29','Por salir desistimiento'),
                              ('status_30','Por resolver recurso apelación'),
                              ('status_31','Por resolver excepción'),
                              ('status_32','Salió embargo y está pendiente devolución fianza'),
                              ('status_33','Salió embargo'),
                              ('status_34','Embargo reflejado en ct y se efectúa dto'),
                              ('status_35','Embargo pendiente')                       
                            ]
                            , tracking=True, string='Estado Legal',help='This is some help!!',)   
  
    header_vibility = fields.Boolean(help='This is some help!',default=False)



    # .................................................................................................................................... Demandas
    archivo_origen = fields.Char(help='This is some help',)
    fecha_reg = fields.Date(string='Fecha de registro')    
    cedula = fields.Many2one(
        comodel_name='demo.clientes', string='No. ID', store=True
    )# Cedula es el No. ID
    cip = fields.Char(help='This is some help', related='cedula.ruced', store=True)    
    title_demanda = fields.Char(help='This is some help', compute='_compute_title', store=True)    
    tcli = fields.Char(help='This is some help', related='cedula.tipo', string='Cliente') # El tcli puede ser P para Cliente Publido, F para Cliente Juridico    
    tcli_desc = fields.Char(help='This is some help', compute='_compute_tcli_desc', string='Cliente')    # TCLI DESCRIPCION   
    codigo_demanda = fields.Char(help='This is some help', compute='_compute_codigo_demanda', string='Código de Demanda') # el codigo de la demanda es el id
    cntacliente = fields.Char(help='This is some help', 
        related='cedula.ctacliente', string='Regitro'
    )  # La cuenta cliente es lo que aparece como numero de registro, podemos halar esta cuenta de la tabla de clientes.
    cntaprestamo = fields.Char(help='This is some help', string='Cuenta de Prestamo', default=' ') # trabajar en la relacion de la cuenta prestamo. # fields.Char(help='This is some help', compute='_get_cnta_prestamo') # Crear esta funcion de llegar a ser necesario    
    ck_crear = fields.Boolean(help='This is some help!',string='Mostrar')  
    demanda_nombre = fields.Char(help='This is some help', compute='_compute_demanda', string='Demanda')    
    sucursal = fields.Many2one('res.company', string='Sucursal')  
    code_sucursal = fields.Integer(help='This is some help!!', related='sucursal.id')
    abogado = fields.Many2one(comodel_name='rf.abogados', string='Abogado'  , help='Hola esto es un mensaje de ayuda')
    cliente_nombre = fields.Char(help='This is some help', 
       related='cedula.nombre', string='Nombre del Cliente'
    )            
    provincia = fields.Many2one(comodel_name='rf.provincias') # fields.Many2one('fc.dirprov') #TODO: ESTA LA CORRECTA RELACION DE PROVINCIA. Esta es la tabla que ha creado Robinson del lado del model demografica   
    juzgado = fields.Many2one(comodel_name='rf.juzgados', string='Juzgado')# RELACIONAR ESTE CAMPO CON LA TABLA DE JUZGADOS (ACTUALIZR EL LOG DE DEMANDAS PARA QUE APUNTEN AL CODIGO CORECTO ESTABLECIDO POR ROBINSON Y ACTUALIZAR EL LOG DE JUZGADOS PARA QUE TAMBIEN CONTANGAN EL CODIGO CORRECT ESTABLECIDO POR ROBINSON EN LAS COLUMNAS DE PROVINCIAS, ETC)    
    ck_sol_sec = fields.Boolean(help='This is some help!',
        string='Solicitud de Secuestro')
    fecha_demanda = fields.Date(string='Fecha de Demanda')
    monto_demanda = fields.Float(string='Monto $')
    admitida = fields.Boolean(help='This is some help!',string='Admitida')
    admitida_desc = fields.Text(help='This is some help!!', string='Admitida Descripción') # fields.Html(string='Admitida Descripción')    
    no_admitida = fields.Boolean(help='This is some help!',string='No Admitida')
    no_adm_desc = fields.Text(help='This is some help!!', string='No Admitida Descripción')    
    abogados_sustitutos_ids = fields.One2many(
        'rf.abosust', 'demanda_id', string='Abogado') # Este campo apunta al id de record en la tabla rf_abosust la cual este vinculada a la demanda por el demanda_id
    


    # .................................................................................................................................... Secuestros
    sec_fianza = fields.Boolean(help='This is some help!',string='Fianza', )
    sec_fecha_consignacion = fields.Date(string='Consignación')
    sec_fc_visivility = fields.Boolean(help='This is some help!',)
    sec_devolucion_fianza = fields.Boolean(help='This is some help!',string='Devolución Fianza', )
    sec_devolucion_fianza_fecha = fields.Date(string='Fecha')
    sec_df_visivility = fields.Boolean(help='This is some help!',)
    sec_fianza_monto = fields.Float(string='Monto $')
    sec_fecha_retiro = fields.Date(string='Fecha Retiro')
    sec_fr_visivility = fields.Boolean(help='This is some help!',)
    sec_fecha_auto = fields.Date(string='Fecha Auto')
    sec_fa_visivility = fields.Boolean(help='This is some help!',)
    sec_fecha_oficio = fields.Date(string='Fecha Oficio')
    sec_fo_visivility = fields.Boolean(help='This is some help!',)
    sec_num_auto = fields.Char(help='This is some help', string='No. Auto')
    sec_num_oficio = fields.Char(help='This is some help', string='No. Oficio')
    sec_costa = fields.Float(string='Costas $')
    sec_total = fields.Float(string='Total $')


    # .................................................................................................................................... Bienes 
    bienes = fields.Boolean(help='This is some help!',string='Bienes a Embargar o Secuestrar', )
    bien_finca_prop = fields.Boolean(help='This is some help!',string='Finca o Propiedades')
    bien_salario = fields.Boolean(help='This is some help!',string='Salario')
    bien_ambos = fields.Boolean(help='This is some help!',string='Ambos')
    ckopbien = fields.Integer(help='This is some help!!', )
    bien_desc = fields.Text(help='This is some help!!', )
    bien_salario_type = fields.Many2one(comodel_name='rf.bienembargable')
    bien_planilla_type = fields.Selection([('planillaa', '(idPlanilla)'), ('planillab', 'Contraloria'), (
        'planillac', 'Caja Seguro Social'), ('planillad', 'Empresa Privada')], help='This is some help!!')
    bien_planilla_id = fields.Char(help='This is some help', string='ID Planilla')
    bien_ministerio = fields.Char(help='This is some help', string='Ministerio')
    bien_planilla = fields.Char(help='This is some help', string='Planilla')
    bien_posicion = fields.Char(help='This is some help', string='Posición')


    # .................................................................................................................................... Notificaciones
    notificacion = fields.Boolean(help='This is some help!',
        string='Notificación', default=False, store=True)
    noti_fecha = fields.Date(string='Fecha')
    noti_nf_visivility = fields.Boolean(help='This is some help!',)
    noti_client = fields.Boolean(help='This is some help!',string='Cliente')
    noti_emplazamiento = fields.Boolean(help='This is some help!',string='Emplazamiento')
    noti_abogado = fields.Boolean(help='This is some help!',string='Abogado')
    ckopnotif = fields.Integer(help='This is some help!!', )
    noti_abogado_nombre = fields.Char(help='This is some help', string='Nombre')
    noti_transaction = fields.Boolean(help='This is some help!',string='Transacción')
    noti_transaction_fecha = fields.Date(string='Fecha')
    noti_tf_visivility = fields.Boolean(help='This is some help!',)
    noti_solicitud = fields.Boolean(help='This is some help!',
        string='Solicitud a Elevar Embargo y Devolución de Fianza')
    noti_solicitud_fecha = fields.Date(string='Fecha')
    noti_sf_visivility = fields.Boolean(help='This is some help!',)
    noti_denuncia_bienes = fields.Boolean(help='This is some help!',string='Denuncia de Bienes')
    noti_db_fecha = fields.Date(string='Fecha')
    noti_db_visivility = fields.Boolean(help='This is some help!',string='Fecha')

    # .................................................................................................................................... Embargos
    embargo_visibility = fields.Boolean(help='This is some help!',
        string='Embargo', store=True)    
    estado = fields.Selection([('estado_proceso', 'En Proceso'),('estado_embargo', 'En Embargo')], help='This is some help!!', default='estado_proceso', string='Estado', compute='_update_estado', inverse='_inverse_estado', groups='modulo_legal.grupo_registros_fiscales_admin')
    emb_fecha_retiro = fields.Date(string='Fecha Retiro')
    emb_fr_visivility = fields.Boolean(help='This is some help!',)
    emb_fecha_auto = fields.Date(string='Fecha Auto')
    emb_fa_visivility = fields.Boolean(help='This is some help!',)
    emb_num_auto = fields.Char(help='This is some help', string='No. Auto')
    emb_fecha_oficio = fields.Date(string='Fecha Oficio')
    emb_fo_visivility = fields.Boolean(help='This is some help!',)
    emb_num_oficio = fields.Char(help='This is some help', string='No. Oficio')
    emb_costas = fields.Float(string='Costas $')
    emb_total = fields.Float(string='Total $')
    adj_finca = fields.Boolean(help='This is some help!',string='Adjudicación de Finca')
    adj_finca_fecha_retiro = fields.Date(string='Fecha Retiro')
    adj_finca_fr_visivility = fields.Boolean(help='This is some help!',)
    adj_emb_fecha_auto_st = fields.Date(string='Fecha Auto')
    adj_emb_fa_visivility_st = fields.Boolean(help='This is some help!',)
    adj_emb_fecha_auto_nd = fields.Date(string='Fecha Auto')
    adj_emb_fa_visivility_nd = fields.Boolean(help='This is some help!',)
    adj_num_auto_st = fields.Char(help='This is some help', string='No. Auto')
    adj_num_auto_nd = fields.Char(help='This is some help', string='No. Auto')
    adj_costas = fields.Float(string='Costas $')
    adj_total = fields.Float(string='Total $')
    adj_finca_fecha_solic_remate = fields.Date(
        string='Solicitud Remate')
    adj_finca_fs_visivility = fields.Boolean(help='This is some help!',)
    adj_finca_fecha_remate_juzgado = fields.Date(
        string='Remate Juzgado')
    adj_finca_rj_visivility = fields.Boolean(help='This is some help!',)
    monto_base_remate = fields.Float(string='Monto Base Remate')


    # .................................................................................................................................... Ampliaciones 
    amp_emb = fields.Boolean(help='This is some help!',string='Ampliación de Embargo', )
    ae_retiro = fields.Date(string='Fecha Retiro')
    ae_retiro_visivility = fields.Boolean(help='This is some help!',)
    ae_fecha_auto = fields.Date(string='Fecha Auto')
    ae_fa_visivility = fields.Boolean(help='This is some help!',)
    ae_fecha_oficio = fields.Date(string='Fecha Oficio')
    ae_fo_visivility = fields.Boolean(help='This is some help!',)
    ae_num_auto = fields.Char(help='This is some help', string='No. Auto')
    ae_num_oficio = fields.Char(help='This is some help', string='No. Oficio')
    ae_bien_ampliar = fields.Text(help='This is some help!!', string='Bien a Ampliar')
    amp_sec = fields.Boolean(help='This is some help!',string='Amplicación de Secuestro', )
    as_fr = fields.Date(string='Fecha Retiro')
    as_fr_visivility = fields.Boolean(help='This is some help!',)
    as_fecha_auto = fields.Date(string='Fecha Auto')
    as_fa_visivility = fields.Boolean(help='This is some help!',)
    as_fecha_oficio = fields.Date(string='Fecha Oficio')
    as_fo_visivility = fields.Boolean(help='This is some help!',)
    as_num_auto = fields.Char(help='This is some help', string='No. Auto')
    as_num_oficio = fields.Char(help='This is some help', string='No. Oficio')
    as_bien_ampliar = fields.Text(help='This is some help!!', string='Bien a Secuestrar')


    # .................................................................................................................................... Fin / En Cierre?
    fin_cerrar_archivar = fields.Boolean(help='This is some help!',string='Cerrar y Archivar Proceso')
    fin_cancel_deuda = fields.Boolean(help='This is some help!',string='Por Cancelación Deuda')
    fin_cancelacion = fields.Date(string='Cancelación')
    fin_c_visivility = fields.Boolean(help='This is some help!',)
    fin_efectivo = fields.Boolean(help='This is some help!',string='Efectivo')
    fin_cheque = fields.Boolean(help='This is some help!',string='Cheque')
    fin_deposito_judicial = fields.Boolean(help='This is some help!',string='Deposito Judicial')    
    optcancel = fields.Integer(help='This is some help!!', )
    fin_solic_desistimiento = fields.Date(string='Solicitud Desistimiento')
    fin_sd_visivility = fields.Boolean(help='This is some help!',)
    fin_oficio_desistimiento = fields.Date(string='Oficio Desistimiento')
    fin_of_visivility = fields.Boolean(help='This is some help!',)    
    fin_env_emp = fields.Boolean(help='This is some help!',)
    fin_env_emp_fecha = fields.Date(string='Envia la Empresa')
    fin_env_emp_visibility = fields.Boolean(help='This is some help!',)
    fin_retira_cliente = fields.Boolean(help='This is some help!',string='Retira Cliente')
    optejedesisti = fields.Integer(help='This is some help!!', )
    fin_retiro_dem = fields.Boolean(help='This is some help!',
        string='Por Retiro de Demanda (Antes de Admisión)')        
    fin_rdem_solic = fields.Date(string='Solicitud: ')
    fin_rdem_solic_visivility = fields.Boolean(help='This is some help!',)
    fin_entrega_desgl_prueb = fields.Date(string='Entrega Desglose Pruebas: ')
    fin_entrega_desgl_prueb_visivility = fields.Boolean(help='This is some help!',)


    # .................................................................................................................................... Libro Legal
    nota_id = fields.One2many('rf.notes', 'demanda_id', string='Notes: ')

   
    # .................................................................................................................................... Columnas generales o internas
    codtran = fields.Char(help='This is some help', )
    status = fields.Char(help='This is some help', )
    renglon = fields.Char(help='This is some help', )
    tags = fields.Char(help='This is some help', )
    clave = fields.Char(help='This is some help', )
    cambios = fields.Char(help='This is some help', )




    #.................................................................................................................................... Funciones utilizadas para computad algunos campos

    # Computamos el titulo de la demanda
    @api.depends('codigo_demanda')
    def _compute_title(self):
        for item in self:                          
            item.title_demanda = 'Demanda No. ' + str(item.codigo_demanda) + '        '  + str(item.cip) + '        ' + str(item.cliente_nombre) + '        $' + str(item.monto_demanda)

    def myfn(self):
        if self.header_vibility:
            self.header_vibility = False
        else:
            self.header_vibility = True

    @api.depends('tcli')
    def _compute_tcli_desc(self):
        for item in self:
            if item.tcli == 'P':
                item.tcli_desc = 'NATURAL'
            elif item.tcli == 'F':
                item.tcli_desc = 'JURÍDICA'
            else:
                item.tcli_desc = ''                

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
            item.demanda_nombre = 'Demanda: [' + str(item.fecha_demanda) + '] ' + str(item.monto_demanda) + ' <' + str(item.code_sucursal) + '>'

    def _update_estado(self):
        for item in self:
            if item.embargo_visibility:            
                item.estado = 'estado_embargo'
            else:
                item.estado = 'estado_proceso'    

    def _inverse_estado(self):
        for item in self:
            if item.embargo_visibility:      
                item.embargo_visibility = False
            else:
                item.embargo_visibility = True 