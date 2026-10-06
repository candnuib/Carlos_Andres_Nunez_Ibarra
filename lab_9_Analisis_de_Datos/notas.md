Del CSV al análisis de datos

Cargar, inspeccionar y manipular una tabla con Python

Objetivo de la práctica

* explicar qué contiene un archivo CSV y cómo se organiza.
* cargarlo con pandas y revisar sus filas, columnas y tipos.
* detectar valores faltantes, filtrar filas y crear una columna.
* resumir datos para responder una pregunta concreta.

Conexión con el laboratorio del robot:
Guardar posición, acción, choques y distancia a la meta en un CSV permite comparar recorridos y generaciones con evidencia.

CSV: una tabla en texto plano.

* Cada línea representa un registro (una fila).
* La primera línea suele nombrar las columnas.
* Un separador, normalmente coma, divide los campos.
* Conviene mantener una unidad y un significado coherentes por columna.

Preparar la herramienta y los archivos

<img width="284" height="97" alt="image" src="https://github.com/user-attachments/assets/00802513-d650-4ab1-8db9-9996e28af2cf" />

python explorar_ventas_csv.py

Muestra de datos:

<img width="634" height="1019" alt="image" src="https://github.com/user-attachments/assets/00cfdabb-13af-4630-8bfc-fb64a78f0bdc" />

Preguntas antes de sacar conclusiones:

1 ¿Qué categoría suma más ventas? ¿Y cuál reúne más unidades?

La categoria de bebidas es la que suma mas ventas y la que reune mas unidades.
 
2 ¿Cuántas filas se descartaron y por qué?

Se descarto una fila, esto es porque en esa fila se nombran las columnas.

3 ¿Una venta total alta significa que se vendieron muchas unidades?

En este ejemplo si fue asi pero no necesariamente, ya que si se compran pocas unidades de un costo alto, esta condicion no se cumple.

4 ¿Qué información adicional necesitaríamos para explicar el resultado?

* Margen de ganancia o estructura de costos: Saber si liderar en ventas y unidades se traduce en una alta rentabilidad, o si otras categorías dejan mejor margen por unidad vendida.
  
* Período temporal y estacionalidad: Conocer las fechas o la época del año en que se registraron las ventas para identificar picos de consumo (por ejemplo, mayor venta de bebidas durante temporadas de calor o festividades).

Un resumen no es una explicación causal.

Una agrupación describe los datos disponibles. Por sí sola no explica por qué ocurrió el patrón ni garantiza que represente otros periodos.

