# Doctors_appointment_boking_system
# Doctor Appointment Booking System (LLM + SQL Server)

This project is a conversational AI-based appointment scheduling system that integrates a Large Language Model (LLM) with a SQL Server backend to help users book medical appointments with doctors based on their symptoms and availability.

## 💡 Features

- 🧠 Chat-based interaction to book doctor appointments
- 🏥 Doctor recommendation based on symptoms (e.g., stomach pain → Gastroenterologist)
- 📆 Fetch and display doctor availability dynamically (Mon–Fri, fixed working hours)
- ❌ Filters out already booked slots using existing `Appointments` table
- ✅ Supports structured booking with patient name, date, time, department, and doctor
- 🗂 Uses LangChain + OpenAI API + pyodbc

---

## 🗃️ Database Structure

### 1. `Appointments`
Stores all booked appointments.
| Column           | Type      |
|------------------|-----------|
| AppointmentID    | INT       |
| PatientName      | NVARCHAR  |
| DoctorName       | NVARCHAR  |
| Department       | NVARCHAR  |
| AppointmentDate  | DATE      |
| AppointmentTime  | TIME      |
| Status           | NVARCHAR  |

### 2. `DoctorAvailability`
Stores weekly working hours for each doctor.
| Column     | Type      |
|------------|-----------|
| DoctorName | NVARCHAR  |
| Department | NVARCHAR  |
| DayOfWeek  | NVARCHAR  |
| StartTime  | TIME      |
| EndTime    | TIME      |

---

## 🧪 Sample POC Steps Logged

- ✅ Added appointment manually through function  
- ✅ Booked an appointment via LLM with default name (`"John Doe"`)  
- ✅ Enabled conversational flow using LangChain AgentExecutor  
- ✅ Implemented name capture in LLM to store patient name during booking  
- ✅ Fully dynamic availability suggestion using unbooked slots per doctor  

---

## 📄 Detailed POC Notes

For full step-by-step tracking, flow breakdowns, and system design insights, see this document:

📄 [Doctors_appointment.docx](./Doctors_appointment.docx)

---


