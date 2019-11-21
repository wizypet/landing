# -*- coding: utf-8 -*-

def tag():
    return locals()

def verify_tag():
    tag_num = request.vars.tag
    select_tag = db(db.pet.pet_tag == tag_num).count()

    if select_tag:
        redirect(URL(c='app', f='show_pet', args=tag_num))
    else:
        redirect(URL(c='app', f='login_register'))

def login_register():
    return locals()

@auth.requires_login()
def register_info():
    form = SQLFORM(db.user_info)
    form.element(_name="user_id")["_value"] = auth.user.id
    form.element(_name="user_id")["_type"] = 'hidden'

    if form.process().accepted:
        redirect(URL(c='app', f='add_pet', args=[auth.user.id, 'first']))
    elif form.errors:
        response.flash = T('Verifique os erros abaixo.')

    return locals()

@auth.requires_login()
def add_pet():
    form = SQLFORM(db.pet)
    form.element(_name="pet_owner")["_value"] = auth.user.id
    form.element(_name="pet_owner")["_type"] = 'hidden'
    form.element(_type="submit")["_value"] = 'Próximo'

    if form.process().accepted:
        redirect(URL(c='app', f='add_service', args=[auth.user.id, 'first']))
    elif form.errors:
        response.flash = T('Verifique os erros abaixo.')

    return locals()

@auth.requires_login()
def add_service():
    form = SQLFORM(db.pet_service)
    form.element(_name="user_id")["_value"] = auth.user.id
    form.element(_name="user_id")["_type"] = 'hidden'
    form.element(_type="submit")["_value"] = 'Próximo'

    if form.process().accepted:
        redirect(URL(c='app', f='finish_registration', args=[auth.user.id, 'first']))
    elif form.errors:
        response.flash = T('Selecione um dos itens abaixo, ou clique em "Pular".')

    return locals()

@auth.requires_login()
def finish_registration():
    first = request.args(1) or 0
    if first:
        redirect(URL(c='app', f='welcome', args=[auth.user.id]))
    else:
        redirect(URL(c='app', f='user_pets', args=[auth.user.id]))

@auth.requires_login()
def welcome():
    mail.send(auth.user.email,'Bem Vindo a Plataforma da Wizy','Conteúdo do email personalizado com as mensagens de boas vindas!')
    return locals()

@auth.requires_login()
def user_pets():
    record = db.user_info(db.user_info.user_id == auth.user.id)
    form = SQLFORM(db.user_info, record)
    form.element(_type="submit")["_value"] = 'Salvar'

    pets = db(db.pet.pet_owner == auth.user.id).select(
        db.pet.pet_name,
        db.pet.pet_image
    )

    if form.process().accepted:
        response.flash = T('Dados Pessoais salvos com sucesso')
    elif form.errors:
        response.flash = T('Verifique os erros abaixo')

    return locals()

def show_pet():
    pet_infos = db(db.pet.pet_tag == request.args(0)).select(db.pet.pet_tag)
    return locals()

def download():
    return response.download(request, db)
