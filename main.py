import datetime
from database import inicializar_db
from gestion_clases import obtener_clases_por_dia
from gestion_tareas import obtener_tareas_pendientes, agregar_tarea
from sesiones_drive import guardar_actividades_sesion, abrir_lista_drive

def mostrar_pantalla_inicio():
    """Pantalla principal de la agenda escolar."""
    # Asegurar que la base de datos esté lista
    inicializar_db()
    
    # Obtener fecha actual
    hoy = datetime.date.today()
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    nombre_dia = dias_semana[hoy.weekday()]
    fecha_formateada = hoy.strftime("%d/%m/%Y")

    print("=" * 50)
    print(f"       AGENDA ESCOLAR - {nombre_dia.upper()} {fecha_formateada}")
    print("=" * 50)
    
    # 1. Mostrar Horarios de Clase del Día
    print("\n--- CLASES PROGRAMADAS HOY ---")
    clases_hoy = obtener_clases_por_dia(nombre_dia)
    
    if clases_hoy:
        for clase in clases_hoy:
            clase_id, materia, grupo, hora_ini, hora_fin, link_drive = clase
            print(f"[{clase_id}] {hora_ini} - {hora_fin} | {materia} ({grupo})")
    else:
        print("No hay clases programadas para el día de hoy.")

    # 2. Mostrar Tareas y Avisos Programados
    print("\n--- TAREAS Y AVISOS PENDIENTES ---")
    tareas = obtener_tareas_pendientes()
    if tareas:
        for tarea in tareas:
            t_id, titulo, desc, fecha_hora = tarea
            print(f"• {titulo} ({fecha_hora}) - {desc}")
    else:
        print("Sin tareas o avisos pendientes.")

    print("\n" + "=" * 50)

def abrir_detalle_clase(clase_id, materia, grupo, hora_ini, hora_fin, link_drive):
    """Pantalla secundaria: Registro de actividades de la sesión."""
    print("\n" + "*" * 50)
    print(f" DETALLE DE SESIÓN: {materia} - GRUPO {grupo}")
    print(f" Horario: {hora_ini} a {hora_fin}")
    print("*" * 50)
    
    print("\n[Opciones disponibles]")
    print("1. Ver/Abrir Listas en Google Drive")
    print("2. Registrar Actividades del Día")
    print("3. Planificar Actividades de la Siguiente Sesión")
    print("4. TERMINAR (Guardar y volver a Inicio)")
    
    # Simulación de enlace a Drive
    print(f"\nLink asignado a Drive: {link_drive}")

if __name__ == "__main__":
    # Ejecución inicial de la app
    mostrar_pantalla_inicio()
