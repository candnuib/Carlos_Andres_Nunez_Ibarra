Experimento guiado.

1. Antes de ejecutar, predice que variante llegara antes y cual conservara mas diversidad.

Yo creo que el que la opcion con mutacion + cruce

2. Ejecuta el modo comparativo con las semillas 7, 21 y 42.

python3 robot_obstaculos.py --semilla 7 --sin-pausa

<img width="730" height="106" alt="image" src="https://github.com/user-attachments/assets/725299af-bab2-4195-bc1e-0b987d74221c" />

python3 robot_obstaculos.py --semilla 21 --sin-pausa

<img width="722" height="104" alt="image" src="https://github.com/user-attachments/assets/f736fb56-7351-4f0b-8f53-8a45d33fe87a" />

python3 robot_obstaculos.py --semilla 42 --sin-pausa

<img width="727" height="100" alt="image" src="https://github.com/user-attachments/assets/9cddeeaf-9ed1-4857-898b-c21d00f58e9f" />


4. Compara los resultados de varias semillas. No uses una sola corrida para armar que un metodo
es mejor.

python3 robot_obstaculos.py --semilla 18 --sin-pausa

<img width="582" height="84" alt="image" src="https://github.com/user-attachments/assets/8677b0bb-1bdd-4977-9473-ffd87505b7a1" />

python3 robot_obstaculos.py --semilla 1 --sin-pausa 

<img width="585" height="83" alt="image" src="https://github.com/user-attachments/assets/ac130e61-294c-4f65-8c43-01a87c6ac40b" />

python3 robot_obstaculos.py --semilla 51 --sin-pausa

<img width="579" height="84" alt="image" src="https://github.com/user-attachments/assets/279de78a-31f2-42f4-a843-f23495b15ef0" />

5. Cambia una sola penalizacion del fitness y repite el experimento.

Aumente la penalizacion por visitas repetidas.

<img width="307" height="33" alt="image" src="https://github.com/user-attachments/assets/a91d5c9e-7830-49ca-8169-8b3082a1c6be" />

Resultados semilla 7 con modificacion:

<img width="610" height="79" alt="image" src="https://github.com/user-attachments/assets/89029fbe-ee00-4b91-bd37-8bd2f2a593d0" />

Resultados semilla 21 con modificacion:

<img width="581" height="88" alt="image" src="https://github.com/user-attachments/assets/2c6f5613-bb32-42b6-a64e-6d04bbf34a91" />

Resultados semilla 42 con modificacion:

<img width="581" height="85" alt="image" src="https://github.com/user-attachments/assets/d73405ca-f3a7-40bb-8ae5-8cb19c7f212f" />

1. Por que un robot cercano a la meta puede tener peor puntaje que otro mas lejano?

Porque fue penalizado a lo largo de su recorrido por las caracteristicas del fitness ya sea si choca o tiene visitas repetidas. ademas de que el que esta al inicio tiene sus puntos iniciales intactos.

2. Que ventaja aporta combinar dos padres en lugar de copiar uno solo?

Que se analizan dos rutas que lograron llegar a la meta, solo que se modifica casi la mitad de estos genes. Logrando la explotacion y exploracion.

4. La mayor diversidad final implica necesariamente una mejor solucion?

No necesariamente, pero si hay ma posibilidades de que en esa diversidad este la mejor solucion.

5. Que parte del programa representa el problema y que parte representa el algoritmo de
busqueda?

El problema esta en los obstaculos, ya que al chocar con ellos, se penaliza.
El algoritmo de busqueda esta en la mutacion y cruce. Logrando buscar nuevos caminos para solucionar el problema.

