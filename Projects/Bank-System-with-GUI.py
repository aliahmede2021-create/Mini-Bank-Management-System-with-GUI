import os
import hashlib
from PIL import Image, ImageTk
import tkinter as tk
import random
from tkinter import messagebox
from datetime import datetime

current_user = None
raw_password = None

def cryptPassword(password):
  return hashlib.sha256(password.encode()).hexdigest()

def readLineFunction(f):
    id_line = f.readline()
    if not id_line:
        return None

    name_line = f.readline()
    gender_line = f.readline()
    balance_line = f.readline()
    password_line = f.readline()

    if not (name_line and gender_line and balance_line and password_line):
        return None

    return {
        "id": id_line.strip(),
        "name": name_line.strip(),
        "gender": gender_line.strip(),
        "balance": balance_line.strip(),
        "password": password_line.strip()
    }

def writeRecord(file, account):
  file.write(account["id"] + "\n")
  file.write(account["name"] + "\n")
  file.write(account["gender"]  + "\n")
  file.write(account["balance"] + "\n")
  file.write(account["password"] + "\n")

def login(id, password):
  global current_user, raw_password
  if not os.path.exists("client.txt"):
    return False
  with open("client.txt", "r") as f:
    while True:
      account = readLineFunction(f)
      if account is None:
        break
      if account["id"] == str(id) and account["password"] == cryptPassword(password):
        current_user = account
        raw_password = password
        return current_user
  current_user = None
  raw_password = None
  return current_user

def log_transaction(account_id, transaction_type, amount, old_balance, new_balance):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  log_entry = (f"Account ID: {account_id} | "
               f"Type: {transaction_type} | "
               f"Amount: {amount} | "
               f"Old Balance: {old_balance} | "
               f"New Balance: {new_balance} | "
               f"Timestamp: {timestamp}")
  try:
    with open("transactions.txt", "a") as f:
      f.write(log_entry + "\n")
  except Exception as e:
    print(f"{'Failed to log transaction :(':>40}", e)

def createAccount(id, name, gender, balance, password):
  with open("client.txt", "a") as f:
    f.write(str(id)+"\n")
    f.write(name+"\n")
    f.write(gender+"\n")
    f.write(str(balance)+"\n")
    f.write(cryptPassword(password)+"\n")

def updateAccount(id, password, new_id, new_name, new_gender, new_balance, new_password):
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  with open("client.txt", "r") as f, open("temp.txt", "w") as temp:    
    while True:
      account = readLineFunction(f)
      if account is None:
        break

      if account["id"] == str(id) and account["password"] == cryptPassword(password):
        new_account = {
          "id": str(new_id),
          "name": new_name,
          "gender": new_gender,
          "balance": str(new_balance),
          "password": cryptPassword(new_password)
        }

        global current_user, raw_password
        current_user = new_account
        raw_password = new_password

    writeRecord(temp, new_account)

  os.remove("client.txt")
  os.rename("temp.txt", "client.txt")

def deposit(id, password, amount):
  global current_user

  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  with  open("client.txt", "r") as f,  open("temp.txt", "w") as temp:
    while True:
      account = readLineFunction(f)
      if account is None:
        break

      if account["id"] == str(id) and account["password"] == cryptPassword(password):
        old_balance = float(account["balance"])
        new_balance = float(account["balance"]) + amount
        account["balance"] = str(new_balance)

        if current_user and current_user["id"] == account["id"]:
          current_user["balance"] = str(new_balance)
        log_transaction(account["id"], "Deposit", amount, old_balance, new_balance)

      writeRecord(temp, account)

  os.remove("client.txt")
  os.rename("temp.txt", "client.txt")

def withdrawal(id, password, amount):
    global current_user

    if not os.path.exists("client.txt"):
      print("No accounts found :(")
      return

    with open("client.txt", "r") as f, open("temp.txt", "w") as temp:
      while True:
        account = readLineFunction(f)
        if account is None:
          break

        if account["id"] == str(id) and account["password"] == cryptPassword(password):
            old_balance = float(account["balance"])
            if old_balance>= amount:
              new_balance = old_balance - amount
              account["balance"] = str(new_balance)
              
              if current_user and current_user["id"] == account["id"]:
                current_user["balance"] = str(new_balance)
              log_transaction(account["id"], "Withdrawal", amount, old_balance, new_balance)
            else:
              messagebox.showerror("Error", "Insufficient funds for this withdrawal.")

        writeRecord(temp, account)

    os.remove("client.txt")
    os.rename("temp.txt", "client.txt")

