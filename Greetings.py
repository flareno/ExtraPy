def greet(who_to_greet):
    greetings = f"Hello, {who_to_greet}!"
    return greetings


name = input("Who's there? ")
print(greet(name))

state = input("Are you hungry? ")

if state == "Yes!":
    print("Let's eat!!!")

elif state == "yes!":
    print("Let's eat!!!")

elif state == "yes":
    print("Let's eat!!!")

elif state == "Yes":
    print("Let's eat!!!")

else:
    print("Ok, I'll eat alone")
