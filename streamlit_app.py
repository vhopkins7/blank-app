import streamlit as st

# Function to calculate training paces
def get_training_paces(vdot):
    # Placeholder for easy run pace, interval pace, and long run pace calculation based on VDOT
    easy_pace = 4.5  # Set to target a pace around 4.5 min/km for faster runners
    interval_pace = 4.5 + (vdot - 20) * 0.08  # Interval pace is usually faster (90-100% of race pace)
    long_run_pace = 5.5 + (vdot - 20) * 0.06  # Long run pace is slower (75-80% of race pace)
    
    return easy_pace, interval_pace, long_run_pace

# Function to calculate weekly training plan
def generate_training_plan(vdot, num_runs_per_week, weeks=4):
    easy_pace, interval_pace, long_run_pace = get_training_paces(vdot)

    plan = []
    longest_run_distance_history = []  # To track the longest run over the past 5 weeks
    
    for week in range(1, weeks + 1):
        weekly_plan = f"Week {week} Training Plan:"
        
        # Add easy runs (split into varied distances)
        easy_runs = []
        for i in range(num_runs_per_week - 2):  # Subtract the interval sessions and long run
            distance = 5 + (week - 1) * 0.5  # Increase easy run distance each week
            easy_runs.append(f"  - Easy run {i + 1}: {distance:.1f} km at {easy_pace} min/km")
        
        # Add interval sessions if applicable
        if num_runs_per_week >= 5:
            easy_runs.append(f"  - Interval run 1: {interval_pace} min/km for 6x400m intervals")
            easy_runs.append(f"  - Interval run 2: {interval_pace} min/km for 6x400m intervals")
        elif num_runs_per_week >= 3:
            easy_runs.append(f"  - Interval run: {interval_pace} min/km for 6x400m intervals")
        
        # Calculate the longest run distance
        if week <= 5:
            longest_run_distance = 10 + (week - 1) * 2  # Initial increase of 2 km each week
        else:
            # Get the longest run from the previous 5 weeks
            longest_run_distance = max(longest_run_distance_history[-5:])
        
        longest_run_distance_history.append(longest_run_distance)
        easy_runs.append(f"  - Long run: {longest_run_distance:.1f} km at {long_run_pace:.2f} min/km")
        
        # Add weekly mileage
        weekly_mileage = sum([float(run.split(" ")[2]) for run in easy_runs if "km" in run])
        plan.append(weekly_plan)
        plan.extend(easy_runs)
        plan.append(f"  - Total weekly mileage: {weekly_mileage:.1f} km")
        plan.append("")
    
    return "\n".join(plan)

# Streamlit App
def app():
    st.title('Running Training Plan Generator')

    # Input fields for the 5K time in minutes and seconds
    mins = st.number_input('Enter 5K time - Minutes:', min_value=0, max_value=100, value=16)
    secs = st.number_input('Enter 5K time - Seconds:', min_value=0, max_value=59, value=0)
    
    # Calculate the total 5K time in minutes
    total_time = mins + secs / 60.0
    
    # Calculate VDOT based on the total 5K time
    vdot = 34  # Placeholder for VDOT calculation (you can adjust this to use a formula)
    
    # Input field for the number of runs per week
    num_runs_per_week = st.slider('Number of runs per week:', 1, 7, 5)

    # Input field for the length of the training plan
    training_weeks = st.selectbox('Training plan length (weeks):', [4, 6, 8, 10, 12, 14, 16], index=3)

    # Generate and display the training plan
    if st.button('Generate Training Plan'):
        plan = generate_training_plan(vdot, num_runs_per_week, weeks=training_weeks)
        st.text(plan)

if __name__ == '__main__':
    app()
