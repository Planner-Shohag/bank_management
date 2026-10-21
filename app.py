
import json
import random as rd
from pathlib import Path

import streamlit as st



DATABASE = Path(__file__).parent / "bankdata.json"


def load_data():
    if not DATABASE.exists():
        DATABASE.write_text("[]", encoding="utf-8")
        return []

    try:
        return json.loads(DATABASE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        st.error("Database file cannot be read.")
        st.stop()


def save_data():
    DATABASE.write_text(
        json.dumps(Bank.data, indent=4),
        encoding="utf-8"
    )




class Bank:
    data = load_data()

    @classmethod
    def update(cls):
        save_data()

    @classmethod
    def find_account(cls, acc_no):
        for user in cls.data:
            if str(user["Account no"]) == str(acc_no):
                return user
        return None

    @classmethod
    def accgen(cls):
        while True:
            acc = rd.randint(10000000, 99999999)
            if cls.find_account(acc) is None:
                return acc




st.set_page_config(
    page_title="OOP Bank System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 OOP Bank Management System")
st.caption("Python OOP + Streamlit + JSON Database")

menu = st.sidebar.selectbox(
    "Select an Operation",
    [
        "Home",
        "Check Balance",
        "Deposit",
        "Withdraw",
        "Create Account",
        "Delete Account"
    ]
)




if menu == "Home":
    st.subheader("Welcome to Your Bank")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Accounts", len(Bank.data))

    with col2:
        total_balance = sum(
            user["Balance"] for user in Bank.data
        )
        st.metric("Total Deposits (BDT)", f"{total_balance:,}")

    st.info(
        "Select an operation from the sidebar "
        "to manage your bank account."
    )




elif menu == "Check Balance":
    st.subheader("Check Account Balance")

    with st.form("balance_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        submitted = st.form_submit_button("Check Balance")

    if submitted:
        user = Bank.find_account(acc)

        if user is None:
            st.error("Invalid account number.")
        elif str(user["Pin"]) != pin:
            st.error("Invalid PIN.")
        else:
            st.success("Account verified.")
            st.metric(
                "Available Balance",
                f"৳ {user['Balance']:,}"
            )




elif menu == "Deposit":
    st.subheader("Deposit Money")

    with st.form("deposit_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input(
            "Deposit Amount (BDT)",
            min_value=1,
            step=100
        )
        submitted = st.form_submit_button("Deposit")

    if submitted:
        user = Bank.find_account(acc)

        if user is None:
            st.error("Invalid account number.")
        elif str(user["Pin"]) != pin:
            st.error("Invalid PIN.")
        else:
            user["Balance"] += amount
            Bank.update()

            st.success(f"Deposit successful: ৳ {amount:,}")
            st.metric("New Balance", f"৳ {user['Balance']:,}")




elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    with st.form("withdraw_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        amount = st.number_input(
            "Withdrawal Amount (BDT)",
            min_value=1,
            step=100
        )
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        user = Bank.find_account(acc)

        if user is None:
            st.error("Invalid account number.")
        elif str(user["Pin"]) != pin:
            st.error("Invalid PIN.")
        elif amount > user["Balance"]:
            st.error("Insufficient balance.")
        else:
            user["Balance"] -= amount
            Bank.update()

            st.success(f"Withdrawal successful: ৳ {amount:,}")
            st.metric(
                "Remaining Balance",
                f"৳ {user['Balance']:,}"
            )




elif menu == "Create Account":
    st.subheader("Create a New Account")

    with st.form("create_form"):
        name = st.text_input("Full Name")
        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            step=1
        )
        pin = st.text_input(
            "Create a 4-digit PIN",
            type="password",
            max_chars=4
        )
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif age < 18:
            st.error("You must be at least 18 years old.")
        elif len(pin) != 4 or not pin.isdigit():
            st.error("PIN must contain exactly 4 digits.")
        else:
            acc = Bank.accgen()

            user_data = {
                "name": name.strip(),
                "Age": int(age),
                "Pin": int(pin),
                "Account no": acc,
                "Balance": 0
            }

            Bank.data.append(user_data)
            Bank.update()

            st.success("Account created successfully!")
            st.write("Account Holder:", name.strip())
            st.write("Account Number:", acc)
            st.write("Initial Balance: ৳ 0")
            st.warning("Remember your account number and PIN.")




elif menu == "Delete Account":
    st.subheader("Delete an Account")

    st.warning(
        "Deleting an account permanently removes it "
        "from this JSON database."
    )

    with st.form("delete_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password")
        confirm = st.checkbox("I confirm account deletion")
        submitted = st.form_submit_button("Delete Account")

    if submitted:
        user = Bank.find_account(acc)

        if user is None:
            st.error("Invalid account number.")
        elif str(user["Pin"]) != pin:
            st.error("Invalid PIN.")
        elif not confirm:
            st.error("Please confirm before deleting.")
        else:
            Bank.data.remove(user)
            Bank.update()
            st.success("Account deleted successfully.")
