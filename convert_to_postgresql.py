#!/usr/bin/env python3
"""
Script para convertir el código de MySQL a PostgreSQL
"""

import re

def convert_mysql_to_postgresql(input_file, output_file):
    """Convertir archivo de MySQL a PostgreSQL"""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar imports
    content = content.replace('from flask_mysqldb import MySQL', 'import psycopg2\nimport psycopg2.extras')
    content = content.replace('import MySQLdb.cursors', '')
    
    # Reemplazar configuración de MySQL
    mysql_config = '''# Configuración para InfinityFree
app.config['MYSQL_HOST'] = 'sql106.infinityfree.com'  # Tu host MySQL
app.config['MYSQL_USER'] = 'if0_39568236'             # Tu usuario MySQL
app.config['MYSQL_PASSWORD'] = 'vAf94vGi8kS'          # Tu password MySQL
app.config['MYSQL_DB'] = 'if0_39568236_galvisapp_db'  # Tu nombre de base de datos

app.secret_key = 'tu_clave_secreta_muy_larga_y_segura_para_produccion'

mysql = MySQL(app)'''
    
    postgres_config = '''# Configuración para Render con PostgreSQL
app.config['POSTGRES_HOST'] = os.environ.get('MYSQL_HOST', 'dpg-d23qq2muk2gs738r9nag-a')
app.config['POSTGRES_USER'] = os.environ.get('MYSQL_USER', 'galvisapp_db_ko5j_user')
app.config['POSTGRES_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'eHdExi5SX9PTAr2BfUfJMv0Kke7fGpRd')
app.config['POSTGRES_DB'] = os.environ.get('MYSQL_DB', 'galvisapp_db_ko5j')
app.config['POSTGRES_PORT'] = '5432'

app.secret_key = os.environ.get('SECRET_KEY', 'galvisapp2025secretkey')

def get_db_connection():
    """Crear conexión a PostgreSQL"""
    return psycopg2.connect(
        host=app.config['POSTGRES_HOST'],
        database=app.config['POSTGRES_DB'],
        user=app.config['POSTGRES_USER'],
        password=app.config['POSTGRES_PASSWORD'],
        port=app.config['POSTGRES_PORT']
    )'''
    
    content = content.replace(mysql_config, postgres_config)
    
    # Reemplazar conexiones de base de datos
    content = re.sub(r'mysql\.connection\.cursor\(MySQLdb\.cursors\.DictCursor\)', 
                    'get_db_connection()\n        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)', content)
    
    content = re.sub(r'mysql\.connection\.cursor\(\)', 
                    'get_db_connection()\n        cur = conn.cursor()', content)
    
    # Reemplazar commits y closes
    content = content.replace('mysql.connection.commit()', 'conn.commit()')
    content = content.replace('mysql.connection.close()', 'conn.close()')
    
    # Agregar conn.close() después de cada operación
    content = re.sub(r'(conn\.commit\(\)\n\s+)(flash\(.*?\)\n\s+return)', 
                    r'\1conn.close()\n        \2', content)
    
    # Cambiar TRUE/FALSE para PostgreSQL
    content = content.replace("'Sí'", 'TRUE')
    content = content.replace("'No'", 'FALSE')
    content = content.replace("1", 'TRUE')
    content = content.replace("0", 'FALSE')
    
    # Agregar import os
    if 'import os' not in content:
        content = content.replace('from flask import', 'import os\nfrom flask import')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Conversión completada: {output_file}")

if __name__ == "__main__":
    convert_mysql_to_postgresql('inicio.py', 'app_postgresql_complete.py') 