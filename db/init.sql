USE consorcio;

CREATE TABLE clientes (
  id_cliente INT PRIMARY KEY,
  password_cliente VARCHAR(255) NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE categorias (
  id_categoria INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE noticias (
  id_noticia INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(255) NOT NULL,
  contenido TEXT NOT NULL,
  time_stamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cliente_categoria (
  id_cliente INT,
  id_categoria INT,
  PRIMARY KEY (id_cliente, id_categoria),

  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

CREATE TABLE cliente_noticia (
  id_cliente INT,
  id_noticia INT,
  PRIMARY KEY (id_cliente, id_noticia),

  FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
  FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia) ON DELETE CASCADE
);

CREATE TABLE noticia_categoria (
  id_noticia INT,
  id_categoria INT,
  PRIMARY KEY (id_noticia, id_categoria),

  FOREIGN KEY (id_noticia) REFERENCES noticias(id_noticia) ON DELETE CASCADE,
  FOREIGN KEY (id_categoria) REFERENCES categorias(id_categoria) ON DELETE CASCADE
);

/* ------------------ VISTAS ------------------ */

/* Ver todos los clientes registrados */
CREATE VIEW vista_clientes_registrados AS
SELECT 
  id_cliente,
  nombre,
  email
FROM clientes;

/* Ver todas las categorias disponibles */
CREATE VIEW vista_categorias_disponibles AS
SELECT 
  id_categoria,
  nombre AS nombre_categoria
FROM categorias;

/* Ver todas las noticias de las últimas 24 hs */
CREATE VIEW vista_noticias_ultimas_24hs AS
SELECT 
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cli.nombre AS cliente,
  cat.nombre AS categoria
FROM noticias n
LEFT JOIN cliente_noticia cn ON n.id_noticia = cn.id_noticia
LEFT JOIN clientes cli ON cn.id_cliente = cli.id_cliente
LEFT JOIN noticia_categoria nc ON n.id_noticia = nc.id_noticia
LEFT JOIN categorias cat ON nc.id_categoria = cat.id_categoria
WHERE n.time_stamp >= NOW() - INTERVAL 1 DAY;

/* Ver todas las noticias que creó el cliente */
CREATE VIEW vista_noticias_creadas_cliente AS
SELECT 
  cli.id_cliente,
  cli.nombre AS autor,
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp
FROM cliente_noticia cn
JOIN clientes cli ON cn.id_cliente = cli.id_cliente
JOIN noticias n ON cn.id_noticia = n.id_noticia;

/* Ver a que categorias está suscripto el cliente */
CREATE VIEW vista_suscripciones_cliente AS
SELECT 
  cli.id_cliente,
  cli.nombre AS cliente,
  cat.id_categoria,
  cat.nombre AS categoria
FROM cliente_categoria cc
JOIN clientes cli ON cc.id_cliente = cli.id_cliente
JOIN categorias cat ON cc.id_categoria = cat.id_categoria;

/* Ver todas las noticias de las categorias a las que está suscripto el cliente */
CREATE VIEW vista_noticias_para_cliente AS
SELECT 
  cc.id_cliente,
  cli.nombre AS cliente,
  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,
  cat.nombre AS categoria,
  autor.id_cliente AS id_autor,
  autor.nombre AS nombre_autor
FROM cliente_categoria cc
JOIN categorias cat ON cc.id_categoria = cat.id_categoria
JOIN noticia_categoria nc ON cat.id_categoria = nc.id_categoria
JOIN noticias n ON nc.id_noticia = n.id_noticia

LEFT JOIN cliente_noticia cn ON n.id_noticia = cn.id_noticia
LEFT JOIN clientes autor ON cn.id_cliente = autor.id_cliente

JOIN clientes cli ON cc.id_cliente = cli.id_cliente;

/* Ver las nuevas noticias (última hora) */
CREATE VIEW vista_nuevas_noticias_para_enviar AS
SELECT 
  cc.id_cliente,
  cli.nombre AS nombre_cliente,
  cli.email,

  n.id_noticia,
  n.titulo,
  n.contenido,
  n.time_stamp,

  cat.id_categoria,
  cat.nombre AS nombre_categoria,

  autor.id_cliente AS id_autor,
  autor.nombre AS nombre_autor
FROM noticias n
JOIN noticia_categoria nc ON n.id_noticia = nc.id_noticia
JOIN categorias cat ON nc.id_categoria = cat.id_categoria

JOIN cliente_categoria cc ON cat.id_categoria = cc.id_categoria
JOIN clientes cli ON cc.id_cliente = cli.id_cliente

LEFT JOIN cliente_noticia cn ON n.id_noticia = cn.id_noticia
LEFT JOIN clientes autor ON cn.id_cliente = autor.id_cliente
WHERE n.time_stamp >= NOW() - INTERVAL 1 HOUR;

/*------------------ STORED PROCEDURE ------------------*/
DELIMITER //

CREATE PROCEDURE registrar_cliente (
  IN p_id_cliente INT,
  IN p_password VARCHAR(255),
  IN p_nombre VARCHAR(100),
  IN p_email VARCHAR(150)
)
BEGIN
  INSERT INTO clientes (id_cliente, password_cliente, nombre, email)
  VALUES (p_id_cliente, MD5(p_password), p_nombre, p_email);
END;//

CREATE PROCEDURE eliminar_cliente (
  IN p_id_cliente INT
)
BEGIN
  DELETE FROM clientes
  WHERE id_cliente = p_id_cliente;
END;//

CREATE PROCEDURE crear_noticia (
  IN p_id_cliente INT,
  IN p_id_categoria INT,
  IN p_titulo VARCHAR(255),
  IN p_contenido TEXT,
  OUT eliminado BOOL
)
BEGIN
  DECLARE v_id_noticia INT;
  DECLARE v_existe INT;

  SELECT COUNT(*) INTO v_existe
  FROM cliente_categoria
  WHERE id_cliente = p_id_cliente AND id_categoria = p_id_categoria;

  IF v_existe > 0 THEN
    INSERT INTO noticias (titulo, contenido)
    VALUES (p_titulo, p_contenido);

    SET v_id_noticia = LAST_INSERT_ID();

    INSERT INTO cliente_noticia (id_cliente, id_noticia)
    VALUES (p_id_cliente, v_id_noticia);

    INSERT INTO noticia_categoria (id_noticia, id_categoria)
    VALUES (v_id_noticia, p_id_categoria);

    SET eliminado = TRUE;
  ELSE
    SET eliminado = FALSE;
  END IF;
END;//

CREATE PROCEDURE eliminar_noticia_cliente (
  IN p_id_cliente INT,
  IN p_id_noticia INT
)
BEGIN
  IF EXISTS (
    SELECT 1 FROM cliente_noticia 
    WHERE id_cliente = p_id_cliente AND id_noticia = p_id_noticia
  ) THEN
    DELETE FROM noticias WHERE id_noticia = p_id_noticia;
  END IF;
END;//

CREATE PROCEDURE agregar_categoria (
  IN p_nombre_categoria VARCHAR(100)
)
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM categorias WHERE nombre = p_nombre_categoria
  ) THEN
    INSERT INTO categorias (nombre) VALUES (p_nombre_categoria);
  END IF;
END;//

CREATE PROCEDURE eliminar_categoria (
  IN p_nombre_categoria VARCHAR(100)
)
BEGIN
  DELETE FROM categorias
  WHERE nombre = p_nombre_categoria;
END;//

CREATE PROCEDURE suscribir_cliente_categoria (
  IN p_id_cliente INT,
  IN p_id_categoria INT
)
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM cliente_categoria 
    WHERE id_cliente = p_id_cliente AND id_categoria = p_id_categoria
  ) THEN
    INSERT INTO cliente_categoria (id_cliente, id_categoria)
    VALUES (p_id_cliente, p_id_categoria);
  END IF;
END;//

CREATE PROCEDURE desuscribir_cliente_categoria (
  IN p_id_cliente INT,
  IN p_id_categoria INT
)
BEGIN
  DELETE FROM cliente_categoria
  WHERE id_cliente = p_id_cliente
    AND id_categoria = p_id_categoria;
END;//

DELIMITER ;

/*------------------ DATOS DE PRUEBA ------------------*/

INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460004, MD5('prueba'), 'Mario', 'prueba@hola.com');
INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460005, MD5('prueba'), 'Pepe', 'prueba2@hola.com');
INSERT INTO clientes(id_cliente, password_cliente, nombre, email) VALUES (41460006, MD5('prueba'), 'Pablo', 'prueba3@hola.com');

