import datetime as dt
print("[ WELCOME ]")
print("[DAILY CALORIE TRACKER ]")

print()
print("NAME : Priyam Sharma") 
print("ROLL NUMBER : 2501730184")
print(f"DATE : {dt.datetime.now()}") 
print()

meals=[]   
calories=[] 

user_input = int(input("How many meals do you want to add :".upper()))

print()
user_intake_limit=float(input("Enter your daily calorie limit :".upper())) 

print()

count = 0
while count < user_input:  
    user_input1 = input("Enter meal name and calories separated by a comma: ").strip() 
    temp_list = user_input1.split(',')
    meals.append(temp_list[0].strip().upper()) 
    calories.append(float(temp_list[1].strip())) 
    count += 1

print()


print("\033[1;96m" + f"{'S NO':<4}{'MEAL NAME':<20}{'CALORIES':<25}" + "\033[0m")  

print("\033[1;96m" + "-" * 50 + "\033[0m")

for i in range(len(meals)):  #
    print("\033[1;96m" + f"{i+1:<4}{meals[i]:<20}{calories[i]:<25}" + "\033[0m")

print("\033[1;96m" + "-" * 50 + "\033[0m")

print("\033[1;96m" + f"Total Calories Consumed : {sum(calories)}" + "\033[0m")

print()
print()
average_calories = sum(calories)/len(calories) 

print(f"Average Calories per Meal : {average_calories:.2f}")
print()

if float(sum(calories)) > user_intake_limit: 
    print("You have exceeded your daily calorie limit.".upper())
else:
    print("You are within your daily calorie limit.".upper())

print()



save_choice = input("\nDo you want to save this session report? (yes/no): ").strip().lower()

if save_choice == "yes":
    
    with open("calorie_log.txt", "w") as file:
        file.write("===== DAILY CALORIE TRACKER REPORT =====\n")
        file.write(f"NAME: Priyam Sharma\n")
        file.write(f"ROLL NUMBER: 2501730184\n")
        file.write(f"DATE: {dt.datetime.now()}\n\n")

        file.write(f"{'S NO':<4}{'MEAL NAME':<20}{'CALORIES':<25}\n")
        file.write("-" * 40 + "\n")

        for i in range(len(meals)):
            file.write(f"{i+1:<4}{meals[i]:<20}{calories[i]:<25}\n")

        file.write("-" * 40 + "\n")
        file.write(f"Total Calories Consumed: {sum(calories):.1f}\n")
        file.write(f"Average Calories per Meal: {average_calories:.2f}\n")
        file.write(f"Daily Calorie Limit: {user_intake_limit:.1f}\n")

        if sum(calories) > user_intake_limit:
            file.write("STATUS: You exceeded your daily calorie limit.\n")
        else:
            file.write("STATUS: You are within your daily calorie limit.\n")

    print("\nSession report saved successfully as 'calorie_log.txt'")
else:
    print("\nReport not saved. Session ended.")