import psycopg2
import random

conn = psycopg2.connect(
    dbname="Management_db",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    if user:
        member_status = user[2]
        if member_status == 1:
            admin_actions(username)
        elif member_status == 2:
            trainer_actions(username)
        elif member_status == 3:
            member_actions(username)  
    else:
        print("Invalid username or password.")
    cursor.close()

def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    cursor = conn.cursor()
    query = "INSERT INTO users (username, password, memberstatus) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, password, 3))  # Always set memberstatus to 3 for new signups
    conn.commit()
    print("Signup successful!")

    cursor.close()

def admin_actions(username):
    print("Hello,", username)
    while True:
        print("\nAdmin Menu:")
        print("1. Equipment Tracking")
        print("2. Room Booking")
        print("3. Payment")
        print("4. End Session")
        print("5. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_equipment_tracking()
        elif choice == "2":
            view_available_rooms()
        elif choice == "3":
            manage_payments()
        elif choice == "4":
            end_session()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

def manage_payments():
    cursor = conn.cursor()
    select_query_payment = "SELECT membername, payment FROM payment"
    cursor.execute(select_query_payment)
    payments = cursor.fetchall()
    if payments:
        for payment in payments:
            print("Member", payment[0], "owes $", payment[1])
        username = input("Which member are you? ")
        select_query_user_payment = "SELECT SUM(payment) FROM payment WHERE membername = %s"
        cursor.execute(select_query_user_payment, (username,))
        total_payment = cursor.fetchone()[0]
        if total_payment is not None:
            print("Hello", username, "you owe $", total_payment)
            pay_off_today = input("Would you like to pay it off today? (yes/no) ")
            if pay_off_today.lower() == "yes":
                delete_query_payment = "DELETE FROM payment WHERE membername = %s"
                cursor.execute(delete_query_payment, (username,))
                conn.commit()
                print("Payment successfully cleared for", username)
            else:
                print("Payment not cleared. Continuing...")
        else:
            print("You have no pending payments.")
    else:
        print("No payments to manage.")

    cursor.close()

def end_session():
    cursor = conn.cursor()
    query = "SELECT specialization, membername, room_number FROM trainer WHERE availability = FALSE"
    cursor.execute(query)
    sessions = cursor.fetchall()
    if sessions:
        insert_query_fd = "INSERT INTO Fitness_Done (username, Fitness_Done, Health_Metric) VALUES (%s, %s, NULL)"
        insert_query_pmt = "INSERT INTO payment (membername, payment, exercise) VALUES (%s, %s, %s)"
        update_query_rs = "UPDATE Room_status SET availability = TRUE WHERE room_number = %s"
        delete_query_trainer = "DELETE FROM trainer WHERE availability = FALSE"
        for session in sessions:
            try:
                payment_amount = round(random.uniform(5, 10), 2)
                cursor.execute(insert_query_fd, (session[1], session[0]))
                cursor.execute(insert_query_pmt, (session[1], payment_amount, session[0]))
                cursor.execute(update_query_rs, (session[2],))
       
            except Exception as e:
                print("An error occurred:", e)
                conn.rollback()
                continue

        cursor.execute(delete_query_trainer)
        refresh_fitness_done()
        conn.commit()
        print("Sessions ended successfully.")
    else:
        print("No active sessions to end.")
    cursor.close()

def refresh_fitness_done():
    cursor = conn.cursor()
    select_query_fd = "SELECT Fitness_Done FROM Fitness_Done"
    cursor.execute(select_query_fd)
    fitness_done_rows = cursor.fetchall()
    for row in fitness_done_rows:
        fitness_done = row[0]
        select_query_es = "SELECT HealthStatistics FROM ExerciseStats WHERE ExerciseRoutine = %s"
        cursor.execute(select_query_es, (fitness_done,))
        health_statistic = cursor.fetchone()
        if health_statistic:
            health_statistic = health_statistic[0]
            update_query_fd = "UPDATE Fitness_Done SET Health_Metric = %s WHERE Fitness_Done = %s"
            cursor.execute(update_query_fd, (health_statistic, fitness_done))
    conn.commit()
    print("Fitness_Done table refreshed successfully.")
    cursor.close()

def view_equipment_tracking():
    cursor = conn.cursor()
    query = "SELECT Equipment, Availability FROM equipment_maintenance_monitoring"
    cursor.execute(query)
    equipment = cursor.fetchall()
    print("\nEquipment Tracking:")
    for item in equipment:
        if item[1]: 
            print(f"{item[0]} is available.")
        else:
            print(f"{item[0]} isn't available.")

    cursor.close()

def view_available_rooms():
    cursor = conn.cursor()
    query = "SELECT room_number FROM Room_status WHERE availability = TRUE"
    cursor.execute(query)
    available_rooms = cursor.fetchall()
    print("\nAvailable Rooms:")
    for room in available_rooms:
        print(room[0])
    cursor.close()
    chosen_room = input("Which room do you want to book? ")
    cursor = conn.cursor()
    query = "SELECT * FROM Room_status WHERE room_number = %s AND availability = TRUE"
    cursor.execute(query, (chosen_room,))
    room = cursor.fetchone()
    if room:
        update_query = "UPDATE Room_status SET availability = FALSE WHERE room_number = %s"
        cursor.execute(update_query, (chosen_room,))
        insert_query = "INSERT INTO trainer (room_number) VALUES (%s)"
        cursor.execute(insert_query, (chosen_room,))
        conn.commit()
        print(f"Room {chosen_room} has been successfully booked.")
    else:
        print(f"Room {chosen_room} is not available for booking.")
    cursor.close()


def trainer_actions(username):
    while True:
        print("\nTrainer Menu:")
        print("1. Search Member")
        print("2. Book Session")
        print("3. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            search_member()
        elif choice == "2":
            book_session(username)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

def search_member():
    cursor = conn.cursor()
    query = "SELECT username FROM users WHERE memberstatus = 3"
    cursor.execute(query)
    members = cursor.fetchall()
    print("\nMembers with memberstatus 3:")
    for member in members:
        print(member[0])
    cursor.close()
    chosen_member = input("Which member would you like to look at? ")
    cursor = conn.cursor()
    query = "SELECT * FROM Fitness_Goals WHERE username = %s"
    cursor.execute(query, (chosen_member,))
    goals = cursor.fetchall()
    if goals:
        print(f"\nFitness Goals of {chosen_member}:")
        for goal in goals:
            print(goal)
    else:
        print(f"No fitness goals found for {chosen_member}.")
    cursor.close()

def book_session(username):
    cursor = conn.cursor()
    query = "SELECT room_number FROM trainer WHERE Trainername IS NULL"
    cursor.execute(query)
    available_rooms = cursor.fetchall()
    print("\nAvailable Rooms:")
    for room in available_rooms:
        print(f"Available room: {room[0]}")
    chosen_room = input("Which room would you like to book? ")
    room_query = "SELECT * FROM trainer WHERE room_number = %s AND Trainername IS NULL"
    cursor.execute(room_query, (chosen_room,))
    room = cursor.fetchone()
    if room:
        exercise = input("What exercise are you doing? ")
        time_slot = input("Enter the time slot you will be booking: ")
        exercise_query = "SELECT * FROM ExerciseStats WHERE ExerciseRoutine = %s"
        cursor.execute(exercise_query, (exercise,))
        exercise_exists = cursor.fetchone()
        if exercise_exists:
            update_query = "UPDATE trainer SET specialization = %s, time = %s, Trainername = %s WHERE room_number = %s"
            cursor.execute(update_query, (exercise, time_slot, username, chosen_room))
            conn.commit()
            print("Session booked successfully.")
        else:
            print("Exercise not found in ExerciseStats table.")
    else:
        print(f"Room {chosen_room} is not available or already booked.")
    cursor.close()

def member_actions(username):
    print("Hello,", username)
    while True:
        print("\nMember Menu:")
        print("1. Fitness Completed")
        print("2. Fitness Goals")
        print("3. Change Personal Information")
        print("4. Dashboard")
        print("5. Member Book Session")
        print("6. Back to Main Menu")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_fitness_completed(username)
        elif choice == "2":
            manage_fitness_goals(username)
        elif choice == "3":
            username = change_personal_info(username)
        elif choice == "4":
            view_dashboard()
        elif choice == "5":
            member_book_session(username)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")
    return username

def member_book_session(username):
    cursor = conn.cursor()
    query = "SELECT * FROM trainer"
    cursor.execute(query)
    sessions = cursor.fetchall()
    print("\nAvailable Sessions:")
    for session in sessions:
        print(f"Room: {session[4]}")

    chosen_room = input("Which session will you join? Enter the room number: ")
    room_query = "SELECT * FROM trainer WHERE room_number = %s AND availability = TRUE"
    cursor.execute(room_query, (chosen_room,))
    room = cursor.fetchone()
    if room:
        update_query = "UPDATE trainer SET membername = %s, availability = FALSE WHERE room_number = %s"
        cursor.execute(update_query, (username, chosen_room))

        conn.commit()
        print("Session booked successfully.")
    else:
        print(f"Session in room {chosen_room} is not available.")
    cursor.close()

def view_dashboard():
    cursor = conn.cursor()
    query = "SELECT * FROM ExerciseStats"
    cursor.execute(query)
    exercises = cursor.fetchall()
    print("\nExercise Stats:")
    for exercise in exercises:
        print(exercise)
    cursor.close()
    
def view_fitness_completed(username):
    cursor = conn.cursor()
    query = "SELECT * FROM Fitness_Done WHERE username = %s"
    cursor.execute(query, (username,))
    fitness_completed = cursor.fetchall()

    if fitness_completed:
        print("\nFitness Completed:")
        for activity in fitness_completed:
            print(activity)
    else:
        print("There are no completed fitness activities.")
    cursor.close()

def manage_fitness_goals(username):
    cursor = conn.cursor()
    query = "SELECT * FROM Fitness_Goals WHERE username = %s"
    cursor.execute(query, (username,))
    goals = cursor.fetchall()
    print("\nYour Fitness Goals:")
    for goal in goals:
        print(goal)

    add_goal = input("Do you want to add a new goal? (yes/no): ")
    if add_goal.lower() == "yes":
        exercise = input("Enter the exercise for your new goal: ")
        query = "SELECT HealthStatistics FROM ExerciseStats WHERE ExerciseRoutine = %s"
        cursor.execute(query, (exercise,))
        health_statistics = cursor.fetchone()
        if health_statistics:
            health_statistics = health_statistics[0]
        else:
            print("Exercise not found in ExerciseStats table.")
            cursor.close()
            return
        query = "INSERT INTO Fitness_Goals (username, Fitness_todo, Health_Metric) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, exercise, health_statistics))
        conn.commit()
        print("New goal added successfully.")

    cursor.close()
def change_personal_info(username):
    new_username = input("Do you want to change your username? (yes/no): ")
    if new_username.lower() == "yes":
        new_username = input("Enter your new username: ")
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (new_username,))
        existing_user = cursor.fetchone()
        if existing_user:
            print("Username already exists. Please choose another one.")
            cursor.close()
            return username
        query = "UPDATE users SET username = %s WHERE username = %s"
        cursor.execute(query, (new_username, username))
        query = "UPDATE Fitness_Goals SET username = %s WHERE username = %s"
        cursor.execute(query, (new_username, username))
        query = "UPDATE Fitness_Done SET username = %s WHERE username = %s"
        cursor.execute(query, (new_username, username))
        conn.commit()
        print("Username changed successfully.")
        cursor.close()
        return new_username

    change_password = input("Do you want to change your password? (yes/no): ")
    if change_password.lower() == "yes":
        new_password = input("Enter your new password: ")
        cursor = conn.cursor()
        query = "UPDATE users SET password = %s WHERE username = %s"
        cursor.execute(query, (new_password, username))
        conn.commit()
        print("Password changed successfully.")
        cursor.close()

    return username

def main():
    while True:
        print("1. Login")
        print("2. Signup")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            login()
        elif choice == "2":
            signup()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()