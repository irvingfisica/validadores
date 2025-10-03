import streamlit as st
import re
import pandas as pd
import hashlib
from difflib import SequenceMatcher

# -------------------
# Funciones auxiliares
# -------------------
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def transformar_a_texto(serie: pd.Series) -> pd.Series:
    return serie.fillna("sin dato").astype(str).str.strip()

def transformar_a_texto_minusculas(serie: pd.Series) -> pd.Series:
    return serie.fillna("sin dato").astype(str).str.strip().str.lower()

def transformar_a_texto_capitalizar(serie: pd.Series) -> pd.Series:
    new_ser = serie.fillna("sin dato").astype(str).str.strip().str.title()
    new_ser = new_ser.str.replace(" De "," de ").str.replace(" Del "," del ")
    new_ser = new_ser.str.replace(" Y "," y ").str.replace(" El "," el ")
    new_ser = new_ser.str.replace(" La "," la ").str.replace(" A "," a ")
    new_ser = new_ser.str.replace(" En "," en ")
    return new_ser

def anonimizar(serie: pd.Series) -> pd.Series:
    return serie.apply(lambda x: hashlib.sha256(str(x).encode()).hexdigest())

def transformar_a_numerica(serie: pd.Series) -> pd.Series:
    serie_limpia = serie.astype(str).str.strip()
    serie_limpia = serie_limpia.str.replace(r'[\$,€]', '', regex=True)
    serie_limpia = serie_limpia.str.replace(",","")
    serie_limpia = serie_limpia.replace(["","-"," ","NA","N/A","ND","nd","*","na","nan","null","None"],pd.NA)

    return pd.to_numeric(serie_limpia, errors="raise")

def transformar_a_numerica_coordenada(serie: pd.Series) -> pd.Series:
    serie_limpia = serie.astype(str).str.strip()
    serie_limpia = serie_limpia.replace(["","-"," ","NA","N/A","na","nan","null","None"],0.0)

    return pd.to_numeric(serie_limpia, errors="raise")

def transformar_a_fecha(serie: pd.Series) -> pd.Series:
    serie_limpia = serie.astype(str).str.strip()
    serie_limpia = serie_limpia.str.replace(r'[/.\s]','-',regex = True)

    serie_limpia = serie_limpia.replace(
        ["", " ", "NaT", "nan", "None", "null", "NA", "N/A"], 
        pd.NaT
    )

    try:
        return pd.to_datetime(serie_limpia,format="%d-%m-%Y", errors="raise")
    except ValueError:
        return pd.to_datetime(serie_limpia, format="%Y-%m-%d", errors="raise")
    
def sugerir_nombre(columna):
    newcol = columna.lower().strip()
    newcol = newcol.replace("\n","_")
    newcol = newcol.replace("_1","_01")
    newcol = newcol.replace("ñ","ni")
    newcol = newcol.replace(",","").replace(".","").replace(";","").replace(":","_").replace("/","_")
    newcol = newcol.replace(" ","_").replace("-","_")
    newcol = newcol.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
    newcol = newcol.replace("_de_","_").replace("_del_","_").replace("_a_","_").replace("_por_","_").replace("_en_","_")
    newcol = newcol.replace("_la_","_").replace("_el_","_").replace("_los_","_").replace("_las_","_")
    newcol = re.sub(r'_+','_',newcol)
    return newcol

def inferir_tipo(serie: pd.Series):
    dtype = df[col].dtype
    if pd.api.types.is_numeric_dtype(dtype):
        sugerido = "numerica"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        sugerido = "fecha"
    else:
        sugerido = "texto"
    return sugerido

# -------------------
# Interfaz principal
# -------------------
st.title("Herramientas de limpiado para CSV")

herramientas = [
    "Cargar CSV",
    "Validador de Columnas",
    "Editor de Valores",
    "Derretidor",
    "Pivoteador"
]
opcion = st.sidebar.selectbox("Selecciona la herramienta", herramientas)

