from scheduler import Scheduler

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
for doctor in doctors:
    scheduler.shift_count(doctor, 5, 4)

scheduler.schedule()
scheduler.print_statistics()
