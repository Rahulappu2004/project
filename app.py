import streamlit as st
import sqlite3

# Database connection
conn = sqlite3.connect('lawbridge.db')
c = conn.cursor()

# Database setup
def create_tables():
    c.execute('CREATE TABLE IF NOT EXISTS admin (username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS advocates (name TEXT, id_proof TEXT, field TEXT)')
    conn.commit()

create_tables()

# Authentication Functions
def authenticate_user(username, password, role):
    if role == 'Admin':
        c.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
    elif role == 'User':
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    elif role == 'Advocate':
        c.execute('SELECT * FROM advocates WHERE name = ? AND id_proof = ?', (username, password))
    return c.fetchone()

def register_user(username, password):
    c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

def register_advocate(name, id_proof, field):
    c.execute('INSERT INTO advocates (name, id_proof, field) VALUES (?, ?, ?)', (name, id_proof, field))
    conn.commit()

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'role' not in st.session_state:
    st.session_state['role'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

# App Interface
st.title("Law Bridge")

# Update the menu based on login status
if st.session_state['logged_in']:
    menu = ["Home", "Logout"]
else:
    menu = ["Admin Login", "User Signup", "User Login", "Advocate Signup", "Advocate Login"]

choice = st.sidebar.selectbox("Menu", menu)

# Home Page - Only accessible if logged in
if choice == "Home":
    if st.session_state['logged_in']:
        st.subheader(f"Welcome to Law Bridge, {st.session_state['username']}!")
        st.write("""
        Law Bridge is your one-stop solution for legal information and connecting with qualified advocates. 
        Here, you can find information on various legal topics, including criminal law, civil law, corporate law, 
        family law, and more. Our platform also allows you to reach out to experienced advocates for further assistance.
        """)
        
        st.subheader("Popular Legal Topics")
        laws = ["Criminal Law", "Civil Law", "Corporate Law", "Family Law"]
        selected_law = st.selectbox("Select a Field to Learn More", laws)
        
        # Display basic information about the selected law
        if selected_law == "Criminal Law":
            st.write("**Criminal Law** deals with offenses against society or the state. It encompasses laws related to crimes, punishments, and legal procedures. Key areas include:\n")
            st.write("- **Offenses:** Crimes such as theft, assault, murder, and fraud.\n")
            st.write("- **Punishments:** Penalties like fines, imprisonment, community service, or the death penalty.\n")
            st.write("- **Legal Procedures:** Arrest, trial, sentencing, and appeal processes.\n")
            st.write("- **Key Acts:** Indian Penal Code (IPC), Criminal Procedure Code (CrPC), and Evidence Act.\n")
            st.write("Criminal law is enforced by the state to maintain public order and safety, deter criminal behavior, and provide justice for victims.")

        elif selected_law == "Civil Law":
            st.write("**Civil Law** governs disputes between individuals or organizations. It covers various areas, including:\n")
            st.write("- **Contract Law:** Governs agreements between parties, ensuring that contracts are fair and legally binding.\n")
            st.write("- **Property Law:** Deals with rights and obligations related to ownership and use of property.\n")
            st.write("- **Family Law:** Covers marriage, divorce, child custody, and inheritance issues.\n")
            st.write("- **Tort Law:** Involves claims for damages due to negligence or harm caused by another party.\n")
            st.write("Civil law aims to resolve disputes and provide remedies to the aggrieved parties, often through compensation.")

        elif selected_law == "Corporate Law":
            st.write("**Corporate Law** deals with the formation, operation, and dissolution of companies. It includes:\n")
            st.write("- **Company Formation:** Legal processes for establishing corporations, including registration and compliance with regulations.\n")
            st.write("- **Corporate Governance:** Rules and practices that govern the management and control of companies, ensuring accountability to shareholders.\n")
            st.write("- **Mergers and Acquisitions:** Laws related to the consolidation or acquisition of companies.\n")
            st.write("- **Compliance:** Adherence to legal standards, including securities regulation, antitrust laws, and corporate social responsibility.\n")
            st.write("Corporate law ensures that businesses operate within legal frameworks, protecting the interests of stakeholders and the public.")

        elif selected_law == "Family Law":
            st.write("**Family Law** addresses legal issues related to family relationships, such as:\n")
            st.write("- **Marriage and Divorce:** Laws governing the legality of marriage, grounds for divorce, and the division of assets.\n")
            st.write("- **Child Custody:** Determining the best interests of the child in custody and visitation arrangements.\n")
            st.write("- **Adoption:** Legal procedures for adopting a child, including consent and parental rights.\n")
            st.write("- **Inheritance and Succession:** Distribution of a deceased person's estate according to wills or state laws.\n")
            st.write("Family law seeks to balance the rights and responsibilities of family members, ensuring fair outcomes in sensitive personal matters.")

        
        # Contact an advocate section
        if st.button("Find Advocates"):
            st.subheader("Advocates Specializing in This Field")
            c.execute('SELECT name, field FROM advocates WHERE field = ?', (selected_law,))
            advocates = c.fetchall()
            
            if advocates:
                for advocate in advocates:
                    st.write(f"Name: {advocate[0]}, Field: {advocate[1]}")
            else:
                st.write("No advocates found for this field.")
    else:
        st.warning("Please log in to access the content.")

# Admin Login
elif choice == "Admin Login":
    st.subheader("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate_user(username, password, 'Admin'):
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'Admin'
            st.session_state['username'] = username
            st.success("Logged in as Admin")
            st.experimental_rerun()

# User Signup
elif choice == "User Signup":
    st.subheader("User Signup")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Signup"):
        register_user(username, password)
        st.success("User Registered")
        st.info("Go to Login Menu to log in")

# User Login
elif choice == "User Login":
    st.subheader("User Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if authenticate_user(username, password, 'User'):
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'User'
            st.session_state['username'] = username
            st.success(f"Logged in as {username}")
            st.experimental_rerun()

# Advocate Signup
elif choice == "Advocate Signup":
    st.subheader("Advocate Signup")
    name = st.text_input("Name")
    id_proof = st.text_input("ID Proof")
    field = st.text_input("Field of Specialization")
    if st.button("Signup"):
        register_advocate(name, id_proof, field)
        st.success("Advocate Registered")
        st.info("Admin will review your registration")

# Advocate Login
elif choice == "Advocate Login":
    st.subheader("Advocate Login")
    name = st.text_input("Name")
    id_proof = st.text_input("ID Proof", type='password')
    if st.button("Login"):
        if authenticate_user(name, id_proof, 'Advocate'):
            st.session_state['logged_in'] = True
            st.session_state['role'] = 'Advocate'
            st.session_state['username'] = name
            st.success(f"Logged in as Advocate {name}")
            st.experimental_rerun()

# Logout option
if choice == "Logout":
    st.session_state['logged_in'] = False
    st.session_state['role'] = None
    st.session_state['username'] = None
    st.experimental_rerun()  # This will refresh the page and take the user to the login menu

# Close the connection
conn.close()
