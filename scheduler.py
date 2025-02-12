import calendar
from datetime import date
from ortools.sat.python import cp_model

class Scheduler(cp_model.CpSolverSolutionCallback):

    def __init__(self, doctors, days, shifts):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._doctors = doctors
        self._days = days
        self._shifts = shifts
        self._model = cp_model.CpModel()
        self._schedule = self._create_schedule()
        self._solver = Scheduler._create_solver()

    # Creates shift variables.
    # schedule[(day, shift, doctor)]: {shift} on {day} is held by the {doctor}
    def _create_schedule(self):
        schedule = {}
        for day in self._days:
            for shift in self._shifts:
                for doctor in self._doctors:
                    schedule[(day, shift, doctor)] = self._model.new_bool_var(f"shift({day},{shift},{doctor})")
        return schedule

    @staticmethod
    def _create_solver():
        solver = cp_model.CpSolver()
        solver.parameters.linearization_level = 0
        return solver

    @staticmethod
    def generate_days(year, month):
        days_in_month = calendar.monthrange(year, month)[1]
        return [date(year, month, day) for day in range(1, days_in_month + 1)]

    # Each shift is assigned to exactly one doctor in the schedule period.
    def one_doctor_per_shift(self, shifts, date_predicate = lambda d: True):
        for day in filter(date_predicate, self._days):
            for shift in shifts:
                self._model.add_exactly_one(self._schedule[(day, shift, doctor)] for doctor in self._doctors)

    def no_shifts(self, shifts, date_predicate):
        shifts_to_avoid = [
            self._schedule[(day, shift, doctor)]
            for day in filter(date_predicate, self._days)
            for shift in shifts
            for doctor in self._doctors
        ]
        self._model.add(sum(shifts_to_avoid) == 0)

    # Each doctor works at most one shift per day.
    def one_shift_per_doctor_in_period(self, num_days=2):
        for doctor in self._doctors:
            for day_index in range(len(self._days) - (num_days-1)):
                days = [self._days[i] for i in range(day_index, day_index+num_days)]
                self._model.add_at_most_one(
                    self._schedule[(d, s, doctor)] for s in self._shifts for d in days
                )

    def shift_count(self, doctor, shifts, min, max):
        shifts_worked = [
            self._schedule[(day, shift, doctor)]
                for shift in shifts
                for day in self._days
        ]
        self._model.add(min <= sum(shifts_worked))
        self._model.add(max >= sum(shifts_worked))

    def requirement_positive(self, doctor, shift, dates):
        self._model.add_bool_and(
            [self._schedule[date, shift, doctor] for date in dates]
        )

    def requirement_negative(self, doctor, dates):
        shifts_to_avoid = [
            self._schedule[(day, shift, doctor)]
                for day in dates
                for shift in self._shifts
        ]
        self._model.add(sum(shifts_to_avoid) == 0)

    def schedule(self):
        self._solver.solve(self._model, self)

    def on_solution_callback(self):
        print("Solution found:")
        self.print_schedule()
        print("\nShift counts per doctor:")
        self.print_schedule_stats()

    def print_schedule(self):
        print("date,oddělení,anestezie,příslužba")
        for day in self._days:
            print(f"{day},", end="")
            shift_doctors = [self.get_doctor(day,shift) for shift in self._shifts]
            print(*shift_doctors, sep=",")

    def print_schedule_stats(self):
        print("doctor,oddělení,anestezie,příslužba,všední,víkend")
        for doctor in self._doctors:
            print(f"{doctor},", end="")
            shift_counts = [self.get_shift_count(doctor,[shift]) for shift in self._shifts]
            print(*shift_counts, sep=",", end="")
            workday_shift_count = self.get_shift_count(doctor, ["oddělení","anestezie"], lambda d: d.weekday() < 5)
            weekend_shift_count = self.get_shift_count(doctor, ["oddělení","anestezie"], lambda d: d.weekday() >= 5)
            print(f",{workday_shift_count},{weekend_shift_count}")

    def get_doctor(self, day, shift):
        return next(
            (doctor for doctor in self._doctors if self.value(self._schedule[(day, shift, doctor)])),
            None
        )

    def get_shift_count(self, doctor, shifts, day_predicate = lambda d: True):
        return sum(
            self.value(self._schedule[day, shift, doctor])
               for shift in shifts
               for day in filter(day_predicate, self._days)
        )

    def print_statistics(self):
        print("\nStatistics")
        print(f"  - conflicts      : {self._solver.num_conflicts}")
        print(f"  - branches       : {self._solver.num_branches}")
        print(f"  - wall time      : {self._solver.wall_time} s")
