#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpc.client
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u', type=str, help='Usuario para la conexion')
parser.add_argument('-p', type=str, help='Contraseña del usuario')
parser.add_argument('-d', type=str, help='Base de datos para la conexion')
parser.add_argument('-url', type=str, help='URL del sistema')
args = parser.parse_args()

if None in [args.u, args.p, args.d, args.url]:
    print("Debe definir todos los argumentos para ejecutar el scritp. \n Ejecute el script con -h para mas detalles")
else:
    # Datos de la cadena de conexion
    url = args.url
    db = args.d
    username = args.u
    password = args.p

    # autenticar el usuario
    common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    print("Conexion realizada al servidor con version %s. "%common.version()['server_version'])

    # Obtener los objetos
    objects = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
    model = 'product.product'
    # LOTE/Nº SERIE             Campo que se tiene en otro tabla de la base datos se busca la mejor solucion para la integracion
    # PRODUCTO                  ???
    # NOMBRE                    name
    # FECHA DE CADUCIDAD
    # MODO DE CONSERVACION      conservation_type
    # INGREDIENTES              ingredients
    # CODIGO DE BARRAS#         barcode
    # REFERENCIA INTERNA#       default_code
    # CANTIDAD#                 qty_available
    # VALOR ENERGETICO (kcal)#  valor_energetico_kcal
    # TOTAL GRASAS (g)#         total_grasas
    # GRASAS SATURADAS (g)#     grasas_saturadas
    # HIDRATOS DE CARBONO#      hidratos_carbono
    # AZUCARES#                 azucares
    # PROTEINAS#                proteinas
    # SAL#                      sal
    ids = objects.execute_kw(db, uid, password, model, 'search', [[['sale_ok', '=', True]]],)
    for product in objects.execute_kw(db, uid, password, model, 'read', [ids],
                                      {'fields': ['name', 'conservation_type', 'ingredients', 'barcode', 'default_code',
                                                  'qty_available', 'list_price', 'valor_energetico_kcal', 'total_grasas',
                                                  'grasas_saturadas', 'hidratos_carbono', 'azucares', 'proteinas', 'sal']}):
        print(product)
