# GUÍA RÁPIDA PARA DEFENDER EL PROYECTO

Archivo principal:
`Grupo_Patitogit/Codigo/06_arbol_decision.ipynb`

---

## 1. ¿Qué problema concreto aborda el proyecto?

**Respuesta:**  
La dificultad para predecir correctamente los resultados de partidos de fútbol debido a la variabilidad de los encuentros y a que las predicciones basadas en la opinión de las personas no siempre coinciden con el resultado real.

**Qué mostrar:**  
Introducción, planteamiento del problema u objetivo general.

---

## 2. ¿Cuál es la métrica principal y cómo se calcula?

**Respuesta:**  
La métrica principal es el **Accuracy**, que indica qué porcentaje de partidos fueron predichos correctamente.

**Fórmula:**  
`Accuracy = predicciones correctas / total de predicciones`

El Árbol de Decisión optimizado obtuvo aproximadamente **52,67%** de Accuracy.

**Qué mostrar:**
```python
accuracy_score(y_test, pred_optimo)
```

**Mejora posible:**  
Agregar mejores variables, ajustar hiperparámetros y trabajar especialmente la clase empate.

---

## 3. ¿Cuál es la unidad de análisis y cuántos datos hay?

**Respuesta:**  
La unidad de análisis es **un partido de fútbol**. Cada fila representa un partido. El conjunto trabajado contiene **11.417 partidos**.

**Qué mostrar:**
```python
print("Dimensiones:", datos.shape)
display(datos.head())
print(datos.columns.tolist())
```

**Importante:** memorizar también la cantidad exacta de columnas que salga en `datos.shape`.

---

## 4. ¿Qué problemas de calidad encontraron y qué preparación aplicaron?

**Respuesta:**  
Se encontraron valores faltantes en varias columnas. En total se detectaron **185.349 celdas con valores faltantes**.  
Los valores numéricos se completaron con la mediana y los categóricos con la moda. Las variables categóricas se transformaron con One-Hot Encoding(convertir texto en números).

**Qué mostrar:**
```python
nulos = datos.isna().sum()
print(nulos[nulos > 0])
```

y:

```python
SimpleImputer(strategy="median")
SimpleImputer(strategy="most_frequent")
OneHotEncoder(handle_unknown="ignore")
```

**Importante:** 185.349 son celdas faltantes, no partidos.

---

## 5. ¿Qué hallazgo interesante encontraron en el EDA?

**Respuesta:**  
Se observaron valores atípicos principalmente en `Total_Bettors`. Algunos partidos presentan mucha más participación que la mayoría.

**Qué mostrar:**  
`Codigo/03_valores_atipicos_grafico.py`  
y el boxplot generado.

**Cómo explicarlo:**  
Los puntos fuera de los bigotes son posibles valores atípicos.

---

## 6. ¿Cuál es la variable objetivo y qué modelo utilizaron?

**Respuesta:**  
La variable objetivo es `resultado_real`.

Clases:
- `S` = victoria local
- `H` = empate
- `A` = victoria visitante

Se utilizó un **Árbol de Decisión para Clasificación** porque permite trabajar con tres clases y además visualizar cómo toma decisiones.

**Qué mostrar:**
```python
y = datos_modelo["resultado_real"]
```

```python
DecisionTreeClassifier(random_state=42)
```

---

## 7. ¿Cómo dividieron entrenamiento y prueba?

**Respuesta:**  
Se utilizó **80% para entrenamiento y 20% para prueba**, con `random_state=42` y `stratify=y`.

**Qué mostrar:**
```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

**Cómo evitaron fuga de información:**  
La limpieza y transformación se aplicaron dentro de un `Pipeline`.

---

## 8. ¿Cuáles son las variables más importantes?

**Respuesta:**  
El árbol calcula la importancia con `feature_importances_`. En el modelo aparecen variables relacionadas con votos, posición en liga y puntos. `Votes_for_Away` aparece desde los primeros nodos del árbol.

**Qué mostrar:**
```python
arbol_entrenado.feature_importances_
```

o la tabla/gráfico de importancia.

**Importante:** revisar en el notebook cuál quedó exactamente como la variable más importante.

**Cómo explicarlo:**  
Una variable importante fue utilizada más por el árbol para separar los datos. Eso no significa causalidad.

---

## 9. ¿Qué desempeño obtuvo el modelo?

**Respuesta:**  
El Árbol de Decisión optimizado obtuvo aproximadamente **52,67% de Accuracy**.  
La predicción mayoritaria de las personas obtuvo aproximadamente **52,45%**.  
La diferencia fue de aproximadamente **0,22 puntos porcentuales**.

También se evaluaron Precision, Recall y F1.

**Qué mostrar:**
```python
classification_report(
    y_test,
    pred_optimo,
    zero_division=0
)
```

y la matriz de confusión:

```python
ConfusionMatrixDisplay.from_predictions(...)
```

**Definiciones rápidas:**
- Accuracy: porcentaje total de aciertos.
- Precision: de lo que el modelo predijo como una clase, cuánto acertó.
- Recall: de los casos reales de una clase, cuántos detectó.
- F1: equilibrio entre Precision y Recall.

**Importante:** copiar del notebook los valores exactos de Precision, Recall y F1 antes de exponer.

---

## 10. ¿Qué visualización permite entender cómo toma decisiones el modelo?

**Respuesta:**  
El gráfico del Árbol de Decisión permite ver las condiciones que utiliza el modelo.

Ejemplo:
`Votos por visitante <= 1.5`

Si se cumple, sigue por la izquierda. Si no, por la derecha.

**Qué mostrar:**  
`arbol_decision_legible.png`  
o la celda con:

```python
plot_tree(...)
```

**Elementos del árbol:**
- `samples`: cantidad de registros del nodo.
- `value`: cantidad de registros de cada clase.
- `class`: clase predominante.
- `gini`: qué tan mezcladas están las clases.
- `(...)`: el árbol continúa, pero se ocultaron niveles para hacerlo legible.

---

# RESPUESTAS ULTRACORTAS

- Problema: predecir resultados de fútbol con datos históricos.
- Variable objetivo: `resultado_real`.
- Clases: S, H y A.
- Modelo: Árbol de Decisión.
- Datos: 11.417 partidos.
- División: 80% / 20%.
- Semilla: `random_state=42`.
- Métrica principal: Accuracy.
- Accuracy árbol: 52,67%.
- Accuracy personas: 52,45%.
- Diferencia: 0,22 puntos porcentuales.
- F1: equilibrio entre Precision y Recall.
- Matriz de confusión: muestra aciertos y errores por clase.
- Feature importance: muestra qué variables utiliza más el árbol.
- `(...)`: hay más niveles ocultos.

---

# CHECKLIST ANTES DE EXPONER

- [ ] Revisar `datos.shape`.
- [ ] Memorizar cantidad exacta de columnas.
- [ ] Revisar Accuracy final.
- [ ] Revisar Precision final.
- [ ] Revisar Recall final.
- [ ] Revisar F1 final.
- [ ] Revisar matriz de confusión.
- [ ] Revisar variable más importante.
- [ ] Tener el árbol legible.
- [ ] Ejecutar todo el notebook.
- [ ] Verificar que los números coincidan con la presentación.

---

# ARCHIVOS A TENER ABIERTOS

Principal:
`Codigo/06_arbol_decision.ipynb`

Apoyo:
- `Codigo/02_datos_faltantes.py`
- `Codigo/03_valores_atipicos_grafico.py`
- `Codigo/04_distribucion_datos.py`
- `Codigo/05_relaciones_variables.py`

Dataset:
`Data/raw/predicciones_personas.csv`
