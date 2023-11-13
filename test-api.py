#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpc.client
# Datos de la cadena de conexion
url = 'https://server-10392046.dev.odoo.com/'
db = 'my-database'
username = 'user@correo.com'
password = 'userpassword'
# clave de secreta del usuario
key = 'mysecretky'

# autenticar el usuario
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
print(common.version())

# Obtener los objetos
objects = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
model = 'product.product'
ids = objects.execute_kw(db, uid, password, model, 'search', [[['sale_ok', '=', True]]],)
for product in objects.execute_kw(db, uid, password, model, 'read', [ids], {'fields': ['name', 'list_price', 'default_code']}):
    print(product)
