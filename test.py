from database import get_available_appointments, book_appointment

# Test fetch
appointments = get_available_appointments()
for appt in appointments:
    print(f"{appt.DoctorName} | {appt.AppointmentDate} {appt.AppointmentTime} | Status: {appt.Status}")

# Test insert
msg = book_appointment("Aryan Agarwal", "Dr. Smith", "Dermatology", "2025-05-30", "10:00:00")
print(msg)