# -------------------
# Sección de carga y exportación
# -------------------
if opcion == "Cargar CSV":

    st.markdown("""
    ### ¿Cómo funciona esta herramienta?
    Aplica las transformaciones que necesites paras que tu base de datos esté más limpia.

    - Comienza cargando un archivo y luego selecciona las herramientas de la izquierda.  
    - Una vez cargado, el sistema **mantiene los datos en memoria** (estado de sesión) para que puedas aplicar varias transformaciones sin perder tu trabajo.  
    - Cada herramienta modifica tus datos y genera una nueva versión sobre la cual puedes seguir aplicando transformaciones.  
    - Cuando estés conforme con los cambios, puedes exportarlos.  
    - Al cargar un nuevo archivo, **todo el estado se reinicia** y se empieza desde cero.
    """)

    st.subheader("Carga un archivo")

    cols_ui = st.columns([2,1])
    with cols_ui[0]:
        upload_file = st.file_uploader("Carga un archivo CSV", type=['csv'])
    with cols_ui[1]:
        encoding = st.text_input("Encoding del archivo:", value="UTF8", help="Si el archivo tiene caracteres extraños, prueba con cp1252, cp850 o Latin1. El archivo de salida siempre será UTF8")

    if upload_file is not None:
        try:
            df = pd.read_csv(upload_file, encoding=encoding)
            df = df.dropna(how="all").dropna(how="all", axis=1)

            for key in list(st.session_state.keys()):
                if key != "upload_file_name": 
                    del st.session_state[key]

        
            st.session_state.upload_file_name = upload_file.name
        
            st.session_state.df = df
            st.success("Archivo cargado correctamente")

        except UnicodeDecodeError as e:
            st.error(
                "⚠️ No se pudo leer el archivo con el encoding seleccionado.\n\n"
                "Prueba con alguno de estos encodings: **cp1252**, **latin1**, **cp850**."
            )
        except pd.errors.ParserError as e:
            st.error(
                "⚠️ El archivo no parece tener un formato CSV válido.\n\n"
                "Verifica que el archivo esté separado por comas (,)."
            )
        except Exception as e:
            st.error(
                f"⚠️ No se pudo leer el archivo. Solo se aceptan archivos CSV.\n\n"
                f"Error técnico: {e}"
            )

    if 'df' in st.session_state:
        st.subheader("Estos son los datos que están cargados actualmente:")
        st.dataframe(st.session_state.df)


