import streamlit as st
import io
import re
import pandas as pd
import hashlib

def transformar_a_texto(serie: pd.Series) -> pd.Series:
    return serie.fillna("sin dato").astype(str).str.strip()

def transformar_a_texto_minusculas(serie: pd.Series) -> pd.Series:
    return serie.fillna("sin dato").astype(str).str.strip().str.lower()

def transformar_a_texto_capitalizar(serie: pd.Series) -> pd.Series:
    new_ser = serie.fillna("sin dato").astype(str).str.strip().str.title().str.title()
    new_ser = new_ser.str.replace(" De "," de ")
    new_ser = new_ser.str.replace(" Del "," del ")
    new_ser = new_ser.str.replace(" Y "," y ")
    new_ser = new_ser.str.replace(" El "," el ")
    new_ser = new_ser.str.replace(" La "," la ")
    new_ser = new_ser.str.replace(" A "," a ")
    new_ser = new_ser.str.replace(" En "," en ")
    return new_ser

def anonimizar(serie: pd.Series) -> pd.Series:
    return serie.apply(
    lambda x: hashlib.sha256(x.encode()).hexdigest())

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

st.title("Validadores")

cols_ui = st.columns([2,1])
with cols_ui[0]:
    upload_file = st.file_uploader("carga un archivo CSV", type=['csv'])
with cols_ui[1]:
    encoding = st.text_input(f"Selecciona el encoding del archivo:", value="UTF8",help="Si el archivo tiene caracteres extraños, prueba con cp1252, cp850 o Latin1. El archivo de salida siempre será UTF8")


if upload_file is not None:
    try:
        df = pd.read_csv(upload_file, encoding=encoding)
        df = df.dropna(how="all").dropna(how="all",axis=1)

        st.success("El archivo ha sido correctamente")
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

        configuracion = {}

        st.subheader("Escribe los nombres de columna deseados y selecciona el tipo de dato para cada columna:")

        for idx,col in enumerate(df.columns):

            tipo_sugerido = inferir_tipo(df[col])
            nombre_sugerido = sugerir_nombre(col)

            cols_ui = st.columns([2,1])
            with cols_ui[0]:
                nuevo_nombre = st.text_input(f"Nombre para '{col}'", value=nombre_sugerido)
            with cols_ui[1]:
                tipo = st.selectbox(f"Tipo de datos: ", 
                                    options=["texto","texto | minusculas","texto | capitalizado","numerica","numerica | coordenada","fecha","anonimizar","eliminar columna"],
                                    index=["texto","texto | minusculas","texto | capitalizado","numerica","numerica | coordenada","fecha","anonimizar","eliminar columna"].index(tipo_sugerido),
                                    key=f"type_{idx}_{col}")
            configuracion[col] = {"nuevo_nombre": nuevo_nombre, "tipo": tipo}

        if st.button("Aplicar transformaciones"):
            df_transformado = df.copy()
            exitosas = []
            sin_cambios = []
            fallidas = []

            for col, conf in configuracion.items():
                original = df[col]
                try:
                    if conf["tipo"] == "texto":
                        df_transformado[col] = transformar_a_texto(df[col])
                    elif conf["tipo"] == "texto | minusculas":
                        df_transformado[col] = transformar_a_texto_minusculas(df[col])
                    elif conf["tipo"] == "texto | capitalizado":
                        df_transformado[col] = transformar_a_texto_capitalizar(df[col])
                    elif conf["tipo"] == "numerica":
                        df_transformado[col] = transformar_a_numerica(df[col])
                    elif conf["tipo"] == "numerica | coordenada":
                        df_transformado[col] = transformar_a_numerica_coordenada(df[col])
                    elif conf["tipo"] == "fecha":
                        df_transformado[col] = transformar_a_fecha(df[col])
                    elif conf["tipo"] == "anonimizar":
                        df_transformado[col] = anonimizar(df[col])

                    if df_transformado[col].equals(original):
                        sin_cambios.append(conf["nuevo_nombre"])
                    else:
                        exitosas.append(conf["nuevo_nombre"])

                except Exception:
                    df_transformado[col] = df[col]
                    fallidas.append(conf["nuevo_nombre"])

            nuevos_nombres = {col: conf["nuevo_nombre"] for col, conf in configuracion.items() if conf["tipo"] != "eliminar columna"}
            df_transformado.rename(columns=nuevos_nombres, inplace=True)

            eliminar = [col for col, conf in configuracion.items() if conf["tipo"] == "eliminar columna"]
            df_transformado.drop(columns=eliminar,inplace=True)
            
            st.subheader("Resultados de las transformaciones")

            if sin_cambios:
                st.success("Columnas sin cambio después de transformadas")
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

            st.write("Vista previa después de transformar y renombrar:")
            st.dataframe(df_transformado)

        if 'df_transformado' in locals():
            st.subheader("Exportar CSV")

            csv_buffer = io.StringIO()
            df_transformado.to_csv(csv_buffer, index=False)
            csv_bytes = csv_buffer.getvalue().encode('utf-8')

            nombre_salida = upload_file.name

            st.download_button(
                label = "Descargar CSV transformado",
                data = csv_bytes,
                file_name = nombre_salida,
                mime="text/csv"
            )
            

    except Exception as e:

        st.error(f"Error al leer el archivo: {e}")



