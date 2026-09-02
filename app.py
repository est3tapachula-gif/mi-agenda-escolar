import streamlit as st
import datetime
import calendar
from database import inicializar_db
from gestion_clases import obtener_clases_por_dia, agregar_clase
from gestion_tareas import obtener_tareas_pendientes, agregar_tarea, marcar_tarea_completada
from sesiones_drive import guardar_actividades_sesion

# Configuración inicial de la app móvil
st.set_page_config(page_title="Agenda Escolar", page_icon="📅", layout="centered")

# Inicializar Base de Datos
inicializar_db()

st.title("📅 Mi Agenda Escolar")

dias_lista = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
hoy = datetime.date.today()
nombre_dia_hoy = dias_lista[hoy.weekday()]

# Barra lateral para navegación
opcion_menu = st.sidebar.radio(
    "Navegación", 
    ["Inicio / Clases de Hoy", "Vista Semanal", "Vista Mensual", "Registrar Nueva Clase", "Tareas y Avisos"]
)

# ---------------------------------------------------------
# PANTALLA 1: INICIO Y CLASES DEL DÍA
# ---------------------------------------------------------
if opcion_menu == "Inicio / Clases de Hoy":
    st.subheader(f"Clases programadas para hoy ({nombre_dia_hoy} {hoy.strftime('%d/%m/%Y')})")
    
    clases_hoy = obtener_clases_por_dia(nombre_dia_hoy)
    
    if clases_hoy:
        for clase in clases_hoy:
            clase_id, materia, grupo, hora_ini, hora_fin, link_drive = clase
            
            with st.expander(f"⏰ {hora_ini} - {hora_fin} | {materia} ({grupo})"):
                st.write(f"**Asignatura:** {materia}")
                st.write(f"**Grupo:** {grupo}")
                
                if link_drive:
                    st.link_button("📁 Abrir Listas en Drive", link_drive)
                else:
                    st.info("No hay un enlace de Google Drive guardado para esta clase.")
                
                st.markdown("---")
                act_hoy = st.text_area("Actividades realizadas en esta sesión:", key=f"act_{clase_id}")
                act_sig = st.text_area("Actividades para la siguiente sesión:", key=f"sig_{clase_id}")
                
                if st.button("✅ Terminar y Guardar", key=f"btn_{clase_id}"):
                    guardar_actividades_sesion(clase_id, hoy.strftime("%Y-%m-%d"), act_hoy, act_sig)
                    st.success("¡Actividades guardadas correctamente!")
    else:
        st.info("No tienes clases registradas para el día de hoy.")

# ---------------------------------------------------------
# PANTALLA 2: VISTA SEMANAL
# ---------------------------------------------------------
elif opcion_menu == "Vista Semanal":
    st.subheader("🗓 Horario General de la Semana")
    
    # Creamos pestañas para cada día lectivo
    tabs = st.tabs(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"])
    
    for idx, dia_nombre in enumerate(["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]):
        with tabs[idx]:
            clases_dia = obtener_clases_por_dia(dia_nombre)
            if clases_dia:
                for c in clases_dia:
                    c_id, materia, grupo, h_ini, h_fin, link = c
                    st.markdown(f"**{h_ini} - {h_fin}** | {materia} *({grupo})*")
                    if link:
                        st.caption(f"[Enlace Drive]({link})")
                    st.divider()
            else:
                st.info(f"Sin clases registradas para el {dia_nombre}.")

# ---------------------------------------------------------
# PANTALLA 3: VISTA MENSUAL
# ---------------------------------------------------------
elif opcion_menu == "Vista Mensual":
    st.subheader("📆 Panorama Mensual y Tareas")
    
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    st.write(f"### {calendar.month_name[mes_actual]} {anio_actual}")
    
    # Obtener y mostrar tareas agendadas en el mes
    tareas = obtener_tareas_pendientes()
    if tareas:
        st.write("**Entregas y Eventos Pendientes este mes:**")
        for t in tareas:
            t_id, tit, desc, f_h = t
            st.warning(f"📌 **{tit}** — Fecha: `{f_h}`\n\n{desc}")
    else:
        st.info("No hay eventos o avisos especiales agendados.")

# ---------------------------------------------------------
# PANTALLA 4: REGISTRAR NUEVA CLASE
# ---------------------------------------------------------
elif opcion_menu == "Registrar Nueva Clase":
    st.subheader("➕ Dar de Alta una Materia / Clase")
    
    with st.form("form_clase"):
        materia = st.text_input("Nombre de la Materia (ej. Español)")
        grupo = st.text_input("Grupo (ej. 2°G)")
        dia_semana = st.selectbox("Día de la semana", dias_lista)
        
        col1, col2 = st.columns(2)
        with col1:
            hora_inicio = st.text_input("Hora Inicio (ej. 08:00)")
        with col2:
            hora_fin = st.text_input("Hora Fin (ej. 08:50)")
            
        link_drive = st.text_input("Enlace a carpeta/archivo de Google Drive (Listas/Rúbricas)")
        
        btn_guardar = st.form_submit_button("Guardar Clase")
        
        if btn_guardar:
            if materia and grupo:
                agregar_clase(materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive)
                st.success(f"¡Clase de {materia} ({grupo}) guardada con éxito!")
            else:
                st.error("Por favor completa al menos la materia y el grupo.")

# ---------------------------------------------------------
# PANTALLA 5: TAREAS Y AVISOS
# ---------------------------------------------------------
elif opcion_menu == "Tareas y Avisos":
    st.subheader("🔔 Tareas y Avisos Programados")
    
    with st.expander("➕ Programar Nueva Tarea o Aviso"):
        titulo = st.text_input("Título de la Tarea/Aviso")
        desc = st.text_area("Descripción")
        fecha_aviso = st.date_input("Fecha de entrega/aviso")
        hora_aviso = st.time_input("Hora del aviso")
        
        if st.button("Programar Aviso"):
            fecha_hora_str = f"{fecha_aviso} {hora_aviso}"
            agregar_tarea(titulo, desc, fecha_hora_str)
            st.success("¡Tarea o aviso programado con éxito!")
            st.rerun()

    st.markdown("---")
    st.write("### Pendientes")
    tareas = obtener_tareas_pendientes()
    
    if tareas:
        for t in tareas:
            t_id, tit, descripcion, f_h = t
            c1, c2 = st.columns([3, 1])
            with c1:
                st.write(f"**{tit}** ({f_h})")
                st.caption(descripcion)
            with c2:
                if st.button("Done", key=f"t_{t_id}"):
                    marcar_tarea_completada(t_id)
                    st.rerun()
    else:
        st.info("No tienes tareas pendientes.")
