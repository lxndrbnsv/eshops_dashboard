from app import db
from app.models import User


while True:
    username = input("Username: ")
    if User.query.filter_by(username=username).first() is not None:
        print("Username is already taken! Try another one!")
        continue
    password = input("Password: ")

    u = User()
    u.username = username
    u.set_password(password)
    db.session.add(u)
    db.session.commit()

    print(f"Added user {username}.")
    while True:
        add_new = input("1 - add another user    2 - quit\n")
        if add_new == "1":
            break
        elif add_new == "2":
            print("Exiting...")
            quit()
        else:
            print("Please select 1 or 2.")