INSERT INTO categorias(nombre) VALUES ('Policial');
INSERT INTO categorias(nombre) VALUES ('Deportiva');
INSERT INTO categorias(nombre) VALUES ('Finanzas');

INSERT INTO noticias(titulo, contenido) VALUES ('Choque sobre ruta 3', 'Por la madrugada del lunes chocaron dos vehiculos. No se registraron heridos.');
INSERT INTO noticias(titulo, contenido) VALUES ('Cientificos reviven al Diego', 'Segun fuentes de tiktok aseguran haber revivido a Maradona pero ahora patea con la derecha');
INSERT INTO noticias(titulo, contenido) VALUES ('Vuela el dolar', 'El dolar toca los $23049 por unidad');
INSERT INTO noticias(titulo, contenido) VALUES ('prueba', 'prueba');

INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460004, 1);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460004, 2);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460005, 2);
INSERT INTO cliente_categoria(id_cliente, id_categoria) VALUES (41460006, 3);

INSERT INTO cliente_noticia(id_cliente, id_noticia) VALUES (41460004, 1);
INSERT INTO cliente_noticia(id_cliente, id_noticia) VALUES (41460004, 2);
INSERT INTO cliente_noticia(id_cliente, id_noticia) VALUES (41460005, 3);

INSERT INTO noticia_categoria(id_noticia, id_categoria) VALUES (1, 1);
INSERT INTO noticia_categoria(id_noticia, id_categoria) VALUES (2, 2);
INSERT INTO noticia_categoria(id_noticia, id_categoria) VALUES (3, 3);