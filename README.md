
                                                               
# 🛠️ Herramientas de limpiado para CSV                               
                                                               
 Este repositorio contiene un conjunto de herramientas para   
 limpiar, transformar y validar bases de datos usando         
 Streamlit.                                                    
                                                               
 El Validador General es la herramienta principal, que        
 integra funcionalidades de:                                   
   - Validación de columnas                                    
   - Edición de valores                                        
   - Derretido de columnas                                     
   - Pivoteado de datos                                        
                                                               

## Requisitos
 - Python con los módulos: pandas, re y hashlib
 - Streamlit: https://streamlit.io/#install
 - Se recomienda usar un entorno virtual independiente (venv o conda)

 ⚠️ Para subir archivos a PNDA, necesitas:
   - VPN activa
   - Autenticación
   - Módulos de PNDA tools: https://github.com/irvingfisica/pndatools/tree/main

 En Conda, para instalar PNDA tools:
 conda install -c anaconda git

# Ejecución de las herramientas

## 🌟 Validador General (recomendado)
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/completo.py

## 🔹 Validador de Columnas
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/validadores.py

## ✏️ Editor de Valores
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/columnas.py

## 🔥 Derretidor
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/derretidor.py

## 📊 Pivoteador
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/pivoteador.py

## ☁️ Subida de Archivos a PNDA
 streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/subir_archivo.py

### Recomendaciones
 - Mantén siempre un backup de tus datos antes de aplicar transformaciones
 - Usa la vista previa antes de promover los cambios en derretido y pivoteado
 - Ejecuta todas las herramientas dentro de un entorno virtual aislado
 - Si eres nuevo, empieza con el Validador General
