# Shor's Algorithm Demo
This is a Streamlit app that shows how RSA encryption works and simulates how Shor’s Algorithm (using a classical method) can factor numbers used in RSA.

What the App Does:
- Encrypts and decrypts messages using RSA
- Simulates factoring a number using a basic version of Shor’s Algorithm
- Compares how many attempts it takes to factor different numbers

How to Run:
1. Make sure Python is installed
   
2. Install the required libraries:
pip install streamlit pycryptodome plotly

3. Run the app:
streamlit run streamlit_Capstone.py

Notes:
This is a classical simulation of Shor’s Algorithm, not the real quantum version.
Use small numbers like 15, 21, or 33 for faster simulations. But the bigger the better for visualisation purposes and understanding the ease at which the numbers are easily guessed with Shors algorithm.
This project is for learning purposes and to show why RSA may be vulnerable to quantum computing in the future.

