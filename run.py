import Utils

difficulty = 1
username = "avivams"

start_url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="
end_url = f"&difficulty={difficulty}"
# url = f"http://aoi.ise.bgu.ac.il/?user={username}&password="

password = Utils.timing_attack(start_url=start_url, end_url=end_url, password_size=16)
