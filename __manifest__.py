{
    'name': 'Legal',
    'summary': """
    Modulo desarrollado para digitalizar los registros fiscales.
    """,
    'author': 'Grupo Saleta',
    'category': 'General',
    'version': '1.0.0',
    'depends': ['base','mail'],
    'data': [

        #.............SECURITY
        'security/rf_security.xml', #GROUPS
        'security/ir.model.access.csv', #ACCESS RIGHTS
        
        #.............ACTIONS
        'views/actions/actions.xml', #ACTIONS

        #.............MODEL DEMANDAS VIEWS
        'views/demandas/form-view.xml', #FORM VIEW
        'views/demandas/tree-view.xml', #TREE VIEW
        'views/demandas/kanban-view.xml', #KANBAN VIEW
        'views/demandas/search-view.xml', #SEARCH VIEW        

        #.............MODEL NOTES VIEWS
        'views/notes/rf_notes.xml', # FORM, TREE, KANBAN VIEWS

        #.............MODEL ABOGADOS VIEWS
        'views/abogados/rf_abogados.xml', # FORM, TREE, KANBAN VIEWS

        #.............MODEL JUZGADOS VIEWS
        'views/juzgados/rf_juzgados.xml', # FORM, TREE, KANBAN VIEWS

        #.............MODEL ABOGADOS SUSTITUTOS VIEWS (Sustitucion de abogados)
        'views/abogados_sustitutos/rf_abosust.xml', # FORM, TREE, KANBAN VIEWS

        #.............MODEL BIENES EMBARGABLES VIEWS
        'views/bien_embargable/rf_bienembargable.xml', # FORM, TREE, KANBAN VIEWS
        
        #.............MODEL PROVINCIAS VIEWS (TODO:Este modelo solo es utilizado para objecto de prueba. Finalmente las conexiones a la provincias se haran directamente al modelo Demografía)
        'views/provincias/rf_provincias.xml', # FORM, TREE, KANBAN VIEWS

        #.............MODEL DEMO CLIENTES VIEWS (TODO:Este modelo solo es utilizado para objecto de prueba. Finalmente las conexiones a la provincias se haran directamente al modelo Clientes)
        'views/demo_clientes/demo_clientes.xml', # FORM, TREE, KANBAN VIEWS
        
        #.............VISTA PRINCIPAL DONDE DEFINIMOS EL MENU DE NAVEGACION DEL MODULO.
        'views/main.xml',

    ],
    'installable': True,
    'application': True,
}