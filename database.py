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
    
    # Si la base de datos está vacía, precargamos todo tu horario del PDF
    if cantidad == 0:
        horario_base = [
            # LUNES
            ("Materia", "3H", "Lunes", "13:40", "14:25", ""),
            ("Materia", "3J", "Lunes", "14:25", "15:10", ""),
            ("Materia", "1G", "Lunes", "15:10", "15:50", ""),
            ("Materia", "1G", "Lunes", "16:15", "17:00", ""),
            ("Materia", "1H", "Lunes", "17:00", "17:45", ""),
            ("Materia", "1H", "Lunes", "17:45", "18:30", ""),
            ("Materia", "2J", "Lunes", "18:30", "19:15", ""),
            ("Materia", "11", "Lunes", "19:15", "20:00", ""),
            
            # MARTES
            ("Materia", "2G", "Martes", "13:40", "14:25", ""),
            ("Materia", "3G", "Martes", "14:25", "15:10", ""),
            ("Materia", "3G", "Martes", "15:10", "15:50", ""),
            ("Materia", "1H", "Martes", "16:15", "17:00", ""),
            ("Materia", "31", "Martes", "17:00", "17:45", ""),
            ("Materia", "31", "Martes", "17:45", "18:30", ""),
            ("Materia", "2K", "Martes", "18:30", "19:15", ""),
            ("Materia", "2H", "Martes", "19:15", "20:00", ""),
            
            # MIÉRCOLES
            ("Materia", "3H", "Miércoles", "13:40", "14:25", ""),
            ("Materia", "3H", "Miércoles", "14:25", "15:10", ""),
            ("Materia", "1K", "Miércoles", "15:10", "15:50", ""),
            ("Materia", "1K", "Miércoles", "16:15", "17:00", ""),
            ("Materia", "2G", "Miércoles", "17:00", "17:45", ""),
            ("Materia", "2G", "Miércoles", "17:45", "18:30", ""),
            ("Materia", "21", "Miércoles", "18:30", "19:15", ""),
            ("Materia", "21", "Miércoles", "19:15", "20:00", ""),
            
            # JUEVES
            ("Materia", "2J", "Jueves", "13:40", "14:25", ""),
            ("Materia", "2J", "Jueves", "14:25", "15:10", ""),
            ("Materia", "2K", "Jueves", "15:10", "15:50", ""),
            ("Materia", "2K", "Jueves", "16:15", "17:00", ""),
            ("Materia", "1K", "Jueves", "17:00", "17:45", ""),
            ("Materia", "1J", "Jueves", "17:45", "18:30", ""),
            ("Materia", "2H", "Jueves", "18:30", "19:15", ""),
            ("Materia", "2H", "Jueves", "19:15", "20:00", ""),
            
            # VIERNES
            ("Materia", "31", "Viernes", "13:40", "14:25", ""),
            ("Materia", "1J", "Viernes", "14:25", "15:10", ""),
            ("Materia", "1J", "Viernes", "15:10", "15:50", ""),
            ("Materia", "1G", "Viernes", "16:15", "17:00", ""),
            ("Materia", "3G", "Viernes", "17:00", "17:45", ""),
            ("Materia", "21", "Viernes", "17:45", "18:30", ""),
            ("Materia", "11", "Viernes", "18:30", "19:15", ""),
            ("Materia", "11", "Viernes", "19:15", "20:00", "")
        ]
        
        cursor.executemany("""
            INSERT INTO clases (materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive)
            VALUES (?, ?, ?, ?, ?, ?)
        """, horario_base)
    
    conexion.commit()
    conexion.close()
