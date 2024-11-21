import streamlit as st

    

# Create Streamlit app layout
st.title("Personalized 5K Training Plan")

# Input fields
st.header("Enter Your Details")
pace_per_km = st.number_input("Enter your pace per km (in minutes)", min_value=4.0, max_value=12.0, value=5.0)
num_runs_per_week = st.slider("How many runs per week do you want?", 3, 7, 5)
longest_run_distance = st.number_input("What is the longest distance you want to run?", min_value=5, max_value=10, value=8)

# Generate the training plan
# if st.button("Generate Training Plan"):
   #  st.subheader("Your Training Plan")
   #  training_plan = generate_training_plan(pace_per_km, num_runs_per_week, longest_run_distance)
   #  st.text(training_plan)

   