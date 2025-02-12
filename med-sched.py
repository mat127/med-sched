from scheduler import Scheduler
from datetime import date

days = Scheduler.generate_days(2025, 2)

shifts = [
    "oddělení",
    "anestezie",
    "příslužba"
]

doctors = [
    "Dorovská",
    "Dudková",
    "Foldynová",
    "Ježová",
    "Hanzlíková",
    "Hermannová",
    "Hindych",
    "Hlista",
    "Hudymač",
    "Káňová",
    "Matoušková",
    "Matulová",
    "Obšívač",
    "Pavlík",
    "Prášková",
    "Smrček",
    "Tisoň"
]

scheduler = Scheduler(doctors, days, shifts)
scheduler.one_doctor_per_shift(["oddělení","anestezie"])
scheduler.one_doctor_per_shift(["příslužba"], lambda d: d.weekday() < 5)
scheduler.no_shifts(["příslužba"], lambda d: d.weekday() >= 5)

scheduler.one_shift_per_doctor_in_period(3)

for doctor in doctors:
    scheduler.shift_count(doctor, ["oddělení", "anestezie"], 3, 4)

not_allowed_shifts = {
    "oddělení": [
        "Hanzlíková",
        "Hermannová",
        "Hindych",
        "Káňová",
        "Obšívač",
        "Prášková",
        "Smrček",
        "Tisoň"
    ],
    "příslužba": [
        "Dudková",
        "Hlista",
        "Dorovská",
        "Obšívač",
        "Smrček",
        "Hanzlíková"
    ]
}

for doctor in not_allowed_shifts["oddělení"]:
    scheduler.shift_count(doctor, ["oddělení"], 0, 0)

for doctor in doctors:
    if doctor in not_allowed_shifts["příslužba"]:
        scheduler.shift_count(doctor, ["příslužba"], 0, 0)
    else:
        scheduler.shift_count(doctor, ["příslužba"], 1, 3)

# individual requirements
scheduler.requirement_positive("Prášková", "anestezie", [date(2025,2,2)])
scheduler.requirement_positive("Dorovská", "oddělení", [date(2025,2,3)])
scheduler.requirement_positive("Hudymač", "oddělení", [
    date(2025,2,4),
    date(2025,2,18),
    date(2025,2,22),
    date(2025,2,25)
])
scheduler.requirement_positive("Hindych", "anestezie", [
    date(2025,2,8),
    date(2025,2,20)
])
scheduler.requirement_positive("Obšívač", "anestezie", [
    date(2025,2,9),
    date(2025,2,17)
])

scheduler.requirement_negative("Ježová", [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,5),
    date(2025,2,7),
    date(2025,2,9),
    date(2025,2,10),
    date(2025,2,28),
])
scheduler.requirement_negative("Hanzlíková", [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,5),
    date(2025,2,10),
    date(2025,2,15),
])
scheduler.requirement_negative("Hermannová", [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,14),
    date(2025,2,15),
    date(2025,2,16),
    date(2025,2,17),
])
scheduler.requirement_negative("Hudymač", [
    date(2025,2,d) for d in [1,2,6,7,8,9,10,11,12,13,14,15,16,20,21]
])
scheduler.requirement_negative("Hlista", [
    date(2025,2,d) for d in [1,2,3,4,5,6,7,8,10,11,14,15,16,17,18,19,20,25,26,27,28]
])
scheduler.requirement_negative("Smrček", [
    date(2025,2,d) for d in [3,5,6,10,13,14,15,16,17,19,20,24,27,28]
])
scheduler.requirement_negative("Dudková", [
    date(2025,2,d) for d in [3,4,7,8,9,10,11,12,14,15,17,18,24,25,28]
])
scheduler.requirement_negative("Dorovská", [
    date(2025,2,d) for d in [5,6,7,8,9,10,11,12,13,20,27]
])
scheduler.requirement_negative("Foldynová", [
    date(2025,2,d) for d in [8,11,12,21,27]
])
scheduler.requirement_negative("Matoušková", [
    date(2025,2,d) for d in [8,9]
])
scheduler.requirement_negative("Hindych", [
    date(2025,2,d) for d in [6,9,10,13,14,15,16]
])
scheduler.requirement_negative("Prášková", [
    date(2025,2,d) for d in [4,11,14,15,16,18,21,22,23,25]
])
scheduler.requirement_negative("Hanzlíková", [
    date(2025,2,d) for d in [1,2,5,10,15]
])
scheduler.requirement_negative("Pavlík", [
    date(2025,2,d) for d in [12,21]
])
scheduler.requirement_negative("Matulová", [
    date(2025,2,d) for d in [17,18,19,20,21]
])
scheduler.requirement_negative("Obšívač", [
    date(2025,2,d) for d in [21,22,23,24,25,26,27,28]
])

scheduler.schedule()
scheduler.print_statistics()
