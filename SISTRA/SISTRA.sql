-- SCHEMA: public

-- DROP SCHEMA public ;

CREATE SCHEMA public
    AUTHORIZATION postgres;

COMMENT ON SCHEMA public
    IS 'standard public schema';

GRANT ALL ON SCHEMA public TO postgres;

GRANT ALL ON SCHEMA public TO PUBLIC;

-- Crear tabla correlativos_pago
CREATE TABLE IF NOT EXISTS correlativos_pago (
    id SERIAL PRIMARY KEY,
    fecha_pago DATE,
    monto NUMERIC(10, 2),
    documento_banco VARCHAR(20),
    nro_documentos INT,
    tipo_pago VARCHAR(10),
    codigo_correlativo VARCHAR(30),
    estado CHAR(1)
);

-- Crear función para generar el código correlativo
CREATE OR REPLACE FUNCTION generar_codigo_correlativo() RETURNS TRIGGER AS $$
BEGIN
    NEW.codigo_correlativo := 'CP-' || TO_CHAR(NEW.fecha_pago, 'YYYYMMDD') || '-' || TO_CHAR(NEW.id, 'FM000000');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear trigger para llamar a la función antes de insertar
CREATE TRIGGER trigger_generar_codigo_correlativo
BEFORE INSERT ON correlativos_pago
FOR EACH ROW
EXECUTE FUNCTION generar_codigo_correlativo();

-- Crear tabla correlativos_adelanto
CREATE TABLE IF NOT EXISTS correlativos_adelanto (
    id SERIAL PRIMARY KEY,
    fecha_pago DATE,
    monto NUMERIC(10, 2),
    documento_banco VARCHAR(20),
    nro_documentos INT,
    tipo_pago VARCHAR(10),
    estado CHAR(1)
);

-- Crear tabla Proveedor
CREATE TABLE IF NOT EXISTS Proveedor (
    id SERIAL PRIMARY KEY,
    rucp BIGINT,      
    razon_social VARCHAR(75),
    tipocuenta VARCHAR(50),
    cuentabanco VARCHAR(20),
    cuentainter VARCHAR(20),
    celular BIGINT,
    correo VARCHAR(60),
    UNIQUE (rucp)
);
    
-- Crear tabla Despacho
CREATE TABLE IF NOT EXISTS Despacho (
    id SERIAL PRIMARY KEY,
    fecha_salida DATE,
    razon_social VARCHAR(75),
    ruc BIGINT,      
    placa_tracto VARCHAR(10),
    placa_ramfla VARCHAR(10),
    tipo_plataforma VARCHAR(12),
    mtc_dos_placas VARCHAR(25),
    apellidos_nombres VARCHAR(100),
    licencia VARCHAR(20),
    celular BIGINT,  
    usuario VARCHAR(20),
    serie_guia VARCHAR(5),
    numero_guia INTEGER,  
    cincuenta_soles BOOLEAN,  
    tipo_mineral VARCHAR(12),
    peso_toneladas NUMERIC(10, 2),
    monto_adelanto NUMERIC(10, 2),
    cliente VARCHAR(10),
    fecha_entrega DATE,
    serie_transporte VARCHAR(5),
    numero_transporte VARCHAR(10),
    fecha_transporte DATE,
    serie_factura VARCHAR(5),
    numero_factura VARCHAR(10),
    fecha_factura DATE,
    monto_factura NUMERIC(10, 2),
    serie_peso VARCHAR(5),
    numero_peso VARCHAR(10),
    fecha_peso DATE,
    monto_peso NUMERIC(10, 2),
    fecha_pago DATE,
    codigo_correlativo VARCHAR(30),
    fecha_detra DATE,
    correlativo_detra NUMERIC(10, 0),
    UNIQUE (serie_guia, numero_guia)
);

