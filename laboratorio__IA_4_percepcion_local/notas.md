Experimento guiado:
1. Ejecuta el modo comparativo con las semillas 7, 21 y 42.
2. Registra llegada, generaciones, puntaje, choques o intentos bloqueados, pasos utiles y diversidad.
3. Observa si la politica llega a la meta o repite un ciclo.
4. Compara mutacion y cruce con el mismo presupuesto de generaciones.
5. Cambia una sola penalizacion del fitness y repite una semilla.

python3 robot_percepcion.py --no-guardar --semilla 7 --sin-pausa

<img width="574" height="112" alt="image" src="https://github.com/user-attachments/assets/452eea5f-57e9-46fc-8ba4-af5d87e17c6e" />

python3 robot_percepcion.py --no-guardar --semilla 21 --sin-pausa

<img width="579" height="112" alt="image" src="https://github.com/user-attachments/assets/279991b9-641b-4978-a72a-ec7caeb9fbbe" />

python3 robot_percepcion.py --no-guardar --semilla 42 --sin-pausa

<img width="576" height="110" alt="image" src="https://github.com/user-attachments/assets/b4a32dd4-2544-4e97-969a-ad1602a3c716" />

Hice la prueba con la semilla 42 de quitarle el no guardar y me genero dos archivos.

<img width="450" height="73" alt="image" src="https://github.com/user-attachments/assets/8de90a1a-bc77-48c0-8e0e-8d8077695634" />

Dentro del archivo pude analiar y ver cada corrida, y en muchos casos ocurre que vuelve.

Para el punto 5, modifique el fitness penalizando cuando hace visitas repetidas.

<img width="297" height="27" alt="image" src="https://github.com/user-attachments/assets/5e4d06b0-edb9-4d84-9bf9-f3844c36fd62" />

Al volver a correr la semilla 42 dio como resultado:

<img width="584" height="98" alt="image" src="https://github.com/user-attachments/assets/b438f823-8d10-4b08-8e23-c73485c51f1f" />