def searchForAccount(id, password):
  if not os.path.exists("client.txt"):
    return
  
  with open("client.txt", "r") as f:
    while True:
      account = readLineFunction(f)
      if account is None:
        break

      if account["id"] == str(id) and account["password"] == cryptPassword(password):
          print(f"{'Account found successfully :)':>43}")
          print(f"{'Name':>18} : {account['name']}")
          print(f"{'Gender':>20} : {account['gender']}")
          print(f"{'Balance':>21} : {account['balance']}")
          return account

def deleteAccount(id, password):
  if not os.path.exists("client.txt"):
     return

  with open("client.txt", "r") as f, open("temp.txt", "w") as temp:
    while True:
      account = readLineFunction(f)
      if account is None:
        break

      if not (account["id"] == str(id) and account["password"] == cryptPassword(password)):
          writeRecord(temp, account)
    
  os.remove("client.txt")
  os.rename("temp.txt", "client.txt")

def accountExists(id):
    if not os.path.exists("client.txt"):
      return False
    with open("client.txt", "r") as f:
      while True:
        account = readLineFunction(f)
        if account is None:
            break
        if account["id"] == id:
            return True
    return False

def generateRandomPassword(user_choice):
   characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
   password = ""
   for i in range(user_choice):
      password += random.choice(characters)
   return password

root = tk.Tk()
root.withdraw() 

def guiCreateAccount():
    createAccount_window = tk.Toplevel()
    createAccount_window.title("Create New Account")
    createAccount_window.geometry("450x450")
    tk.Label(createAccount_window, text="Create a New Account", font=("Helvetica", 14, "bold")).pack(pady=10)

    tk.Label(createAccount_window, text="ID:").pack()
    create_id_entry = tk.Entry(createAccount_window)
    create_id_entry.pack()

    tk.Label(createAccount_window, text="Name:").pack()
    create_name_entry = tk.Entry(createAccount_window)
    create_name_entry.pack()

    tk.Label(createAccount_window, text="Gender:").pack()
    create_gender_entry = tk.Entry(createAccount_window)
    create_gender_entry.pack()

    tk.Label(createAccount_window, text="Balance:").pack()
    create_balance_entry = tk.Entry(createAccount_window)
    create_balance_entry.pack()    

    tk.Label(createAccount_window, text="Password:").pack()
    create_password_entry = tk.Entry(createAccount_window, show="*")
    create_password_entry.pack()
    
    tk.Label(createAccount_window, text="Enter the desired password length (minimum 8 characters):").pack()
    password_length_entry = tk.Entry(createAccount_window)
    password_length_entry.pack()

    generated_password_label = tk.Label(createAccount_window, text="")
    generated_password_label.pack(pady=5)

    def generateAndFillPassword():
       try:
          length = int(password_length_entry.get())
          if length < 8:
             messagebox.showerror("Error", "Password length must be at least 8 characters.")
             return
          if length >= 50:
             messagebox.showerror("Error", "Password length must be less than or equal to 50 characters.")
             return
          
          generated_password = generateRandomPassword(length)
          create_password_entry.delete(0, tk.END)
          create_password_entry.insert(0, generated_password)

          generated_password_label.config(text=f"Generated Password: {generated_password}")
       except ValueError:
          messagebox.showerror("Error", "Please enter a valid number for password length.")

    tk.Button(createAccount_window, text="Generate Random Password", command=generateAndFillPassword).pack(pady=5)

    def toCreateAccount():
       try:
          create_id = int(create_id_entry.get())
          create_name = create_name_entry.get()
          create_gender = create_gender_entry.get()
          create_balance = float(create_balance_entry.get())
          create_password = create_password_entry.get()

          if accountExists(create_id_entry.get()):
            messagebox.showerror("Error", "An account with this ID already exists. Please choose a different ID.")
            return
          
          if not create_name.strip():
            messagebox.showerror("Error", "Name cannot be empty.")
            return
          
          if create_gender.lower() not in ["male", "m", "female", "f"]:
            messagebox.showerror("Error", "Please enter Male or Female for gender.")
            return

          if create_balance <= 0:
            messagebox.showerror("Error", "Balance must be a positive number.")
            return
          
          if not create_password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return
          
          if len(create_password) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long.")
            return

          createAccount(create_id, create_name, create_gender, create_balance, create_password)
          messagebox.showinfo("Success", "Account created successfully!")
          createAccount_window.destroy()
          showLoginScreen()
       except ValueError:
          messagebox.showerror("Error", "Please enter valid input for ID and Balance")
    tk.Button(createAccount_window, text="Create Account", command=toCreateAccount, bg="green", fg="white").pack(pady=10)

    tk.Button(createAccount_window, text="Cancel", command=lambda: (createAccount_window.destroy(), showLoginScreen()), bg="red", fg="white").pack()

