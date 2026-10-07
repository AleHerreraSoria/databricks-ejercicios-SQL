# Databricks notebook source
# MAGIC %md
# MAGIC ##PARTE 1: Consultas Básicas de Exploración

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Familiarizarse con Databricks y ejecutar una primer query
# MAGIC -- ¿Cuántos viajes hay en total en el dataset de NYC Taxi Trips?
# MAGIC select count(*)
# MAGIC from samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Explorar estructura y Entender qué columnas tiene el dataset.
# MAGIC -- ¿Qué columnas tiene la tabla samples.nyctaxi.trips? ¿Qué tipos de datos tienen?
# MAGIC describe samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Encontrar valores extremos en los datos.
# MAGIC -- ¿Cuál es el viaje más largo (mayor distancia) en el dataset?
# MAGIC -- ¿Y el más corto (excluyendo ceros)?
# MAGIC select max(trip_distance), min(trip_distance)
# MAGIC from samples.nyctaxi.trips
# MAGIC where trip_distance > 0;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Estadísticas básicas. Calcular promedios y estadísticas descriptivas.
# MAGIC -- ¿Cuál es el promedio de tarifa (fare_amount) y distancia (trip_distance) de los viajes?
# MAGIC select avg(fare_amount) AS promoedio_tarifa, avg(trip_distance) AS promedio_distancia
# MAGIC from samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Viajes recientes (Ordenar y limitar resultados).
# MAGIC -- Muestra los 20 viajes más recientes con su fecha, distancia y tarifa.
# MAGIC select tpep_pickup_datetime AS fecha_y_hora_viaje, trip_distance as distancia, fare_amount as tarifa
# MAGIC from samples.nyctaxi.trips
# MAGIC order by tpep_pickup_datetime desc
# MAGIC limit 20;

# COMMAND ----------

# MAGIC %md
# MAGIC ##PARTE 2: Filtros y Condiciones

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Aplicación de filtros simples con WHERE.
# MAGIC -- Muestra todos los viajes que tienen una distancia mayor a 10 millas.
# MAGIC -- Usando WHERE trip_distance > 10
# MAGIC select *
# MAGIC from samples.nyctaxi.trips
# MAGIC where trip_distance > 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Múltiples condiciones combinando condiciones con AND.
# MAGIC -- Encuentra viajes que tengan distancia > 5 millas
# MAGIC -- "Y" tarifa > $10. Pista: Usa WHERE ... AND ...
# MAGIC SELECT *
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 5 AND fare_amount > 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Usando OR para condiciones alternativas.
# MAGIC -- Mostrar viajes que tengan distancia > a 20 millas "O" tarifa > a $100.
# MAGIC -- Usando WHERE ... OR ...
# MAGIC SELECT *
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 20 OR fare_amount > 100;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Probando BETWEEN para Rango de valores
# MAGIC -- Encontrar viajes con tarifa entre $10 y $20, 
# MAGIC -- Usando WHERE fare_amount BETWEEN 10 AND 20
# MAGIC SELECT *
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE fare_amount BETWEEN 10 AND 20;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Filtrando por múltiples valores específicos.
# MAGIC -- Mostrando viajes que comenzaron en los pickup_zip = 10009, 10013 o 10014.
# MAGIC -- Usando WHERE pickup_zip IN (10009, 10013, 10014)
# MAGIC SELECT *
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE pickup_zip IN (10009, 10013, 10014);

# COMMAND ----------

# MAGIC %md
# MAGIC ##PARTE 3: Agregaciones

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Conteo básico: Contar registros para saber ¿Cuántos viajes hay en total?
# MAGIC -- Usando SELECT COUNT(*) FROM ...
# MAGIC SELECT COUNT(*)
# MAGIC FROM samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Sumando valores numéricos: ¿Cuál es el total de tarifas y la distancia total recorrida por todos los viajes?
# MAGIC -- Usamos SUM() para ambas columnas con REDONDEO a 2 decimales.
# MAGIC SELECT
# MAGIC     round(SUM(fare_amount), 2) AS total_tarifa,
# MAGIC     round(SUM(trip_distance), 2) AS total_distancia
# MAGIC FROM samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Calculando promedios: ¿Cuál es la distancia promedio y la tarifa promedio de los viajes? (excluyendo valores cero)
# MAGIC -- Usamos AVG() con WHERE para filtrar ceros
# MAGIC SELECT
# MAGIC     round(AVG(trip_distance), 2) AS promedio_distancia,
# MAGIC     round(AVG(fare_amount), 2) AS promedio_tarifa
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Encontrando valores extremos: ¿Cuál es la tarifa MIN, MAX, distancia MIN y MAX? (excluyendo valores cero)
# MAGIC -- Usamos MIN() y MAX() con filtros
# MAGIC SELECT
# MAGIC     round(MIN(fare_amount),2) AS tarifa_MIN,
# MAGIC     round(MAX(fare_amount),2) AS tarifa_MAX,
# MAGIC     MIN(trip_distance) AS distancia_MIN,
# MAGIC     MAX(trip_distance) AS distancia_MAX
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0 AND fare_amount > 0;

