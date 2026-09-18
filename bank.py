import smtplib
import ssl
import random

def send_otp_email(receiver_email):
    otp = str(random.randint(100000, 999999))  # 6-digit OTP

    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "hardik.bankotp@gmail.com"
    password = "vuglrlhumcyxenuk"

    message = f"""\
Subject: Your HSP Bank OTP

Your OTP for login is: {otp}
Please do not share it with anyone."""

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        print(f"✅ OTP sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending OTP: {e}")

    return otp

from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["banking_system"]
users_collection = db["users"]

# Add a new user to MongoDB
def add_new_user():

    firstname = input("Enter First Name: ").strip().lower()
    lastname = input("Enter Last Name: ").strip()
    email = input("Enter Email: ").strip().lower()
    pin = input("Enter 4-digit PIN: ").strip()

    # Check PIN
    if len(pin) != 4 or not pin.isdigit():
        print("PIN must be exactly 4 numbers.\n")
        return

    new_user = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "Account Balance": 0.0,
        "Pin": int(pin)
    }

    users_collection.insert_one(new_user)

    print("New user added successfully.\n")

# Show balance
def show_balance(username):
    user = users_collection.find_one({"firstname": username})
    if user:
        print(f"\nYour Current Balance is: {user['Account Balance']}\n")
    else:
        print("User not found.")

# Withdraw
def withdraw(username):
    user = users_collection.find_one({"firstname": username})
    if user:
        try:
            amount = float(input("Enter amount to withdraw: "))
            if amount > user["Account Balance"]:
                print("Insufficient funds.\n")
            else:
                users_collection.update_one(
                    {"firstname": username},
                    {"$inc": {"Account Balance": -amount}}
                )
                print("Withdrawal successful.\n")
        except ValueError:
            print("Please enter a valid amount.\n")
    else:
        print("User not found.\n")

# Deposit
def deposit(username):
    user = users_collection.find_one({"firstname": username})
    if user:
        try:
            amount = float(input("Enter amount to deposit: "))
            if amount < 0:
                print("Enter a valid amount.\n")
            else:
                users_collection.update_one(
                    {"firstname": username},
                    {"$inc": {"Account Balance": amount}}
                )
                print("Deposit successful.\n")
        except ValueError:
            print("Please enter a valid amount.\n")
    else:
        print("User not found.\n")

# User login
def user_login():
    attempts = 0
    while attempts < 3:
        print("\nWELCOME TO HSP BANK")
        username = input("Enter Your Name To Login: ").strip().lower()
        user = users_collection.find_one({"firstname": username})

        if user:
            try:
                pin_input = int(input("Enter Your 4-digit PIN: "))
            except ValueError:
                print("Invalid PIN format. Enter numbers only.")
                attempts += 1
                continue



            if user["Pin"] == pin_input:

                otp_sent = send_otp_email(user["email"])
                otp_input = input("Enter the OTP sent to your email: ").strip()

                if otp_input == otp_sent:
                    print(f"\n✅ WELCOME {username.upper()}\n")
                    return username
                else:
                    print(" Incorrect OTP.\n")
                    attempts += 1
            else:
                attempts += 1
                print(f" Incorrect PIN. Attempts left: {3 - attempts}\n")
        else:
            choice = input("User does not exist.\nPress 1 to add user or any other key to exit: ")
            if choice == "1":
                add_new_user()
            else:
                return None
    print(" Too many failed attempts. Exiting.")
    return None

# Main menu
def main():
    while True:
        username = user_login()
        if username is None:
            print("Exiting... Thank you!")
            break

        while True:
            print("******************************")
            print("* WELCOME TO HSP BANK")
            print("* 1: Show Balance")
            print("* 2: Withdraw")
            print("* 3: Deposit")
            print("* 4: Logout")
            print("******************************")
            choice = input("Enter Your Choice: ").strip()

            if choice == "1":
                show_balance(username)
            elif choice == "2":
                withdraw(username)
            elif choice == "3":
                deposit(username)
            elif choice == "4":
                print(f"Goodbye, {username.upper()}!\n")
                break
            else:
                print("Invalid input.\n")

# Run the program
main()
