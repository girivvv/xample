import json
import tornado.ioloop
import tornado.web

# Store switch state globally for simplicity
switch_state = {
    "switch_1": "off",
    "switch_2": "off",
    "switch_3": "off"
}

class GetStateHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(switch_state))

class HTMLHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class ToggleHandler(tornado.web.RequestHandler):
    def post(self):
        data = json.loads(self.request.body)
        switch_id = data.get("switch_id")
        new_state = data.get("state")

        if switch_id and new_state in ["on", "off"]:
            switch_state[switch_id] = new_state
            self.write({"status": "success", "switch_state": switch_state[switch_id]})
        else:
            self.set_status(400)
            self.write({"status": "error", "message": "Invalid payload"})

class NotFoundHandler(tornado.web.RequestHandler):
    def prepare(self):
        self.set_status(404)
        self.write({"error": "Route not found"})

def make_app():
    return tornado.web.Application([
        (r"/get_state", GetStateHandler),
        (r"/", HTMLHandler),
        (r"/toggle", ToggleHandler),
        (r".*", NotFoundHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(9000)
    print("Tornado server running on port 9000...")
    tornado.ioloop.IOLoop.current().start()
