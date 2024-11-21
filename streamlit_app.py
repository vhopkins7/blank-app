import streamlit as st
import random

# Function to generate the training plan
def generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance, training_duration=4):
    random.seed(42)  # Fixed seed for reproducibility
    plan = []
    
    # Calculate the 5K pace (minutes per km) from the PB time
    five_k_pace_per_km = five_k_pb_minutes / 5  # 5K is 5 kilometers

    # Define a base range for easy runs (e.g., 70% to 90% of the longest run distance)
    min_easy_run_distance = longest_run_distance * 0.7  # 70% of longest run distance
    max_easy_run_distance = longest_run_distance * 0.9  # 90% of longest run distance

    current_long_run_distance = longest_run_distance  # Initialize the long run distance

    # Add interval sessions based on the number of runs per week
    if num_runs_per_week >= 5:
        interval_sessions = [
            f"{round(random.uniform(1.5, 3), 2)} km at {round(five_k_pace_per_km * 0.85, 2)} min/km (hard effort)",
            f"{round(random.uniform(1.5, 3), 2)} km at {round(five_k_pace_per_km * 0.85, 2)} min/km (hard effort)"
        ]
    elif 3 <= num_runs_per_week < 5:
        interval_sessions = [
            f"{round(random.uniform(1.5, 3), 2)} km at {round(five_k_pace_per_km * 0.85, 2)} min/km (hard effort)"
        ]
    else:
        interval_sessions = []  # No interval sessions if less than 3 runs

    # Generate weekly plan for the specified duration
    for week in range(1, training_duration + 1):
        weekly_plan = f"Week {week} Training Plan:"
        plan.append(weekly_plan)

        # Add easy runs with varying distances
        easy_run_count = num_runs_per_week - 1 - len(interval_sessions)  # Subtract interval sessions
        for i in range(easy_run_count):
            easy_run_distance = random.uniform(min_easy_run_distance, max_easy_run_distance)
            easy_run_pace = five_k_pace_per_km * 1.2  # Easy run pace is 20% slower than the base pace
            plan.append(f" - Easy run {i+1}: {easy_run_distance:.2f} km at {easy_run_pace:.2f} min/km")

        # Add interval sessions
        for idx, interval in enumerate(interval_sessions):
            plan.append(f" - Interval session {idx + 1}: {interval}")

        # Add long run
        long_run_pace = five_k_pace_per_km * 1.3  # Long run pace is 30% slower than the base pace
        plan.append(f" - Long run: {current_long_run_distance:.2f} km at {long_run_pace:.2f} min/km")

        # Calculate weekly mileage
        total_easy_runs_distance = sum(random.uniform(min_easy_run_distance, max_easy_run_distance) for _ in range(easy_run_count))
        weekly_mileage = total_easy_runs_distance + current_long_run_distance + sum(random.uniform(1.5, 3) for _ in interval_sessions)
        plan.append(f" - Total weekly mileage: {weekly_mileage:.2f} km")
        plan.append("")  # Empty line between weeks

        # Increase long run distance by 5% for the next week
        current_long_run_distance *= 1.05

    return plan


# Streamlit app layout
st.title("Running Training Plan Generator")

# User inputs
st.sidebar.header("Input Your Details")
five_k_pb_minutes = st.sidebar.number_input("Enter your 5K PB time (in minutes):", min_value=10, max_value=60, value=25, step=1)
num_runs_per_week = st.sidebar.number_input("Number of runs per week:", min_value=1, max_value=7, value=4)
longest_run_distance = st.sidebar.number_input("Longest run distance (in km):", min_value=1, max_value=42, value=10, step=1)
training_duration = st.sidebar.slider("Training duration (weeks):", min_value=4, max_value=12, step=1, value=4)

# Generate and display the plan when the user clicks the button
if st.button("Generate Training Plan"):
    if five_k_pb_minutes < 10 or five_k_pb_minutes > 60:
        st.warning("Please enter a realistic 5K PB time (between 10 and 60 minutes).")
    elif num_runs_per_week < 1 or longest_run_distance < 1:
        st.warning("Ensure you provide meaningful input values.")
    else:
        # Generate the plan
        training_plan = generate_training_plan(num_runs_per_week, five_k_pb_minutes, longest_run_distance, training_duration)

        # Display the result in a structured format
        st.subheader("Your Training Plan:")
        for week in range(training_duration):
            with st.expander(f"Week {week + 1} Plan"):
                week_plan = training_plan[week * (num_runs_per_week + 3):(week + 1) * (num_runs_per_week + 3)]
                for day in week_plan:
                    st.markdown(f"- {day}")

        # Weekly mileage chart
        weekly_mileage_list = [
            float(plan_line.split(": ")[1].split(" km")[0])
            for plan_line in training_plan if "Total weekly mileage" in plan_line
        ]
        st.subheader("Weekly Mileage Progression")
        st.line_chart(weekly_mileage_list)
