import streamlit as st
import datetime
import calendar
from datetime import timezone, timedelta
from database import inicializar_db
from gestion_clases import (
    obtener_clases_por_dia, 
    agregar_clase, 
    obtener_todas_las_clases, 
    actualizar_clase, 
    eliminar_clase
)
from gestion_tareas import obtener_tareas_pendientes, agregar_tarea, marcar_tarea_completada
from sesiones_drive import guardar_actividades_sesion, obtener_actividad_sesion

# Configuración de página para vista móvil
st.set_page_config(page_title="Agenda Escolar", page_icon="📅", layout="centered")

# Inicializar Base de Datos
inicializar_db()

# Ajuste de Zona Horaria (UTC-6)
TZ_MEX = timezone(timedelta(hours=-6))
hoy = datetime.datetime.now(TZ_MEX).date()
fecha_str = hoy.strftime("%Y-%m-%d")

dias_lista = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
nombre_dia_hoy = dias_lista[hoy.weekday()]

st.title("📅 Mi Agenda Escolar")

# Barra lateral para navegación
opcion_menu = st.sidebar.radio(
    "Navegación", 
    [
        "Inicio / Clases de Hoy", 
        "Vista Semanal", 
        "Vista Mensual", 
        "Registrar Nueva Clase", 
        "Editar / Eliminar Clases", 
        "Tareas y Avisos"
    ]
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
            
            # Cargar actividades de hoy (traspasando la nota previa del grupo si aplica)
            act_hoy_guardada, act_sig_guardada = obtener_actividad_sesion(clase_id, fecha_str, grupo=grupo)
            
            with st.expander(f"⏰ {hora_ini} - {hora_fin} | {materia} ({grupo})"):
                st.write(f"**Asignatura:** {materia}")
                st.write(f"**Grupo:** {grupo}")
                
                if link_drive:
                    st.link_button("📁 Abrir Listas en Drive", link_drive)
                else:
                    st.info("No hay un enlace de Google Drive guardado para esta clase.")
                
                st.markdown("---")
                
                # Cajas de texto inicializadas con el arrastre de información
                act_hoy = st.text_area(
                    "Actividades realizadas en esta sesión:", 
                    value=act_hoy_guardada, 
                    key=f"act_{clase_id}"
                )
                act_sig = st.text_area(
                    "Actividades para la siguiente sesión:", 
                    value=act_sig_guardada, 
                    key=f"sig_{clase_id}"
                )
                
                if st.button("✅ Terminar y Guardar", key=f"btn_{clase_id}"):
                    guardar_actividades_sesion(clase_id, fecha_str, act_hoy, act_sig)
                    st.success("¡Actividades guardadas y vinculadas correctamente!")
                    st.rerun()
    else:
        st.info("No tienes clases registradas para el día de hoy.")

# ---------------------------------------------------------
# PANTALLA 2: VISTA SEMANAL
# ---------------------------------------------------------
elif opcion_menu == "Vista Semanal":
    st.subheader("🗓 Horario General de la Semana")
    
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
        materia = st.text_input("Nombre de la Materia (ej. Inglés)")
        grupo = st.text_input("Grupo (ej. 1G)")
        dia_semana = st.selectbox("Día de la semana", dias_lista)
        
        col1, col2 = st.columns(2)
        with col1:
            hora_inicio = st.text_input("Hora Inicio (ej. 13:40)")
        with col2:
            hora_fin = st.text_input("Hora Fin (ej. 14:25)")
            
        link_drive = st.text_input("Enlace a listas o Google Drive")
        
        btn_guardar = st.form_submit_button("Guardar Clase")
        
        if btn_guardar:
            if materia and grupo:
                agregar_clase(materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive)
                st.success(f"¡Clase de {materia} ({grupo}) guardada con éxito!")
            else:
                st.error("Por favor completa al menos la materia y el grupo.")

# ---------------------------------------------------------
# PANTALLA 5: EDITAR / ELIMINAR CLASES
# ---------------------------------------------------------
elif opcion_menu == "Editar / Eliminar Clases":
    st.subheader("✏️ Gestionar y Modificar Clases")
    
    todas_las_clases = obtener_todas_las_clases()
    
    if todas_las_clases:
        opciones_clases = {
            f"{c[3]} | {c[1]} ({c[2]}) [{c[4]}-{c[5]}]": c for c in todas_las_clases
        }
        
        seleccion = st.selectbox("Selecciona la clase que deseas editar o borrar:", list(opciones_clases.keys()))
        clase_sel = opciones_clases[seleccion]
        c_id, c_mat, c_grp, c_dia, c_h_ini, c_h_fin, c_link = clase_sel
        
        st.markdown("---")
        st.write(f"### Modificar: **{c_mat} ({c_grp})**")
        
        with st.form("form_editar_clase"):
            edit_materia = st.text_input("Materia", value=c_mat)
            edit_grupo = st.text_input("Grupo", value=c_grp)
            
            idx_dia = dias_lista.index(c_dia) if c_dia in dias_lista else 0
            edit_dia = st.selectbox("Día de la semana", dias_lista, index=idx_dia)
            
            col1, col2 = st.columns(2)
            with col1:
                edit_h_ini = st.text_input("Hora Inicio", value=c_h_ini)
            with col2:
                edit_h_fin = st.text_input("Hora Fin", value=c_h_fin)
                
            edit_link = st.text_input("Enlace de Google Drive", value=c_link if c_link else "")
            
            btn_actualizar = st.form_submit_button("💾 Guardar Cambios")
            
            if btn_actualizar:
                actualizar_clase(c_id, edit_materia, edit_grupo, edit_dia, edit_h_ini, edit_h_fin, edit_link)
                st.success("¡La clase ha sido actualizada correctamente!")
                st.rerun()

        st.markdown("---")
        st.write("⚠️ **Zona de Eliminación**")
        if st.button("🗑️ Eliminar esta Clase", type="secondary"):
            eliminar_clase(c_id)
            st.warning(f"La clase '{c_mat}' fue eliminada.")
            st.rerun()
    else:
        st.info("No hay clases registradas en el sistema para editar.")

# ---------------------------------------------------------
# PANTALLA 6: TAREAS Y AVISOS
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
