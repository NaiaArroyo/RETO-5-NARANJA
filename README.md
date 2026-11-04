# RETO-5-NARANJA
repositorio reto 5 equipo naranja


REQUISITOS PARA EJECUTAR
Ejecutar los cuadernos en este orden estricto:

preprocesamiento.ipynb
regresion_logistica.ipynb
modelo_regresion_prima.ipynb
Notebook_Amortizacion_Francesa_y_Aleman.ipynb

COMPONENTES
1. Preprocesamiento (preprocesamiento.ipynb)

Entrada: 
data/Prestamos_Data_Alumnos_v5.xlsx

Salidas:
data/prestamos_automovil.csv (Filtrado solo para el propósito "Automóvil" y limpio).
data/X_train_impago.csv, y_train_impago.csv, X_test_impago.csv, y_test_impago.csv (Datos procesados para predecir el impago).
data/X_train_prima.csv, y_train_prima.csv, X_test_prima.csv, y_test_prima.csv (Datos procesados para predecir la prima).

2. Modelo de Impago (regresion_logistica.ipynb)

Entrada:
data/X_train_impago.csv, data/y_train_impago.csv
data/X_test_impago.csv, data/y_test_impago.csv

Salidas:
data/prob_impago_train.csv (Probabilidad de impago calculada para el conjunto de entrenamiento).
data/prob_impago_test.csv (Probabilidad de impago calculada para el conjunto de prueba).

3. Modelo de la Prima (modelo_regresion_prima.ipynb)

Entrada:
data/X_train_prima.csv, data/y_train_prima.csv
data/X_test_prima.csv, data/y_test_prima.csv
data/prob_impago_train.csv, data/prob_impago_test.csv (Usadas como variable predictora extra).

Salida:
Evaluación de modelos (Regresión Lineal vs Regresión Polinómica) y métricas de error (RMSE/MAE).

4. Sistemas de Amortización (Notebook_Amortizacion_Francesa_y_Aleman.ipynb)

Entrada:
data/prestamos_automovil.csv

Salida:
Elección entre sistema francés o alemán por préstamo.
Tablas de amortización, cálculo del VAN/TIR y capital pendiente a mitad del préstamo.


