import pyodbc
from datetime import datetime


DB_CONFIG = {
    'DRIVER': 'ODBC Driver 17 for SQL Server',
    'SERVER': 'ARYAN\\SQLEXPRESS',
    'DATABASE': 'Doctor_appointment',
}

def get_connection():
    try:
        conn_str = (
            f"DRIVER={DB_CONFIG['DRIVER']};"
            f"SERVER={DB_CONFIG['SERVER']};"
            f"DATABASE={DB_CONFIG['DATABASE']};"
            "Trusted_Connection=yes;"
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except Exception as e:
        print("❌ Failed to connect to database:", e)
        return None


# 1. Fetch all available (Pending or Confirmed) appointments
def get_available_appointments():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = """
        SELECT AppointmentID, DoctorName, Department, AppointmentDate, AppointmentTime, Status
        FROM Appointments
        WHERE Status IN ('Pending', 'Confirmed')
        ORDER BY AppointmentDate, AppointmentTime;
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    
    except Exception as e:
        print("❌ Failed to fetch appointments:", e)
        return []


# 2. Book a new appointment (Insert record)
def book_appointment(patient_name, doctor_name, department, date, time):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print(f"Inserting: {patient_name}, {doctor_name}, {department}, {date}, {time}")
        
        query = """
        INSERT INTO Appointments (PatientName, DoctorName, Department, AppointmentDate, AppointmentTime, Status)
        VALUES (?, ?, ?, ?, ?, 'Pending');
        """
        
        cursor.execute(query, (patient_name, doctor_name, department, date, time))
        conn.commit()
        conn.close()
        return "✅ Appointment booked successfully (Pending status)."
    except Exception as e:
        return f"❌ Booking failed due to: {e}"

def list_doctors(_=None):  # underscore means: unused argument
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    SELECT DISTINCT DoctorName, Department FROM Appointments
    """
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    return "\n".join([f"{row.DoctorName} ({row.Department})" for row in results])
