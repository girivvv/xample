import tornado.ioloop
import tornado.web
import tornado.httpclient
from tornado import escape
import json

# IP address of the ESP32 server
SERVER_IP = "http://localhost:80"

class StatusHandler(tornado.web.RequestHandler):
    async def get(self):
        client = tornado.httpclient.AsyncHTTPClient()
        try:
            response = await client.fetch(f"{SERVER_IP}/status")
            data = escape.json_decode(response.body)
            self.write({
                "switch_1": data.get('switch1', "unknown"),
                "switch_2": data.get('switch2', "unknown"),
                "switch_3": data.get('switch3', "unknown")
            })
        except Exception as e:
            self.write({"status": "error", "message": str(e)})

class ToggleHandler(tornado.web.RequestHandler):
    async def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
            switch_id = data.get("switch_id")
            state = data.get("state")

            if switch_id not in ["switch_1", "switch_2", "switch_3"]:
                self.write({"status": "error", "message": "Invalid switch_id"})
                return

            toggle_url = f"{SERVER_IP}/set-status"
            client = tornado.httpclient.AsyncHTTPClient()
            payload = {"switch_id": switch_id, "state": state}

            response = await client.fetch(toggle_url, method="POST", body=json.dumps(payload), headers={'Content-Type': 'application/json'})
            response_data = escape.json_decode(response.body)
            self.write({"status": response_data.get('status', 'success')})
        except Exception as e:
            self.write({"status": "error", "message": str(e)})

def make_app():
    return tornado.web.Application([
        (r"/api/get-status", StatusHandler),  # Updated API endpoint for Nginx proxying
        (r"/api/set-status", ToggleHandler),  # Updated API endpoint for Nginx proxying
    ], debug=True)

if __name__ == "__main__":
    app = make_app()
    app.listen(80)  # Tornado backend listens on port 9000
    print("Tornado server running on http://localhost:80")
    tornado.ioloop.IOLoop.current().start()
