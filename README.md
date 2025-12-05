# LOGIMAYAB DATA
## Presentado por FITME
Paulina Almada Martínez (A01710029)
Mauricio Benavente Revuelta (A01705898)
Sol Venecia Ramos Vallejo (A01066646)
Daniela Isabel Tapia Martínez (A01710768)

## ¿Cuál fue nuestro enfoque?
El dashboard se construyó a partir del entendimiento de que la Planificación & Gestión de la Demanda Logística en LOGÍSTICA DEL MAYAB debe operar bajo un modelo jerárquico —Ruta/Cliente/Unidad— debido a las diferencias estructurales, la concentración extrema del volumen y la variabilidad severa observada en la operación.
Los insights estadísticos definieron qué debía verse, cómo debía agruparse, y qué decisiones debía habilitar el dashboard.

### 1. Actual State (Vista General a Nivel Ruta)

Insight que responde: Variabilidad extrema del tiempo de ciclo (heterocedasticidad, p = 0).
Por qué existe esta lámina:
El análisis demostró que la operación NO puede planearse con tiempos promedio porque las rutas no se comportan igual: algunas son estables y otras caóticas.
Por eso, la primera lámina se centra en mostrar el estado actual a nivel ruta, con:
* Tiempo de ciclo real vs histórico
* Nivel de variabilidad
* Buffer sugerido según estabilidad/caos
* Indicadores esenciales de comportamiento por ruta

### 2. Unidades — “Asigna tus unidades”
Esta lámina integra el insight del ralentí.
El modelo estadístico y la simulación mostraron que reasignar las unidades con mayor ralentí hacia rutas cortas reduce 7,307.33 horas de tiempo muerto (p = 0.0315).

Por eso, en esta sección se puede:
* Ver el ralentí actual por unidad
* Comparar el escenario real vs simulado
* Identificar qué unidades deben moverse a qué rutas
* Aplicar filtros por categoría de ruta (corta / media / larga / urbana) definidos en la lámina anterior
* Optimizar la asignación para disminuir desperdicio operativo

En esencia: aquí se decide cómo usar la flota para maximizar eficiencia.

### 3. Rutas — “Conoce tus rutas”
Esta lámina establece la base del dashboard porque el análisis demostró que la operación requiere planificación segmentada por predictibilidad debido a la variabilidad extrema del tiempo de ciclo (p = 0).

Sin embargo, en esta sección solo se presentan dos elementos clave:

La categorización de cada ruta en corta, media, larga y urbana.

La distribución de los viajes por tipo de ruta, mostrando cómo se comporta el volumen operativo en cada categoría.

Esta lámina sirve como marco de referencia: define la estructura de rutas que se utilizará en las secciones posteriores para filtrar y analizar la asignación de unidades y la gestión de demanda de forma coherente con la operación real.

### 4. Demanda — “Gestiona tu demanda”
Esta lámina convierte el insight de variabilidad extrema en acción directa.

El análisis mostró heterocedasticidad severa, lo que implica que no todas las rutas se pueden planear igual.
Por eso esta sección permite:
* Identificar las rutas más variables vs más estables
* Visualizar el riesgo operativo de cada una
* Asignar buffers recomendados basados en variabilidad histórica
* Priorizar dónde se necesita protección para mantener la confiabilidad operativa

Esta lámina responde a la necesidad de manejar la incertidumbre con precisión, no con promedios.

### Recomendaciones (para todo el dashboard)
En una futura reconstrucción del dashboard se recomienda integrar un filtro por cliente, ya que el insight de concentración de la demanda (20% de los clientes generan el 91% de los viajes) habilita que cada vista —rutas, unidades y demanda— pueda analizarse también desde la perspectiva de los clientes críticos que realmente determinan el comportamiento operativo.

## ¿Cómo corre la aplicación?
La aplicación está desarrollada con Streamlit y el archivo principal es `app.py`. Para ejecutarla, sigue estos pasos:

1. Instala las librerías necesarias usando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta la aplicación con el siguiente comando:
   ```bash
   streamlit run app/app.py
   ```
   En caso de que este comando marque error, intente:
   ```bash
   python -m streamlit run app/app.py
   ```
   Para Macs:
   ```bash
   python3 -m streamlit run app/app.py
   ```

## ¿Qué tecnologías usamos?
Las principales tecnologías utilizadas en este proyecto son:
### **Streamlit**: Para la creación de la interfaz web interactiva.
Utilizamos Streamlit por su flexibilidad y su facilidad de creación de dashboards interactivos. Nos permitió acercarnos a nuestro diseño original y crear gráficas interactivas complejas, incluyendo filtros como sliders y selección, sin tener que sacrificar el rendimiento de la página o tener que llevar un proceso muy intensivo de programación. Además, permitió tener un proceso de integración muy simple con las librerías de Pandas que ya estabamos manejando para la analítica de los datos.
### **Plotly**: Para la visualización de datos y gráficos dinámicos.
Utilizamos Plotly por su integración con Streamlit. Permite generar gráficas complejas e interactivas pero ligeras, que responden nativamente a los filtros de Streamlit. Es una tecnología muy intuitiva que no requiere tener que especificar de más cada detalle de información que se quiere desplegar. Además, nos permitió personalizar los gráficos generados.
### **Pandas**: Para la manipulación y análisis de datos.
Utilizamos Pandas porque es una de las librerías más poderosas para el manejo de datos con Python. La estructura de los dataframes, además, se adecua muy bien en forma de tablas para desplegar información en Streamlit al igual que en el entrenamiento y evaluación de modelos con Scikit-learn.
### **Scikit-learn**: Para tareas de machine learning y análisis estadístico.
Utilizamos Sckiti-learn porque es una librería que tiene una gran variedad de distintos modelos de machine learning con una implementación, fine-tuning y evaluación simple e intuitiva. Pudimos generar modelos confiables con poco código. Además, se integra bien con el resto de nuestro ambiente de desarrollo del proyecto. En específico, utilizamos RandomForest porque buscamos un modelo predictivo que respondiera a los features, en este caso de ralentí en rutas, pero no tuviera overfitting.