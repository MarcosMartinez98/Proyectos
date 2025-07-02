import streamlit as st
import plotly.express as px
import pandas as pd

# ESTA DEBE SER LA PRIMERA LLAMADA DE STREAMLIT
st.set_page_config(layout="wide", page_title="Dashboard Aceites La Canal SA")

# Título y Logo (con contenedor de fondo blanco)
col_title, col_logo = st.columns([3, 1], gap="small")
with col_title:
    st.title("Rendimiento Horeca 2024 - Aceites La Canal SA")
with col_logo:
    st.markdown(
        f"""
        <div style='background-color: white; border-radius: 10px; display: flex; justify-content: center; align-items: center; padding: 5px;'>
            <img src="https://aceiteslacanal.com/wp-content/uploads/2018/07/Logo-aceiteslacanal-200.png" style="max-width: 100%; height: auto;">
        </div>
        """,
        unsafe_allow_html=True,
    )

# Paleta de colores
verde_principal = "#2E8B57"  # Un verde más intenso (Sea Green)
otro_color = "#FF8C00"     # Un naranja para contrastar (Dark Orange)
color_resaltado_kpi = "#E0E0E0" # Un gris claro para el fondo de los KPI principales
color_titulo_seccion = "#ADD8E6" # Azul claro para los títulos de sección

