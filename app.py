import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
# import psycopg2
# import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuración para Render con PostgreSQL
app.config['POSTGRES_HOST'] = os.environ.get('MYSQL_HOST', 'dpg-d23qq2muk2gs738r9nag-a.oregon-postgres.render.com')
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
    )



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
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        existe = cur.fetchone()
        if existe:
            flash('El correo ya está registrado', 'danger')
            conn.close()
            return redirect(url_for('registro'))
        
        # Verificar si es el primer usuario
        cur.execute('SELECT COUNT(*) FROM usuarios')
        total = cur.fetchone()[0]
        if total == 0:
            # Primer usuario: admin y aprobado
            cur.execute('INSERT INTO usuarios (nombre, email, password, es_admin, aprobado) VALUES (%s, %s, %s, TRUE, TRUE)', (nombre, email, hash_pass))
            conn.commit()
            conn.close()
            flash('¡Registro exitoso! Eres el administrador principal.', 'success')
            return redirect(url_for('login'))
        else:
            # Usuarios normales
            cur.execute('INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)', (nombre, email, hash_pass))
            conn.commit()
            conn.close()
            flash('Registro exitoso. Espera la aprobación del administrador.', 'success')
            return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        cur.execute('SELECT * FROM usuarios WHERE email = %s', (email,))
        user = cur.fetchone()
        conn.close()
        
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
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM usuarios WHERE aprobado = FALSE')
    pendientes = cur.fetchall()
    conn.close()
    
    return render_template('admin_usuarios.html', pendientes=pendientes)

@app.route('/admin/aprobar/<int:user_id>')
def aprobar_usuario(user_id):
    if 'usuario_id' not in session or not session.get('es_admin'):
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('UPDATE usuarios SET aprobado = TRUE WHERE id = %s', (user_id,))
    conn.commit()
    conn.close()
    
    flash('Usuario aprobado exitosamente', 'success')
    return redirect(url_for('admin_usuarios'))

# Rutas para las páginas principales
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
