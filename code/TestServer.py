from http.server import BaseHTTPRequestHandler, HTTPServer
import time

# Passwords for different difficulties
passwords_list = {
    1: "jtkfyyjvmyzljuyh",
    2: "clydmpotnvywywce",
    3: "uqmetgcpjngxkazr",
    4: "koyzkbzehgmriyxp",
    5: "ebyshfchgsyuqegg",
    6: "bcggxwwoilrfhrhy",
    7: "iefxjzqrrauzfcao",
    8: "gujophmhnilcayzn",
    9: "yojbpywukpbrsyvl",
    10: "qgkyyyedmabziyvx",
    11: "ncowjdugkeidjsuw",
    12: "mcihfsdjwslsdkls",
    13: "dmskadakslcnsksd",
    14: "qdskacsacjiajasc",
    15: "dskapjcokaxsqkds",
    16: "dksapcnkssckaqoe",
    17: "csaqwuryqifavasc",
    18: "qpwyuibvxxmmcpow",
    19: "mvaeruqopkqwddlp",
    20: "kosphprqandkcpma"
}


# Server class
class TestServer(BaseHTTPRequestHandler):

    # Get method
    def do_GET(self):

        # Ignore irrelevant get request
        if self.path == "/favicon.ico":
            return

        # Sleeping delay after each "successful" hit
        sleeping_delay = 0.1

        # HTTP Response
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Try will fail if parameters aren't as described in the homework instructions
        try:

            # User parameters
            user_password = self.path[self.path.find("&password=") + 10: self.path.find("&difficulty")]
            user_difficulty = int(self.path[self.path.find("&difficulty=") + 12:])

            # Stored password for difficulty received
            stored_password = passwords_list[user_difficulty]

            # Checking lengths of passwords
            if len(user_password) == len(stored_password):
                time.sleep(sleeping_delay)
            else:
                self.wfile.write(bytes("0", "utf-8"))
                return

            # Flag for correct password guess
            guessed = True

            # Checking each character of the password received against the DB password
            for i in range(len(stored_password)):
                if user_password[i] == stored_password[i]:
                    time.sleep(sleeping_delay)
                else:
                    guessed = False
                    break

            # Return result
            if guessed is True:
                self.wfile.write(bytes("1", "utf-8"))
            else:
                self.wfile.write(bytes("0", "utf-8"))

        except Exception as e:
            print(e)


if __name__ == "__main__":

    # Server address and port
    server_address = "127.0.0.1"
    server_port = 8080

    # Launch server
    webServer = HTTPServer((server_address, server_port), TestServer)
    print("Server started at address: http://%s:%s" % (server_address, server_port))

    try:

        # Keep server alive
        webServer.serve_forever()

    except KeyboardInterrupt:
        pass
