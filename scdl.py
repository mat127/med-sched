"""Example of a simple nurse scheduling problem."""
from datetime import date, timedelta
from ortools.sat.python import cp_model

def generate_dates(year, month):
    first_day = date(year, month, 1)
    next_month = month % 12 + 1
    last_day = (date(year + (month // 12), next_month, 1) - timedelta(days=1)).day
    
    return [date(year, month, day) for day in range(1, last_day + 1)]

# Data.
all_nurses = [
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
all_shifts = [
    "oddělení",
    "anestezie",
    "příslužba"
]
all_days = generate_dates(2025, 2)

# Creates the model.
model = cp_model.CpModel()

# Creates shift variables.
# schedule[(n, d, s)]: nurse 'n' works shift 's' on day 'd'.
schedule = {}
for n in all_nurses:
    for d in all_days:
        for s in all_shifts:
            schedule[(n, d, s)] = model.new_bool_var(f"shift_n{n}_d{d}_s{s}")

# Each shift is assigned to exactly one nurse in the schedule period.
for d in all_days:
    for s in all_shifts:
        model.add_exactly_one(schedule[(n, d, s)] for n in all_nurses)

# Each nurse works at most one shift per day.
for n in all_nurses:
    for di in range(len(all_days)-1):
        model.add_at_most_one(schedule[(n, d, s)] for s in all_shifts for d in [all_days[di], all_days[di+1]])

# Try to distribute the shifts evenly, so that each nurse works
# min_shifts_per_nurse shifts. If this is not possible, because the total
# number of shifts is not divisible by the number of nurses, some nurses will
# be assigned one more shift.
# min_shifts_per_nurse = (num_shifts * num_days) // num_nurses
# if num_shifts * num_days % num_nurses == 0:
#     max_shifts_per_nurse = min_shifts_per_nurse
# else:
#     max_shifts_per_nurse = min_shifts_per_nurse + 1
min_shifts_per_nurse = 1
max_shifts_per_nurse = 3
for n in all_nurses:
    shifts_worked = []
    for d in all_days:
        for s in all_shifts:
            shifts_worked.append(schedule[(n, d, s)])
    model.add(min_shifts_per_nurse <= sum(shifts_worked))
    model.add(sum(shifts_worked) <= max_shifts_per_nurse)

# Creates the solver and solve.
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0
# Enumerate all solutions.
solver.parameters.enumerate_all_solutions = True

class NursesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, schedule, nurses, days, shifts, limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._schedule = schedule
        self._nurses = nurses
        self._days = days
        self._shifts = shifts
        self._solution_count = 0
        self._solution_limit = limit

    def on_solution_callback(self):
        self._solution_count += 1
        print(f"Solution {self._solution_count}")
        for d in self._days:
            print(f"Day {d}")
            for n in self._nurses:
                is_working = False
                for s in self._shifts:
                    if self.value(self._schedule[(n, d, s)]):
                        is_working = True
                        print(f"  Nurse {n} works shift {s}")
                if not is_working:
                    print(f"  Nurse {n} does not work")
        if self._solution_count >= self._solution_limit:
            print(f"Stop search after {self._solution_limit} solutions")
            self.stop_search()

    def solutionCount(self):
        return self._solution_count

# Display the first five solutions.
solution_limit = 5
solution_printer = NursesPartialSolutionPrinter(
    schedule, all_nurses, all_days, all_shifts, solution_limit
)

solver.solve(model, solution_printer)

# Statistics.
print("\nStatistics")
print(f"  - conflicts      : {solver.num_conflicts}")
print(f"  - branches       : {solver.num_branches}")
print(f"  - wall time      : {solver.wall_time} s")
print(f"  - solutions found: {solution_printer.solutionCount()}")
