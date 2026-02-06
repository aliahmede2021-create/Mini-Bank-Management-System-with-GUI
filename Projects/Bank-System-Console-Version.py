import os
import hashlib
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
  log_entry = (f'''
               Account ID: {account_id} |
               Type: {transaction_type} | 
               Amount: {amount} | 
               Old Balance: {old_balance} | 
               New Balance: {new_balance} | 
               Timestamp: {timestamp}\n''')
  try:
    with open("transactions.txt", "a") as f:
      f.write(log_entry)
  except Exception as e:
    print(f"{'Failed to log transaction :(':>40}", e)

def createAccount(id, name, gender, balance, password):
  try:
    with open("client.txt", "a") as f:
      f.write(str(id)+"\n")
      f.write(name+"\n")
      f.write(gender+"\n")
      f.write(str(balance)+"\n")
      f.write(cryptPassword(password)+"\n")
      print(f"\n{'SAVED SUCCESSFULLY :)':>37}")
  except Exception as e:
    print(f"{'NOT SAVED :(':>27}", e)

def showAccountDetails():
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  with open("client.txt", "r") as f:
    while True:
      account = readLineFunction(f)
      if account is None:
        break
      print(f"\n{'='*39:>47}")
      print(f"{'ID':>18}: {account['id']}")
      print(f"{'Name':>20}: {account['name']}")
      print(f"{'Gender':>22}: {account['gender']}")
      print(f"{'Balance':>23}: {account['balance']}")
    print(f"{'='*39:>47}")

def updateAccount(id, password):
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  try:
    with open("client.txt", "r") as f, open("temp.txt", "w") as temp:    
      updated = False
      while True:
        account = readLineFunction(f)
        if account is None:
          break

        if account["id"] == str(id):
          if account["password"] == cryptPassword(password):
            updated = True
            ID = int(input(f"\n{'Enter your new ID:':>34} "))
            Name = input(f"{'Enter your new Name:':>36} ")
            Gender = input(f"{'Enter your new Gender:':>38} ")
            Balance = float(input(f"{'Enter your new Balance:':>39} "))
            Password = input(f"{'Set your new password:':>38} ")
            new_account = {
              "id": str(ID),
              "name": Name,
              "gender": Gender,
              "balance": str(Balance),
              "password": cryptPassword(Password)
            }
            writeRecord(temp, new_account)
          else:
            writeRecord(temp, account)
            print(f"{'Password Incorrect :(':>35}")
        else:
            writeRecord(temp, account)

    os.remove("client.txt")
    os.rename("temp.txt", "client.txt")

    if updated:
      print(f"{'Account Updated Successfully :)':>45}")
    else:
      print(f"{'Account Not Updated :(':>36}")
  except Exception as e:
    print(f"{'Update Unsuccessful :(':>36}", e)

def deposit(id, password, amount):
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  try:
    with  open("client.txt", "r") as f,  open("temp.txt", "w") as temp:
    
      found = False
      while True:
        account = readLineFunction(f)
        if account is None:
          break

        if account["id"] == str(id):
          found = True
          if account["password"] == cryptPassword(password):
            new_balance = float(account["balance"]) + amount
            account["balance"] = str(new_balance)
            writeRecord(temp, account)
            log_transaction(account["id"], "Deposit", amount, float(account["balance"]) - amount, new_balance)
            print(f"{'Deposit successful :) ! New balance':>51}: {new_balance}")
          else:
            writeRecord(temp, account)
            print(f"{'Password Incorrect :(':>38}")
        else:
            writeRecord(temp, account)

    os.remove("client.txt")
    os.rename("temp.txt", "client.txt")

    if not found:
      print(f"{'Account not found :(':>34}")

  except Exception as e:
    print(f"{'Deposit Unsuccessful :(':>38}", e)

def withdrawal(id, password, amount):
    if not os.path.exists("client.txt"):
      print("No accounts found :(")
      return

    try:
      with open("client.txt", "r") as f, open("temp.txt", "w") as temp:
        found = False
        while True:
          account = readLineFunction(f)
          if account is None:
            break

          if account["id"] == str(id):
            found = True
            if account["password"] == cryptPassword(password):
              if float (account["balance"]) >= amount:
                new_balance = float(account["balance"]) - amount
                account["balance"] = str(new_balance)
                writeRecord(temp, account)
                log_transaction(account["id"], "Withdrawal", amount, float(account["balance"]) + amount, new_balance)
                print(f"{'Withdrawal successful :) ! New balance':>54}: {new_balance}")
              else:
                writeRecord(temp, account)
                print(f"{'Insufficient balance :(':>35}")
              
            else:
              writeRecord(temp, account)
              print(f"{'Password Incorrect :(':>38}")
          else:
            writeRecord(temp, account)

      os.remove("client.txt")
      os.rename("temp.txt", "client.txt")

      if not found:
        print(f"{'Account not found :(':>34}")

    except Exception as e:
      print(f"{'Withdrawal Unsuccessful :(':>35}", e)

