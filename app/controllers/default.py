# -*- coding: utf-8 -*-

# ---- example index page ----
def index():
    return locals()

# ---- Action for login/register/etc (required for auth) -----
def user():
    db.auth_user.last_name.readable = db.auth_user.last_name.writable=False

    return dict(form=auth())