# -------------------
# Validador de Columnas
# -------------------
elif opcion == "Validador de Columnas":

    st.markdown("""
    ### Validador de columnas

    Permite modificar los nombres de las columnas y transformar el tipo de datos de cada una.

    - La herramienta sugiere nombres de columna que puedes editar.  
    - Permite aplicar transformaciones al texto para manejar mejor mayúsculas y minúsculas.  
    - Permite corregir valores de cifras para que sean columnas numéricas.  

    """)

    if 'df' not in st.session_state:
        st.warning("Carga primero un archivo CSV en la sección 'Cargar / Exportar'")
    else:
        df = st.session_state.df.copy()
        st.subheader("Vista previa del CSV")
        st.dataframe(df)
        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

        configuracion = {}

        st.subheader("Escribe los nombres de columna deseados y selecciona el tipo de dato para cada columna:")

        for idx, col in enumerate(df.columns):
            tipo_sugerido = inferir_tipo(df[col])
            nombre_sugerido = sugerir_nombre(col)

            cols_ui = st.columns([2,1])
            with cols_ui[0]:
                nuevo_nombre = st.text_input(f"Nombre para '{col}'",
                                             value=nombre_sugerido,
                                             key=f"nombre_{idx}_{col}")
            with cols_ui[1]:
                tipo = st.selectbox("Tipo de datos:",
                                    options=[
                                        "texto",
                                        "texto | minusculas",
                                        "texto | capitalizado",
                                        "numerica",
                                        "numerica | coordenada",
                                        "fecha",
                                        "anonimizar",
                                        "eliminar columna"
                                    ],
                                    index=["texto","texto | minusculas","texto | capitalizado",
                                           "numerica","numerica | coordenada","fecha",
                                           "anonimizar","eliminar columna"].index(tipo_sugerido),
                                    key=f"tipo_{idx}_{col}")
            configuracion[col] = {"nuevo_nombre": nuevo_nombre, "tipo": tipo}

        if st.button("Aplicar transformaciones", key="btn_validador"):
            df_trans = df.copy()
            exitosas, sin_cambios, fallidas = [], [], []

            for col, conf in configuracion.items():
                original = df[col]
                try:
                    if conf["tipo"] == "texto":
                        df_trans[col] = transformar_a_texto(df[col])
                    elif conf["tipo"] == "texto | minusculas":
                        df_trans[col] = transformar_a_texto_minusculas(df[col])
                    elif conf["tipo"] == "texto | capitalizado":
                        df_trans[col] = transformar_a_texto_capitalizar(df[col])
                    elif conf["tipo"] == "numerica":
                        df_trans[col] = transformar_a_numerica(df[col])
                    elif conf["tipo"] == "numerica | coordenada":
                        df_trans[col] = transformar_a_numerica_coordenada(df[col])
                    elif conf["tipo"] == "fecha":
                        df_trans[col] = transformar_a_fecha(df[col])
                    elif conf["tipo"] == "anonimizar":
                        df_trans[col] = anonimizar(df[col])

                    if df_trans[col].equals(original):
                        sin_cambios.append(conf["nuevo_nombre"])
                    else:
                        exitosas.append(conf["nuevo_nombre"])
                except Exception:
                    df_trans[col] = df[col]
                    fallidas.append(conf["nuevo_nombre"])

            # Renombrar columnas
            nuevos_nombres = {col: conf["nuevo_nombre"] for col, conf in configuracion.items() if conf["tipo"] != "eliminar columna"}
            df_trans.rename(columns=nuevos_nombres, inplace=True)

            # Eliminar columnas
            eliminar = [col for col, conf in configuracion.items() if conf["tipo"] == "eliminar columna"]
            df_trans.drop(columns=eliminar, inplace=True)

            # Guardar en session_state
            st.session_state.df = df_trans

            # Reporte
            st.subheader("Resultados de las transformaciones")
            if sin_cambios:
                st.success("Columnas sin cambio")
                st.table(pd.DataFrame({"Columna": sin_cambios, "Estado": "Sin cambio"}))
            if exitosas:
                st.success("Transformaciones exitosas")
                st.table(pd.DataFrame({"Columna": exitosas, "Estado": "Transformada"}))
            if fallidas:
                st.error("Transformaciones fallidas")
                st.table(pd.DataFrame({"Columna": fallidas, "Estado": "Falló"}))
            if eliminar:
                st.error("Columnas eliminadas")
                st.table(pd.DataFrame({"Columna": eliminar, "Estado": "Eliminada"}))

            st.subheader("Vista previa después de aplicar transformaciones")
            st.dataframe(df_trans)


