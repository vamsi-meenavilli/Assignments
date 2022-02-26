import pandas as pd

class employee:
    def __init__(self):
        self.keys = ['name', 'aadhar_number', 'phone_number', 'pan_number', 'age', 'gender', 'monthly_income', 'family_size', 'total_wealth', 'city', 'state', 'pincode', 'street', 'building_info']
        self.index = 0
        self.integer_keys = [4, 6, 7, 8]
        self.string_keys = [0, 1, 2, 5, 9, 10, 11, 12, 13]
        self.alpha_numeric_keys = [3]
        self.find_by_operation_keys = { '1' : 0, '2' : 1, '3' : 4, '4' : 3, '5' : 2}
        self.select_by_opeartion_keys = {'6' : 4, '7' : 7, '8' : 9, '9' : 10, '10' : 6, '11' : 8 }
        self.employees = []
        self.generate_key_maps()
        self.show_menu()
        

    def generate_key_maps(self):
        for i in self.keys:
            setattr(self, i, {})

    def show_menu(self):
        print("Welcome to Vamsi's Employee Management System!!!")
        print("Available Operations:")
        print("Find by:\n 1.  name\n 2.  aadhar number\n 3.  age \n 4.  pan id\n 5.  phone number\n")
        print("Selcet by:\n 6.  age range\n 7.  family size\n 8.  city\n 9.  state\n 10. income range\n 11. wealth range\n")
        print("Modify data:\n12. add\n13. delete\n14. update\n\n15. show all\n16. get data from csv\n17. exit")
        
        self.handle_operation(int(input("Pass in the number against the operation:\n")))

    def handle_operation(self, operation):
        if operation not in range(1,17):
            print("Please choose a valid operation")
            self.show_menu()
            return

        if operation in range(1,6):
            self.find_by({ 'operation' : str(operation) })
        elif operation in range(6,12):
            self.select_by({ 'operation' : str(operation) })
        elif operation == 12:
            self.add_employee()
        elif operation == 13:
            self.delete_employee()
        elif operation == 14:
            self.update_employee()
        elif operation == 15:
            self.show_all()
        elif operation == 16:
            self.get_data_from_csv()
        else:
            exit

    def find_by(self, args):
        operation = args['operation']
        key_index = self.find_by_operation_keys[operation]
        key = self.keys[key_index]
        value = [input("Enter the " + key + " of the employee:\n")]
        values = self.format_data({
            'keys' : [key],
            'values' : value,
            'key_indexes' : [key_index]
        })

        employees = self.find_employees({
            'keys' : [key],
            'values' : values,
            'key_indexes' : [key_index]
        })

        if employees:
            self.show_employees({ 'indexes' : employees })
        else:
            print("No records found!!!")

        self.show_menu()

    def select_by(self, args):
        operation = args['operation']
        key_index = self.select_by_opeartion_keys[operation]
        key = self.keys[key_index]

        if key_index not in self.string_keys:
            display_text = "Enter , separated range values:\n"
            values =  input(display_text).strip().split(',')
        else:
            display_text = "Enter the " + key + " of the employee:\n"
            values =  input(display_text).strip().split(',')

        values = self.format_data({
            'keys' : [key],
            'values' : values,
            'key_indexes' : [key_index]
        })
        
        employees = self.find_employees({
            'keys' : [key],
            'values' : values,
            'key_indexes' : [key_index]
        })

        if employees:
            self.show_employees({ 'indexes' : employees })
        else:
            print("No records found!!!")

        self.show_menu()

    def add_employee(self):
        print("Pass in the below , separated values")
        self.show_keys()
        values = input().strip().split(',')

        if len(values) != 14:
            print("Please pass all the values!!")
            self.show_menu()
            return

        formatted_values = self.format_data({
            'keys' : self.keys,
            'values' : values
        })

        self.employees.append(formatted_values)
        self.add_to_key_maps({ 'employee' : formatted_values })
        self.index += 1
        print("Employee details added sucessfully!!!")
        self.show_menu()

    def add_to_key_maps(self, args):
        employee = args['employee']
        keys = self.keys
        if 'index' in args:
            index = args['index']
        else:
            index = self.index

        for i in range(len(keys)):
            key_map = getattr(self, keys[i])
            if employee[i] in key_map:
                key_map[employee[i]].append(index)
            else:
                key_map[employee[i]] = [index]

        return

    def update_employee(self):
        print("Pass in any 2 of the keys with values in this format key:value,key:value\n")
        self.show_keys()
        key_values = self.get_and_format_data()
        keys = key_values['keys']
        values = key_values['values']

        employees = self.find_employees({
            'keys' : keys,
            'values' : values,
        })

        if not employees:
            print("No employees found!!!")
            self.show_menu()
            return

        employees = [i for i in set(employees)]

        if len(employees) == 0:
            print("No employees found!!!")
            self.show_menu()
            return
        elif len(employees) > 1:
            print("Multiple employees found. Choose one by passing the row numer, row number starts from 1")
            self.show_employees(employees)
            index = employees[int(input()) - 1]
        else:
            index = employees[0]

        key_values = self.get_and_format_data()
        keys = key_values['keys']
        values = key_values['values']
        key_indexes = self.get_key_indexes({ 'keys' : keys})

        self.delete_from_key_maps({ 'employee' : self.employees[index], 'index' : index })

        for i in range(len(key_indexes)):
            self.employees[index][key_indexes[i]] = values[i]

        self.add_to_key_maps({ 'employee' : self.employees[index], 'index' : index })
        self.show_menu()

    def delete_from_key_maps(self, args):
        keys = self.keys
        values = args['employee']
        index = args['index']

        for i in range(len(keys)):
            key_map = getattr(self, keys[i])
            key_map_value = key_map[values[i]]
            
            if len(key_map_value) == 1:
                del key_map[values[i]]
            else:
                key_map_value_index = key_map_value.index(index)

                if key_map_value_index == len(key_map_value) - 1:
                    key_map[values[i]].pop()
                else:
                    key_map[values[i]], key_map[values[-1]] = key_map[values[-1]], key_map[values[i]]
                    key_map[values[i]].pop()

            setattr(self, keys[i], key_map)


    def get_and_format_data(self):
        self.show_keys()
        keys = []
        values = []
        for i in input().strip().split(','):
            key_value = i.split(':')
            keys.append(key_value[0])
            values.append(key_value[1])

        formatted_values = self.format_data({
            'keys' : keys,
            'values' : values
        })

        return { 'keys' : keys, 'values' : formatted_values }

    def delete_employee(self):
        print("Pass in any 2 of the keys with values in this format key:value,key:value\n")
        self.show_keys()
        key_values = self.get_and_format_data()
        keys = key_values['keys']
        values = key_values['values']

        employees = self.find_employees({
            'keys' : keys,
            'values' : values,
        })

        if not employees:
            print("No employees found!!!")
            self.show_menu()
            return

        employees = [int(i) for i in set(employees)]
        print(employees)
        if len(employees) == 0:
            print("No employees found!!!")
            self.show_menu()
            return
        elif len(employees) > 1:
            print("Multiple employees found. Choose one by passing the row numer, row number starts from 1")
            self.show_employees(employees)
            index = employees[int(input()) - 1]
        else:
            index = employees[0]

        if index == self.index - 1:
            self.delete_from_key_maps({
                'index' : index,
                'employee' : self.employees[index]
            })
        else:
            self.delete_from_key_maps({
                'index' : index,
                'employee' : self.employees[index]
            })
            self.delete_from_key_maps({
                'index' : self.index,
                'employee' : self.employees[self.index - 1]
            })
            self.employees[index], self.employees[-1] = self.employees[-1], self.employees[index]
            self.employees.pop()
            self.add_to_key_maps({
                'employee' : self.employees[index],
                'index' : index, 
            })

        print("Employee deleted sucessfully!!!")
        
        self.show_menu()
    
    def show_all(self):
        indexes = [i for i in range(self.index)]
        
        self.show_employees({ 'indexes' : indexes })
        self.show_menu()

    def get_data_from_csv(self):
        path = input("Pass in the file path").strip()
        for i in open(path).readlines()[1:]:
            self.employees.append(i.split(','))
        
        print("Done reading data from csv!!!")
        self.show_menu()

    def format_data(self, args):
        keys = args['keys']
        values = args['values']
        
        print(values)
        if 'key_indexes' in args:
            key_indexes = args['key_indexes']
        else:
            key_indexes = self.get_key_indexes({ 'keys' : keys})

        for i in range(len(keys)):
            if key_indexes[i] in self.integer_keys:
                if type(values[i]) == list:
                    for j in range(len(values[i])):
                        values[i][j] = int(values[i][j])
                else:
                    values[i] = int(values[i])
            else:
                values[i] = values[i].strip().replace(' ', '').upper()

        return values

    def get_key_indexes(self, args):
        keys = args['keys']
        key_indexes = []

        for i in keys:
            key_indexes.append(self.keys.index(i))

        return key_indexes

    def find_employees(self, args):
        keys = args['keys']
        values = args['values']
        indexes = []

        for i in range(len(keys)):
            key_map = getattr(self, keys[i])
            if len(keys) == len(values):
                if values[i] in key_map:
                    for j in key_map[values[i]]:
                        indexes.append(j)
            else:
                for j in key_map.keys():
                    if j in range(values[i][0], values[i][1]):
                        for k in key_map[j]:
                            indexes.append(k)

        if len(indexes) != 0:
            return indexes
        else:
            return False
        
    def show_employees(self, args):
        indexes = args['indexes']
        print(indexes)
        self.show_keys()

        for i in indexes:
            print(", ".join([str(i) for i in self.employees[i]]))

    def show_keys(self):
        print(", ".join(self.keys))


x = employee()