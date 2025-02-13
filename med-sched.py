from datetime import date
from enum import Enum

from scheduler import Scheduler

days = Scheduler.generate_days(2025, 2)

class Shifts(Enum):
    ODDELENI  = "oddělení"
    ANESTEZIE = "anestezie"
    PRISLUZBA = "příslužba"

    def others(self):
        return list(filter(lambda s: not s == self, Shifts))

class Doctor(Enum):
    DOROVSKA = "Dorovská"
    DUDKOVA = "Dudková"
    FOLDYNOVA = "Foldynová"
    JEZOVA = "Ježová"
    HANZLIKOVA = "Hanzlíková"
    HERMANNOVA = "Hermannová"
    HINDYCH = "Hindych"
    HLISTA = "Hlista"
    HUDYMAC = "Hudymač"
    KANOVA = "Káňová"
    MATOUSKOVA = "Matoušková"
    MATULOVA = "Matulová"
    OBSIVAC = "Obšívač"
    PAVLIK = "Pavlík"
    PRASKOVA = "Prášková"
    SMRCEK = "Smrček"
    TISON = "Tisoň"

scheduler = Scheduler(Doctor, days, Shifts, Shifts.PRISLUZBA.others())
scheduler.one_doctor_per_shift(Shifts.PRISLUZBA.others())

# PRISLUZBA only on workdays
scheduler.one_doctor_per_shift([Shifts.PRISLUZBA], lambda d: d.weekday() < 5)
scheduler.no_shifts([Shifts.PRISLUZBA], lambda d: d.weekday() >= 5)

# days off between shifts (including the shift day)
scheduler.one_shift_per_doctor_in_period(3)

for doctor in Doctor:
    # how many non-PRISLUZBA shifts per doctor
    scheduler.shift_count(doctor, Shifts.PRISLUZBA.others(), 3, 4)
    # how many non-PRISLUZBA shifts per doctor during weekend
    scheduler.shift_count(doctor, Shifts.PRISLUZBA.others(), 0, 1, lambda d: d.weekday() >= 5)

not_allowed_shifts = {
    Shifts.ODDELENI: [
        Doctor.HANZLIKOVA,
        Doctor.HERMANNOVA,
        Doctor.HINDYCH,
        Doctor.KANOVA,
        Doctor.OBSIVAC,
        Doctor.PRASKOVA,
        Doctor.SMRCEK,
        Doctor.TISON
    ],
    Shifts.PRISLUZBA: [
        Doctor.DUDKOVA,
        Doctor.HLISTA,
        Doctor.DOROVSKA,
        Doctor.OBSIVAC,
        Doctor.SMRCEK,
        Doctor.HANZLIKOVA
    ]
}

for doctor in not_allowed_shifts[Shifts.ODDELENI]:
    scheduler.shift_count(doctor, [Shifts.ODDELENI], 0, 0)

for doctor in Doctor:
    if doctor in not_allowed_shifts[Shifts.PRISLUZBA]:
        scheduler.shift_count(doctor, [Shifts.PRISLUZBA], 0, 0)
    else:
        scheduler.shift_count(doctor, [Shifts.PRISLUZBA], 1, 2)

# individual requirements
scheduler.requirement_positive(Doctor.PRASKOVA, Shifts.PRISLUZBA.others(), [
    date(2025,2,2)
])
scheduler.requirement_positive(Doctor.DOROVSKA, Shifts.PRISLUZBA.others(), [
    date(2025,2,3)
])
scheduler.requirement_positive(Doctor.HUDYMAC, Shifts.PRISLUZBA.others(), [
    date(2025,2,4),
    date(2025,2,18),
    date(2025,2,22),
    date(2025,2,25)
])
scheduler.requirement_positive(Doctor.HINDYCH, Shifts.PRISLUZBA.others(), [
    date(2025,2,8),
    date(2025,2,20)
])
scheduler.requirement_positive(Doctor.OBSIVAC, Shifts.PRISLUZBA.others(), [
    date(2025,2,9),
    date(2025,2,17)
])

scheduler.requirement_negative(Doctor.JEZOVA, [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,5),
    date(2025,2,7),
    date(2025,2,9),
    date(2025,2,10),
    date(2025,2,28),
])
scheduler.requirement_negative(Doctor.HANZLIKOVA, [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,5),
    date(2025,2,10),
    date(2025,2,15),
])
scheduler.requirement_negative(Doctor.HERMANNOVA, [
    date(2025,2,1),
    date(2025,2,2),
    date(2025,2,14),
    date(2025,2,15),
    date(2025,2,16),
    date(2025,2,17),
])
scheduler.requirement_negative(Doctor.HUDYMAC, [
    date(2025,2,d) for d in [1,2,6,7,8,9,10,11,12,13,14,15,16,20,21]
])
scheduler.requirement_negative(Doctor.HLISTA, [
    date(2025,2,d) for d in [1,2,3,4,5,6,7,8,10,11,14,15,16,17,18,19,20,25,26,27,28]
])
scheduler.requirement_negative(Doctor.SMRCEK, [
    date(2025,2,d) for d in [3,5,6,10,13,14,15,16,17,19,20,24,27,28]
])
scheduler.requirement_negative(Doctor.DUDKOVA, [
    date(2025,2,d) for d in [3,4,7,8,9,10,11,12,14,15,17,18,24,25,28]
])
scheduler.requirement_negative(Doctor.DOROVSKA, [
    date(2025,2,d) for d in [5,6,7,8,9,10,11,12,13,20,27]
])
scheduler.requirement_negative(Doctor.FOLDYNOVA, [
    date(2025,2,d) for d in [8,11,12,21,27]
])
scheduler.requirement_negative(Doctor.MATOUSKOVA, [
    date(2025,2,d) for d in [8,9]
])
scheduler.requirement_negative(Doctor.HINDYCH, [
    date(2025,2,d) for d in [6,9,10,13,14,15,16]
])
scheduler.requirement_negative(Doctor.PRASKOVA, [
    date(2025,2,d) for d in [4,11,14,15,16,18,21,22,23,25]
])
scheduler.requirement_negative(Doctor.HANZLIKOVA, [
    date(2025,2,d) for d in [1,2,5,10,15]
])
scheduler.requirement_negative(Doctor.PAVLIK, [
    date(2025,2,d) for d in [12,21]
])
scheduler.requirement_negative(Doctor.MATULOVA, [
    date(2025,2,d) for d in [17,18,19,20,21]
])
scheduler.requirement_negative(Doctor.OBSIVAC, [
    date(2025,2,d) for d in [21,22,23,24,25,26,27,28]
])

scheduler.requirement_negative_weekday(Doctor.MATOUSKOVA, [1,2,3,4])

scheduler.schedule()
scheduler.print_statistics()
