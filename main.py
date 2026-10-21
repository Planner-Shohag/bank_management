# bank oop project
import json
from pathlib import Path
import random as rd

class Bank():
    database = "bankdata.json"
    data = []
    with open(database) as fs:
        data = json.loads(fs.read())
    @classmethod
    def update(cls):
        with open(cls.database,"w") as fs:
            fs.write(json.dumps(Bank.data))
    def accgen(self):
        acc = int(rd.randint(10000000,99999999))
        return acc

    
    def find_account(self, acc_no):
        for user in Bank.data:
            if user["Account no"] == acc_no:
                return user
        return None




    def __init__(self):
        
      
        print("""
            Enter 1 to check balance
            Enter 2 to deposit
            Enter 3 to withdraw 
            Enter 4 to create account
            Enter 5 to Delete account
            Enter 6 to exit
""")
        self.user_input()

    def user_input(self):
        
        accept = int(input("Press a number between 1 to 6:- "))
        if accept == 1:
            self.chck_balance()
        elif accept == 2:
            self.dep()
        elif accept == 3:
            self.withdraw()
        elif accept == 4:
            self.createacc()
        elif accept == 5:
            self.deleteacc()
        elif accept == 6:
            print("BYE")
            
        else:
            print("Invalid input")

   
    def chck_balance(self):
        account = int(input("Enter your account number:-"))
        user = self.find_account(account)

        if user is None:
            print("Invalid account number")
            return
            
        pin = int(input("Enter your PIN: "))

        if pin == user["Pin"]:
            print(f"Your balance is {user['Balance']} BDT")
      
            

    def dep(self):
        account = int(input("Enter your account number:-"))
        user = self.find_account(account)
        if user is None:
            print("Invalid account number")
            return
        pin = int(input("Enter your PIN: "))

        if pin == user["Pin"]:
            amount = int(input("How much do you want to deposit: "))

            if amount <= 0:
                print("Enter a valid amount")
                return

            user["Balance"] += amount
            Bank.update()

            print(f"Deposit successful. Balance: {user['Balance']} BDT")
        else:
            print("Invalid PIN")

    def withdraw(self):
        account = int(input("Enter your account no: "))
        user = self.find_account(account)

        if user is None:
            print("Invalid account no")
            return

        pin = int(input("Enter your PIN: "))

        if pin == user["Pin"]:
            amount = int(input("How much do you want to withdraw: "))

            if amount <= 0:
                print("Enter a valid amount")
            elif amount > user["Balance"]:
                print("Insufficient balance")
            else:
                user["Balance"] -= amount
                Bank.update()

                print(f"Withdrawal successful. Remaining balance: {user['Balance']} BDT")
        else:
            print("Invalid PIN")


    def createacc(self):
        user_data = {
            "name" : input("Enter your name: "),
            "Age" : int(input("Enter your age: ")),
            "Pin" : int(input("Enter your 4 digit pin:")),
            "Account no" : self.accgen(),
            "Balance" : 0,

        }

        if user_data["Age"] < 18:
            print("You can't open acount")
        else:
            print("Account created successfully")
            for i in user_data:
                print(f"{i} : {user_data[i]}\n Remember your account no. and pin")
            Bank.data.append(user_data)
            Bank.update()
        

    def deleteacc(self):
        again = int(input("Enter your Account no: "))
        for i in Bank.data:
            if again == i["Account no"]:
                b = int(input("Enter your pin: "))
                if b == i["Pin"]:
                    Bank.data.remove(i)
                    Bank.update()
                    print("Account deleted successfully")
        
            
                else:
                    print("Wrong Pin")
                return
        else:
            print("Invllid Account no")

bank_user = Bank()   

         
         




