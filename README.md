# LOGIMAYAB DATA
## Presentado por FITME
Paulina Almada Martínez (A01710029)
Mauricio Benavente Revuelta (A01705898)
Sol Venecia Ramos Vallejo (A01066646)
Daniela Isabel Tapia Martínez (A01710768)

## ¿Cuál fue nuestro enfoque?

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