def showLoginScreen():
    login_window = tk.Toplevel()
    login_window.title("Bank Login")
    login_window.geometry("350x400")

    global logo
    logo_img = Image.open("Projects/images/Logo.jpg")
    logo_img = logo_img.resize((150, 150))
    logo = ImageTk.PhotoImage(logo_img)

    tk.Label(login_window, image=logo).pack(pady=10)

    tk.Label(login_window, text="MESA VERDE BANK AND TRUST", font=("Helvetica", 12, "bold")).pack(pady=5)
    
    tk.Label(login_window, text="ID:").pack()
    id_entry = tk.Entry(login_window)
    id_entry.pack()
    
    tk.Label(login_window, text="Password:").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()
    
    def try_login():
        try:
            user_id = int(id_entry.get())
            password = password_entry.get()
            account = login(user_id, password)
            
            if account:
                login_window.destroy()
                showMainMenu(account)
            else:
                messagebox.showerror("Login Failed", "Invalid ID or Password")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numeric ID")
    
    tk.Button(login_window, text="Login", command=try_login, bg="blue", fg="white").pack(pady=10)

    tk.Button(login_window, text="Create Account", command=lambda: (login_window.destroy(), guiCreateAccount()), bg="blue", fg="white").pack(pady=10)
    
    tk.Button(login_window, text="Exit", command=login_window.quit, bg="red", fg="white").pack()
    
