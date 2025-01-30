import streamlit as st
import requests

# Define FastAPI backend URL (update if running on a different port)
API_URL = "http://127.0.0.1:8000/api"

# Streamlit UI
st.title("ATM Banking System 💰")

# Check if the user is logged in
is_logged_in = "api_key" in st.session_state

# Sidebar for Login
if not is_logged_in:
    st.sidebar.header("Login")
    username = st.sidebar.text_input("Username")
    pin = st.sidebar.text_input("PIN", type="password")

    if st.sidebar.button("Login"):
        payload = {"username": username, "pin": pin}
        response = requests.post(f"{API_URL}/login/", json=payload)

        if response.status_code == 200:
            st.session_state["api_key"] = response.json().get("token")  # Store API token
            st.session_state["username"] = username  # Store username for transactions
            st.success("Login successful!")
            st.rerun()  # Refresh the UI to hide login fields
        else:
            st.error("Invalid username or PIN.")

# Account Creation (Only show if NOT logged in)
if not is_logged_in:
    st.header("Create an Account 🏦")
    new_username = st.text_input("New Username")
    new_pin = st.text_input("New PIN", type="password")
    initial_deposit = st.number_input("Initial Deposit", min_value=0.0, format="%.2f")

    if st.button("Create Account"):
        payload = {
            "username": new_username,
            "pin": new_pin,
            "initial_deposit": initial_deposit
        }
        response = requests.post(f"{API_URL}/create-account/", json=payload)

        if response.status_code == 200:
            st.success("Account created successfully!")
        else:
            st.error("Error creating account.")

# ATM Operations (Only show if logged in)
if is_logged_in:
    st.header("ATM Operations 🏧")
    username = st.session_state["username"]  # Retrieve username from session

    # Check Balance
    if st.button("Check Balance"):
        headers = {"Authorization": f"Bearer {st.session_state['api_key']}"}
        response = requests.get(f"{API_URL}/check-balance/", headers=headers, params={"username": username})

        if response.status_code == 200:
            st.info(f"Your balance is: ${response.json()['balance']}")
        else:
            st.error("Error fetching balance.")

    # Deposit Form
    deposit_amount = st.number_input("Deposit Amount", min_value=0.0, format="%.2f")
    if st.button("Deposit"):
        headers = {"Authorization": f"Bearer {st.session_state['api_key']}"}
        payload = {"username": username, "amount": deposit_amount}
        response = requests.post(f"{API_URL}/deposit/", json=payload, headers=headers)

        if response.status_code == 200:
            st.success(f"Deposited ${deposit_amount:.2f}.")
        else:
            st.error("Error depositing amount.")

    # Withdraw Form
    withdraw_amount = st.number_input("Withdraw Amount", min_value=0.0, format="%.2f")
    if st.button("Withdraw"):
        headers = {"Authorization": f"Bearer {st.session_state['api_key']}"}
        payload = {"username": username, "amount": withdraw_amount}
        response = requests.post(f"{API_URL}/withdraw/", json=payload, headers=headers)

        if response.status_code == 200:
            st.success(f"Withdrew ${withdraw_amount:.2f}.")
        else:
            st.error("Error withdrawing amount.")

    # Logout
    if st.button("Logout"):
        st.session_state.pop("api_key", None)  # Remove API key from session
        st.session_state.pop("username", None)  # Remove username
        st.success("Logout successful!")
        st.rerun()  # Refresh the UI to show login fields again
