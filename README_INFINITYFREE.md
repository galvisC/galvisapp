# 🚀 Guía para subir GalvisApp a InfinityFree

## 📋 Pasos para subir tu aplicación

### 1. Crear cuenta en InfinityFree
1. Ve a [infinityfree.net](https://infinityfree.net)
2. Haz clic en "Create Account" o "Registrarse"
3. Completa el formulario de registro
4. Verifica tu email

### 2. Crear hosting gratuito
1. Inicia sesión en tu cuenta
2. Ve a "Create Account" (crear cuenta de hosting)
3. Elige tu dominio gratuito:
   - **Opción 1:** `tuusuario.infinityfreeapp.com`
   - **Opción 2:** `tuusuario.epizy.com`
   - **Recomendado:** `galvisapp.infinityfreeapp.com`
4. Selecciona el plan gratuito
5. Completa la creación

### 3. Configurar base de datos MySQL
1. En tu panel de control de InfinityFree, ve a "MySQL Databases"
2. Crea una nueva base de datos
3. Anota estos datos:
   - **Host:** `sql.infinityfree.com` (o el que te den)
   - **Usuario:** `tu_usuario_mysql`
   - **Password:** `tu_password_mysql`
   - **Base de datos:** `tu_base_de_datos`

### 4. Crear las tablas en la base de datos
1. Ve a "phpMyAdmin" en tu panel
2. Selecciona tu base de datos
3. Ejecuta estos comandos SQL:

```sql
-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    es_admin TINYINT(1) DEFAULT 0,
    aprobado TINYINT(1) DEFAULT 0,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tablas para Carnicería 88
CREATE TABLE carniceria_88_gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE carniceria_88_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE carniceria_88_menudos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad INT NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE carniceria_88_pollo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad_kg DECIMAL(10,2) NOT NULL,
    precio_total DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE carniceria_88_menudencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cantidad_kg DECIMAL(10,2) NOT NULL,
    precio_total DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- Tablas para Fama 46
CREATE TABLE fama_46_gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE fama_46_ventas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE fama_46_ganado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_compra DATE NOT NULL,
    dueno VARCHAR(100),
    peso_kg DECIMAL(10,2) NOT NULL,
    precio_kg DECIMAL(15,2) NOT NULL,
    precio_total DECIMAL(15,2) NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

### 5. Configurar archivos para subir
1. **Edita el archivo `app.py`:**
   - Cambia las credenciales de MySQL con las que te dio InfinityFree
   - Reemplaza:
     ```python
     app.config['MYSQL_HOST'] = 'sql.infinityfree.com'  # Tu host
     app.config['MYSQL_USER'] = 'tu_usuario_mysql'      # Tu usuario
     app.config['MYSQL_PASSWORD'] = 'tu_password_mysql' # Tu password
     app.config['MYSQL_DB'] = 'tu_base_de_datos'        # Tu base de datos
     ```

### 6. Subir archivos via FTP
1. En tu panel de InfinityFree, ve a "FTP Accounts"
2. Crea una cuenta FTP
3. Descarga un cliente FTP como FileZilla
4. Conéctate con los datos FTP que te dieron
5. Sube estos archivos a la carpeta `htdocs`:
   - `app.py`
   - `requirements.txt`
   - Carpeta `templates/` (completa)
   - Carpeta `static/` (si tienes archivos estáticos)

### 7. Activar la aplicación
1. En tu panel de InfinityFree, ve a "Domains"
2. Tu aplicación estará disponible en tu dominio
3. La primera vez que accedas, se instalará automáticamente

## ⚠️ Notas importantes

- **Primer usuario:** El primer usuario que se registre será automáticamente el administrador
- **Aprobación:** Los usuarios nuevos necesitan aprobación del admin
- **Base de datos:** Asegúrate de crear todas las tablas antes de usar la app
- **Archivos:** Todos los archivos HTML deben estar en la carpeta `templates/`

## 🔧 Solución de problemas

- **Error de conexión a BD:** Verifica las credenciales en `app.py`
- **Página en blanco:** Revisa los logs de error en el panel de InfinityFree
- **Archivos no encontrados:** Asegúrate de subir todos los archivos a `htdocs`

## 📞 Soporte

Si tienes problemas, revisa:
1. Los logs de error en tu panel de InfinityFree
2. Que todas las tablas estén creadas correctamente
3. Que las credenciales de MySQL sean correctas

¡Tu GalvisApp estará funcionando en la nube! 🌐 