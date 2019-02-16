""" 

Author: Taha Aziz
CWID: 20341903
Date: 12/01/2018

Enhancements in this release:

- print a table that shows avg temperature by
day of week and hour of day

"""

import math

class TempDataset:
    DEFAULT_STATISTICS = (0, 0, 0)

    num_of_dataset_obj = 0

    def __init__(self):
        self.data_set = None
        self.dataset_name = "Unnamed"

        TempDataset.num_of_dataset_obj += 1

    def set_name(self, name):
        size = len(name)
        if (3 <= size <= 20 and type(name) == str):
            self.dataset_name = name
            return True
        # else
        return False

    def get_name(self):
        return self.dataset_name

    def process_file(self, filename):
        try:
            my_file = open(filename, 'r')
        except FileNotFoundError:
            return False
        self.data_set = []

        for line in my_file:
            line = line.split(",")
            if (line[3] == "TEMP"):
                day = int(line[0])
                time = math.floor(float(line[1]) * 24)
                sensor = int(line[2])
                temp = float(line[4])
                my_tuple = tuple((day, time, sensor, temp))
                self.data_set.append(my_tuple)

        return True

        my_file.close()

    def get_summary_statistics(self, active_sensors):
        if (self.data_set == None):
            return None
        size = len(self.data_set)
        temp_list = [(self.data_set[i][3]) for i in range(size) \
                     if self.data_set[i][2] in active_sensors]
        min_temp = min(temp_list)
        max_temp = max(temp_list)
        avg_temp = sum(temp_list) / len(temp_list)
        temp_stats = tuple((min_temp, max_temp, avg_temp))
        return temp_stats

    def get_avg_temperature_day_time(self, active_sensors, day, time):
        if (self.data_set == None):
            return None
        elif (active_sensors == [] or len(active_sensors) == 0):
            return None
        size = len(self.data_set)
        temp_list = [(self.data_set[i][3]) for i in range(size) \
                    if self.data_set[i][0] == day \
                    and self.data_set[i][1] == time \
                    and self.data_set[i][2] in active_sensors]
        avg = sum(temp_list) / len(temp_list)
        return avg

    def get_num_temps(self, active_sensors, lower_bound, upper_bound):
        if (self.data_set == None):
            return None
        return

    def get_loaded_temps(self):
        if (self.data_set == None):
            return None
        num_of_samples = len(self.data_set)
        if (num_of_samples == 0):
            return None
        return num_of_samples

    @classmethod
    def get_num_objects(cls):
        return cls.num_of_dataset_obj
#end class

def convert_units(celsius_value, units):
    """ Function that accepts celsius value as one
   parameter and units as another parameter that determines
   which temp to convert to and return """
    if (units == 0):
        temp = celsius_value
        return temp
    elif (units == 1):
        temp = ((9 / 5) * celsius_value) + 32
        return temp
    elif (units == 2):
        temp = celsius_value + 273.15
        return temp

def print_menu():
    """ Prints the possible options in a menu """
    print("\nMain Menu\n" 
          "---------\n" 
          "1 - Process a new data file\n" 
          "2 - Choose units\n" 
          "3 - Edit room filter\n" 
          "4 - Show summary statistics\n" 
          "5 - Show temperature by date and time\n" 
          "6 - Show histogram of temperatures\n" 
          "7 - Quit")

#the following functions will be implemented shortly
def new_file(dataset):
    """ This functions processes the data set and gets a name for it"""
    filename = input("Please enter the filename of " 
                     "the new dataset: ")
    try:
        dataset.process_file(filename)
    except FileNotFoundError:
        print("Unable to load file! ")
        main()

    samples = dataset.get_loaded_temps()
    print("Loaded " + str(samples) + " samples")
    while(True):
        data_name = input("Please provide a 3 to 20 character " 
                          "name for the data set: ")
        if (not dataset.set_name(data_name)):
            print("Invalid name. Please try again. ")
            continue
        break

current_unit = 0
unit_name = "C"
UNITS = {
        0 : ("Celsius", "C"),
        1 : ("Fahrenheit", "F"),
        2 : ("Kelvin", "K")
}

def choose_units():
    global current_unit
    print("Current units in " + UNITS[current_unit][0])

    global unit_name

    while (True):
        try:
            for unit in UNITS:
                print(str(unit) + " - " + str(UNITS[unit][0]))
            choice = int(input("Which unit? \n"))
            if choice not in UNITS.keys():
                print("Please choose a unit from the list ")
                continue
            current_unit = choice
            unit_name = UNITS[current_unit][1]
            break
        except ValueError:
           print("*** Please enter a number only *** ")
           continue

