import streamlit as st
import io
import pandas as pd

st.title("Pivoteador")

cols_ui = st.columns([2,1])
with cols_ui[0]:
    upload_file = st.file_uploader("carga un archivo CSV", type=['csv'])
with cols_ui[1]:
    encoding = st.text_input(f"Selecciona el encoding del archivo:", value="UTF8",help="Si el archivo tiene caracteres extraños, prueba con cp1252, cp850 o Latin1. El archivo de salida siempre será UTF8")


if upload_file is not None:
    try:
        df = pd.read_csv(upload_file, encoding=encoding)

        st.success("El archivo fue cargado correctamente")
        st.write("Vista previa de los datos:")
        st.dataframe(df)

        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

        df_transformado = df.copy()
        configuracion = {}

        st.subheader("Selecciona las columnas que usarás como id, como nuevas columnas y como valores")

        for col in df.columns:
            seleccion = st.selectbox(
                f"Columna: {col}",
                options = ["identificador","columnas","valores","eliminar"],
                index = 0
            )
            configuracion[col] = seleccion
            
        if st.button("Transformar"):

            index = [col for col,value in configuracion.items() if value == "identificador"]
            columns = [col for col,value in configuracion.items() if value == "columnas"]
            values = [col for col,value in configuracion.items() if value == "valores"]
            df_transformado = pd.pivot(df_transformado,index=index,columns=columns,values=values)
            df_transformado.columns = ['_'.join(column) for column in df_transformado.columns.to_flat_index()]
            df_transformado = df_transformado.reset_index()

            st.write("Vista previa después de pivotear las columnas:")
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