# -------------------
# Editor de Cadenas
# -------------------
elif opcion == "Editor de Valores":

    st.markdown("""
    ### Editor de valores

    Permite aplicar reglas de limpieza sobre los valores dentro de las columnas:

    - Al seleccionar una columna detecta valores similares.  
    - Permite cambiar un valor por alguno similar o editarlo para generar uno nuevo.  
    - Se puede usar para corregir valores directamente, poner acentos, cambiar nombres, etc.  

    """)

    if 'df' not in st.session_state:
        st.warning("Carga primero un archivo CSV en la sección 'Cargar / Exportar'")
    else:
        df = st.session_state.df.copy()
        st.subheader("Vista previa del CSV")
        st.dataframe(df)

        st.subheader("Selecciona una columna para explorar sus valores y modificarlos:")

        text_columns = [c for c in df.columns if df[c].dtype == object or str(df[c].dtype).startswith("string")]
        if not text_columns:
            st.warning("No hay columnas de texto en el CSV")
        else:
            col = st.selectbox("Selecciona la columna a editar", text_columns, key="editor_columna")

            counts = df[col].value_counts().reset_index()
            counts.columns = [col, "Frecuencia"]

            threshold = st.slider("Selecciona un valor para el umbral de similitud entre valores", 0.3, 0.99, 0.85, 0.01, key="editor_umbral")

            # Calcular sugerencias
            suggestions = {}
            for i, row in counts[::-1].iterrows():
                val = row[col]
                for j, candidate in counts.iterrows():
                    if candidate[col] == val:
                        continue
                    score = similar(val, candidate[col])
                    if score >= threshold:
                        suggestions.setdefault(val, []).append(candidate[col])

            def highlight_similar(val):
                if val in suggestions:
                    return "background-color: #ffcccc"
                return "background-color: #ccffcc"

            st.markdown("Los valores en rojo son similares a otros en la columna, revísalos:")
            st.dataframe(counts.style.applymap(highlight_similar, subset=[col]))

            st.markdown("### Corrige los valores que desees cambiar, puedes usar otros valores o escribir un nuevo valor")
            edited = {}

            for i, row in counts.iterrows():
                val = row[col]
                freq = row["Frecuencia"]
                options = [val] + suggestions.get(val, [])

                c1, c2 = st.columns([2, 3])
                with c1:
                    selected = st.selectbox(f"{val} ({freq} veces)", options, index=0, key=f"selector_{col}_{i}")
                with c2:
                    new_val = st.text_input("Editar valor", value=selected, key=f"text_{col}_{i}")
                edited[val] = new_val

            if st.button("Aplicar cambios", key="editor_aplicar"):
                before = df[col].copy()
                df[col] = df[col].map(lambda x: edited.get(x, x))
                st.session_state.df = df

                # Recuento de cambios por valor
                mask = before != df[col]
                total_cambios = mask.sum()

                st.subheader("Reporte de cambios aplicados")
                if total_cambios > 0:
                    st.success(f"Se aplicaron {total_cambios} cambios en la columna `{col}`.")
                    resumen = []
                    for old_val, new_val in edited.items():
                        if old_val != new_val:
                            reemplazos = ((before == old_val) & mask).sum()
                            if reemplazos > 0:
                                resumen.append({"Valor original": old_val, "Nuevo valor": new_val, "Reemplazos": reemplazos})
                    st.table(pd.DataFrame(resumen))
                else:
                    st.info("No se realizaron cambios en esta columna.")

                st.subheader("Vista previa después de aplicar cambios")
                st.dataframe(df)