def searchForAccount(id, password):
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  try:
    with open("client.txt", "r") as f:
      found = False
      while True:
        account = readLineFunction(f)
        if account is None:
          break

        if account["id"] == str(id):
          found = True
          if account["password"] == cryptPassword(password):
            print(f"{'Account found successfully :)':>43}")
            print(f"{'Name':>18} : {account['name']}")
            print(f"{'Gender':>20} : {account['gender']}")
            print(f"{'Balance':>21} : {account['balance']}")
          else:
            print(f"{'Password Incorrect :(':>35}")
            break

    if not found:
      print(f"{'Account not found':>31}")

  except Exception as e:
    print(f"{'Search Unsuccessful :(':>35}", e)

def deleteAccount(id, password):
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  
  try:
    with open("client.txt", "r") as f, open("temp.txt", "w") as temp:
      deleted = False
      while True:
        account = readLineFunction(f)
        if account is None:
          break

        if account["id"] == str(id):
          if account["password"] == cryptPassword(password):
            deleted = True
          else:
            writeRecord(temp, account)
            print(f"{'Password Incorrect :(':>35}")
        else:
            writeRecord(temp, account)
      
    os.remove("client.txt")
    os.rename("temp.txt", "client.txt")

    if deleted == True:
      print(f"{'Account deleted successfully :)':>45}")

  except Exception as e:
    print(f"{'Deletion Unsuccessful :(':>35}", e)

def viewTransactionHistory():
  if not os.path.exists("client.txt"):
    print("No accounts found :(")
    return
  try:
    print(f"{'='*39:>47}")
    print(f"{'Transaction History':>35}")
    print(f"{'='*39:>47}")

    with open("transactions.txt", "r") as f:
      transactions = f.readlines()
    if not transactions:
      print(f"{'No transactions found :(':>40}")
      return
    else:
      user_transactions = [t for t in transactions if f"Account ID: {current_user['id']}" in t]
      
      if not user_transactions:
          print(f"{'No transactions for your account.':>53}")
      else:
          for trans in user_transactions[-10:]:  # Show last 10 transactions
              print(f"{trans.strip():>90}")
    print(f"{'='*39:>47}")
  except Exception as e:
      print(f"{'Failed to read transaction history :(':>53}", e)