def change_filter(sensors, sensor_list, filter_list):
    """ This function print the sensor list and then ask the
    user to enter a sensor to have added to/removed from list """
    print_filter(sensor_list, filter_list)

    while(True):
        room_number = (input("\nType the sensor" 
        " number to toggle (e.g.4201) or x to end "))

        if (room_number == "x"):
            break
        elif room_number not in sensors.keys():
            print("Invalid Sensor")
            continue
        elif room_number in sensors:
            if sensors[room_number][1] in filter_list:
                filter_list.remove(sensors[room_number][1])
            else:
                filter_list.append(sensors[room_number][1])
        print_filter(sensor_list, filter_list)

def print_summary_statistics(dataset, active_sensors):
    if (dataset.data_set == None or active_sensors == []):
        print("Please load a data file and make sure at least "
              "one sensor is active")
    else:
        temp_stats = dataset.get_summary_statistics(active_sensors)
        name = dataset.get_name()
        global current_unit
        global unit_name
        min_temp = convert_units(temp_stats[0], current_unit)
        max_temp = convert_units(temp_stats[1], current_unit)
        avg_temp = convert_units(temp_stats[2], current_unit)
        output = ("Summary statistics for " + name + "\n"
                  "Minimum temperature: {:.2f} ".format(min_temp) \
                  + unit_name + "\n"
                  "Maximum temperature: {:.2f} ".format(max_temp) \
                  + unit_name + "\n"
                  "Average temperature: {:.2f} ".format(avg_temp) \
                  + unit_name + "\n")
        print(output)

DAYS = {
    0 : "SUN",
    1 : "MON",
    2 : "TUE",
    3 : "WED",
    4 : "THU",
    5 : "FRI",
    6 : "SAT"
}

HOURS = {
    0 : "Mid-1AM  ",
    1 : "1AM-2AM  ",
    2 : "2AM-3AM  ",
    3 : "3AM-4AM  ",
    4 : "4AM-5AM  ",
    5 : "5AM-6AM  ",
    6 : "6AM-7AM  ",
    7 : "7AM-8AM  ",
    8 : "8AM-9AM  ",
    9 : "9AM-10AM ",
    10 : "10AM-11AM",
    11 : "11AM-NOON",
    12 : "NOON-1PM ",
    13 : "1PM-2PM  ",
    14 : "2PM-3PM  ",
    15 : "3PM-4PM  ",
    16 : "4PM-5PM  ",
    17 : "5PM-6PM  ",
    18 : "6PM-7PM  ",
    19 : "7PM-8PM  ",
    20 : "8PM-9PM  ",
    21 : "9PM-10PM ",
    22 : "10PM-11PM",
    23 : "11PM-MID ",
}

def print_temp_by_day_time(dataset, active_sensors):
    if (dataset.get_loaded_temps() == None):
        print("\nYou need to load a data set! ")
    else:
        name = dataset.get_name()
        units = UNITS[current_unit][0]
        print("\nAverage temperature for " + name +
              "\nUnits are in " + units )
        for day in DAYS:
            if (units == 'Kelvin'):
                if (day == 0):
                    print("{:>13}    ".format(DAYS[day]), end="")
                else:
                    print("{:7}".format(DAYS[day]), end="")
            else:
                if (day == 0):
                    print("{:>13}   ".format(DAYS[day]), end="")
                else:
                    print("{:6}".format(DAYS[day]), end="")
        print()
        for time in HOURS:
            print("{:9} ".format(HOURS[time]), end = "")
            for day_key in DAYS:
                print("{:4.1f}  ".format(
                convert_units(dataset.get_avg_temperature_day_time(active_sensors,
                day_key, time), current_unit)), end = "")
                if (day_key % 6 == 0 and day_key != 0):
                    print()

def print_histogram(dataset, active_sensors):
    pass

def recursive_sort(list_to_sort, key=0):
    """ This implements bubble sort recursively"""
    size = len(list_to_sort)
    my_list = list_to_sort.copy()

    if (size == 0 or size == 1):
        return my_list

    for i in range(size - 1):
        if my_list[i][key] > my_list[i + 1][key]:
            (my_list[i], my_list[i + 1]) \
            = (my_list[i+1], my_list[i])

    return (recursive_sort(my_list[:-1], key) + my_list[-1:])

def print_filter(sensor_list, filter_list):
    """ This function prints the list of filters and
    notes all of the active ones"""
    print("")
    size = len(sensor_list)
    for i in range(size):
        print(sensor_list[i][0] + ": " + \
              sensor_list[i][1], end = " ")
        if (sensor_list[i][2] in filter_list):
            print("[ACTIVE]")
        else: print("")

