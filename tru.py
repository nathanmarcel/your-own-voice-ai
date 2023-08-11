import datetime

current_datetime = datetime.datetime.now()

# Convert the datetime object to a string
datetime_string = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")
print("Current date and time:", datetime_string)