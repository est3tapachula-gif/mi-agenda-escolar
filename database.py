import sqlite3

def obtener_conexion():
    """Establece la conexión con la base de datos SQLite."""
    conexion = sqlite3.connect("agenda_escolar.db")
    return conexion

def inicializar_db():
    """Crea las tablas necesarias si no existen y precarga el horario escolar fijo."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Tabla de clases / horario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            materia TEXT NOT NULL,
            grupo TEXT NOT NULL,
            dia_semana TEXT NOT NULL,
            hora_inicio TEXT NOT NULL,
            hora_fin TEXT NOT NULL,
            link_drive TEXT DEFAULT ''
        )
    """)
    
    # Tabla de sesiones de bitácora
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clase_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            actividades_hoy TEXT DEFAULT '',
            actividades_siguiente TEXT DEFAULT '',
            FOREIGN KEY (clase_id) REFERENCES clases (id)
        )
    """)
    
    # Tabla de tareas y avisos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_hora TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente'
        )
    """)
    
    # Verificar si ya existen clases registradas
    cursor.execute("SELECT COUNT(*) FROM clases")
    cantidad = cursor.fetchone()[0]
    
    # URL general de tus Listas de Google Sheets
    link_listas = "https://docs.google.com/spreadsheets/d/1epXAXdJ5tDi_7zq_hSvV1hUAcMUT3pF7j2yEtgPMibE/edit?usp=sharing"
    
    # Si la base de datos está vacía, precargamos todo tu horario del PDF con la materia e enlace a Listas
    if cantidad == 0:
        horario_base = [
            # LUNES
            ("Inglés", "3H", "Lunes", "13:40", "14:25", link_listas),
            ("Inglés", "3J", "Lunes", "14:25", "15:10", link_listas),
            ("Inglés", "1G", "Lunes", "15:10", "15:50", link_listas),
            ("Inglés", "1G", "Lunes", "16:15", "17:00", link_listas),
            ("Inglés", "1H", "Lunes", "17:00", "17:45", link_listas),
            ("Inglés", "1H", "Lunes", "17:45", "18:30", link_listas),
            ("Inglés", "2J", "Lunes", "18:30", "19:15", link_listas),
            ("Inglés", "11", "Lunes", "19:15", "20:00", link_listas),
            
            # MARTES
            ("Inglés", "2G", "Martes", "13:40", "14:25", link_listas),
            ("Inglés", "3G", "Martes", "14:25", "15:10", link_listas),
            ("Inglés", "3G", "Martes", "15:10", "15:50", link_listas),
            ("Inglés", "1H", "Martes", "16:15", "17:00", link_listas),
            ("Inglés", "31", "Martes", "17:00", "17:45", link_listas),
            ("Inglés", "31", "Martes", "17:45", "18:30", link_listas),
            ("Inglés", "2K", "Martes", "18:30", "19:15", link_listas),
            ("Inglés", "2H", "Martes", "19:15", "20:00", link_listas),
            
            # MIÉRCOLES
            ("Inglés", "3H", "Miércoles", "13:40", "14:25", link_listas),
            ("Inglés", "3H", "Miércoles", "14:25", "15:10", link_listas),
            ("Inglés", "1K", "Miércoles", "15:10", "15:50", link_listas),
            ("Inglés", "1K", "Miércoles", "16:15", "17:00", link_listas),
            ("Inglés", "2G", "Miércoles", "17:00", "17:45", link_listas),
            ("Inglés", "2G", "Miércoles", "17:45", "18:30", link_listas),
            ("Inglés", "21", "Miércoles", "18:30", "19:15", link_listas),
            ("Inglés", "21", "Miércoles", "19:15", "20:00", link_listas),
            
            # JUEVES
            ("Inglés", "2J", "Jueves", "13:40", "14:25", link_listas),
            ("Inglés", "2J", "Jueves", "14:25", "15:10", link_listas),
            ("Inglés", "2K", "Jueves", "15:10", "15:50", link_listas),
            ("Inglés", "2K", "Jueves", "16:15", "17:00", link_listas),
            ("Inglés", "1K", "Jueves", "17:00", "17:45", link_listas),
            ("Inglés", "1J", "Jueves", "17:45", "18:30", link_listas),
            ("Inglés", "2H", "Jueves", "18:30", "19:15", link_listas),
            ("Inglés", "2H", "Jueves", "19:15", "20:00", link_listas),
            
            # VIERNES
            ("Inglés", "31", "Viernes", "13:40", "14:25", link_listas),
            ("Inglés", "1J", "Viernes", "14:25", "15:10", link_listas),
            ("Inglés", "1J", "Viernes", "15:10", "15:50", link_listas),
            ("Inglés", "1G", "Viernes", "16:15", "17:00", link_listas),
            ("Inglés", "3G", "Viernes", "17:00", "17:45", link_listas),
            ("Inglés", "21", "Viernes", "17:45", "18:30", link_listas),
            ("Inglés", "11", "Viernes", "18:30", "19:15", link_listas),
            ("Inglés", "11", "Viernes", "19:15", "20:00", link_listas)
        ]
        
        cursor.executemany("""
            INSERT INTO clases (materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive)
            VALUES (?, ?, ?, ?, ?, ?)
        """, horario_base)
    
    conexion.commit()
    conexion.close()
