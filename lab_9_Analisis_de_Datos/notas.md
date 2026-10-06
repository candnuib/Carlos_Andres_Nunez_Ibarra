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

La categoria de bebidas es la que suma mas ventas.
 
2 ¿Cuántas filas se descartaron y por qué?



3 ¿Una venta total alta significa que se vendieron muchas unidades?

No necesariamente, ya que depende del precio. Pero si es probable que si es una venta alta es por que se vendieron muchas unidades.

4 ¿Qué información adicional necesitaríamos para explicar el resultado?