-- Crear tabla Despacho
CREATE TABLE IF NOT EXISTS Despacho_zhonghui (
    id SERIAL PRIMARY KEY,  -- Identificador único del despacho
    
    fecha_recepcion DATE,  -- Fecha de recepción
    fecha_salida_mina DATE,  -- Fecha de salida de la mina
    
    placa_tracto VARCHAR(10),  -- Placa del tracto
    placa_ramfla VARCHAR(10),  -- Placa de la ramfla
    tipo_plataforma VARCHAR(12),  -- Tipo de plataforma utilizada
    
    razon_social VARCHAR(75),  -- Razón social de la empresa
    chofer VARCHAR(100),  -- Nombre del chofer
    licencia VARCHAR(20),  -- Número de licencia del chofer
    tipo_mineral VARCHAR(12),  -- Tipo de mineral
    
    ticket_balanza VARCHAR(20),  -- Número de ticket de balanza
    fecha_matarani DATE,  -- Fecha de llegada a Matarani

    peso_kg NUMERIC(10, 2),  -- Peso en kilogramos
    peso_tn NUMERIC(10, 2),  -- Peso en toneladas

    serie_factura VARCHAR(5),  -- Serie de la factura
    numero_factura VARCHAR(10),  -- Número de la factura

    fecha_factura DATE,  -- Fecha de emisión de la factura
    fecha_pago DATE,  -- Fecha de pago de la factura

    observaciones TEXT,  -- Observaciones

    numero_cuenta VARCHAR(20),  -- Número de cuenta
    numero_cuenta_interbancaria VARCHAR(20),  -- Número de cuenta interbancaria
    precio_tonelada NUMERIC(10, 2),  -- Precio por tonelada
    monto_factura NUMERIC(10, 2),  -- Monto total de la factura (peso en toneladas * precio por tonelada)

    base_factura NUMERIC(10, 2),  -- Base imponible de la factura
    igv_factura NUMERIC(10, 2),  -- IGV de la factura
    detraccion_factura NUMERIC(10, 2),  -- Detracción de la factura

    monto_sn_detraccion NUMERIC(10, 2),  -- Monto total menos detracción
    
    pago_comunidad NUMERIC(10, 2),  -- Pago a la comunidad (0.5/ton)
    monto_adelanto NUMERIC(10, 2),  -- Monto de adelanto
    saldo_pagar NUMERIC(10, 2),  -- Saldo a pagar
    
    rucp BIGINT,  -- RUC del proveedor
    direccion VARCHAR(255),  -- Dirección del proveedor
    banco VARCHAR(50),  -- Banco

    estado VARCHAR(20),  -- Estado del despacho
    usuario VARCHAR(20),  -- Usuario que registra el despacho
    placa_mtc VARCHAR(25),  -- Código MTC de dos placas
    celular BIGINT,  -- Número de celular del chofer

    fecha_detraccion DATE,  -- Fecha de detracción
    correlativo_pago VARCHAR(30),  -- Correlativo de pago
    correlativo_detraccion NUMERIC(10, 0),  -- Correlativo de detracción
    
    UNIQUE (serie_factura, numero_factura)  -- Llave única para la combinación de serie y número de factura
);

-- Crear tabla Despacho
CREATE TABLE IF NOT EXISTS Despacho_zhenco (
    id SERIAL PRIMARY KEY,  -- Identificador único del despacho
    
    fecha_recepcion DATE,  -- Fecha de recepción
    fecha_salida_mina DATE,  -- Fecha de salida de la mina
    
    placa_tracto VARCHAR(10),  -- Placa del tracto
    placa_ramfla VARCHAR(10),  -- Placa de la ramfla
    tipo_plataforma VARCHAR(12),  -- Tipo de plataforma utilizada
    
    razon_social VARCHAR(75),  -- Razón social de la empresa
    chofer VARCHAR(100),  -- Nombre del chofer
    licencia VARCHAR(20),  -- Número de licencia del chofer
    tipo_mineral VARCHAR(12),  -- Tipo de mineral
    
    ticket_balanza VARCHAR(20),  -- Número de ticket de balanza
    fecha_matarani DATE,  -- Fecha de llegada a Matarani

    peso_kg NUMERIC(10, 2),  -- Peso en kilogramos
    peso_tn NUMERIC(10, 2),  -- Peso en toneladas

    serie_factura VARCHAR(5),  -- Serie de la factura
    numero_factura VARCHAR(10),  -- Número de la factura

    fecha_factura DATE,  -- Fecha de emisión de la factura
    fecha_pago DATE,  -- Fecha de pago de la factura

    observaciones TEXT,  -- Observaciones

    numero_cuenta VARCHAR(20),  -- Número de cuenta
    numero_cuenta_interbancaria VARCHAR(20),  -- Número de cuenta interbancaria
    precio_tonelada NUMERIC(10, 2),  -- Precio por tonelada
    monto_factura NUMERIC(10, 2),  -- Monto total de la factura (peso en toneladas * precio por tonelada)

    base_factura NUMERIC(10, 2),  -- Base imponible de la factura
    igv_factura NUMERIC(10, 2),  -- IGV de la factura
    detraccion_factura NUMERIC(10, 2),  -- Detracción de la factura

    monto_sn_detraccion NUMERIC(10, 2),  -- Monto total menos detracción
    
    --pago_comunidad NUMERIC(10, 2),  -- Pago a la comunidad (0.5/ton)
    --monto_adelanto NUMERIC(10, 2),  -- Monto de adelanto
    --saldo_pagar NUMERIC(10, 2),  -- Saldo a pagar
    
    rucp BIGINT,  -- RUC del proveedor
    direccion VARCHAR(255),  -- Dirección del proveedor
    
	banco VARCHAR(50),  -- Banco
	proveedor
	
    estado VARCHAR(20),  -- Estado del despacho
    usuario VARCHAR(20),  -- Usuario que registra el despacho
    placa_mtc VARCHAR(25),  -- Código MTC de dos placas
    celular BIGINT,  -- Número de celular del chofer
	
	cta_detrraccion
    fecha_detraccion DATE,  -- Fecha de detracción
    correlativo_pago VARCHAR(30),  -- Correlativo de pago
    correlativo_detraccion NUMERIC(10, 0),  -- Correlativo de detracción

	
    UNIQUE (serie_factura, numero_factura)  -- Llave única para la combinación de serie y número de factura
	--creaer tempo
);