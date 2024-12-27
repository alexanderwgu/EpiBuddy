from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
from datetime import datetime
import csv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from the environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI API
client = OpenAI(
    api_key = os.getenv("OPENAI_API_KEY"),
)

# Streamlit UI
st.title("EpiBuddy - Your Friendly Epilepsy Support Chatbot")
st.subheader("Chat with EpiBuddy and get epilepsy advice.🌟")

# Define instructions for the chatbot to keep it teen-friendly
INSTRUCTIONS = """
You are a friendly chatbot providing epilepsy support for teens. Speak in teen-friendly language, avoid medical jargon, and answer embarrassing questions with empathy. Always clarify that you are not a replacement for medical advice. Include emojis and provide links to verified epilepsy resources when relevant.
"""

# Function for chatting using OpenAI's API
def chat_with_bot(text, stop_sequence="\nUser:"):
    full_input = f"{INSTRUCTIONS}\nUser: {text}\nChatbot:"
    try:
        # Call the OpenAI API with the user input and instructions
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role": "system", "content": INSTRUCTIONS},
                {"role": "user", "content": text},
            ]
        )
     
        # Get the chatbot's response from the OpenAI API
        chatbot_response = response.choices[0].message.content.strip()

        # Truncate the response at the stop sequence if it exists
        if stop_sequence in chatbot_response:
            chatbot_response = chatbot_response.split(stop_sequence)[0].strip()

        return chatbot_response
    except Exception as e:
        st.error(f"Error while getting response: {e}")
        return "Sorry, I couldn't process your request. Please try again later."

# Input box for user message
user_input = st.text_input("Ask a question...", key="user_input")

# Display only the chatbot's response (no history)
if user_input:
    # Get chatbot's response
    chatbot_response = chat_with_bot(user_input)
    st.markdown(f"{chatbot_response}")

# Seizure log section
st.subheader("Log Your Seizure 📅")

# Start of the form
with st.form("seizure_form"):
    # Allow the user to choose any date and time with a 1-minute interval
    date = st.date_input("Date", key="date_input")
    time = st.time_input("Time", key="time_input", step=60)  # 1-minute intervals
    duration = st.number_input("Duration (in minutes)", min_value=1, key="duration_input")
    symptoms = st.text_area("Symptoms", key="symptoms_input")

    # Submit button inside the form
    submit_button = st.form_submit_button("Log Seizure")

    if submit_button:
        seizure_data = {
            "date": str(date),
            "time": str(time),
            "duration": duration,
            "symptoms": symptoms
        }

        try:
            # Ensure the CSV file exists, and if not, create it with headers
            csv_file_path = 'seizure_data.csv'
            file_exists = os.path.exists(csv_file_path)

            with open(csv_file_path, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["date", "time", "duration", "symptoms"])

                # Write headers if the file does not exist
                if not file_exists:
                    writer.writeheader()

                # Write the seizure data to the CSV file
                writer.writerow(seizure_data)

            st.success("Seizure logged successfully! ✅")

        except IOError as e:
            st.error(f"Failed to save seizure data: {e}")

st.subheader("Seizure Log and Analysis 📊")

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", key="viz_start_date")
with col2:
    end_date = st.date_input("End Date", key="viz_end_date")

create_charts_button = st.button("Visualize Log")

if create_charts_button:
    def load_and_process_data():
        if os.path.exists('seizure_data.csv'):
            df = pd.read_csv('seizure_data.csv')
            if not df.empty:
                df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])
                df['date'] = pd.to_datetime(df['date'])
                return df
        return None

    df = load_and_process_data()
    if df is not None:
        mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
        filtered_df = df.loc[mask]

        if not filtered_df.empty:
            def categorize_time_of_day(time):
                if 6 <= time < 12:
                    return 'Blue (6am - 12pm)'
                elif 12 <= time < 18:
                    return 'Green (12pm - 6pm)'
                elif 18 <= time < 22:
                    return 'Yellow (6pm - 10pm)'
                else:
                    return 'Brown (10pm - 6am)'

            filtered_df['time_category'] = filtered_df['datetime'].dt.hour.apply(categorize_time_of_day)

            # Create a bar chart with color based on the time category
            fig = px.bar(filtered_df, x='date', y='duration', color='time_category',
                        labels={'duration': 'Duration (minutes)', 'time_category': 'Time of Day', 'date': 'Date'},
                        title="Seizure Duration by Date and Time",
                        color_discrete_map={
                            'Blue (6am - 12pm)': 'blue',
                            'Green (12pm - 6pm)': 'green',
                            'Yellow (6pm - 10pm)': 'yellow',
                            'Brown (10pm - 6am)': 'brown'
                        })
            st.plotly_chart(fig)

            # Download section
            st.subheader("Download Log 📥")
            
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv_data,
                file_name=f"seizure_log_{start_date}_{end_date}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data available for selected date range")
    else:
        st.warning("No seizure data available. Please log some seizures first.")
