import streamlit as st

# Function to calculate training paces based on VDOT
def get_training_paces(vdot):
    # For simplicity, assume fixed paces based on VDOT
    easy_pace = 4.5  # Example pace (min/km) for easy runs
    interval_pace = 4.0  # Example pace (min/km) for interval runs
    long_run_pace = 5.0  # Example pace (min/km) for long runs
    
    return easy_pace, interval_pace, long_run_pace

# Function to calculate weekly training plan
def generate_training_plan(vdot, num_runs_per_week, weeks=4, longest_run_past_month=10):
    easy_pace, interval_pace, long_run_pace = get_training_paces(vdot)

    plan = []
    
    for week in range(1, weeks + 1):
        weekly_plan = f"Week {week} Training Plan:"
        
        # Add easy runs (split into varied distances)
        easy_runs = []
        for i in range(num_runs_per_week - 2):  # Subtract interval sessions and long run
            distance = 5 + (week - 1) * 0.5  # Increase easy run distance each week
            easy_runs.append(f"  - Easy run {i + 1}: {distance:.1f} km at {easy_pace} min/km")
        
        # Add interval sessions if applicable
        if num_runs_per_week >= 5:
            easy_runs.append(f"  - Interval run 1: {interval_pace} min/km for 6x400m intervals")
            easy_runs.append(f"  - Interval run 2: {interval_pace} min/km for 6x400m intervals")
        elif num_runs_per_week >= 3:
            easy_runs.append(f"  - Interval run: {interval_pace} min/km for 6x400m intervals")
        
        # Longest run (user input, no history logic)
        longest_run_distance = longest_run_past_month + (week - 1) * 2  # Increase by 2 km each week

        # Add the long run to the weekly plan
        easy_runs.append(f"  - Long run: {longest_run_distance:.1f} km at {long_run_pace:.2f} min/km")
        
        # Calculate total weekly mileage (sum of easy runs and the long run)
        weekly_mileage = 0
        for run in easy_runs:
            if "km" in run:
                # Extract the distance value before the 'km'
                km_distance = float(run.split(":")[1].split("km")[0].strip()) 
                weekly_mileage += km_distance
        
        plan.append(weekly_plan)
        plan.extend(easy_runs)
        plan.append(f"  - Total weekly mileage: {weekly_mileage:.1f} km")
        plan.append("")  # Add a blank line between weeks
    
    return "\n".join(plan)

# Streamlit App
def app():
    st.title('Running Training Plan Generator')

    # Input fields for the 5K time in minutes and seconds
    mins = st.number_input('Enter 5K time - Minutes:', min_value=0, max_value=100, value=16)
    secs = st.number_input('Enter 5K time - Seconds:', min_value=0, max_value=59, value=0)
    
    # Calculate the total 5K time in minutes
    total_time = mins + secs / 60.0
    
    # Calculate VDOT based on the total 5K time (simple example, use a better method if needed)
    vdot = 34  # Placeholder for VDOT calculation (you can adjust this to use a formula
