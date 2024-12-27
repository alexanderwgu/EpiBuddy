# EpiBuddy - Epilepsy Support Chatbot
EpiBuddy is a friendly chatbot designed to provide epilepsy support for teens. It allows users to interact with a chatbot powered by OpenAI GPT-3.5-turbo or the Google Gemma-7B model, log seizure data, and analyze the logs over time with interactive visualizations. Please note that you will need to pay to OpenAI a small fee in order to access its models, while Google Gemma-7B model is free of charge through Hugging Face.

## Features
Chat with EpiBuddy: Get friendly, teen-oriented advice and answers to epilepsy-related questions.
Seizure Log: Log seizure events with details such as date, time, duration, and symptoms.
Visualization: View seizure data over a selected date range with color-coded time categories (morning, afternoon, evening, night).
Download Data: Download seizure logs as a CSV file for further analysis or record-keeping.

## Installation
### 1. Clone the repository
git clone https://github.com/your-username/epibuddy.git
cd epibuddy
### 2. Create and activate a virtual environment
python -m venv epi
source epi/bin/activate  # On Windows, use epi\Scripts\activate
### 3. Install the required dependencies
pip install -r requirements.txt
### 4. Set up environment variables
Create a .env file in the root directory of the project (where the epibuddy_gpt_app.py and epibuddy_gemma_app.py files are located) with the following content (You only need to keep one variable depending on which model you plan to use between OpenAI GPT-3.5-turbo or Gemma2-7B through Hugging Face):
OPENAI_API_KEY=your_openai_api_key
HF_API_KEY=your_huggingface_api_key

You can get your OpenAI API key from OpenAI and Hugging Face API key from Hugging Face.

## Running the App
Once you've installed the dependencies and set up your environment, you can start the Streamlit app with the following command:
streamlit run epibuddy_gpt_app.py
or
streamlit run epibuddy_gemma_app.py

This will launch the app in your default web browser. The chatbot will be accessible, and you can start logging seizure data, generating visualizations, and download seizure logs.

## Project Structure
epibuddy_gpt_app.py: Main Streamlit application with chatbot functionality with GPT-3.5-turbo and seizure logging.
epibuddy_gemma_app.py: Main Streamlit application with chatbot functionality with Gemma2-7B and seizure logging.
.env: Environment file to store your Hugging Face API key.
seizure_data.csv: Stores logged seizure data (automatically created and updated).
requirements.txt: Includes required dependencies.

## Contributing
Feel free to open issues or submit pull requests if you'd like to contribute to the project.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
OpenAI and Hugging Face for providing the models used in this project.
Streamlit for creating a great framework for interactive web apps.
Plotly for interactive charts and visualizations.