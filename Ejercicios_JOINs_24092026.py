# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# MAGIC %md
# MAGIC # Práctica de JOINs — Semana 1
# MAGIC **Bootcamp: Fundamentos de Ingeniería de Datos**
# MAGIC
# MAGIC Dominar los diferentes tipos de JOINs en SQL.
# MAGIC Dataset: Tablas en `bootcamp.practice` (clientes, productos, ordenes, empleados).
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC **Instrucciones:**
# MAGIC 1. Ejecutá primero el bloque de SETUP para crear las tablas
# MAGIC 2. Resolvé cada ejercicio en la celda vacía debajo de la consigna
# MAGIC 3. Verificá que los resultados tengan sentido

# COMMAND ----------

# MAGIC %md
# MAGIC ## ⚙ SETUP — Ejecutar una vez

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE CATALOG IF NOT EXISTS bootcamp;
# MAGIC CREATE SCHEMA IF NOT EXISTS bootcamp.practice;
# MAGIC
# MAGIC -- CLIENTES (6 registros, incluye Pedro sin órdenes)
# MAGIC CREATE OR REPLACE TABLE bootcamp.practice.clientes (
# MAGIC     cliente_id INT, nombre STRING, email STRING, ciudad STRING
# MAGIC );
# MAGIC INSERT INTO bootcamp.practice.clientes VALUES
# MAGIC (1, 'Ana',    'ana@email.com',    'Buenos Aires'),
# MAGIC (2, 'Carlos', 'carlos@email.com', 'Córdoba'),
# MAGIC (3, 'María',  'maria@email.com',  'Buenos Aires'),
# MAGIC (4, 'Diego',  'diego@email.com',  'Rosario'),
# MAGIC (5, 'Laura',  'laura@email.com',  'Mendoza'),
# MAGIC (6, 'Pedro',  'pedro@email.com',  'Buenos Aires');
# MAGIC
# MAGIC -- PRODUCTOS (8 productos, Silla Gamer nunca vendida)
# MAGIC CREATE OR REPLACE TABLE bootcamp.practice.productos (
# MAGIC     producto_id INT, nombre STRING, categoria STRING, precio DOUBLE
# MAGIC );
# MAGIC INSERT INTO bootcamp.practice.productos VALUES
# MAGIC (101, 'Laptop Pro',        'Electrónica', 1200.00),
# MAGIC (102, 'Mouse Inalámbrico', 'Electrónica',   35.00),
# MAGIC (103, 'Teclado Mecánico',  'Electrónica',   89.00),
# MAGIC (104, 'Monitor 27"',       'Electrónica',  450.00),
# MAGIC (105, 'Auriculares BT',    'Audio',         75.00),
# MAGIC (106, 'Webcam HD',         'Accesorios',    55.00),
# MAGIC (107, 'Hub USB-C',         'Accesorios',    42.00),
# MAGIC (108, 'Silla Gamer',       'Muebles',      380.00);
# MAGIC
# MAGIC -- ORDENES (11 órdenes, incluye cliente_id=99 y producto_id=999 inexistentes)
# MAGIC CREATE OR REPLACE TABLE bootcamp.practice.ordenes (
# MAGIC     orden_id INT, cliente_id INT, producto_id INT, cantidad INT, fecha DATE
# MAGIC );
# MAGIC INSERT INTO bootcamp.practice.ordenes VALUES
# MAGIC (1001, 1, 101, 1, '2024-01-15'), (1002, 1, 102, 2, '2024-01-15'),
# MAGIC (1003, 2, 103, 1, '2024-02-01'), (1004, 3, 101, 1, '2024-02-10'),
# MAGIC (1005, 3, 105, 3, '2024-02-10'), (1006, 4, 104, 1, '2024-03-05'),
# MAGIC (1007, 5, 106, 2, '2024-03-12'), (1008, 5, 107, 1, '2024-03-12'),
# MAGIC (1009, 2, 102, 1, '2024-04-01'),
# MAGIC (1010, 99, 101, 1, '2024-04-15'),
# MAGIC (1011, 1, 999, 2, '2024-05-01');
# MAGIC
# MAGIC -- EMPLEADOS (jerarquía para SELF JOIN)
# MAGIC CREATE OR REPLACE TABLE bootcamp.practice.empleados (
# MAGIC     empleado_id INT, nombre STRING, cargo STRING, jefe_id INT
# MAGIC );
# MAGIC INSERT INTO bootcamp.practice.empleados VALUES
# MAGIC (1, 'Roberto',   'CEO',                 NULL),
# MAGIC (2, 'Silvia',    'Directora de Datos',  1),
# MAGIC (3, 'Martín',    'Director Comercial',  1),
# MAGIC (4, 'Lucía',     'Data Engineer Sr',    2),
# MAGIC (5, 'Pablo',     'Data Engineer Jr',    4),
# MAGIC (6, 'Camila',    'Data Analyst',        2),
# MAGIC (7, 'Tomás',     'Vendedor Sr',         3),
# MAGIC (8, 'Valentina', 'Vendedora Jr',        3);

