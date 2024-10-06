employee_data = {}
emp_id = 1
def create_profile():
    global employee_data, emp_id
    while True:
        print(f"Profile no: {len(employee_data) + 1}")
        print(f"emp id: {emp_id}")
        name = input("Enter employee name: ")
        location = input("Enter employee location: ")
        salary = input("Enter employee salary: ")
        age = int(input("Enter employee age: "))

        employee_dict = {
            "emp_id": emp_id,
            "name": name,
            "age": age,
            "location": location,
            "salary": salary
        }
        employee_data[emp_id] = employee_dict
        print("Employee added:")
        print(f"Employee id assigned to this profile is: {emp_id}")
        emp_id += 1
        input_exit = input("Do you want to add another profile? (yes/no): ")
        if input_exit == "no":
            print("Successfully added.")
            break

def read():
    print("Do you want to read all profiles or an individual profile?")
    read_input = input("Press 1 for an individual profile and 2 for all: ")
    if read_input == "1":
        emp_id = int(input("Enter the employee ID: "))
        if emp_id in employee_data:
            print(f"Employee ID: {emp_id}, Data: {employee_data[emp_id]}")
        else:
            print("Employee not found.")
    elif read_input == "2":
        for emp_id, data in employee_data.items():
            print(f"Employee ID: {emp_id}, Data: {data}")
    else:
        print("Invalid option.")

def exit_menu():
    print("Exiting the program. Thank you!")
    exit()

def update_profile():
    emp_id = int(input("Enter the employee ID to update: "))
    if emp_id in employee_data:
        print(f"Employee ID: {emp_id}, Data: {employee_data[emp_id]}")
        print("enter details to update:")
        name = input("Enter employee name: ")
        location = input("Enter employee location: ")
        salary = input("Enter employee salary: ")
        age = int(input("Enter employee age: "))
        employee_data [emp_id]= {
            "name" : name,
            "location" : location,
            "salary" : salary,
            "age" : age
        }
        print(f"Employee ID: {emp_id}, Data: {employee_data[emp_id]}")
        print("update profile successfully")
    else:
        print("profile is not existed:")

def delete_profile():
    emp_id = int(input("Enter the employee ID to delete: "))
    if emp_id in employee_data:
     print(f"Employee ID: {emp_id}, Data: {employee_data[emp_id]}")
     del employee_data[emp_id]
     print("delete profile successfully")
    else:
        print("print not existed :")

def age_identifier():
    print("age identifier")
    emp_id = int(input("Enter the employee ID to age identify: "))
    age = employee_data [emp_id].get('age')
    if age >= 25 :
        name = employee_data[emp_id].get('name')
        print(f"{name}:employe is not young:")
    elif age <= 25 :
        name = employee_data[emp_id].get('name')
        print(f"{name}:employee is young")

def adrress_locate():
    emp_id = int(input("Enter the employee ID to check the location: "))
    if emp_id in employee_data:
        name = employee_data[emp_id].get('name')
        location = employee_data[emp_id].get('location')
        if location == 'islamabad':
            print(f"{name}:employee is belong :{location}")
        elif location == 'lahore':
            print(f"{name}:employee is belong :{location}")
        elif location == 'karachi':
            print(f"{name}:employee is belong :{location}")
        else :
            print(f"{name}:employee is belong to unkown area:") 
    else:
        print("id not existed :")

switch_dict = {
    1: create_profile,
    2: read,
    3: update_profile,
    4: delete_profile,
    5: exit, 
}

def salary():

    increment = 50000
    emp_id = int(input("Enter the employee ID to check salary: "))
    if emp_id in employee_data:
        salary = employee_data[emp_id].get('salary')
        name = employee_data[emp_id].get('name') 

        print (f"{name}: current salary: {salary}")
    else:
        print("Employee not found.")

def name():
    emp_id = int(input("Enter the employee ID to check the name characters : "))
    if emp_id in employee_data:
        name = employee_data[emp_id].get('name') # accessing dictionary
        print(f"name: {name}")
        length = len(name)# len is used to find legnth 
        print(f"the length of the characters in name:{length}")
    else:
        print("print not existed :")
create_profile()
read()
update_profile()
age_identifier()
adrress_locate()
name()
salary()
delete_profile()
exit()
