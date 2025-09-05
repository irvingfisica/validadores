## Validadores

Estos validadores son un conjunto de herramientas para limpiar, transformar y validar bases de datos.

Para usarlos es necesario [instalar Streamlit](https://streamlit.io/#install). 

Una vez installado Streamlit se debe ejecutar en la terminal la siguiente línea de código:

Para el validador general:
`streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/validadores.py` 

Para el derretidor:
`streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/derretidor.py` 

Para el pivoteador:
`streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/pivoteador.py` 


Además hay una herramienta que permite subir datos al repo de la PNDA. (Para poder hacerlo es necesario tener activa la VPN y autenticar el ingreso.)

Herramienta para subir archivos:
`streamlit run https://raw.githubusercontent.com/irvingfisica/validadores/refs/heads/main/subir_archivo.py` 

Para poder ejecutar esta herramienta es necesario instalar los módulos de apoyo que se encuentran en este repo: [PNDA tools](https://github.com/irvingfisica/pndatools/tree/main).

Para todas las herramientas es necesario instalar PANDAS, re y hashlib. Se recomienda hacerlo en un env independiente.

En conda para poder instalar las PNDA tools es necesario instalar git en el env. (conda install -c anaconda git)