import streamlit as st
import random

# Function to generate the training plan
def generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance):
    plan = []
    
    # Calculate the 5K pace (minutes per km) from the PB time
    pace_per_km = five_k_pb_minutes / 5  # 5K is 5 kilometers, so divide the total PB time by 5

    # Define a base range for easy runs (e.g., 70% to 90% of the longest run distance)
    min_easy_run_distance = longest_run_distance * 0.7  # 70% of longest run distance
    max_easy_run_distance = longest_run_distance * 0.9  # 90% of longest run distance
    
    current_long_run_distance = longest_run_distance  # Initialize the long run distance
    
    for week in range(1, 5):  # Assuming a 4-week plan
        weekly_plan = f"Week {week} Training Plan:"
        plan.append(weekly_plan)

        # Add easy runs with varying distances
        for i in range(num_runs_per_week - 1):  # Easy runs are the total runs minus the long run
            easy_run_distance = random.uniform(min_easy_run_distance, max_easy_run_distance)
            easy_run_pace = pace_per_km * 1.2  # Easy run pace is 20% slower than the base pace
            plan.append(f" - Easy run {i+1}: {round(easy_run_distance, 2)} km at {round(easy_run_pace, 2)} min/km")
        
        # Add long run
        long_run_pace = pace_per_km * 1.3  # Long run pace is 30% slower than the base pace
        plan.append(f" - Long run: {round(current_long_run_distance, 2)} km at {round(long_run_pace, 2)} min/km")

        # Calculate weekly mileage
        total_easy_runs_distance = sum(random.uniform(min_easy_run_distance, max_easy_run_distance) for _ in range(num_runs_per_week - 1))
        weekly_mileage = total_easy_runs_distance + current_long_run_distance
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

# Generate and display the plan when the user clicks the button
if st.button("Generate Training Plan"):
    # Generate the plan
    training_plan = generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance)
    
    # Display the result in the app
    st.subheader("Your 4-Week Training Plan:")
    st.text(training_plan)


   