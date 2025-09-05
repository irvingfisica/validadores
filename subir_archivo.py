import streamlit as st
from pndatools import SFTPCliente
import os
import pandas as pd
import shutil
import ckanapi

st.title("Subida de archivos al repo")

st.header("Conexión al repo")
ip_servidor = '192.168.246.10'
url_base = 'https://repodatos.atdt.gob.mx/'
usuario = 'cloud-user'

ckan = ckanapi.RemoteCKAN('https://www.datos.gob.mx/')

if "cliente" not in st.session_state:
    st.session_state.cliente = None

if st.button("Conectar"):
    if not ip_servidor or not usuario:
        st.error("Debes agregar el IP y el usuario")
    else:
        try:
            st.session_state.cliente = SFTPCliente("", ip_servidor, usuario)
            st.success("Conexión exitosa")
        except Exception as e:
            st.error(f"No se pudo conectar: {e}")
            st.session_state.cliente = None

cliente = st.session_state.cliente

st.header("Información del archivo")
instituciones_disponibles = ckan.action.organization_list()
institucion = st.selectbox("Selecciona la institución (si la institución que necesitas no está disponible dala de alta en la PNDA)", instituciones_disponibles)

conjuntos_disponibles = [i["name"] for i in ckan.action.organization_show(id=institucion, include_datasets=True)["packages"]]
conjunto = st.selectbox("Selecciona el conjunto (si el conjunto que necesitas no está disponible dalo de alta en la PNDA)", conjuntos_disponibles)

archivo_subir = st.file_uploader("Selecciona el archivo CSV", type=["csv"])

if archivo_subir is not None:
    try:
        df_preview = pd.read_csv(archivo_subir)
        st.write("Preview del CSV:")
        st.dataframe(df_preview)
    except Exception as e:
        st.error(f"No se pudo leer el CSV: {e}")

if st.button("Subir archvio"):
    if cliente is None:
        st.error("Debes conectar primero al repo")
    elif not conjunto:
        st.error("Debes indicar el directorio del conjunto")
    elif archivo_subir is None:
        st.error("Debes seleccionar un archivo CSV")
    else:
        temp_dir = "temp_upload"
        os.makedirs(temp_dir, exist_ok=True)
        ruta_local_temp = os.path.join(temp_dir, archivo_subir.name)
        try:
            with open(ruta_local_temp, "wb") as f:
                f.write(archivo_subir.getbuffer())

            ruta_remota = f"api_update/{institucion}/{conjunto}/"
            cliente.crear_ruta_abs(ruta_remota)
            st.write(f"Ruta remota creada: {ruta_remota}")

            cliente.subir_archivo(ruta_local_temp, archivo_subir.name)
            st.success("Archivo subido correctamente")

            archivos = cliente.sftp.listdir()
            df_archivos = pd.DataFrame(archivos, columns=["Nombre del archivo"])
            st.write("Archivos en el repo:")
            st.dataframe(df_archivos)

            url_repo = cliente.obtener_ruta_repo(ruta_remota + archivo_subir.name, url_base)
            st.write(f"Archivo disponible en repo:")
            st.write(url_repo)

        except Exception as e:
            st.error(f"Error al subir archivo: {e}")
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
