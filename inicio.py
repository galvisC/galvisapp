from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'

# Configuración de conexión con MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Cali2424*'
app.config['MYSQL_DB'] = 'flaskapp'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        hash_pass = generate_password_hash(password)
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existe = cur.fetchone()
        if existe:
            flash('El correo ya está registrado', 'danger')
            return redirect(url_for('registro'))
        # Verificar si es el primer usuario
        cur.execute('SELECT COUNT(*) FROM usuarios')
        total = cur.fetchone()[0]
        if total == 0:
            # Primer usuario: admin y aprobado
            cur.execute('INSERT INTO usuarios (nombre, email, password, es_admin, aprobado) VALUES (%s, %s, %s, 1, 1)', (nombre, email, hash_pass))
            mysql.connection.commit()
            flash('¡Registro exitoso! Eres el administrador principal.', 'success')
            return redirect(url_for('login'))
        else:
            # Usuarios normales
            cur.execute('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)', (nombre, email, hash_pass))
            mysql.connection.commit()
            flash('Registro exitoso. Espera la aprobación del administrador.', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cur.fetchone()
        if user and check_password_hash(user['password'], password):
            if not user['aprobado']:
                flash('Tu cuenta aún no ha sido aprobada por el administrador.', 'warning')
                return redirect(url_for('login'))
            session['usuario_id'] = user['id']
            session['nombre'] = user['nombre']
            session['es_admin'] = user['es_admin']
            flash('Bienvenido, ' + user['nombre'], 'success')
            return redirect(url_for('panel'))
        else:
            flash('Correo o contraseña incorrectos', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/panel')
def panel():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('panel.html', nombre=session['nombre'], es_admin=session['es_admin'])

@app.route('/admin/usuarios')
def admin_usuarios():
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM usuarios WHERE aprobado = 0')
    pendientes = cur.fetchall()
    return render_template('admin_usuarios.html', pendientes=pendientes)

@app.route('/admin/aprobar/<int:user_id>')
def aprobar_usuario(user_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('UPDATE usuarios SET aprobado = 1 WHERE id = %s', (user_id,))
    mysql.connection.commit()
    flash('Usuario aprobado correctamente', 'success')
    return redirect(url_for('admin_usuarios'))

@app.route('/carniceria88')
def carniceria88():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('carniceria88.html')

@app.route('/fama46')
def fama46():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('fama46.html')

@app.route('/finca_esmeralda')
def finca_esmeralda():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('finca_esmeralda.html')

@app.route('/arriendos')
def arriendos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    return render_template('arriendos.html')

@app.route('/carniceria88/gastos/editar/<int:gasto_id>', methods=['GET', 'POST'])
def editar_gasto_c88(gasto_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('UPDATE carniceria_88_gastos SET descripcion=%s, monto=%s, fecha=%s, pago=%s WHERE id=%s',
                    (descripcion, monto, fecha, pago, gasto_id))
        mysql.connection.commit()
        flash('Gasto editado correctamente', 'success')
        return redirect(url_for('carniceria88_gastos'))
    cur.execute('SELECT * FROM carniceria_88_gastos WHERE id = %s', (gasto_id,))
    gasto = cur.fetchone()
    return render_template('editar_gasto_c88.html', gasto=gasto)

@app.route('/carniceria88/gastos/borrar/<int:gasto_id>')
def borrar_gasto_c88(gasto_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carniceria_88_gastos WHERE id = %s', (gasto_id,))
    mysql.connection.commit()
    flash('Gasto borrado correctamente', 'success')
    return redirect(url_for('carniceria88_gastos'))

# Actualizar consulta de gastos para incluir el id
@app.route('/carniceria88/gastos', methods=['GET', 'POST'])
def carniceria88_gastos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('INSERT INTO carniceria_88_gastos (descripcion, monto, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                    (descripcion, monto, fecha, pago, session['usuario_id']))
        mysql.connection.commit()
        flash('Gasto agregado correctamente', 'success')
        return redirect(url_for('carniceria88_gastos'))
    # Mostrar todos los gastos con el nombre del usuario que los agregó
    cur.execute('''
        SELECT cg.id, cg.descripcion, cg.monto, cg.fecha, cg.pago, u.nombre as usuario_nombre 
        FROM carniceria_88_gastos cg 
        JOIN usuarios u ON cg.usuario_id = u.id 
        ORDER BY cg.fecha DESC
    ''')
    gastos = cur.fetchall()
    cur.execute("SELECT SUM(monto) as total FROM carniceria_88_gastos WHERE pago = 'Sí'")
    total_gastos = cur.fetchone()['total'] or 0
    return render_template('carniceria88_gastos.html', gastos=gastos, total_gastos=total_gastos)

@app.route('/carniceria88/ventas/editar/<int:venta_id>', methods=['GET', 'POST'])
def editar_venta_c88(venta_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        monto = request.form['monto']
        fecha = request.form['fecha']
        cur.execute('UPDATE carniceria_88_ventas SET monto=%s, fecha=%s WHERE id=%s', (monto, fecha, venta_id))
        mysql.connection.commit()
        flash('Venta editada correctamente', 'success')
        return redirect(url_for('carniceria88_ventas'))
    cur.execute('SELECT * FROM carniceria_88_ventas WHERE id = %s', (venta_id,))
    venta = cur.fetchone()
    return render_template('editar_venta_c88.html', venta=venta)

@app.route('/carniceria88/ventas/borrar/<int:venta_id>')
def borrar_venta_c88(venta_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carniceria_88_ventas WHERE id = %s', (venta_id,))
    mysql.connection.commit()
    flash('Venta borrada correctamente', 'success')
    return redirect(url_for('carniceria88_ventas'))

@app.route('/carniceria88/menudos', methods=['GET', 'POST'])
def carniceria88_menudos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('INSERT INTO carniceria_88_menudos (cantidad, monto, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                    (cantidad, monto, fecha, pago, session['usuario_id']))
        mysql.connection.commit()
        flash('Menudo agregado correctamente', 'success')
        return redirect(url_for('carniceria88_menudos'))
    # Mostrar todos los menudos con el nombre del usuario que los agregó
    cur.execute('''
        SELECT cm.id, cm.cantidad, cm.monto, cm.fecha, cm.pago, u.nombre as usuario_nombre 
        FROM carniceria_88_menudos cm 
        JOIN usuarios u ON cm.usuario_id = u.id 
        ORDER BY cm.fecha DESC
    ''')
    menudos = cur.fetchall()
    cur.execute("SELECT SUM(cantidad) as total_cantidad FROM carniceria_88_menudos")
    total_cantidad = cur.fetchone()['total_cantidad'] or 0
    cur.execute("SELECT SUM(monto) as total_monto FROM carniceria_88_menudos WHERE pago = 'Sí'")
    total_monto = cur.fetchone()['total_monto'] or 0
    return render_template('carniceria88_menudos.html', menudos=menudos, total_cantidad=total_cantidad, total_monto=total_monto)

@app.route('/carniceria88/menudos/editar/<int:menudo_id>', methods=['GET', 'POST'])
def editar_menudo_c88(menudo_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        cantidad = request.form['cantidad']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('UPDATE carniceria_88_menudos SET cantidad=%s, monto=%s, fecha=%s, pago=%s WHERE id=%s',
                    (cantidad, monto, fecha, pago, menudo_id))
        mysql.connection.commit()
        flash('Menudo editado correctamente', 'success')
        return redirect(url_for('carniceria88_menudos'))
    cur.execute('SELECT * FROM carniceria_88_menudos WHERE id = %s', (menudo_id,))
    menudo = cur.fetchone()
    return render_template('editar_menudo_c88.html', menudo=menudo)

@app.route('/carniceria88/menudos/borrar/<int:menudo_id>')
def borrar_menudo_c88(menudo_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carniceria_88_menudos WHERE id = %s', (menudo_id,))
    mysql.connection.commit()
    flash('Menudo borrado correctamente', 'success')
    return redirect(url_for('carniceria88_menudos'))

@app.route('/carniceria88/pollo/editar/<int:pollo_id>', methods=['GET', 'POST'])
def editar_pollo_c88(pollo_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM carniceria_88_pollo WHERE id = %s', (pollo_id,))
    pollo = cur.fetchone()
    if request.method == 'POST':
        tipo = request.form['tipo_compra']
        cantidad_kg = request.form['cantidad_kg']
        precio_total = request.form['precio_total']
        fecha = request.form['fecha']
        pago = request.form['pago']
        if tipo == 'pollo':
            cur.execute('UPDATE carniceria_88_pollo SET cantidad_kg=%s, precio_total=%s, fecha=%s, pago=%s WHERE id=%s',
                        (cantidad_kg, precio_total, fecha, pago, pollo_id))
        else:
            # Mover a menudencias
            cur.execute('INSERT INTO carniceria_88_menudencias (cantidad_kg, precio_total, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                        (cantidad_kg, precio_total, fecha, pago, pollo['usuario_id']))
            cur.execute('DELETE FROM carniceria_88_pollo WHERE id = %s', (pollo_id,))
        mysql.connection.commit()
        flash('Compra editada correctamente', 'success')
        return redirect(url_for('carniceria88_pollo'))
    return render_template('editar_pollo_c88.html', compra=pollo, tipo='pollo')

@app.route('/carniceria88/menudencias/editar/<int:menudencia_id>', methods=['GET', 'POST'])
def editar_menudencia_c88(menudencia_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM carniceria_88_menudencias WHERE id = %s', (menudencia_id,))
    menudencia = cur.fetchone()
    if request.method == 'POST':
        tipo = request.form['tipo_compra']
        cantidad_kg = request.form['cantidad_kg']
        precio_total = request.form['precio_total']
        fecha = request.form['fecha']
        pago = request.form['pago']
        if tipo == 'menudencia':
            cur.execute('UPDATE carniceria_88_menudencias SET cantidad_kg=%s, precio_total=%s, fecha=%s, pago=%s WHERE id=%s',
                        (cantidad_kg, precio_total, fecha, pago, menudencia_id))
        else:
            # Mover a pollo
            cur.execute('INSERT INTO carniceria_88_pollo (cantidad_kg, precio_total, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                        (cantidad_kg, precio_total, fecha, pago, menudencia['usuario_id']))
            cur.execute('DELETE FROM carniceria_88_menudencias WHERE id = %s', (menudencia_id,))
        mysql.connection.commit()
        flash('Compra editada correctamente', 'success')
        return redirect(url_for('carniceria88_pollo'))
    return render_template('editar_menudencia_c88.html', compra=menudencia, tipo='menudencia')

@app.route('/carniceria88/pollo/borrar/<int:pollo_id>')
def borrar_pollo_c88(pollo_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carniceria_88_pollo WHERE id = %s', (pollo_id,))
    mysql.connection.commit()
    flash('Compra de pollo borrada correctamente', 'success')
    return redirect(url_for('carniceria88_pollo'))

# Actualizar consultas para incluir el id en ventas, menudos y pollo
@app.route('/carniceria88/ventas', methods=['GET', 'POST'])
def carniceria88_ventas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        monto = request.form['monto']
        fecha = request.form['fecha']
        cur.execute('INSERT INTO carniceria_88_ventas (monto, fecha, usuario_id) VALUES (%s, %s, %s)', (monto, fecha, session['usuario_id']))
        mysql.connection.commit()
        flash('Venta agregada correctamente', 'success')
        return redirect(url_for('carniceria88_ventas'))
    # Mostrar todas las ventas con el nombre del usuario que las agregó
    cur.execute('''
        SELECT cv.id, cv.monto, cv.fecha, u.nombre as usuario_nombre 
        FROM carniceria_88_ventas cv 
        JOIN usuarios u ON cv.usuario_id = u.id 
        ORDER BY cv.fecha DESC
    ''')
    ventas = cur.fetchall()
    cur.execute('SELECT SUM(monto) as total FROM carniceria_88_ventas')
    total_ventas = cur.fetchone()['total'] or 0
    return render_template('carniceria88_ventas.html', ventas=ventas, total_ventas=total_ventas)

@app.route('/carniceria88/pollo', methods=['GET', 'POST'])
def carniceria88_pollo():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Guardar compra (pollo o menudencia)
    if request.method == 'POST':
        tipo = request.form['tipo_compra']
        cantidad_kg = request.form['cantidad_kg']
        precio_total = request.form['precio_total']
        fecha = request.form['fecha']
        pago = request.form['pago']
        if tipo == 'pollo':
            cur.execute('INSERT INTO carniceria_88_pollo (cantidad_kg, precio_total, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                        (cantidad_kg, precio_total, fecha, pago, session['usuario_id']))
        else:
            cur.execute('INSERT INTO carniceria_88_menudencias (cantidad_kg, precio_total, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                        (cantidad_kg, precio_total, fecha, pago, session['usuario_id']))
        mysql.connection.commit()
        flash('Compra agregada correctamente', 'success')
        return redirect(url_for('carniceria88_pollo'))
    # Unificar compras para la tabla con nombres de usuarios
    cur.execute('''
        SELECT cp.id, cp.cantidad_kg, cp.precio_total, cp.fecha, cp.pago, "pollo" as tipo, u.nombre as usuario_nombre 
        FROM carniceria_88_pollo cp 
        JOIN usuarios u ON cp.usuario_id = u.id
    ''')
    pollos = list(cur.fetchall())
    cur.execute('''
        SELECT cm.id, cm.cantidad_kg, cm.precio_total, cm.fecha, cm.pago, "menudencia" as tipo, u.nombre as usuario_nombre 
        FROM carniceria_88_menudencias cm 
        JOIN usuarios u ON cm.usuario_id = u.id
    ''')
    menudencias = list(cur.fetchall())
    compras = pollos + menudencias
    compras.sort(key=lambda x: x['fecha'], reverse=True)
    # Totales pollo
    total_pagado_pollo = sum(float(p['cantidad_kg']) * float(p['precio_total']) for p in pollos if p['pago'] == 'Sí')
    total_pagar_pollo = sum(float(p['cantidad_kg']) * float(p['precio_total']) for p in pollos if p['pago'] == 'No')
    # Totales menudencia
    total_pagado_menudencia = sum(float(m['cantidad_kg']) * float(m['precio_total']) for m in menudencias if m['pago'] == 'Sí')
    total_pagar_menudencia = sum(float(m['cantidad_kg']) * float(m['precio_total']) for m in menudencias if m['pago'] == 'No')
    # Total a pagar general
    total_pagar_general = total_pagar_pollo + total_pagar_menudencia
    return render_template('carniceria88_pollo.html', compras=compras, total_pagado_pollo=total_pagado_pollo, total_pagar_pollo=total_pagar_pollo, total_pagado_menudencia=total_pagado_menudencia, total_pagar_menudencia=total_pagar_menudencia, total_pagar_general=total_pagar_general)

@app.route('/fama46/gastos', methods=['GET', 'POST'])
def fama46_gastos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('INSERT INTO fama_46_gastos (descripcion, monto, fecha, pago, usuario_id) VALUES (%s, %s, %s, %s, %s)',
                    (descripcion, monto, fecha, pago, session['usuario_id']))
        mysql.connection.commit()
        flash('Gasto agregado correctamente', 'success')
        return redirect(url_for('fama46_gastos'))
    # Mostrar todos los gastos con el nombre del usuario que los agregó
    cur.execute('''
        SELECT fg.id, fg.descripcion, fg.monto, fg.fecha, fg.pago, u.nombre as usuario_nombre 
        FROM fama_46_gastos fg 
        JOIN usuarios u ON fg.usuario_id = u.id 
        ORDER BY fg.fecha DESC
    ''')
    gastos = cur.fetchall()
    cur.execute("SELECT SUM(monto) as total FROM fama_46_gastos WHERE pago = 'Sí'")
    total_gastado = cur.fetchone()['total'] or 0
    return render_template('fama46_gastos.html', gastos=gastos, total_gastado=total_gastado)

@app.route('/fama46/gastos/editar/<int:gasto_id>', methods=['GET', 'POST'])
def editar_gasto_f46(gasto_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        monto = request.form['monto']
        fecha = request.form['fecha']
        pago = request.form['pago']
        cur.execute('UPDATE fama_46_gastos SET descripcion=%s, monto=%s, fecha=%s, pago=%s WHERE id=%s',
                    (descripcion, monto, fecha, pago, gasto_id))
        mysql.connection.commit()
        flash('Gasto editado correctamente', 'success')
        return redirect(url_for('fama46_gastos'))
    cur.execute('SELECT * FROM fama_46_gastos WHERE id = %s', (gasto_id,))
    gasto = cur.fetchone()
    return render_template('editar_gasto_f46.html', gasto=gasto)

@app.route('/fama46/gastos/borrar/<int:gasto_id>')
def borrar_gasto_f46(gasto_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM fama_46_gastos WHERE id = %s', (gasto_id,))
    mysql.connection.commit()
    flash('Gasto borrado correctamente', 'success')
    return redirect(url_for('fama46_gastos'))

@app.route('/fama46/ventas', methods=['GET', 'POST'])
def fama46_ventas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        monto = request.form['monto']
        fecha = request.form['fecha']
        cur.execute('INSERT INTO fama_46_ventas (monto, fecha, usuario_id) VALUES (%s, %s, %s)', (monto, fecha, session['usuario_id']))
        mysql.connection.commit()
        flash('Venta agregada correctamente', 'success')
        return redirect(url_for('fama46_ventas'))
    # Mostrar todas las ventas con el nombre del usuario que las agregó
    cur.execute('''
        SELECT fv.id, fv.monto, fv.fecha, u.nombre as usuario_nombre 
        FROM fama_46_ventas fv 
        JOIN usuarios u ON fv.usuario_id = u.id 
        ORDER BY fv.fecha DESC
    ''')
    ventas = cur.fetchall()
    cur.execute('SELECT SUM(monto) as total FROM fama_46_ventas')
    total_ventas = cur.fetchone()['total'] or 0
    return render_template('fama46_ventas.html', ventas=ventas, total_ventas=total_ventas)

@app.route('/fama46/ventas/editar/<int:venta_id>', methods=['GET', 'POST'])
def editar_venta_f46(venta_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        monto = request.form['monto']
        fecha = request.form['fecha']
        cur.execute('UPDATE fama_46_ventas SET monto=%s, fecha=%s WHERE id=%s', (monto, fecha, venta_id))
        mysql.connection.commit()
        flash('Venta editada correctamente', 'success')
        return redirect(url_for('fama46_ventas'))
    cur.execute('SELECT * FROM fama_46_ventas WHERE id = %s', (venta_id,))
    venta = cur.fetchone()
    return render_template('editar_venta_f46.html', venta=venta)

@app.route('/fama46/ventas/borrar/<int:venta_id>')
def borrar_venta_f46(venta_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM fama_46_ventas WHERE id = %s', (venta_id,))
    mysql.connection.commit()
    flash('Venta borrada correctamente', 'success')
    return redirect(url_for('fama46_ventas'))

@app.route('/fama46/ganado', methods=['GET', 'POST'])
def fama46_ganado():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        fecha_compra = request.form['fecha_compra']
        dueno = request.form['dueno']
        peso_kg = request.form['peso_kg']  # NO limpiar, solo tomar el valor tal cual
        precio_kg = limpiar_numero(request.form['precio_kg'])
        pago = request.form['pago']
        try:
            precio_total = float(peso_kg) * precio_kg
        except Exception:
            precio_total = 0
        print('DEBUG peso_kg:', peso_kg)
        print('DEBUG precio_kg:', precio_kg)
        cur.execute('INSERT INTO fama_46_ganado (fecha_compra, dueno, peso_kg, precio_kg, precio_total, pago, usuario_id) VALUES (%s, %s, %s, %s, %s, %s, %s)', (fecha_compra, dueno, peso_kg, precio_kg, precio_total, pago, session['usuario_id']))
        mysql.connection.commit()
        flash('Compra de ganado agregada correctamente', 'success')
        return redirect(url_for('fama46_ganado'))
    # Mostrar todo el ganado con el nombre del usuario que lo agregó
    cur.execute('''
        SELECT fg.id, fg.fecha_compra, fg.dueno, fg.peso_kg, fg.precio_kg, fg.pago, u.nombre as usuario_nombre 
        FROM fama_46_ganado fg 
        JOIN usuarios u ON fg.usuario_id = u.id 
        ORDER BY fg.fecha_compra DESC
    ''')
    ganados = cur.fetchall()
    total_pagado = 0
    total_pendiente = 0
    for ganado in ganados:
        try:
            total = float(ganado['peso_kg']) * float(ganado['precio_kg'])
        except Exception:
            total = 0
        pago_val = (ganado['pago'] or '').strip().lower()
        if pago_val == 'sí':
            total_pagado += total
        else:
            total_pendiente += total
    return render_template('fama46_ganado.html', ganados=ganados, total_pagado=total_pagado, total_pendiente=total_pendiente)

@app.route('/fama46/ganado/editar/<int:ganado_id>', methods=['GET', 'POST'])
def editar_ganado_f46(ganado_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        fecha_compra = request.form['fecha_compra']
        dueno = request.form['dueno']
        peso_kg = request.form['peso_kg']  # NO limpiar, solo tomar el valor tal cual
        precio_kg = limpiar_numero(request.form['precio_kg'])
        pago = request.form['pago']
        try:
            precio_total = float(peso_kg) * precio_kg
        except Exception:
            precio_total = 0
        print('DEBUG peso_kg:', peso_kg)
        print('DEBUG precio_kg:', precio_kg)
        cur.execute('UPDATE fama_46_ganado SET fecha_compra=%s, dueno=%s, peso_kg=%s, precio_kg=%s, precio_total=%s, pago=%s WHERE id=%s', (fecha_compra, dueno, peso_kg, precio_kg, precio_total, pago, ganado_id))
        mysql.connection.commit()
        flash('Compra de ganado editada correctamente', 'success')
        return redirect(url_for('fama46_ganado'))
    cur.execute('SELECT * FROM fama_46_ganado WHERE id = %s', (ganado_id,))
    ganado = cur.fetchone()
    return render_template('editar_ganado_f46.html', ganado=ganado)

@app.route('/fama46/ganado/borrar/<int:ganado_id>')
def borrar_ganado_f46(ganado_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM fama_46_ganado WHERE id = %s', (ganado_id,))
    mysql.connection.commit()
    flash('Compra de ganado borrada correctamente', 'success')
    return redirect(url_for('fama46_ganado'))

@app.route('/carniceria88/menudencias/borrar/<int:menudencia_id>')
def borrar_menudencia_c88(menudencia_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM carniceria_88_menudencias WHERE id = %s', (menudencia_id,))
    mysql.connection.commit()
    flash('Menudencia borrada correctamente', 'success')
    return redirect(url_for('carniceria88_pollo'))

def limpiar_numero(valor):
    try:
        return float(str(valor).replace('.', '').replace(',', ''))
    except Exception:
        return 0

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
