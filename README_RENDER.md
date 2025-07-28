# 🚀 Guía para subir GalvisApp a Render.com

## 📋 Pasos para subir tu aplicación

### 1. Crear cuenta en Render.com
1. Ve a [render.com](https://render.com)
2. Haz clic en **"Get Started"** o **"Sign Up"**
3. Regístrate con tu email o GitHub
4. Verifica tu cuenta

### 2. Crear base de datos MySQL
1. En Render, ve a **"New"** → **"PostgreSQL"** (Render usa PostgreSQL, pero es compatible)
2. Elige un nombre: `galvisapp-db`
3. Selecciona el plan gratuito
4. Anota los datos de conexión que te den

### 3. Crear aplicación web
1. En Render, ve a **"New"** → **"Web Service"**
2. Conecta tu repositorio de GitHub (si lo tienes) o sube los archivos
3. Configura:
   - **Name:** `galvisapp`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### 4. Configurar variables de entorno
En tu aplicación web, ve a **"Environment"** y agrega:
```
MYSQL_HOST=tu_host_de_render
MYSQL_USER=tu_usuario
MYSQL_PASSWORD=tu_password
MYSQL_DB=tu_base_de_datos
```

### 5. ¡Listo!
Tu aplicación estará disponible en: `https://galvisapp.onrender.com`

## ⚠️ Notas importantes

- **Primer usuario:** El primer usuario que se registre será el administrador
- **Base de datos:** Render usa PostgreSQL, pero Flask-MySQLdb es compatible
- **Dominio:** Tu app tendrá un dominio gratuito de Render

## 🔧 Archivos necesarios

- ✅ `app.py` - Tu aplicación Flask
- ✅ `requirements.txt` - Dependencias
- ✅ `render.yaml` - Configuración de Render
- ✅ `Procfile` - Comando de inicio
- ✅ `templates/` - Plantillas HTML

¡Tu GalvisApp estará funcionando en la nube! 🌐 