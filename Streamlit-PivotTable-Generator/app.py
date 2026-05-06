import streamlit as st
import pandas as pd
import csv
import io



st.set_page_config(page_title="Fusionador y Analizador de Datos", layout="wide")
st.title("📊 Fusionador y Analizador Dinámico de Archivos")
# 🔧 Inicializar merged_df
merged_df = None

st.write("""
Subí tus archivos **CSV o Excel (.xlsx)**.  
El programa los leerá, los unirá automáticamente por columnas comunes y permitirá analizarlos dinámicamente.
""")

uploaded_files = st.file_uploader(
    "Subí tus archivos CSV o Excel", type=["csv", "xlsx"], accept_multiple_files=True
)

if uploaded_files:
    dfs = []
    for uploaded_file in uploaded_files:
        try:
            if uploaded_file.name.endswith(".csv"):
                content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
                sample = "\n".join(content.splitlines()[:10])
                dialect = csv.Sniffer().sniff(sample)
                df = pd.read_csv(io.StringIO(content), sep=dialect.delimiter, low_memory=False, on_bad_lines='skip')
            else:
                df = pd.read_excel(uploaded_file)

            dfs.append(df)
            st.write(f"✅ Archivo leído: {uploaded_file.name} ({len(df)} filas)")
        except Exception as e:
            st.error(f"❌ Error al leer {uploaded_file.name}: {e}")

    if not dfs:
        st.stop()

    # Unión automática por columnas comunes
    if len(dfs) > 1:
        common_cols = list(set.intersection(*(set(df.columns) for df in dfs)))
        if not common_cols:
            st.error("❌ No hay columnas comunes entre los archivos.")
            merged_df = None
        else:
            st.write("Columnas comunes detectadas:", common_cols)
            merged_df = dfs[0]
            for df in dfs[1:]:
                merged_df = pd.merge(merged_df, df, on=common_cols, how="outer")
    else:
        merged_df = dfs[0]
# Después del merge
if 'merged_df' in locals() and merged_df is not None:
    # Crear id_base único por fila
    merged_df = merged_df.reset_index(drop=True)  # aseguramos índice limpio
    merged_df.insert(0, 'id_base', merged_df.index + 1)  # ID empezando en 1

import streamlit as st
import pandas as pd
import re

if 'merged_df' in locals() and merged_df is not None:

    st.write("## 📋 Previsualización del DataFrame combinado")
    st.write(f"Filas: {merged_df.shape[0]} | Columnas: {merged_df.shape[1]}")

    # --- Layout: filtros y previsualización ---
    col_filters, col_preview = st.columns([1, 3])

    with col_filters:
        with st.expander("⚙️ Opciones de Filtrado", expanded=True):
            # Selección de columnas a mostrar
            selected_cols = st.multiselect(
                "Columnas a mostrar",
                merged_df.columns.tolist(),
                default=merged_df.columns.tolist()
            )
            # Filtrado por texto
            text_filter_col = st.selectbox(
                "Filtrar por texto en columna (opcional)",
                [None] + merged_df.columns.tolist()
            )
            text_filter_value = None
            if text_filter_col:
                text_filter_value = st.text_input(f"Texto a filtrar en '{text_filter_col}'")

    with col_preview:
        df_preview = merged_df[selected_cols].copy()
        if text_filter_col and text_filter_value:
            df_preview = df_preview[df_preview[text_filter_col].astype(str).str.contains(text_filter_value, case=False, na=False)]
        st.dataframe(df_preview, height=500, use_container_width=True)

        # Botón de descarga cerca del DataFrame
        st.download_button(
            label="📥 Descargar previsualización como CSV",
            data=df_preview.to_csv(index=False).encode("utf-8"),
            file_name="previsualizacion.csv",
            mime="text/csv"
        )
st.write("## 🔄 Tabla Dinámica Interactiva")

if merged_df is not None:
    col_table_filters, col_table_result = st.columns([1, 3])

    with col_table_filters:
        with st.expander("⚙️ Opciones de Tabla Dinámica", expanded=True):
            all_cols = merged_df.columns.tolist()

            rows = st.multiselect("Columnas para filas", all_cols)
            values = st.multiselect("Columnas para valores", all_cols)

            agg_options = ["sum", "mean", "count", "max", "min"]
            agg_dict = {val: st.selectbox(f"Función de agregación para '{val}'", agg_options)
                        for val in values} if values else {}

            filter_col = st.selectbox("Filtrar por columna (opcional)", [None] + all_cols)
            filter_val = None
            if filter_col:
                filter_val = st.text_input(f"Valor a filtrar en '{filter_col}' (ej: >30, <=50, ==18, texto parcial)")

    df_table = merged_df.copy()

    # Aplicar filtro si corresponde
    if filter_col and filter_val:
        if pd.api.types.is_numeric_dtype(df_table[filter_col]):
            m = re.match(r'(>=|<=|>|<|==)\s*(\d+(\.\d+)?)', filter_val.strip())
            if m:
                op, num, _ = m.groups()
                num = float(num)
                if op == '>': df_table = df_table[df_table[filter_col] > num]
                if op == '<': df_table = df_table[df_table[filter_col] < num]
                if op == '>=': df_table = df_table[df_table[filter_col] >= num]
                if op == '<=': df_table = df_table[df_table[filter_col] <= num]
                if op == '==': df_table = df_table[df_table[filter_col] == num]
            else:
                st.warning("Formato inválido para filtro numérico. Usá: >30, <=50, ==18")
        else:
            df_table = df_table[df_table[filter_col].astype(str).str.contains(filter_val, case=False, na=False)]

    with col_table_result:
        if rows and values:
            try:
                pivot = pd.pivot_table(
                    df_table,
                    index=rows,
                    values=values,
                    aggfunc=agg_dict,
                    fill_value=0
                ).reset_index()

                st.dataframe(pivot, height=500, use_container_width=True)

                # Descargar CSV
                st.download_button(
                    label="📥 Descargar tabla dinámica CSV",
                    data=pivot.to_csv(index=False).encode("utf-8"),
                    file_name="tabla_dinamica.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"❌ Error al crear la tabla dinámica: {e}")
        else:
            st.info("Seleccioná al menos una columna para filas y una para valores para generar la tabla dinámica.")
else:
    st.warning("🔹 Subí y fusioná archivos para habilitar la tabla dinámica.")

# =========================
# PROFILING (OPCIONAL)
# =========================
try:
    from ydata_profiling import ProfileReport
    from streamlit_pandas_profiling import st_profile_report

    if merged_df is not None and st.button("🚀 Generar profiling"):
        pr = ProfileReport(merged_df, explorative=True)
        st_profile_report(pr)

except:
    st.warning("Profiling no disponible (instalar ydata-profiling)")