while(True):
  if current_user is None:
    try:
      choice = int(input('''
                      MESA VERDE
                    BANK AND TRUST
          =======================================                       
                  1) Login to your Account
                  2) Create an Account
                  3) Exit                             
          =======================================
                  Enter your choice: '''))
    except Exception as e:
      print(f"{'='*39:>47}")
      print(f"{'Invalid choice! Please enter numbers only :(':>55}", e)
      print(f"{'='*39:>47}")
      continue
    match choice:
      case 1:
        try:
          ID = int(input(f"\n{'Enter your ID:':>30} "))
        except Exception as e:
          print(f"{'Invalid ID! Please enter numbers only :(':>48}", e)
          continue
        Password = input(f"{'Enter your account password:':>44} ")
        account = login(ID, Password)
        if account:
          current_user = account
          print(f"\n{'Login Successful! Welcome, ' + current_user['name'] + ' :)':>47}")
        else:
          print(f"\n{'Login Failed! Invalid ID or Password :(':>61}")
      case 2:
        print(f"{'='*39:>47}")

        while True:
          try:
              print(f"\n{'='*39:>47}")
              ID = int(input(f"{'Enter your ID:':>30} "))

              duplicate = False
              if os.path.exists("client.txt"):
                f = open("client.txt", "r")
                while True:
                  account = readLineFunction(f)
                  if account is None:
                    break
                  if account["id"] == str(ID):
                    duplicate = True
                    break
                f.close()

              if duplicate == True:
                print(f"{'Error: Account with this ID already exists :)':>55}")
              else:
                break

          except Exception as e:
              print(f"{'Invalid ID! Please enter numbers only :(':>51}", e)

        while True:
          Name = input(f"{'Enter your Name:':>32} ")
          if Name == "":
            print(f"{'Invalid Name! Please enter a valid name :(':>55}")
            print(f"\n{'='*39:>47}")
          else:
            break

        while True:
          Gender = input(f"{'Enter your Gender:':>34} ")
          if Gender.lower() in ["male", "female", "m", "f"]:
            break
          else:
            print(f"{'Invalid Gender! Please enter Male or Female only :(':>65}")
            print(f"\n{'='*39:>47}")

        while True:
          try:
            Balance = float(input(f"{'How much money you want to save?':>48} "))
            if Balance <=0:
              print(f"{'Invalid Amount :(':>35}")
              print(f"\n{'='*39:>47}")
            else:
              break
          except Exception as e:
            print(f"{'Invalid Amount! Please enter numbers only :(':>58}", e)
          
        Password = input(f"{'Set your account password:':>42} ")
        createAccount(ID, Name, Gender, Balance, Password)
        print(f"\n{'='*39:>47}")
      case 3:
        print(f"{'='*39:>47}")
        print(f"{'Program Terminated! Goodbye :)':>46}")
        break
      case _:
        print(f"{'='*39:>47}")
        print(f"{'Error! Try Again':>30}")
        print(f"{'='*39:>47}")
  else:
    try:
      choice = int(input(f'''
                      MESA VERDE
                    BANK AND TRUST
          ======================================= 
                    !Welcome, {current_user['name']}!
          =======================================                       
                  1) Show Account Details
                  2) Deposit Money
                  3) Withdraw Money
                  4) Update Account
                  5) Search for an Account
                  6) Delete Account
                  7) View Transaction History
                  8) Logout                      
          =======================================
                  Enter your choice: '''))
    except Exception as e:
      print(f"{'='*39:>47}")
      print(f"{'Invalid choice! Please enter numbers only :(':>55}", e)
      print(f"{'='*39:>47}")
      continue
        
    match choice:
      case 1:
        print(f"{'='*39:>47}")
        showAccountDetails()
        print(f"{'='*39:>47}")
      case 2:
        print(f"{'='*39:>47}")
        while True:
          try:
            Amount = float(input(f"{'Enter the amount you want to deposit:':>53} "))
            if Amount <= 0:
              print(f"{'Invalid Amount :(':>35}")
              print(f"{'='*39:>47}")
            else:
              deposit(current_user["id"], raw_password, Amount)
              print(f"{'='*39:>47}")
              break
          except Exception as e:
            print(f"{'Invalid Amount! Please enter numbers only :(':>58}", e)
            print(f"{'='*39:>47}")
      case 3:
        print(f"{'='*39:>47}")
        while True:
          try:
            Amount = float(input(f"{'Enter the amount you want to withdraw:':>54} "))
            if Amount <= 0:
              print(f"{'Invalid Amount :(':>35}")
              print(f"{'='*39:>47}")
            else:
              withdrawal(current_user["id"], raw_password, Amount)
              print(f"{'='*39:>47}")
              break
          except Exception as e:
            print(f"{'Invalid Amount! Please enter numbers only :(':>58}", e)
            print(f"{'='*39:>47}")
      case 4:
        print(f"{'='*39:>47}")
        updateAccount(current_user["id"], raw_password)
        print(f"{'='*39:>47}")   
      case 5:
        print(f"{'='*39:>47}")
        while True:
          try:
            ID = int(input(f"\n{'Enter the ID of the account to search:':>47} "))
            break
          except Exception as e:
            print(f"{'Invalid ID! Please enter numbers only :(':>48}", e)
        Password = input(f"{'Enter the account password:':>42} ")
        searchForAccount(ID, Password)
        print(f"{'='*39:>47}")
      case 6:
        print(f"{'='*39:>47}")
        deleteAccount(current_user["id"], raw_password)
        current_user = None
        raw_password = None
        print(f"{'='*39:>47}")
      case 7:
        print(f"{'='*39:>47}")
        viewTransactionHistory()
        print(f"{'='*39:>47}")
      case 8:
        print(f"{'='*39:>47}")
        print(f"{'You have been logged out. :)':>44}")
        current_user = None
        raw_password = None
        print(f"{'='*39:>47}")
      case _:
        print(f"{'='*39:>47}")
        print(f"{'Error! Try Again':>30}")
        print(f"{'='*39:>47}")