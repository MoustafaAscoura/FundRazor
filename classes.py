from getpass import getpass
from datetime import date
import ast

class User():
    users = {}
    def __init__(self,fname, lname, email, phone, ownprojectsids = []):
        self.fname = fname
        self.lname = lname
        self.email = email
        self.phone = phone
        self.ownprojectsids = ownprojectsids
        self.users[email]=self

    def encrypt_pass(self, password):
        shift = len(self.email)
        newpass = ""
        for char in password:
            newchar = chr(ord(char) + shift)
            newpass += newchar

        return newpass
       
    def login(self):
        password = getpass("Password: ")

        if self.encrypt_pass(password) != self.password:
            print("wrong password! try again")
            self.login()
        
        else:
            print(f"Logged in successfully! Welcome back {self.fname} {self.lname}")
    
    def create_project(self):
        title = input("New Project Title: ")
        while title == "": title = input("Title Cannot be empty!\nProject Title: ")

        details = input("Project details: ")
        target = input("Target Money: ")
        while not target.isnumeric(): target = input("Inavlid number! Target Money: ")

        while True:
            end = input("Project Deadline: ")
            try:
                end = date.fromisoformat(end)
                if end <= date.today():
                    print("Project end must be in the future!")
                    continue
            except:
                print ("Invalid date format, please reenter")
            else:
                break


        id = max(Project.ids) + 1
        self.ownprojectsids.append(id)

        newproject = Project(id, title, details, float(target), end)
        newproject.start = date.today()
        newproject.owner = self.email
        self.save()
        Project.save()
        
    def view_projects(self):
        print("Your Projects are: ")
        for project_id in self.ownprojectsids:
            project = Project.projects[project_id]
            print ( list(project.__dict__.values()))

    def edit_project(self):
        self.view_projects()
        edit_id = input("Enter project id to edit: ")
        if edit_id not in self.ownprojectsids:
            print("Id not found!")
        else:
            project = Project.projects[edit_id]
            while True:
                query = input("Input desired change as attr=newval\nor any val to go back")
                try:
                    attr,newval = query.replace(" ","").split("=")
                except:
                    break
                
                if attr in project.__dir__():
                    try:
                        if attr in ["id", "start", "owner"]:
                            print("This attribute cannot be edited!")
                        elif attr == "target":
                            project.target = float(newval)
                        elif attr == "end":
                            project.end = date.isoformat(newval)
                        else:
                            project.__setattr__(attr,newval)

                    except ValueError:
                        print("New Value is not in the correct format!")

                else:
                    print ("Project has no such attribute!")
        
        Project.save()
   
    def delete_project(self):
        self.view_projects()
        del_id = input("Enter project id to delete: ")
        if int(del_id) not in self.ownprojectsids:
            print("Id not found!")
        else:
            self.ownprojectsids.remove(del_id)
            del Project.projects[del_id]
            del Project.ids[del_id]
            Project.save()
            self.save()

    def search_by_date(self):
        while True:
            search_date = input("Enter date to search: ")
            try:
                search_date = date.fromisoformat(search_date)
            except:
                print ("Invalid date format, please reenter")
            else:
                break
        
        for project_id in self.projects:
            project = Project.projects[project_id]
            if search_date == project.start:
                print(f"Project: {project_id} started in {search_date}")
            elif search_date == project.end:
                print(f"Project: {project_id} ends in {search_date}")
            else:
                print ("Project Not Found!")
        
    @classmethod
    def save(cls):
        file=open("users.txt","w")
        for user in cls.users.values():   
            file.write(user.__dict__.__str__()+"\n")
        file.close()

    @classmethod
    def load(cls):
        file=open("users.txt","r")
        lines = file.read().splitlines()

        for line in lines:
            attrs = ast.literal_eval(line)
            newuser = User(attrs['fname'],attrs['lname'], attrs['email'], attrs['phone'], attrs['ownprojectsids'])
            newuser.password = attrs['password']
         
        file.close()
        try: Project.load()
        except: pass
        
class Project():
    projects = {}
    ids = [0]

    def __init__(self, id, title, details, target, end) -> None:
        self.id = id
        Project.ids.append(self.id)
        self.projects[id] = self

        self.title = title
        self.details = details
        self.target = target
        self.end = end    

    @classmethod
    def save(cls):
        file=open("projects.txt","w")
        for project in cls.projects.values():
            temp = project.__dict__.copy()
            temp['end'] = temp['end'].isoformat()
            temp['start'] = temp['start'].isoformat()
            file.write(temp.__str__()+"\n")
        file.close()

    @classmethod
    def load(cls):
        file=open("projects.txt","r")
        lines = file.read().splitlines()

        for line in lines:
            attrs = ast.literal_eval(line)
            newproject = Project(attrs['id'],attrs['title'], attrs['details'],\
                         float(attrs['target']), date.fromisoformat(attrs['end']))
            newproject.__setattr__('start', date.fromisoformat(attrs['start']))
            newproject.__setattr__('owner', attrs['owner'])
         
        file.close()
