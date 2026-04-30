# 🛠️ Herramientas de limpiado para CSV 
 
 Este repositorio contiene un conjunto de herramientas para limpiar, transformar y validar bases de datos en CSV usando Streamlit.
 
 El Validador General es la herramienta principal, que integra funcionalidades de: 
 - Validación de columnas
 - Edición de valores
 - Derretido de columnas 
 - Pivoteado de datos

Puedes usar la herramienta en este enlace: https://validadores.streamlit.app/

O puedes usarla en tu compu como servicio local:

# Ejecución de las herramientas en local

## Forma de ejecutar recomendada:
La forma más fácil de ejecutarlo es a través de uv: https://docs.astral.sh/uv/

Si se tiene instalado uv no hay que instalar nada más. uv se encargará de instalar una vez todo lo necesario...

Para ejecutar cada herramienta tienes que ejecutar esto en tu terminal:

## 🌟 Validador General (recomendado)
 `uv run --with streamlit streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/completo.py`

## Herramientas por separado

### 🔹 Validador de Columnas
 `uv run --with streamlit streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/validadores.py`

### ✏️ Editor de Valores
 `uv run --with streamlit streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/columnas.py`

### 🔥 Derretidor
 `uv run --with streamlit streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/derretidor.py`

### 📊 Pivoteador
 `uv run --with streamlit streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/pivoteador.py`

## Ejecución en local sin uv
Tambien puedes ejecutarlo en un ambiente de python local

### Requisitos
 - Python con los módulos: pandas, re y hashlib
 - Streamlit: https://streamlit.io/#install
 - Se recomienda usar un entorno virtual independiente (venv o conda)

## 🌟 Validador General (recomendado)
 `streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/completo.py`

## Herramientas por separado

### 🔹 Validador de Columnas
 `streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/validadores.py`

### ✏️ Editor de Valores
 `streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/columnas.py`

### 🔥 Derretidor
 `streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/derretidor.py`

### 📊 Pivoteador
 `streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/pivoteador.py`

### Recomendaciones
 - Mantén siempre un backup de tus datos antes de aplicar transformaciones
 - Usa la vista previa antes de promover los cambios en derretido y pivoteado
 - Ejecuta todas las herramientas dentro de un entorno virtual aislado
 - Si eres nuevo, empieza con el Validador General



