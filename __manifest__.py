{
    'name': 'Registros Fiscales',
    'summary': """
    Modulo desarrollado para digitalizar los registros fiscales.
    """,
    'author': 'Grupo Saleta',
    'category': 'General',
    'version': '1.0.0',
    'depends': [],
    'data': [
        'security/rf_security.xml',
        'security/ir.model.access.csv',
        'views/actions/actions.xml',
        'views/demandas/form-view.xml',
        'views/demandas/tree-view.xml',
        'views/demandas/kanban-view.xml',
        'views/demandas/search-view.xml',
        'views/demo_partner.xml',
        'views/notes/rf_notes.xml',
        'views/abogados/rf_abogados.xml',
        'views/juzgados/rf_juzgados.xml',
        'views/abogados_sustitutos/rf_abosust.xml',
        'views/bien_embargable/rf_bienembargable.xml',
        'views/corregimientos/rf_corregimientos.xml',
        'views/distritos/rf_distritos.xml',
        'views/provincias/rf_provincias.xml',
        'views/demo_clientes/demo_clientes.xml',
        'views/main.xml',
    ],
}