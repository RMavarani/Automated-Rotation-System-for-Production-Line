from pulp import LpMaximize, LpProblem, LpVariable
import pandas as pd
import random
def schedule_shifts(data):
    # Define the model
    model = LpProblem(name="scheduling-problem", sense=LpMaximize)

    # Decision variable
    employees = data['employees']
    stations = data['stations']
    sessions = data['session']
    x = {
        (i, j, k): LpVariable(name=f"x_{i}_{j}_{k}", cat='Binary')
        for i in employees for j in stations for k in sessions
    }

    # Objective Function
    model += sum(x[i, j, k] * (1 + 0.001 * random.random()) for i in employees for j in stations for k in sessions), "Objective"

    # Constraints
    # Availability of employee
    for i in employees:
        for j in stations:
            for k in sessions:
                model += x[i, j, k] <= employees[i]['availability']

    # Station capacity
    for j in stations:
        for k in sessions:
            model += sum(x[i, j, k] for i in employees) == stations[j]['capacity']

    # Not working on the same station in consecutive sessions
    for i in employees:
        for j in stations:
            for k in sessions[:-1]:
                model += x[i, j, k] + x[i, j, k+1] <= 1
    for i in employees:
            for k in sessions:
                model += sum(x[i, j, k] for j in stations) <= 1
    # Solve the model
    model.solve()

    # Extract solution
    schedule = {session: {station: None for station in stations} for session in sessions}
    for i in employees:
        for j in stations:
            for k in sessions:
                if x[i, j, k].varValue > 0.5:
                    schedule[k][j] = employees[i]['name']

    return schedule









def calculate_rotation_percentage(schedule, total_unique_employees):
    unique_assignments = set()

    for assignment in schedule:
        unique_assignments.add((assignment['Employee'], assignment['Station']))

    rotation_percentage = (len(unique_assignments) / total_unique_employees) * 100
    return rotation_percentage

def Createschedule(value:dict):
    schedule_data=[]
    total_unique_employee=len(value['stations'])*len(value["session"])
    rotation_percentage = calculate_rotation_percentage(schedule_data, total_unique_employee)
    while rotation_percentage <= 90:
        schedule=schedule_shifts(value)
        for session, station_assignment in schedule.items():
            for station, employee in station_assignment.items():
                station_name = value['stations'][station]['name']
                schedule_data.append({'Station':station_name,'Employee':employee,'Session':session})
        rotation_percentage = calculate_rotation_percentage(schedule_data, total_unique_employee)
        if rotation_percentage >= 90:
            print(f"Date: {value['shifts']}")
            print(f'Rotation Rate: {rotation_percentage}%')
            schedule_df = pd.DataFrame(schedule_data).pivot(index='Employee', columns='Session', values='Station')
            print(schedule_df)
            schedule_final=schedule_df.to_json(orient='records')
    return schedule_final