# Función para dar formato a los títulos de sección
def styled_subheader(text, color):
    st.markdown(
        f"""
        <div style='background-color: {color}; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;'>
            <h3 style='color: black; margin: 0; padding: 0;'>{text}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

@st.cache_data
def load_df(file_path):
    df = pd.read_csv(file_path)
    return df

# Cargar tus DataFrames
ventas_beneficio_por_mes_24 = load_df('ventas_beneficio_por_mes_24.csv')
ventas_beneficio_comerciales24 = load_df('ventas_beneficio_comerciales_24.csv')
ventas_beneficio_comercial_mes_24 = load_df('ventas_beneficio_comercial_mes_24.csv')

# Orden de los meses
orden_meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

# Calcular KPIs totales (sin filtrar)
ventas_totales_2024 = ventas_beneficio_comerciales24['ventas'].sum()
beneficios_totales_2024 = ventas_beneficio_comerciales24['beneficio'].sum()

# Sidebar para filtros
st.sidebar.header("Filtros")

# Filtro por Mes (multiselección con opción "Todos" y orden)
all_months_list = sorted(ventas_beneficio_por_mes_24['mes'].unique(), key=lambda m: orden_meses.index(m) if m in orden_meses else len(orden_meses))
all_months = ["Todos"] + all_months_list
default_months = []  # No seleccionar nada por defecto
selected_months = st.sidebar.multiselect("Seleccionar Meses:", all_months, default=default_months)
if "Todos" in selected_months:
    selected_months = all_months_list

# Filtro por Comercial (multiselección con opción "Todos")
all_comerciales_list = sorted(ventas_beneficio_comerciales24['comercial'].unique())
all_comerciales = ["Todos"] + all_comerciales_list
default_comerciales = []  # No seleccionar nada por defecto
selected_comerciales = st.sidebar.multiselect("Seleccionar Comerciales:", all_comerciales, default=default_comerciales)
if "Todos" in selected_comerciales:
    selected_comerciales = all_comerciales_list

# Filtrar DataFrames basados en las selecciones
filtered_mes_df = ventas_beneficio_por_mes_24[ventas_beneficio_por_mes_24['mes'].isin(selected_months)]
filtered_comercial_df = ventas_beneficio_comerciales24[ventas_beneficio_comerciales24['comercial'].isin(selected_comerciales)]
filtered_comercial_mes_df = ventas_beneficio_comercial_mes_24[ventas_beneficio_comercial_mes_24['mes'].isin(selected_months) &
                                                              ventas_beneficio_comercial_mes_24['comercial'].isin(selected_comerciales)]

# KPIs fijos en la parte superior con recuadro resaltado
styled_subheader("KPIs Totales 2024", color_titulo_seccion)
col_kpi1, col_kpi2 = st.columns(2)

# Estilo CSS para los recuadros de los KPIs principales
kpi_style = f"background-color: {color_resaltado_kpi}; padding: 15px; border-radius: 10px; border: 1px solid #ccc; text-align: center; color: black;"

with col_kpi1:
    st.markdown(f"<div style='{kpi_style}'><h4>Ventas Totales 2024</h4><h3>{ventas_totales_2024:,.2f} €</h3></div>", unsafe_allow_html=True)
with col_kpi2:
    st.markdown(f"<div style='{kpi_style}'><h4>Beneficios Totales 2024</h4><h3>{beneficios_totales_2024:,.2f} €</h3></div>", unsafe_allow_html=True)

st.markdown("---")

# KPIs dinámicos por Comercial (Suma de Meses Seleccionados)
styled_subheader("KPIs por Comercial", color_titulo_seccion)
if filtered_comercial_mes_df.empty:
    st.info("No hay datos disponibles con los filtros seleccionados.")
else:
    # Agrupar por comercial y sumar ventas y beneficios para los meses seleccionados
    kpis_agrupados_comercial = filtered_comercial_mes_df.groupby('comercial').agg(
        ventas_sum=('ventas', 'sum'),
        beneficio_sum=('beneficio', 'sum')
    ).reset_index()

    # Iterar sobre el DataFrame agrupado para mostrar un solo KPI por comercial
    for index, row in kpis_agrupados_comercial.iterrows():
        st.markdown(
            f"<div style='border: 1px solid #ddd; padding: 10px; margin-bottom: 5px; border-radius: 5px;'>"
            f"<strong>{row['comercial']}</strong><br>"
            f"Ventas Totales: {row['ventas_sum']:,.2f} €<br>"
            f"Beneficio Total: {row['beneficio_sum']:,.2f} €"
            f"</div>",
            unsafe_allow_html=True
        )

st.markdown("---")

# MODIFICACIÓN DE LA SECCIÓN: Ventas y Beneficios por Comercial (Mensual/Seleccionada)
styled_subheader("Ventas y Beneficios por Comercial", color_titulo_seccion)

# Agrupamos los datos por comercial y sumamos ventas y beneficios para los meses seleccionados
aggregated_comercial_mes_for_charts_df = filtered_comercial_mes_df.groupby('comercial').agg(
    ventas=('ventas', 'sum'),
    beneficio=('beneficio', 'sum')
).reset_index()

# DataFrame para el gráfico de Ventas (ordenado por Ventas)
df_ventas_sorted = aggregated_comercial_mes_for_charts_df.sort_values(by='ventas', ascending=False)

# DataFrame para el gráfico de Beneficios (ordenado por Beneficios)
df_beneficios_sorted = aggregated_comercial_mes_for_charts_df.sort_values(by='beneficio', ascending=False)

col_com1, col_com2 = st.columns(2)

# Gráfico de Ventas por Comercial (ordenado por Ventas)
fig_ventas_comercial_meses = px.bar(df_ventas_sorted,
                                     x='comercial',
                                     y='ventas',
                                     title='Ventas por Comercial',
                                     labels={'ventas': 'Ventas (€)', 'comercial': 'Comercial'},
                                     color_discrete_sequence=[verde_principal])
col_com1.plotly_chart(fig_ventas_comercial_meses, use_container_width=True)

# Gráfico de Beneficios por Comercial (ordenado por Beneficios)
fig_beneficio_comercial_meses = px.bar(df_beneficios_sorted, # <-- Usa el DataFrame ordenado por beneficio
                                       x='comercial',
                                       y='beneficio',
                                       title='Beneficios por Comercial',
                                       labels={'beneficio': 'Beneficio (€)', 'comercial': 'Comercial'},
                                       color_discrete_sequence=[otro_color])
col_com2.plotly_chart(fig_beneficio_comercial_meses, use_container_width=True)


st.markdown("---")

# Sección de Ventas y Beneficios por Mes
styled_subheader("Evolución Mensual de Ventas y Beneficios", color_titulo_seccion)

fig_mes = px.line(filtered_mes_df.sort_values(by='mes', key=lambda x: x.map(lambda m: orden_meses.index(m) if m in orden_meses else len(orden_meses))),
                  x='mes',
                  y=['ventas', 'beneficio'],
                  title='Evolución Mensual de Ventas y Beneficios',
                  labels={'beneficio': 'Beneficio (€)', 'ventas': 'Ventas (€)', 'mes': 'Mes', 'value': 'Valor (€)'},
                  color_discrete_sequence=[verde_principal, otro_color])

st.plotly_chart(fig_mes, use_container_width=True)

