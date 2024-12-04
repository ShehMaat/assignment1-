import random

# File paths
USERS_FILE = "user.txt"
QUESTIONS_FILE = "questions.txt"

# Load questions from file
def load_questions():
    questions = {}
    try:
        with open(QUESTIONS_FILE, "r") as file:
            topic = None
            for line in file:
                line = line.strip()
                if line.startswith("Topic:"):
                    topic = line.split(":", 1)[1].strip()
                    questions[topic] = []
                elif topic and line:
                    parts = line.split(";")
                    if len(parts) >= 6:  # Ensure there are at least 5 options and 1 answer
                        question, *options, answer = parts
                        questions[topic].append({
                            "question": question.strip(),
                            "options": [opt.strip() for opt in options],
                            "answer": answer.strip()
                        })
    except FileNotFoundError:
        print(f"Error: The file {QUESTIONS_FILE} was not found!")
    except Exception as e:
        print(f"Error loading questions: {e}")

    if not questions:
        print("Error: No questions loaded. Check your questions file.")
    else:
        print(f"Successfully loaded topics: {list(questions.keys())}")
    return questions

# Load users from file
def load_users():
    users = {}
    try:
        with open(USERS_FILE, "r") as file:
            for line in file:
                username, password, score = line.strip().split(";")
                users[username] = {"password": password, "score": int(score)}
    except FileNotFoundError:
        pass
    return users


# Save users to file
def save_users(users):
    with open(USERS_FILE, "w") as file:
        for username, data in users.items():
            file.write(f"{username};{data['password']};{data['score']}\n")


# Register function
def register(users):
    username = input("Enter a username: ")
    if username in users:
        print("Username already exists! Try logging in.")
        return None
    password = input("Enter a password: ")
    users[username] = {"password": password, "score": 0}
    save_users(users)
    print("Registration successful!")
    return username


# Login function
def login(users):
    username = input("Enter your username: ")
    if username not in users:
        print("Username not found! Try registering.")
        return None
    password = input("Enter your password: ")
    if users[username]["password"] == password:
        print("Login successful!")
        return username
    else:
        print("Incorrect password!")
        return None


# Quiz function
def take_quiz(username, users, questions):
    if not questions:
        print("No questions available to take the quiz. Exiting.")
        return

    print("\nTopics available:")
    topic_keys = list(questions.keys())
    for idx, topic in enumerate(topic_keys, 1):
        print(f"{idx}. {topic}")

    try:
        chosen_index = int(input("Enter the number of your chosen topic: "))
        if chosen_index < 1 or chosen_index > len(topic_keys):
            print("Invalid choice! Please select a valid topic number.")
            return
        chosen_topic = topic_keys[chosen_index - 1]
    except ValueError:
        print("Invalid input! Please enter a valid number.")
        return

    print(f"\nYou selected: {chosen_topic}")
    quiz_questions = random.sample(questions[chosen_topic], min(5, len(questions[chosen_topic])))
    score = 0

    for i, q in enumerate(quiz_questions, 1):
        print(f"\nQ{i}: {q['question']}")
        for idx, option in enumerate(q["options"], 1):
            print(f"{idx}. {option}")
        try:
            answer = int(input("Enter the option number: "))
            if q["options"][answer - 1] == q["answer"]:
                print("Correct!")
                score += 1
            else:
                print(f"Wrong! Correct answer is: {q['answer']}")
        except (ValueError, IndexError):
            print("Invalid input! Skipping question.")

    print(f"\nYour score: {score}/{len(quiz_questions)}")
    users[username]["score"] = score
    save_users(users)

# Main function
def main():
    users = load_users()
    questions = load_questions()

    print("Welcome to the Quiz Application!")
    username = None
    while not username:
        action = input("Do you want to (1) Register or (2) Login? Enter 1 or 2: ")
        if action == "1":
            username = register(users)
        elif action == "2":
            username = login(users)
        else:
            print("Invalid choice!")

    while True:
        take_quiz(username, users, questions)
        choice = input("Do you want to (1) Reattempt the quiz or (2) Exit? Enter 1 or 2: ")
        if choice == "2":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