# COMMAND ----------

# MAGIC %md
# MAGIC ## INNER JOIN
# MAGIC Devuelve solo las filas que tienen coincidencia en ambas tablas.
# MAGIC
# MAGIC ### Ejercicio 2.1 — Clientes con sus órdenes
# MAGIC Mostrá todos los clientes que tienen órdenes, con: cliente_id, nombre, ciudad, orden_id, producto_id, cantidad, fecha.
# MAGIC
# MAGIC **Reflexión:** ¿Por qué Pedro (cliente_id=6) no aparece?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.cliente_id,
# MAGIC     c.nombre,
# MAGIC     c.ciudad,
# MAGIC     o.orden_id,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad,
# MAGIC     o.fecha
# MAGIC FROM 
# MAGIC     bootcamp.practice.clientes c
# MAGIC INNER JOIN 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON c.cliente_id = o.cliente_id;
# MAGIC
# MAGIC -- La consigna pide listar a "todos los clientes que tienen órdenes".
# MAGIC -- Esto es: la intersección exacta entre la tabla de (clientes) y la tabla de (ordenes).
# MAGIC -- El operador adecuado para esto es un INNER JOIN (descarta automáticamente cualquier registro que no exista de manera simultánea en ambas tablas).
# MAGIC -- Pedro se registró en la tabla clientes con el cliente_id = 6.
# MAGIC -- Sin embargo, Pedro nunca realizó una compra, por lo que su cliente_id no existe en la tabla (ordenes).
# MAGIC -- INNER JOIN opera como filtro excluyente. Solo devuelve las tuplas que hacen match en ambos lados de la relacion: Pedro es descartado del conjunto final de datos.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 2.2 — Órdenes con detalle de producto
# MAGIC Mostrá todas las órdenes con el nombre del producto y calculá el total (cantidad × precio).
# MAGIC Incluí: orden_id, fecha, nombre del producto, categoría, cantidad, precio unitario, total.
# MAGIC
# MAGIC **Reflexión:** ¿Por qué la orden 1011 no aparece?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     p.nombre AS nombre_del_producto,
# MAGIC     p.categoria,
# MAGIC     o.cantidad,
# MAGIC     p.precio AS precio_unitario,
# MAGIC     (o.cantidad * p.precio) AS total
# MAGIC FROM 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC INNER JOIN 
# MAGIC     bootcamp.practice.productos p
# MAGIC     ON o.producto_id = p.producto_id;
# MAGIC
# MAGIC -- La orden 1011 no aparece porque utiliza un producto_id = 999, que no existe en la tabla de productos.
# MAGIC -- El catálogo solo contiene los productos con IDs del 101 al 108.
# MAGIC -- INNER JOIN requiere "coincidencia estricta" en ambas tablas.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 2.3 — Reporte completo (3 tablas)
# MAGIC Creá un reporte con: nombre del cliente, ciudad, orden_id, fecha, nombre del producto, categoría, cantidad, precio unitario, total.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.nombre AS nombre_del_cliente,
# MAGIC     c.ciudad,
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     p.nombre AS nombre_del_producto,
# MAGIC     p.categoria,
# MAGIC     o.cantidad,
# MAGIC     p.precio AS precio_unitario,
# MAGIC     (o.cantidad * p.precio) AS total
# MAGIC FROM 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC INNER JOIN 
# MAGIC     bootcamp.practice.clientes c 
# MAGIC     ON o.cliente_id = c.cliente_id
# MAGIC INNER JOIN 
# MAGIC     bootcamp.practice.productos p 
# MAGIC     ON o.producto_id = p.producto_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## LEFT JOIN
# MAGIC Devuelve todos los registros de la tabla izquierda + coincidencias de la derecha. Donde no hay match, aparece NULL.
# MAGIC
# MAGIC ### Ejercicio 3.1 — Todos los clientes con sus órdenes
# MAGIC Mostrá TODOS los clientes, hayan comprado o no. Si tienen órdenes, mostrá los detalles. Si no, mostrá NULL.
# MAGIC
# MAGIC **Reflexión:** ¿Qué cliente aparece con NULL en las columnas de órdenes?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.cliente_id,
# MAGIC     c.nombre AS nombre_cliente,
# MAGIC     c.ciudad,
# MAGIC     o.orden_id,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad,
# MAGIC     o.fecha
# MAGIC FROM 
# MAGIC     bootcamp.practice.clientes c
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON c.cliente_id = o.cliente_id;
# MAGIC
# MAGIC -- Aparece con NULL en las columnas de órdenes: Pedro (cliente_id = 6).

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 3.2 — Clientes que nunca compraron
# MAGIC Encontrá los clientes que NUNCA hicieron una compra.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.cliente_id,
# MAGIC     c.nombre AS nombre_cliente,
# MAGIC     c.ciudad
# MAGIC FROM 
# MAGIC     bootcamp.practice.clientes c
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON c.cliente_id = o.cliente_id
# MAGIC WHERE 
# MAGIC     o.orden_id IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 3.3 — Todos los productos (vendidos o no)
# MAGIC Mostrá TODOS los productos, hayan sido vendidos o no.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     p.producto_id,
# MAGIC     p.nombre AS producto_nombre,
# MAGIC     p.categoria,
# MAGIC     p.precio,
# MAGIC     o.orden_id,
# MAGIC     o.cantidad,
# MAGIC     o.fecha
# MAGIC from
# MAGIC     bootcamp.practice.productos p
# MAGIC left join
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     on p.producto_id = o.producto_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 3.4 — Productos nunca vendidos
# MAGIC ¿Qué productos nunca se vendieron?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     p.producto_id,
# MAGIC     p.nombre AS producto_nombre,
# MAGIC     p.categoria,
# MAGIC     p.precio
# MAGIC FROM 
# MAGIC     bootcamp.practice.productos p
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON p.producto_id = o.producto_id
# MAGIC WHERE 
# MAGIC     o.orden_id IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## RIGHT JOIN
# MAGIC Devuelve todos los registros de la tabla derecha + coincidencias de la izquierda. En la práctica, se reescribe como LEFT JOIN.
# MAGIC
# MAGIC ### Ejercicio 4.1 — Todas las órdenes con cliente
# MAGIC Mostrá TODAS las órdenes, tengan cliente válido o no.
# MAGIC
# MAGIC **Reflexión:** ¿Qué orden aparece con NULL en los datos del cliente?

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     c.cliente_id,
# MAGIC     c.nombre AS nombre_cliente,
# MAGIC     c.ciudad,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad
# MAGIC from
# MAGIC     bootcamp.practice.clientes c
# MAGIC right join
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     on c.cliente_id = o.cliente_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 4.2 — Órdenes huérfanas
# MAGIC Encontrá las órdenes que tienen un cliente_id que no existe en la tabla de clientes.

