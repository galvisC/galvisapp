-- Script para crear las tablas en PostgreSQL
-- Ejecutar en DBeaver conectado a tu base de datos de Render

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    es_admin BOOLEAN DEFAULT FALSE,
    aprobado BOOLEAN DEFAULT FALSE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de gastos Carnicería 88
CREATE TABLE IF NOT EXISTS carniceria_88_gastos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ventas Carnicería 88
CREATE TABLE IF NOT EXISTS carniceria_88_ventas (
    id SERIAL PRIMARY KEY,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de menudos Carnicería 88
CREATE TABLE IF NOT EXISTS carniceria_88_menudos (
    id SERIAL PRIMARY KEY,
    cantidad INTEGER NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de pollo/menudencias Carnicería 88
CREATE TABLE IF NOT EXISTS carniceria_88_pollo (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL, -- 'Pollo' o 'Menudencia'
    cantidad DECIMAL(10,2) NOT NULL,
    precio_total DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de gastos Fama 46
CREATE TABLE IF NOT EXISTS fama_46_gastos (
    id SERIAL PRIMARY KEY,
    descripcion TEXT NOT NULL,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ventas Fama 46
CREATE TABLE IF NOT EXISTS fama_46_ventas (
    id SERIAL PRIMARY KEY,
    monto DECIMAL(15,2) NOT NULL,
    fecha DATE NOT NULL,
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de ganado Fama 46
CREATE TABLE IF NOT EXISTS fama_46_ganado (
    id SERIAL PRIMARY KEY,
    fecha_compra DATE NOT NULL,
    dueno VARCHAR(100),
    peso_kg DECIMAL(10,2) NOT NULL,
    precio_kg DECIMAL(15,2) NOT NULL,
    precio_total DECIMAL(15,2) NOT NULL,
    pago VARCHAR(5) DEFAULT 'No',
    usuario_id INTEGER REFERENCES usuarios(id),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 