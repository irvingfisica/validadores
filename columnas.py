import streamlit as st
import io
import pandas as pd
from difflib import SequenceMatcher

def similar(a,b):
    return SequenceMatcher(None, a, b).ratio()

st.title("Editor de cadenas")

cols_ui = st.columns([2,1])
with cols_ui[0]:
    upload_file = st.file_uploader("carga un archivo CSV", type=['csv'])
with cols_ui[1]:
    encoding = st.text_input(f"Selecciona el encoding del archivo:", value="UTF8",help="Si el archivo tiene caracteres extraños, prueba con cp1252, cp850 o Latin1. El archivo de salida siempre será UTF8")


if upload_file is not None:
    try:
        if "df" not in st.session_state:
            df = pd.read_csv(upload_file)
            df = df.dropna(how="all").dropna(how="all",axis=1)
            st.session_state.df = df

        st.success("El archivo se cargó correctamente")

        df = st.session_state.df

        st.write("Vista previa de los datos:")
        st.dataframe(st.session_state.df)

        st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

        st.subheader("Selecciona la columna que quieras revisar:")

        text_columns = [c for c in df.columns if df[c].dtype == object or str(df[c].dtype).startswith("string")]
        if not text_columns:
            st.warning("No hay columnas de texto en este archivo.")
        else:
            col = st.selectbox("Selecciona la columna a validar", text_columns)

        if "last_col" not in st.session_state or st.session_state.last_col != col:
            for k in list(st.session_state.keys()):
                if k.startswith("selector_") or k.startswith("input_") or k.startswith("text_"):
                    del st.session_state[k]
            st.session_state.last_col = col

        if col:
            st.subheader(f"Valores únicos en columna: `{col}`")

            counts = df[col].value_counts().reset_index()
            counts.columns = [col, "Frecuencia"]

            threshold = st.slider("Umbral de similitud", 0.3, 0.99, 0.85, 0.01)

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
                    return "background-color: #ffcccc"  # rojo claro
                return "background-color: #ccffcc"  
            
            styled_counts = counts.style.applymap(highlight_similar, subset=[col])
            st.dataframe(styled_counts)

            st.markdown("### Corrección manual")
            edited = {}

            for i, row in counts.iterrows():
                val = row[col]
                freq = row["Frecuencia"]

                options = [val] + suggestions.get(val, [])

                c1, c2 = st.columns([2, 3])

                selector_key = f"selector_{col}_{val}"
                input_key = f"input_{col}_{val}"
                text_key = f"text_{col}_{val}"

                if input_key not in st.session_state:
                    st.session_state[input_key] = val

                with c1:
                    selected = st.selectbox(
                        f"{val} ({freq} veces)",
                        options,
                        index=0,
                        key=selector_key
                    )

                if selected != st.session_state[input_key]:
                    st.session_state[input_key] = selected

                with c2:
                    new_val = st.text_input(
                        "Editar valor",
                        value = st.session_state[input_key],
                        key=text_key
                    )

                st.session_state[input_key] = new_val
                edited[val] = new_val

            if st.button("Aplicar cambios"):
                before = st.session_state.df[col].copy()
                st.session_state.df[col] = st.session_state.df[col].map(lambda x: edited.get(x, x))

                mask = before != st.session_state.df[col]
                changes = mask.sum()

                if changes > 0:
                    st.success(f"Se aplicaron los cambios en la columna `{col}`. {changes} valores fueron remplazados.")

                    summary = []
                    for old_val, new_val in edited.items():
                        if old_val != new_val:
                            replaced_count = ((before == old_val) & (mask)).sum()
                            if replaced_count > 0:
                                summary.append(f"**{old_val}** -> **{new_val}** ({replaced_count} veces)")

                    if summary:
                        st.markdown("#### Resumen de remplazos realizados:")
                        for s in summary:
                            st.markdown(f"- {s}")

                else:
                    st.info("No se realizaron cambios en esta columna.")

                counts = st.session_state.df[col].value_counts().reset_index()
                counts.columns = [col, "Frecuencia"]
                styled_counts = counts.style.applymap(highlight_similar, subset=[col])
                st.dataframe(styled_counts)

                st.write("Vista previa de los datos:")
                st.dataframe(st.session_state.df)

            st.subheader("Exportar CSV")

            csv_bytes = st.session_state.df.to_csv(index=False).encode("utf-8")

            nombre_salida = upload_file.name

            st.download_button(
                label = "Descargar CSV transformado",
                data = csv_bytes,
                file_name = nombre_salida,
                mime="text/csv"
            )

    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")