# -------------------
# Derretidor
# -------------------
elif opcion == "Derretidor":
    st.markdown("""
    ### Derretidor (Melt)

    Convierte columnas en filas, útil para **normalizar tablas anchas**.  

    Ejemplo:  
    - Tienes una tabla con las columnas `Enero, Febrero, Marzo` → se derrite en dos columnas: `Mes` y `Valor`.  

    Útil cuando los datos están en formato **wide** y necesitas pasarlos a **long** para análisis estadístico o carga en base de datos.
    """)
    
    if 'df' not in st.session_state:
        st.warning("Carga primero un archivo CSV")
    else:
        df = st.session_state.df.copy()
        st.subheader("Vista previa del CSV")
        st.dataframe(df)

        st.subheader("Selecciona el rol de cada columna para poder derretir el CSV:")

        configuracion = {}
        for col in df.columns:
            seleccion = st.selectbox(
                f"Columna: {col}",
                options = ["identificador","valor","eliminar"],
                index = 0
            )
            configuracion[col] = seleccion
        
        st.write("Define los nombres de las columnas a crear")
        cols_ui = st.columns([2,1])
        with cols_ui[0]:
            var_name = st.text_input("Nombre para la columna de variables:", value="categorias")
        with cols_ui[1]:
            value_name = st.text_input("Nombre para la columna de valores:", value="valor")
            
        # Botón para generar vista previa
        if st.button("Transformar"):
            id_vars = [col for col,value in configuracion.items() if value == "identificador"]
            value_vars = [col for col,value in configuracion.items() if value == "valor"]

            df_melted = pd.melt(df, id_vars=id_vars, value_vars=value_vars,
                                var_name=var_name, value_name=value_name)
            st.session_state['derretidor_preview'] = df_melted  # << guarda en session_state

        # Mostrar preview si existe
        if 'derretidor_preview' in st.session_state:
            st.write("Vista previa después de derretir las columnas:")
            st.dataframe(st.session_state['derretidor_preview'])

            c1, c2 = st.columns([1,1])
            with c1:
                if st.button("Promover cambio"):
                    st.session_state.df = st.session_state['derretidor_preview']
                    del st.session_state['derretidor_preview']
                    st.success("Cambio promovido al frame principal.")
            with c2:
                if st.button("Descartar vista previa"):
                    del st.session_state['derretidor_preview']
                    st.info("Vista previa descartada.")

# -------------------
# Pivoteador
# -------------------
elif opcion == "Pivoteador":
    st.markdown("""
    ### Pivoteador

    Convierte filas en columnas.  

    Ejemplo:  
    - Tienes una columna `Mes` con valores `Enero, Febrero, Marzo` → se transforma en columnas `Enero, Febrero, Marzo`.  

    Útil cuando necesitas tablas **resumidas por categorías**.
    """)
    
    if 'df' not in st.session_state:
        st.warning("Carga primero un archivo CSV")
    else:
        df = st.session_state.df.copy()
        st.subheader("Vista previa del CSV")
        st.dataframe(df)

        st.subheader("Selecciona el rol de cada columna para poder pivotear el CSV:")

        configuracion = {}
        for col in df.columns:
            seleccion = st.selectbox(
                f"Columna: {col}",
                options = ["identificador","columnas","valores","eliminar"],
                index = 0
            )
            configuracion[col] = seleccion

        # Botón para generar vista previa
        if st.button("Transformar"):
            index = [col for col,value in configuracion.items() if value == "identificador"]
            columns = [col for col,value in configuracion.items() if value == "columnas"]
            values = [col for col,value in configuracion.items() if value == "valores"]

            df_pivot = pd.pivot(df, index=index, columns=columns, values=values)
            df_pivot.columns = ['_'.join(column) for column in df_pivot.columns.to_flat_index()]
            df_pivot = df_pivot.reset_index()

            st.session_state['pivoteador_preview'] = df_pivot  # << guarda en session_state

        # Mostrar preview si existe
        if 'pivoteador_preview' in st.session_state:
            st.write("Vista previa después de pivotear las columnas:")
            st.dataframe(st.session_state['pivoteador_preview'])

            c1, c2 = st.columns([1,1])
            with c1:
                if st.button("Promover cambio"):
                    st.session_state.df = st.session_state['pivoteador_preview']
                    del st.session_state['pivoteador_preview']
                    st.success("Cambio promovido al frame principal.")
            with c2:
                if st.button("Descartar vista previa"):
                    del st.session_state['pivoteador_preview']
                    st.info("Vista previa descartada.")

# -------------------
# Exportar CSV común
# -------------------
if 'df' in st.session_state and opcion != "Cargar / Exportar":
    st.sidebar.subheader("Exportar CSV")
    csv_bytes = st.session_state.df.to_csv(index=False).encode("utf-8")
    nombre_salida = st.session_state.get('upload_file_name', 'exportado.csv')
    st.sidebar.download_button(
        "Descargar CSV",
        data=csv_bytes,
        file_name=nombre_salida,
        mime="text/csv"
    )
