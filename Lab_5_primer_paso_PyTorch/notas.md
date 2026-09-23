Modelo neuronal.

* Individuo: parametros de una red.
* Mejora: gradiente y retropropagacion.
* Guia: funcion de perdida.
* Datos: ejemplos de entrada y salida.

nota: el fitness y perdida cumplen papeles parecidos, pero no son el mismo algoritmo.

Datos y tensores -> modelo neuronal -> perdida y gradientes -> actualizar parametros de modelo neuronal

* Un tensor es un arreglo numerico con forma y tipo.
* PyTorch calcula gradientes automaticamente.
* La GPU es opcional para comenzar; CPU basta para el mini tutorial.

Linux:

<img width="979" height="318" alt="image" src="https://github.com/user-attachments/assets/237cbd65-dad6-4375-8403-fd76b010dc3b" />

El entorno virtual mantiene la dependencias de esta clase separadas de otros proyectos.

Instalacion inicial, CPU.

<img width="643" height="241" alt="image" src="https://github.com/user-attachments/assets/d4e9288d-7244-458c-9dcb-bd9888bf7974" />

La instalacion tardo y descarg varios MB.

<img width="661" height="129" alt="image" src="https://github.com/user-attachments/assets/0e1f89be-0a2b-4413-9027-7227f998addd" />

Codigo ejemplo:

<img width="659" height="126" alt="image" src="https://github.com/user-attachments/assets/1bde0ca2-31c5-481a-bba8-bfd1a8aee086" />

Un tensor guarda numeros y conoe su forma. Aqui tenemos 2 filas y 3 columnas; podemos operar con todos sus valores de una vez y seccionar una columna.

Representar → medir → mejorar → verificar

¿que diferencia hay entre una regla escrita, una politica evolucionada y un modelo entrenado?

La diferencia radica en que las reglas dictan un comportamiento que simplemente se sigue y se cumple. Una política evolucionada, en cambio, propone un nuevo camino o versión para solucionar un mismo problema, mientras que un modelo entrenado es capaz de aprender y discernir qué decisión tomar.
