import streamlit as st
import requests

st.title("AQUA SHIELD AI Login")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":

    st.subheader("Create Account")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        res = requests.post("http://127.0.0.1:8000/register",
                            json={"username": username, "email": email, "password": password})
        try:
            data = res.json()
            st.write(data)
        except:
            st.error("Backend error. Check server terminal.")


if choice == "Login":

    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post("http://127.0.0.1:8000/login",
                            json={"username": username, "password": password})

        data = res.json()
        if res.status_code == 200:
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
            