# COMMAND ----------

# MAGIC %sql
# MAGIC select
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     o.cliente_id AS cliente_id_invalido,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad
# MAGIC from
# MAGIC     bootcamp.practice.clientes c
# MAGIC right join
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     on c.cliente_id = o.cliente_id
# MAGIC where
# MAGIC     c.cliente_id IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 4.3 — Equivalencia LEFT vs RIGHT
# MAGIC Reescribí el ejercicio 4.1 usando LEFT JOIN en vez de RIGHT JOIN (invirtiendo el orden de las tablas).

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     c.cliente_id,
# MAGIC     c.nombre AS cliente_nombre,
# MAGIC     c.ciudad,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad
# MAGIC FROM 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.clientes c
# MAGIC     ON o.cliente_id = c.cliente_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## FULL OUTER JOIN
# MAGIC Devuelve todos los registros de ambas tablas, haya coincidencia o no. Ideal para auditorías de integridad.
# MAGIC
# MAGIC ### Ejercicio 5.1 — Todos los clientes y todas las órdenes
# MAGIC Mostrá TODOS los clientes Y TODAS las órdenes, haya coincidencia o no.
# MAGIC
# MAGIC **Reflexión:** ¿Qué registros aparecen con NULL en algún lado?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.cliente_id AS cliente_id_maestro,
# MAGIC     c.nombre AS nombre_cliente,
# MAGIC     c.ciudad,
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     o.cliente_id AS cliente_id_transaccion,
# MAGIC     o.producto_id,
# MAGIC     o.cantidad
# MAGIC FROM 
# MAGIC     bootcamp.practice.clientes c
# MAGIC FULL OUTER JOIN
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON c.cliente_id = o.cliente_id;
# MAGIC
# MAGIC -- 2 situaciones opuestas reflejando nomalías de integridad en nuestra base de práctica:
# MAGIC -- Clientes sin compras (Lado derecho con NULL): cliente_id = 6
# MAGIC -- Compras sin clientes (Lado izquierdo con NULL): cliente_id = 99

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 5.2 — Detectar problemas de datos
# MAGIC Encontrá: (1) Clientes sin órdenes y (2) Órdenes sin cliente válido.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     c.cliente_id AS cliente_id_maestro,
# MAGIC     c.nombre AS nombre_cliente,
# MAGIC     o.orden_id,
# MAGIC     o.cliente_id AS cliente_id_transaccion,
# MAGIC     CASE 
# MAGIC         WHEN o.orden_id IS NULL THEN 'Cliente sin órdenes'
# MAGIC         WHEN c.cliente_id IS NULL THEN 'Orden sin cliente válido'
# MAGIC         ELSE 'Normal'
# MAGIC     END AS tipo_de_anomalia
# MAGIC FROM 
# MAGIC     bootcamp.practice.clientes c
# MAGIC FULL OUTER JOIN 
# MAGIC     bootcamp.practice.ordenes o
# MAGIC     ON c.cliente_id = o.cliente_id
# MAGIC WHERE 
# MAGIC     o.orden_id IS NULL 
# MAGIC     OR c.cliente_id IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## SELF JOIN
# MAGIC Une una tabla consigo misma usando alias diferentes. Para jerarquías y relaciones recursivas.
# MAGIC
# MAGIC ### Ejercicio 6.1 — Jerarquía de empleados
# MAGIC Mostrá cada empleado con el nombre de su jefe. Incluí: empleado_id, nombre del empleado, cargo, jefe_id, nombre del jefe.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     e.empleado_id,
# MAGIC     e.nombre AS nombre_del_empleado,
# MAGIC     e.cargo AS cargo,
# MAGIC     e.jefe_id,
# MAGIC     j.nombre AS nombre_del_jefe
# MAGIC FROM 
# MAGIC     bootcamp.practice.empleados e
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.empleados j
# MAGIC     ON e.jefe_id = j.empleado_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 6.2 — Empleados sin jefe
# MAGIC ¿Qué empleado no tiene jefe? (el CEO)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     e.empleado_id,
# MAGIC     e.nombre AS nombre_del_empleado,
# MAGIC     e.cargo AS cargo,
# MAGIC     e.jefe_id,
# MAGIC     j.nombre AS nombre_del_jefe
# MAGIC FROM 
# MAGIC     bootcamp.practice.empleados e
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.empleados j
# MAGIC     ON e.jefe_id = j.empleado_id
# MAGIC WHERE 
# MAGIC     j.nombre IS NULL;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 6.3 — Subordinados directos
# MAGIC Mostrá quién reporta directamente a cada jefe.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     j.nombre AS nombre_del_jefe,
# MAGIC     j.cargo AS cargo_del_jefe,
# MAGIC     e.nombre AS nombre_del_subordinado,
# MAGIC     e.cargo AS cargo_del_subordinado
# MAGIC FROM 
# MAGIC     bootcamp.practice.empleados j
# MAGIC LEFT JOIN 
# MAGIC     bootcamp.practice.empleados e
# MAGIC     ON j.empleado_id = e.jefe_id;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## JOINs Múltiples
# MAGIC
# MAGIC ### Ejercicio 7.1 — Reporte completo con 3 tablas
# MAGIC Creá un reporte con: nombre del cliente, ciudad, orden_id, fecha, nombre del producto, categoría, cantidad, precio unitario, total. Ordená por cliente y fecha.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     c.nombre AS nombre_del_cliente,
# MAGIC     c.ciudad,
# MAGIC     o.orden_id,
# MAGIC     o.fecha,
# MAGIC     p.nombre AS nombre_del_producto,
# MAGIC     p.categoria,
# MAGIC     o.cantidad,
# MAGIC     p.precio AS precio_unitario,
# MAGIC     (o.cantidad * p.precio) AS total
# MAGIC FROM bootcamp.practice.ordenes o
# MAGIC INNER JOIN
# MAGIC     bootcamp.practice.clientes c
# MAGIC     ON o.cliente_id = c.cliente_id
# MAGIC INNER JOIN
# MAGIC     bootcamp.practice.productos p
# MAGIC     ON o.producto_id = p.producto_id
# MAGIC order by
# MAGIC     o.fecha,
# MAGIC     c.nombre;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 7.2 — Resumen por cliente
# MAGIC Para cada cliente mostrá: nombre, ciudad, cantidad total de órdenes, monto total gastado. Incluí clientes sin órdenes (con 0).

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH resumen_ordenes AS (
# MAGIC     SELECT
# MAGIC         o.cliente_id,
# MAGIC         COUNT(o.orden_id) AS cantidad_de_ordenes,
# MAGIC         SUM(o.cantidad * p.precio) AS monto_gastado
# MAGIC     FROM bootcamp.practice.ordenes o
# MAGIC     INNER JOIN
# MAGIC         bootcamp.practice.productos p
# MAGIC         ON o.producto_id = p.producto_id
# MAGIC     GROUP BY
# MAGIC         o.cliente_id
# MAGIC )
# MAGIC SELECT
# MAGIC     c.nombre,
# MAGIC     c.ciudad,
# MAGIC     coalesce(r.cantidad_de_ordenes, 0) AS cantidad_total_ordenes,
# MAGIC     coalesce(r.monto_gastado, 0.00) AS monto_total_gastado
# MAGIC FROM
# MAGIC     bootcamp.practice.clientes c
# MAGIC LEFT JOIN
# MAGIC     resumen_ordenes r
# MAGIC     ON c.cliente_id = r.cliente_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### Ejercicio 7.3 — Resumen por producto
# MAGIC Para cada producto mostrá: nombre, categoría, cantidad total vendida, ingresos totales. Incluí productos que nunca se vendieron (con 0).

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH ventas_producto AS (
# MAGIC     SELECT 
# MAGIC         o.producto_id,
# MAGIC         SUM(o.cantidad) AS cantidad_vendida,
# MAGIC         SUM(o.cantidad * p.precio) AS ingresos_totales
# MAGIC     FROM 
# MAGIC         bootcamp.practice.ordenes o
# MAGIC     INNER JOIN 
# MAGIC         bootcamp.practice.productos p 
# MAGIC         ON o.producto_id = p.producto_id
# MAGIC     GROUP BY 
# MAGIC         o.producto_id
# MAGIC )
# MAGIC SELECT 
# MAGIC     p.nombre AS producto_nombre,
# MAGIC     p.categoria,
# MAGIC     COALESCE(v.cantidad_vendida, 0) AS cantidad_total_vendida,
# MAGIC     COALESCE(v.ingresos_totales, 0.00) AS ingresos_totales
# MAGIC FROM 
# MAGIC     bootcamp.practice.productos p
# MAGIC LEFT JOIN 
# MAGIC     ventas_producto v
# MAGIC     ON p.producto_id = v.producto_id;
# MAGIC