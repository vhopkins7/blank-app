import streamlit as st


# Define training plan generator function
def generate_training_plan(pace_per_km, num_runs_per_week, longest_run_distance):
    # Placeholder for training plan logic
    # This is a simplified example, but you can expand this based on your previous logic

    plan = []
    weekly_mileage = 0

    for week in range(1, 5):  # Assuming a 4-week plan for simplicity
        weekly_plan = f"Week {week} Training Plan:"
        
        # Add easy runs (e.g., 3-5 runs per week)
        easy_runs = f" - Easy runs: {num_runs_per_week - 1} days, each of {pace_per_km * 1.2} min/km"
        plan.append(weekly_plan)
        plan.append(easy_runs)

        # Add long run
        long_run = f" - Long run: {longest_run_distance} km at {pace_per_km * 1.3} min/km"
        plan.append(long_run)

        # Calculate weekly mileage
        weekly_mileage = (num_runs_per_week - 1) * (pace_per_km * 1.2 * 5) + longest_run_distance
        plan.append(f" - Total weekly mileage: {weekly_mileage} km")
        plan.append("")

    return "\n".join(plan)

# Create Streamlit app layout
st.title("Personalized 5K Training Plan")

# Input fields
st.header("Enter Your Details")
pace_per_km = st.number_input("Enter your pace per km (in minutes)", min_value=4.0, max_value=12.0, value=5.0)
num_runs_per_week = st.slider("How many runs per week do you want?", 3, 7, 5)
longest_run_distance = st.number_input("What is the longest distance you want to run?", min_value=5, max_value=10, value=8)

# Generate the training plan
if st.button("Generate Training Plan"):
    st.subheader("Your Training Plan")
    training_plan = generate_training_plan(pace_per_km, num_runs_per_week, longest_run_distance)
    st.text(training_plan)