from pulp import LpMaximize, LpProblem, LpVariable, lpSum,LpStatus
import random
import pandas as pd

class Employee:
    def __init__(self, id,name, skills, availability):
        self.id = id
        self.name=name
        self.skills = skills
        self.availability = availability
        self.assignments = []

    def is_available(self, session):
        return self.availability[session]

    def has_skills(self, required_skills):
        return all(skill in self.skills for skill in required_skills)

    def set_unavailable(self, session):
        self.availability[session] = False

    def add_assignment(self, assignment):
        self.assignments.append(assignment)

    def calculate_rotation_rate(self):
        total_assignments = len(self.assignments)
        unique_assignments = set((assignment['session'], assignment['station']) for assignment in self.assignments)
        unique_assignment_count = len(unique_assignments)

        if total_assignments == 0:
            return 0.0

        rotation_rate = (unique_assignment_count / total_assignments) * 100
        return rotation_rate
       
class Station:
    def __init__(self, id, required_skills, capacity):
        self.id = id
        self.required_skills = required_skills
        self.capacity = capacity
    
    def is_filled(self, session, schedule):
        return len([assignment for assignment in schedule if assignment['session'] == session and assignment['station'] == self]) >= self.capacity

def solve_schedule_linear_programming(employees, stations, sessions):
    model = LpProblem("Employee_Scheduling", LpMaximize)
    x = LpVariable.dicts("x", ((employee.id, station.id, session) for employee in employees
                                                      for station in stations
                                                      for session in sessions), cat='Binary')
    
    rotation_rates = {employee.id: employee.calculate_rotation_rate() for employee in employees}
    
    # Objective function
    model += lpSum(x[(i, j, k)] * rotation_rates[i] for i in rotation_rates 
                                                     for j in range(1, len(stations)+1) 
                                                     for k in sessions), "Total_Rotation_Percentage"

    for i in rotation_rates:
        for k in sessions:
            model += lpSum(x[(i, j, k)] for j in range(1, len(stations)+1)) == 1, f"Unique_Assignment_{i}_{k}"
            
            # New constraint to enforce that an employee can only be assigned to one station in a session
            model += lpSum(x[(i, j, k)] for j in range(1, len(stations)+1)) <= 1, f"One_Station_Assignment_{i}_{k}"
            
        for j in range(1, len(stations)+1):
            model += lpSum(x[(i, j, k)] for k in sessions) <= stations[j-1].capacity, f"Capacity_{i}_{j}"
        for j in range(1, len(stations)+1):
            for k in sessions:
                if not employees[i-1].is_available(k) or not employees[i-1].has_skills(stations[j-1].required_skills):
                    model += x[(i, j, k)] == 0, f"Availability_Skill_{i}_{j}_{k}"

    # Additional constraint to ensure each station is assigned at least one employee in each session
    for j in range(1, len(stations)+1):
        for k in sessions:
            model += lpSum(x[(i, j, k)] for i in rotation_rates) >= 1, f"At_Least_One_Assignment_{j}_{k}"

    # Solve the problem
    model.solve()


    # Solve the problem
    model.solve()
    
    
    # Print results
    if LpStatus[model.status] == "Optimal":
        schedule = []
        for i in rotation_rates:
            for j in range(1, len(stations)+1):
                for k in sessions:
                    if x[(i, j, k)].value() == 1:
                        assignment = {
                            'employee': employees[i-1].name,
                            'station': stations[j-1].required_skills[0],
                            'session': k
                        }
                        schedule.append(assignment)
        return schedule
    else:
        return None
def calculate_rotation_percentage(schedule, total_unique_employees):
    unique_assignments = set()

    for assignment in schedule:
        unique_assignments.add((assignment['employee'], assignment['station']))

    rotation_percentage = (len(unique_assignments) / total_unique_employees) * 100
    return rotation_percentage
employees = [
    Employee(1, "John", ['Station A', 'Station C', 'Station F'], {1: True, 2: True, 3: True}),
    Employee(2, "Alex", ['Station B', 'Station D', 'Station E', 'Station F'], {1: True, 2: True, 3: True}),
    Employee(3, "Sam", ['Station C', 'Station B', 'Station G', 'Station E'], {1: True, 2: True, 3: True}),
    Employee(4, "Sean", ['Station E', 'Station A', 'Station H'], {1: True, 2: True, 3: True}),
    Employee(5, "Tony", ['Station F', 'Station E', 'Station D'], {1: True, 2: True, 3: True}),
    Employee(6, "Mark", ['Station G', 'Station F', 'Station B', 'Station C'], {1: True, 2: True, 3: True}),
    Employee(7, "Jeff", ['Station H', 'Station G', 'Station A'], {1: True, 2: True, 3: True}),
    Employee(8, "Tom", ['Station D', 'Station H', 'Station C', 'Station G'], {1: True, 2: True, 3: True}),
]

stations = [
    Station(1, ['Station A'], 1),
    Station(2, ['Station B'], 1),
    Station(3, ['Station C'], 1),
    Station(4, ['Station D'], 1),
    Station(5, ['Station E'], 1),
    Station(6, ['Station F'], 1),
    Station(7, ['Station G'], 1),
    Station(8, ['Station H'], 1),
]
shifts = ['Monday','Tuesday', 'Wednesday', 'Thursday','Friday'] 
def Createschedule(value:dict):
    shifts=value["shifts"]
    session=value["session"]
    NUMBER_OF_SCHEDULES_TO_GENERATE = 5  # Adjust this as needed
    stat=value["stations"]
    employ=value["employees"]
    stations = [Station(stat[station]['id'], [stat[station]["name"]], stat[station]["session"]) for station in stat]
    employees= [Employee(employ[employee]["id"],employ[employee]["name"],employ[employee]["stations"],employ[employee]["availability"])for employee in employ]
    for shift in shifts:
        sessions = list(session)  # List of sessions for the current shift
        schedule_lp_options = []     # List to store multiple schedule options

        for _ in range(NUMBER_OF_SCHEDULES_TO_GENERATE):  # Specify the number of options you want to generate
            shuffled_employees = employees.copy()
            random.shuffle(shuffled_employees)
            
            shuffled_stations = stations.copy()
            random.shuffle(shuffled_stations)
            
            schedule_lp = solve_schedule_linear_programming(shuffled_employees, shuffled_stations, sessions)
            
            if schedule_lp:
                total_unique_employees = (len(set(assignment['employee'] for assignment in schedule_lp))) * len(sessions)
                unique_schedule_lp = [dict(t) for t in {tuple(d.items()) for d in schedule_lp}]
                schedule_lp_options.append(unique_schedule_lp)

        if schedule_lp_options:
            for idx, option in enumerate(schedule_lp_options):
                print(f'Option {idx + 1} - {shift} Shift:')
                print(f'Rate: {calculate_rotation_percentage(option, total_unique_employees)}')
                pivot_table_lp = pd.DataFrame(option).pivot(index='station', columns='session', values='employee')
                print(pivot_table_lp)
            return schedule_lp_options
        else:
            print(f"No optimal solutions found for {shift} shift.")