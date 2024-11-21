import streamlit as st
import random

# Function to calculate VDOT based on 5K time
def calculate_vdot(five_k_time_minutes):
    # Jack Daniels VDOT table is not linear, but we can use an approximation based on 5K time
    vdot_lookup = {
        15: 35.0, 16: 34.0, 17: 33.0, 18: 32.0, 19: 31.0, 20: 30.0, 21: 29.0, 22: 28.0, 23: 27.0,
        24: 26.0, 25: 25.0, 26: 24.0, 27: 23.0, 28: 22.0, 29: 21.0, 30: 20.0, 31: 19.0, 32: 18.0
        # Simplified VDOT lookup (you could expand this lookup table as needed)
    }
    
    # Approximate VDOT based on the 5K time (rounded)
    vdot = vdot_lookup.get(five_k_time_minutes, 18.0)  # Default to VDOT 18 if not found
    return vdot

# Function to get paces based on VDOT
def get_training_paces(vdot):
    # Jack Daniels training paces:
    easy_pace = 5.0 + (vdot - 20) * 0.05  # Easy pace is 65-75% of VDOT pace
    interval_pace = 4.5 + (vdot - 20) * 0.08  # Interval pace is 90-100% of VDOT pace
    long_run_pace = 5.5 + (vdot - 20) * 0.06  # Long run pace is 75-80% of VDOT pace
    
    return easy_pace, interval_pace, long_run_pace

# Function to generate the training plan
def generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance, num_weeks):
    plan = []
    
    # Calculate VDOT from 5K time and derive paces
    vdot = calculate_vdot(five_k_pb_minutes)
    easy_pace, interval_pace, long_run_pace = get_training_paces(vdot)
    
    # Define a base range for easy runs (e.g., 70% to 90% of the longest run distance)
    min_easy_run_distance = longest_run_distance * 0.7  # 70% of longest run distance
    max_easy_run_distance = longest_run_distance * 0.9  # 90% of longest run distance
    
    current_long_run_distance = longest_run_distance  # Initialize the long run distance
    
    # Add interval sessions based on number of runs per week
    if num_runs_per_week >= 5:
        interval_sessions = [
            f" - Interval session 1: {round(random.uniform(1.5, 3), 2)} km at {round(interval_pace, 2)} min/km (hard effort)",
            f" - Interval session 2: {round(random.uniform(1.5, 3), 2)} km at {round(interval_pace, 2)} min/km (hard effort)"
        ]
    elif 3 <= num_runs_per_week < 5:
        interval_sessions = [
            f" - Interval session 1: {round(random.uniform(1.5, 3), 2)} km at {round(interval_pace, 2)} min/km (hard effort)"
        ]
    else:
        interval_sessions = []  # No interval sessions if less than 3 runs

    # Generate weekly plan for the specified number of weeks
    for week in range(1, num_weeks + 1):  # Plan length is determined by num_weeks
        weekly_plan = f"Week {week} Training Plan:"
        plan.append(weekly_plan)

        # Add easy runs with varying distances
        easy_run_count = num_runs_per_week - 1 - len(interval_sessions)  # Subtract interval sessions
        for i in range(easy_run_count):  # Easy runs are the total runs minus the long run and intervals
            easy_run_distance = random.uniform(min_easy_run_distance, max_easy_run_distance)
            plan.append(f" - Easy run {i+1}: {round(easy_run_distance, 2)} km at {round(easy_pace, 2)} min/km")
        
        # Add interval sessions
        for interval in interval_sessions:
            plan.append(interval)

        # Add long run
        plan.append(f" - Long run: {round(current_long_run_distance, 2)} km at {round(long_run_pace, 2)} min/km")

        # Calculate weekly mileage
        total_easy_runs_distance = sum(random.uniform(min_easy_run_distance, max_easy_run_distance) for _ in range(easy_run_count))
        weekly_mileage = total_easy_runs_distance + current_long_run_distance + sum(random.uniform(1.5, 3) for _ in interval_sessions)
        plan.append(f" - Total weekly mileage: {round(weekly_mileage, 2)} km")
        plan.append("")  # Empty line between weeks

        # Increase long run distance by 5% for the next week
        current_long_run_distance *= 1.05

    return "\n".join(plan)


# Streamlit app layout
st.title("Running Training Plan Generator")

# User inputs
five_k_pb_minutes = st.number_input("Enter your 5K PB time (in minutes):", min_value=1, value=25, step=1)
num_runs_per_week = st.number_input("Number of runs per week:", min_value=1, max_value=7, value=4)
longest_run_distance = st.number_input("Longest run distance (in km):", min_value=1, value=10, step=1)

# Add a dropdown for selecting the training plan length (4 to 16 weeks in intervals of 2)
training_plan_length = st.selectbox("Select training plan length (weeks):", [4, 6, 8, 10, 12, 14, 16])

# Generate and display the plan when the user clicks the button
if st.button("Generate Training Plan"):
    # Generate the plan
    training_plan = generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance, training_plan_length)
    
    # Display the result in the app
    st.subheader(f"Your {training_plan_length}-Week Training Plan:")
    st.text(training_plan)
