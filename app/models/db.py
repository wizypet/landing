# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.15.5":
    raise HTTP(500, "Requires web2py 2.15.5 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

db = DAL(configuration.get('db.uri'),
            pool_size=configuration.get('db.pool_size'),
            migrate_enabled=configuration.get('db.migrate'),
            check_reserved=['all'])

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = 'bootstrap4_inline'
response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------

def Hidden(*a,**b):
    b["writable"]=b["readable"]=False
    return Field(*a,**b)

auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
mail.settings.sender = configuration.get('smtp.sender')
mail.settings.login = configuration.get('smtp.login')
mail.settings.tls = configuration.get('smtp.tls') or False
mail.settings.ssl = configuration.get('smtp.ssl') or False

auth.settings.login_next = URL(c='app', f='user_pets')
auth.settings.change_password_next = URL(c='app', f='user_pets')
auth.settings.register_next = URL('app', 'register_info')
auth.settings.remember_me_form = True

auth.messages.login_log = 'Conectado com Sucesso'
auth.messages.logout_log = 'Desconectado com Sucesso'
# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')
response.show_toolbar = configuration.get('app.toolbar')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
if configuration.get('scheduler.enabled'):
    from gluon.scheduler import Scheduler
    scheduler = Scheduler(db, heartbeat=configuration.get('scheduler.heartbeat'))

# -------------------------------------------------------------------------
# tables
# -------------------------------------------------------------------------

db.define_table('user_state', 
    Field('state_name', 'string', label=T('Estado:')),
    Field('state_short_name', 'string', label=T('UF:')),
    format='%(state_name)s'
)

db.define_table('user_city', 
    Field('city_name', 'string', label=T('Cidade:')),
    Field('cit_state_id', 'reference user_state', label=T('Estado:')),
    format='%(city_name)s'
)

db.define_table('user_info', 
    Field('name_1', 'string', label=T('Nome do tutor:')),
    Field('name_2', 'string', label=T('Nome do tutor secundário:')),
    Field('phone_1', 'string', label=T('Telefone 1:')),
    Field('phone_2', 'string', label=T('Telefone 2:')),
    Field('zip_code', 'string', label=T('CEP:')),
    Field('street', 'string', label=T('Rua:')),
    Field('home_number', 'integer', label=T('Número:')),
    Field('optional', 'string', label=T('Complemento:')),
    Field('neighborhood', 'string', label=T('Bairro:')),
    Field('user_state', 'reference user_state', label=T('Estado:')),
    Field('user_city', 'reference user_city', label=T('Cidade:')),
    Field('user_id', 'integer')
)

db.define_table('race', 
    Field('race_name', 'string', label=T('Raça:')),
    Field("race_species", label=T('Espécie:'), requires=IS_IN_SET([("1",T("Cachorro")),("2",T("Gato")),("3",T("Outro"))], zero=T("Selecione"))),
    format='%(race_name)s'
)

db.define_table('pet', 
    Field('pet_image', 'upload'),
    Field('pet_name', 'string', label=T('Nome:')),
    Field('pet_species', label=T('Espécie:'), requires=IS_IN_SET([("1",T("Cachorro")),("2",T("Gato")),("3",T("Outro"))], zero=T("Selecione"))),
    Field('pet_gender', label=T('Sexo:'), requires=IS_IN_SET([("male",T("Macho")),("female",T("Fêmea"))], zero=T("Selecione"))),
    Field('pet_birth', 'date', label=T('Data de Nascimento:')),
    Field('pet_race', 'reference race', label=T('Raça:')),
    Field('pet_size', label=T('Porte:'), requires=IS_IN_SET([
                                    ("1", T("Micro Toy (até 2 kg)")),
                                    ("2", T("Toy (2 - 5 kg)")),
                                    ("3", T("Pequeno (5 - 10 kg)")),
                                    ("4", T("Médio (10 - 20 kg)")),
                                    ("5", T("Grande (20 - 40 kg)")),
                                    ("6", T("Muito Grande (+ 40 kg)"))
                                ], zero=T("Selecione"))),
    Field('pet_microchip', 'string', label=T('Nº do Microchip:')),
    Field('pet_tag', 'string', label=T('WizyPet Tag ID:')),
    Field('pet_castrated', 'boolean', label=T('Castrado')),
    Field('pet_people_friendly', 'boolean', label=T('Amigável com pessoas')),
    Field('pet_animal_friendly', 'boolean', label=T('Amigável com outros animais')),
    Field('pet_trained', 'boolean', label=T('Adestrado')),
    Field('pet_rabies_vaccine', 'boolean', label=T('Vacina antirrábica')),
    Field('pet_v_vaccine', 'boolean', label=T('Vacina V8 e V10')),
    Field('pet_owner', 'integer')
)

db.define_table('pet_service',
    Field('pet_service_1', 'boolean', label=T('Banho e Tosa')),
    Field('pet_service_2', 'boolean', label=T('Hospedagem')),
    Field('pet_service_3', 'boolean', label=T('Clínico e Veterinário')),
    Field('pet_service_4', 'boolean', label=T('Adestramento')),
    Field('user_id', 'integer'),
)