#building the necessary dictionary/lists for sensors
sensors = {
    "4213" : ("STEM Center", 0),
    "4201" : ("Foundations Lab", 1),
    "4204" : ("CS Lab", 2),
    "4218" : ("Workshop Room", 3),
    "4205" : ("Tiled Room", 4),
    "Out" : ("Outside", 5),
}
#list with tuple format of (room number, desc, sensor number)
sensor_list = [(k, v[0], v[1]) for k, v in sensors.items()]

#list containing all sensor numbers
filter_list = [(i[1][1]) for i in sensors.items()]

#instantiate a TempDataset() object
current_set = TempDataset()

print("STEM Center Temperature Project")
print("Taha Aziz")

# main program ---------------------------------------------------
def main():

    some_list = recursive_sort(sensor_list)

    while(True):
        print_menu()
        try:
            choice = int(input("\nWhat is your choice? "))
            if(choice < 1 or choice > 7):
                print("Invalid choice")
                continue
        except ValueError:
            print("*** Please enter an integer only ***")
            continue
        if(choice == 1):
            new_file(current_set)
        elif(choice == 2):
            choose_units()
        elif(choice == 3):
            change_filter(sensors, some_list, filter_list)
        elif(choice == 4):
            print_summary_statistics(current_set, filter_list)
        elif(choice == 5):
            print_temp_by_day_time(current_set, filter_list)
        elif(choice == 6):
            print_histogram(current_set, None)
        elif(choice == 7):
            print("Thank you for using the STEM Center Temperature Project")
            break

if __name__ == "__main__":
    main()

""" SAMPLE OUTPUT

/Users/tahaaziz/PycharmProjects/Assignment11/venv/bin/python /Users/tahaaziz/PycharmProjects/Assignment11/Assignment11.py
STEM Center Temperature Project
Taha Aziz

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

What is your choice? 1
Please enter the filename of the new dataset: Temperatures2017-08-06.csv
Loaded 11724 samples
Please provide a 3 to 20 character name for the data set: Dataset

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

What is your choice? 5

Average temperature for Dataset
Units are in Celsius
          SUN   MON   TUE   WED   THU   FRI   SAT   
Mid-1AM   21.1  20.6  21.7  21.5  21.0  21.1  19.8  
1AM-2AM   21.1  20.5  21.6  21.5  20.9  21.1  19.9  
2AM-3AM   21.1  20.4  21.5  21.4  20.9  21.1  19.8  
3AM-4AM   21.1  20.4  21.4  21.3  20.8  21.0  19.8  
4AM-5AM   21.1  20.4  21.4  21.2  20.8  21.0  19.9  
5AM-6AM   21.0  20.2  21.4  21.2  20.7  20.8  19.8  
6AM-7AM   20.9  19.9  21.3  21.0  20.6  20.6  19.8  
7AM-8AM   20.7  20.0  21.1  20.9  20.6  20.5  19.9  
8AM-9AM   20.6  20.2  21.2  20.8  20.7  20.3  19.9  
9AM-10AM  20.9  21.1  22.0  20.9  21.2  20.2  20.2  
10AM-11AM 21.2  21.9  22.8  21.5  22.1  20.4  20.6  
11AM-NOON 21.5  22.6  23.4  22.2  22.7  20.7  20.8  
NOON-1PM  21.6  23.0  23.9  22.6  23.0  21.0  21.0  
1PM-2PM   21.7  23.3  24.0  23.1  23.2  21.0  21.0  
2PM-3PM   21.9  23.6  24.2  23.5  23.3  21.1  21.0  
3PM-4PM   21.9  24.0  24.4  23.6  23.5  21.1  20.8  
4PM-5PM   21.7  24.2  24.5  23.8  23.6  21.0  20.9  
5PM-6PM   21.6  24.1  24.4  23.7  23.7  20.8  20.9  
6PM-7PM   21.5  23.4  23.9  23.4  23.2  20.7  20.7  
7PM-8PM   21.4  23.0  23.2  22.8  22.3  20.3  20.5  
8PM-9PM   21.2  22.6  22.3  22.1  21.6  19.8  20.2  
9PM-10PM  21.0  22.3  21.8  21.7  21.2  19.7  19.9  
10PM-11PM 20.8  22.0  21.7  21.5  21.2  19.8  19.8  
11PM-MID  20.8  21.9  21.6  21.2  21.1  19.8  19.7  

Main Menu
---------
1 - Process a new data file
2 - Choose units
3 - Edit room filter
4 - Show summary statistics
5 - Show temperature by date and time
6 - Show histogram of temperatures
7 - Quit

What is your choice? 7
Thank you for using the STEM Center Temperature Project

"""