def showMainMenu(account):
    menu_window = tk.Toplevel()
    menu_window.title(f"Welcome, {current_user['name']}")
    menu_window.geometry("400x550")

    original_bg = Image.open("Projects/images/Logo-4.jpg")
    bg_label = tk.Label(menu_window)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1) 
    bg_label.lower()

    def resizeBg(event):
       if event.widget != menu_window:
          return 
       
       resized = original_bg.resize((event.width, event.height))
       bg_img = ImageTk.PhotoImage(resized)
       bg_label.config(image=bg_img)
       bg_label.image = bg_img

    menu_window.bind("<Configure>", resizeBg)

    welcome_text = f"Welcome, {current_user['name']}!\nBalance: {current_user['balance']}"
    tk.Label(menu_window, text=welcome_text, font=("Helvetica", 12)).pack(pady=10)
    
    def guiShowDetails():
        details_window = tk.Toplevel(menu_window)
        details_window.title("Account Details")
        details_window.geometry("300x200")
        
        tk.Label(details_window, text=f"ID: {current_user['id']}", font=("Helvetica", 11)).pack(pady=5)
        tk.Label(details_window, text=f"Name: {current_user['name']}", font=("Helvetica", 11)).pack(pady=5)
        tk.Label(details_window, text=f"Gender: {current_user['gender']}", font=("Helvetica", 11)).pack(pady=5)
        tk.Label(details_window, text=f"Balance: ${current_user['balance']}", font=("Helvetica", 11)).pack(pady=5)
        tk.Button(details_window, text="Close", command=details_window.destroy).pack()
    
    def guiDeposit():
        deposit_window = tk.Toplevel(menu_window)
        deposit_window.title("Deposit Money")
        deposit_window.geometry("300x150")
        
        tk.Label(deposit_window, text="Enter amount to deposit:").pack(pady=10)
        
        amount_entry = tk.Entry(deposit_window)
        amount_entry.pack()
        
        def doDeposit():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                
                deposit(current_user["id"], raw_password, amount)
                messagebox.showinfo("Success", f"Deposited ${amount:.2f}\nNew balance: ${float(current_user['balance']):.2f}")
                deposit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        tk.Button(deposit_window, text="DEPOSIT", command=doDeposit, bg="green", fg="white").pack(pady=10)
        tk.Button(deposit_window, text="CANCEL", command=deposit_window.destroy).pack()
    
    def guiWithdrawal():
        withdraw_window = tk.Toplevel(menu_window)
        withdraw_window.title("Withdraw Money")
        withdraw_window.geometry("300x150")
        
        tk.Label(withdraw_window, text="Enter amount to withdraw:").pack(pady=10)
        
        amount_entry = tk.Entry(withdraw_window)
        amount_entry.pack()
        
        def doWithdraw():
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("Error", "Amount must be positive")
                    return
                
                withdrawal(current_user["id"], raw_password, amount)
                messagebox.showinfo("Success", f"Withdrew ${amount:.2f}")
                withdraw_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number")
        
        tk.Button(withdraw_window, text="WITHDRAW", command=doWithdraw, bg="orange", fg="white").pack(pady=10)
        tk.Button(withdraw_window, text="CANCEL", command=withdraw_window.destroy).pack()

    def guiUpdateAccount():
       update_window = tk.Toplevel(menu_window)
       update_window.title("Update Account")
       update_window.geometry("350x450")
       
       tk.Label(update_window, text="To update your account details, press 'Update'. To cancel, press 'Cancel'").pack(pady=10)

       tk.Label(update_window, text="Enter new ID").pack()
       new_id_entry = tk.Entry(update_window)
       new_id_entry.pack()

       tk.Label(update_window, text="Enter new Name").pack()
       new_name_entry = tk.Entry(update_window)
       new_name_entry.pack()

       tk.Label(update_window, text="Enter new Gender").pack()
       new_gender_entry = tk.Entry(update_window)
       new_gender_entry.pack()

       tk.Label(update_window, text="Enter new Balance").pack()
       new_balance_entry = tk.Entry(update_window)
       new_balance_entry.pack()

       tk.Label(update_window, text="Enter new Password").pack()
       new_password_entry = tk.Entry(update_window, show="*")
       new_password_entry.pack()

       tk.Label(update_window, text="Enter the desired password length (minimum 8 characters):").pack()
       new_password_length_entry = tk.Entry(update_window)
       new_password_length_entry.pack()

       newly_generated_password_label = tk.Label(update_window, text="")
       newly_generated_password_label.pack(pady=5)   

       def generateAndFillPassword():
        try:
            length = int(new_password_length_entry.get())
            if length < 8:
              messagebox.showerror("Error", "Password length must be at least 8 characters.")
              return
            if length >= 50:
              messagebox.showerror("Error", "Password length must be less than or equal to 50 characters.")
              return
            
            generated_password = generateRandomPassword(length)
            new_password_entry.delete(0, tk.END)
            new_password_entry.insert(0, generated_password)

            newly_generated_password_label.config(text=f"Generated Password: {generated_password}")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for password length.")

       def toUpdateAccount():
         try:
            new_id = int(new_id_entry.get())
            new_name = new_name_entry.get()
            new_gender = new_gender_entry.get()
            new_balance = float(new_balance_entry.get())
            new_password = new_password_entry.get()

            if accountExists(new_id_entry.get()):
              messagebox.showerror("Error", "An account with this ID already exists. Please choose a different ID.")
              return
          
            if not new_name.strip():
              messagebox.showerror("Error", "Name cannot be empty.")
              return
          
            if new_gender.lower() not in ["male", "m", "female", "f"]:
              messagebox.showerror("Error", "Please enter Male or Female for gender.")
              return

            if new_balance <= 0:
              messagebox.showerror("Error", "Balance must be a positive number.")
              return
          
            if not new_password:
              messagebox.showerror("Error", "Password cannot be empty.")
              return
            
            if len(new_password) < 8:
               messagebox.showerror("Error", "Password must be at least 8 characters long.")
               return
         
            updateAccount(current_user["id"], raw_password, new_id, new_name, new_gender, new_balance, new_password)
            messagebox.showinfo("Account Updated", "Your account details have been updated.")
         except ValueError:
            messagebox.showerror("Error", "Please enter valid input for ID and Balance")

       tk.Button(update_window, text="Update", command=toUpdateAccount, bg="blue", fg="white").pack(pady=10)

       tk.Button(update_window, text="Generate Random Password", command=generateAndFillPassword, bg="lightgreen", fg="black").pack(pady=5)

       tk.Button(update_window, text="Cancel", command=update_window.destroy, bg="red", fg="white").pack(pady=10)

    def guiSearch():
       search_window = tk.Toplevel(menu_window)
       search_window.title("Search for an Account")
       search_window.geometry("400x250")

       tk.Label(search_window, text="Enter Account ID to search:").pack(pady=10)

       tk.Label(search_window, text="(You must know the password to view details)").pack(pady=5)

       tk.Label(search_window, text="Account ID:").pack()
       search_id_entry = tk.Entry(search_window)
       search_id_entry.pack()

       tk.Label(search_window, text="Account Password:").pack()
       search_password_entry = tk.Entry(search_window, show="*")
       search_password_entry.pack()

       def doSearch():
          try:
              search_id = int(search_id_entry.get())
              search_password = search_password_entry.get()
              found = searchForAccount(search_id, search_password)

              if found:
                  messagebox.showinfo("Account Found", f"Account ID: {found['id']}\nName: {found['name']}\nGender: {found['gender']}\nBalance: {found['balance']}")
              else:
                  messagebox.showerror("Not Found", "Account not found or incorrect password")
              search_window.destroy()
              menu_window.destroy()
              showMainMenu(account)
              
          except ValueError:
              messagebox.showerror("Error", "Please enter a valid numeric ID")

       tk.Button(search_window, text="SEARCH", command=doSearch, bg="blue", fg="white").pack(pady=10)

       tk.Button(search_window, text="Cancel", command=search_window.destroy, bg="red", fg="white").pack(pady=10)

    
    def guiViewTransactions():
        trans_window = tk.Toplevel(menu_window)
        trans_window.title("Transaction History")
        trans_window.geometry("500x300")
        
        tk.Label(trans_window, text="Your Recent Transactions:", font=("Helvetica", 12, "bold")).pack(pady=10)
        
        text_widget = tk.Text(trans_window, height=10, width=63)
        text_widget.pack(pady=10)
        
        try:
            if os.path.exists("transactions.txt"):
                with open("transactions.txt", "r") as f:
                    transactions = f.readlines()
                    user_transactions = [t for t in transactions if f"Account ID: {current_user['id']} |" in t]
                    
                    if user_transactions:
                        for trans in user_transactions[-10:]:  
                            text_widget.insert(tk.END, trans)
                    else:
                        text_widget.insert(tk.END, "No transactions found.")
            else:
                text_widget.insert(tk.END, "No transaction history.")
        except Exception as e:
            text_widget.insert(tk.END, f"Error: {str(e)}")
        
        text_widget.config(state=tk.DISABLED)  
        
        tk.Button(trans_window, text="Close", command=trans_window.destroy).pack()

    def guiDelete():
       window_delete = tk.Toplevel(menu_window)
       window_delete.title("Delete Account")
       window_delete.geometry("400x150")

       tk.Label(window_delete, text="If you want to delete your account, press 'Yes'. If you don't, press 'No'").pack(pady=10)

       def doDelete():
          window_delete.destroy()
          deleteAccount(current_user["id"], raw_password)
          messagebox.showinfo("Account Deleted", "Your account has been deleted.")
          menu_window.destroy()
          showLoginScreen()

       tk.Button(window_delete, text="YES", command=doDelete, bg="red", fg="white").pack(pady=10)
       tk.Button(window_delete, text="NO", command=window_delete.destroy).pack()

    def guiLogout():
        global current_user, raw_password
        current_user = None
        raw_password = None
        menu_window.destroy()
        showLoginScreen()
    
    buttons = [
        ("Show Account Details", guiShowDetails),
        ("Deposit Money", guiDeposit),
        ("Withdraw Money", guiWithdrawal),
        ("Update Account Details", guiUpdateAccount),
        ("Search for an Account", guiSearch),
        ("View Transaction History", guiViewTransactions),
        ("Delete Account", guiDelete),
        ("Logout", guiLogout)
    ]
    
    for text, command in buttons:
        tk.Button(menu_window, text=text, command=command, width=30).pack(pady=5)
    
if __name__ == "__main__":
    showLoginScreen()
    root.mainloop()