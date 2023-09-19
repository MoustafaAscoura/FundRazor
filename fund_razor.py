from classes import User
from getpass import getpass
import re

curruser = None

def get_valid_mail():
    email = input("Email: ")
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        print ("Invalid Email Form. Try Again!")
        return get_valid_mail()
    
    elif email in User.users.keys():
        print ("Email Already Exists. Try Again!")
        return get_valid_mail()
    
    else:
        return email

def get_valid_password():
    password = getpass("Password: ")

    if len(password) < 8 or len(list(filter(lambda x: x.isalpha(), password))) in [0,len(password)]:
        print("Password must be longer than 8 chars and must be mix of chars and numbers!")
        return get_valid_password()
    
    cpassword = getpass("Confirm Password: ")
    if password != cpassword:
        print("Non matching passwords")
        return get_valid_password()
    
    return password

def get_valid_phone():
    phone = input("Phone: ")
    if not re.fullmatch(r'^01[0125]{1}\d{8}$', phone):
        print ("Invalid phone number. Try Again!")
        return get_valid_phone()
    
    elif phone in [user.phone for user in User.users.values()]:
        print ("Phone Already Exists. Try Again!")
        return get_valid_phone()
    
    else:
        return phone

def signup():
    fname = input("First Name: ")
    while not fname.isalpha():
        fname = input("Name must be chars only!\nFirst Name: ")

    lname = input("Last Name: ")
    while not lname.isalpha():
        lname = input("Name must be chars only!\nLast Name: ")

    phone = get_valid_phone()

    email = get_valid_mail()    
    password = get_valid_password()    

    curruser =  User(fname, lname ,email, phone)
    curruser.password = curruser.encrypt_pass(password)

    print(f"Account created successfully! You are now logged in as {fname} {lname}")
    User.save()
    return curruser

def login():
    global curruser
    email = input("Email: ")
    
    if email in User.users.keys():
        curruser = User.users[email]
        curruser.login()
        return curruser


    option = input("email not found! would you like to (1) try again (2) main menu? ")
    while option not in ["1","2"]:
        option = input("invalid choice! (1) reenter email (2) main menu ")

    if option == "1": return login()
    else: return authenticate()
    
def authenticate():
    option=input("Welcome to Fund Razor! You tell and we Raise!\nChoose an option:\nSign up (1) or Log in (2): ")
    if option=="1": return signup()
    elif option=="2": return login()
    else:
        print("Invalid option! Try again")
        return authenticate()

def main():
    curruser = authenticate()
    print("Greetings,\nChoose an option:")
    while True:
        prompt = input("1) Create a new project\n2) View all projects\n\
3) Edit your projects\n4) Delete a project\n5) Search by Date\n6) sign out\n")
        
        if prompt == "1": curruser.create_project()
        elif prompt == "2": curruser.view_projects()
        elif prompt == "3": curruser.edit_project()
        elif prompt == "4": curruser.delete_project()
        elif prompt == "5": curruser.search_by_date()
        elif prompt == "6": break
        else: print('Invalid Choice')
    
    main()

if __name__=="__main__":
    try: User.load()
    except: pass

    main()