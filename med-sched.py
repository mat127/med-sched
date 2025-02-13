from enum import Enum

from scheduler import Scheduler

days = Scheduler.generate_days(2025, 2)

class Shift(Enum):
    ODDELENI  = "oddělení"
    ANESTEZIE = "anestezie"
    PRISLUZBA = "příslužba"

    def others(self):
        return list(filter(lambda s: not s == self, Shift))

    @staticmethod
    def main():
        return Shift.PRISLUZBA.others()

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

scheduler = Scheduler(Doctor, days, Shift, Shift.main())
scheduler.one_doctor_per_shift(Shift.main())

# PRISLUZBA only on workdays
scheduler.one_doctor_per_shift([Shift.PRISLUZBA], lambda d: d.weekday() < 5)
scheduler.no_shifts([Shift.PRISLUZBA], lambda d: d.weekday() >= 5)

# days off between shifts (including the shift day)
scheduler.one_shift_per_doctor_in_period(3)

for doctor in Doctor:
    # how many main shifts per doctor
    scheduler.shift_count(doctor, Shift.main(), 3, 4)
    # how many main shifts per doctor during weekend
    scheduler.shift_count(doctor, Shift.main(), 0, 1, lambda d: d.weekday() >= 5)

not_allowed_shifts = {
    Shift.ODDELENI: [
        Doctor.HANZLIKOVA,
        Doctor.HERMANNOVA,
        Doctor.HINDYCH,
        Doctor.KANOVA,
        Doctor.OBSIVAC,
        Doctor.PRASKOVA,
        Doctor.SMRCEK,
        Doctor.TISON
    ],
    Shift.PRISLUZBA: [
        Doctor.DUDKOVA,
        Doctor.HLISTA,
        Doctor.DOROVSKA,
        Doctor.OBSIVAC,
        Doctor.SMRCEK,
        Doctor.HANZLIKOVA
    ]
}

for doctor in not_allowed_shifts[Shift.ODDELENI]:
    scheduler.shift_count(doctor, [Shift.ODDELENI], 0, 0)

for doctor in Doctor:
    if doctor in not_allowed_shifts[Shift.PRISLUZBA]:
        scheduler.shift_count(doctor, [Shift.PRISLUZBA], 0, 0)
    else:
        scheduler.shift_count(doctor, [Shift.PRISLUZBA], 1, 2)

# individual requirements
scheduler.requirement_positive(Doctor.PRASKOVA, Shift.main(), [2])
scheduler.requirement_positive(Doctor.DOROVSKA, Shift.main(), [3])
scheduler.requirement_positive(Doctor.HUDYMAC, Shift.main(), [4,18,22,25])
scheduler.requirement_positive(Doctor.HINDYCH, Shift.main(), [8,20])
scheduler.requirement_positive(Doctor.OBSIVAC, Shift.main(), [9,17])

scheduler.requirement_negative(Doctor.JEZOVA, [1,2,5,7,9,10,28])
scheduler.requirement_negative(Doctor.HANZLIKOVA, [1,2,5,10,15])
scheduler.requirement_negative(Doctor.HERMANNOVA, [1,2,14,15,16,17])
scheduler.requirement_negative(Doctor.HUDYMAC, [1,2,6,7,8,9,10,11,12,13,14,15,16,20,21])
scheduler.requirement_negative(Doctor.HLISTA, [1,2,3,4,5,6,7,8,10,11,14,15,16,17,18,19,20,25,26,27,28])
scheduler.requirement_negative(Doctor.SMRCEK, [3,5,6,10,13,14,15,16,17,19,20,24,27,28])
scheduler.requirement_negative(Doctor.DUDKOVA, [3,4,7,8,9,10,11,12,14,15,17,18,24,25,28])
scheduler.requirement_negative(Doctor.DOROVSKA, [5,6,7,8,9,10,11,12,13,20,27])
scheduler.requirement_negative(Doctor.FOLDYNOVA, [8,11,12,21,27])
scheduler.requirement_negative(Doctor.MATOUSKOVA, [8,9])
scheduler.requirement_negative(Doctor.HINDYCH, [6,9,10,13,14,15,16])
scheduler.requirement_negative(Doctor.PRASKOVA, [4,11,14,15,16,18,21,22,23,25])
scheduler.requirement_negative(Doctor.HANZLIKOVA, [1,2,5,10,15])
scheduler.requirement_negative(Doctor.PAVLIK, [12,21])
scheduler.requirement_negative(Doctor.MATULOVA, [17,18,19,20,21])
scheduler.requirement_negative(Doctor.OBSIVAC, [21,22,23,24,25,26,27,28])

scheduler.requirement_negative_weekday(Doctor.MATOUSKOVA, [1,2,3,4])

scheduler.schedule()
scheduler.print_statistics()