# COMMAND ----------

# MAGIC %md
# MAGIC ##PARTE 4: GROUP BY   ///   PARTE 5: HAVING

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Agrupando datos por zona para calcular métricas por grupo.
# MAGIC -- ¿Cuántos viajes hay por zona de inicio (pickup_zip)?
# MAGIC -- ¿Cuál es el ingreso total y promedio por zona?
# MAGIC -- Ordenamos por ingreso total descendente.
# MAGIC -- Usamos GROUP BY pickup_zip, COUNT(*), SUM(fare_amount), AVG(fare_amount), ORDER BY
# MAGIC SELECT
# MAGIC     pickup_zip,
# MAGIC     COUNT(*) AS total_viajes,
# MAGIC     ROUND(SUM(fare_amount),2) AS total_ingreso,
# MAGIC     ROUND(AVG(fare_amount),2) AS promedio_ingreso
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY pickup_zip
# MAGIC ORDER BY total_ingreso DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Buscando Viajes por día de la semana, agrupados por fecha con calculo de estadísticas.
# MAGIC -- ¿Cuántos viajes hay por día de la semana? ¿Cuál es la distancia promedio por día?
# MAGIC -- Usamos GROUP BY.
# MAGIC SELECT
# MAGIC     tpep_pickup_datetime,
# MAGIC     EXTRACT(DAYOFWEEK FROM tpep_pickup_datetime) AS dia_semana,
# MAGIC     COUNT(*) AS total_viajes,
# MAGIC     ROUND(AVG(trip_distance),2) AS promedio_distancia
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY tpep_pickup_datetime, dia_semana
# MAGIC ORDER BY total_viajes DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Analizamos Viajes / hora buscando patrones horarios.
# MAGIC -- ¿Cuántos viajes hay por hora del día?
# MAGIC -- ¿Cuál es la tarifa promedio por hora? Ordenamos por hora.
# MAGIC -- Usamos EXTRACT(HOUR FROM ...) y GROUP BY
# MAGIC SELECT
# MAGIC     EXTRACT(HOUR FROM tpep_pickup_datetime) AS hora,
# MAGIC     COUNT(*) AS total_viajes,
# MAGIC     ROUND(AVG(fare_amount),2) AS promedio_tarifa
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY hora
# MAGIC ORDER BY hora;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Filtrando grupos grandes después de agrupar.
# MAGIC -- Muestrar solo las zonas que tienen + 1,000 viajes.
# MAGIC -- Usando GROUP BY con HAVING COUNT(*) > 1000
# MAGIC SELECT
# MAGIC     pickup_zip,
# MAGIC     COUNT(*) AS total_viajes
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY pickup_zip
# MAGIC HAVING total_viajes > 1000
# MAGIC ORDER BY total_viajes DESC;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Identificamos los días con mayor actividad.
# MAGIC -- ¿Qué días tuvieron más de 200 viajes?
# MAGIC -- Mostramos fecha, cantidad de viajes y tarifa promedio.
# MAGIC -- Usando GROUP BY, HAVING, ORDER BY y LIMIT
# MAGIC SELECT
# MAGIC     cast(tpep_pickup_datetime as date) AS fecha,
# MAGIC     COUNT(*) AS cantidad_de_viajes,
# MAGIC     ROUND(AVG(fare_amount),2) AS tarifa_promedio
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY
# MAGIC     cast(tpep_pickup_datetime as date)
# MAGIC HAVING cantidad_de_viajes > 200
# MAGIC ORDER BY cantidad_de_viajes DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Identificando horas con mayor actividad.
# MAGIC -- ¿Qué horas tienen más de 1,000 viajes? Ordenamos por cantidad de viajes DESC.
# MAGIC -- Usamos GROUP BY, HAVING COUNT(*) > 1000
# MAGIC SELECT
# MAGIC     EXTRACT(HOUR FROM tpep_pickup_datetime) AS hora,
# MAGIC     COUNT(*) AS total_viajes
# MAGIC FROM samples.nyctaxi.trips
# MAGIC GROUP BY hora
# MAGIC HAVING total_viajes > 1000
# MAGIC ORDER BY total_viajes DESC;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ##Parte 6: Análisis Combinado

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Análisis completo por zona
# MAGIC -- Combinamos WHERE, GROUP BY y HAVING para responder:
# MAGIC -- Para zonas con + 1,000 viajes, muestra: zona, cantidad de viajes, tarifa máxima, promedio y mínima.
# MAGIC -- Solo mostraremos viajes con tarifa > $5 y distancia > 0.
# MAGIC -- Usaremos WHERE para filtrar registros, GROUP BY para agrupar, HAVING para filtrar grupos.
# MAGIC SELECT
# MAGIC     pickup_zip AS zona,
# MAGIC     COUNT(*) AS cantidad_de_viajes,
# MAGIC     ROUND(MAX(fare_amount),2) AS tarifa_maxima,
# MAGIC     ROUND(AVG(fare_amount),2) AS tarifa_promedio,
# MAGIC     ROUND(MIN(fare_amount),2) AS tarifa_minima
# MAGIC FROM samples.nyctaxi.trips
# MAGIC WHERE trip_distance > 0 AND fare_amount > 5
# MAGIC GROUP BY pickup_zip
# MAGIC HAVING cantidad_de_viajes > 1000
# MAGIC ORDER BY cantidad_de_viajes DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Categorizando viajes por distancia. Usaremos CASE WHEN para crear categorías.
# MAGIC -- Categorizar los viajes por distancia:
# MAGIC -- Corto: < 2 millas
# MAGIC -- Medio: 2-5 millas
# MAGIC -- Largo: 5-10 millas
# MAGIC -- Muy largo: > 10 millas
# MAGIC -- Agrupamos por categoría y mostramos: categoría, cantidad de viajes, tarifa promedio, distancia promedio. Solo categorías con más de 100 viajes.
# MAGIC -- Usaremos CASE WHEN en el SELECT y también en el GROUP BY.
# MAGIC SELECT
# MAGIC     CASE WHEN trip_distance < 2 THEN 'Corto'
# MAGIC          WHEN trip_distance >= 2 AND trip_distance < 5 THEN 'Medio'
# MAGIC          WHEN trip_distance >= 5 AND trip_distance < 10 THEN 'Largo'
# MAGIC          WHEN trip_distance >= 10 THEN 'Muy largo'
# MAGIC     END AS categoria,
# MAGIC     COUNT(*) AS cantidad_de_viajes,
# MAGIC     ROUND(AVG(fare_amount),2) AS tarifa_promedio,
# MAGIC     ROUND(AVG(trip_distance),2) AS distancia_promedio
# MAGIC FROM
# MAGIC     samples.nyctaxi.trips
# MAGIC GROUP BY
# MAGIC     categoria
# MAGIC HAVING
# MAGIC     cantidad_de_viajes > 100
# MAGIC ORDER BY
# MAGIC     cantidad_de_viajes DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Buscando el "Top Ten" de viajes.
# MAGIC -- Mostraremos los 10 viajes más largos (mayor distancia) con su fecha, distancia y tarifa.
# MAGIC -- Usaremos ORDER BY trip_distance DESC LIMIT 10
# MAGIC SELECT
# MAGIC     tpep_pickup_datetime,
# MAGIC     trip_distance,
# MAGIC     fare_amount
# MAGIC FROM
# MAGIC     samples.nyctaxi.trips
# MAGIC ORDER BY
# MAGIC     trip_distance DESC
# MAGIC LIMIT 10;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- el resultado anterior nos ha devuelto un viaje con fare_amount = 0, lo cual no es correcto o no los queremos en el top ten por esa razón (pudo haber sido una "promoción").
# MAGIC -- Reescribimos la query para excluírlos.
# MAGIC SELECT
# MAGIC     tpep_pickup_datetime,
# MAGIC     trip_distance,
# MAGIC     fare_amount
# MAGIC FROM
# MAGIC     samples.nyctaxi.trips
# MAGIC WHERE
# MAGIC     fare_amount > 0
# MAGIC     AND fare_amount IS NOT NULL
# MAGIC     AND trip_distance IS NOT NULL
# MAGIC ORDER BY
# MAGIC     trip_distance DESC
# MAGIC LIMIT 10;