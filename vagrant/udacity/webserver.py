from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from session import session
from database_setup import Restaurant


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith("/restaurants/new"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message_new = ""
            message_new += "<html><body><h1>New Restaurants</h1></body></html>"
            message_new += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
            message_new += "<input name='newRestaurantName' type='text', placeholder='New Restaurant Name'>"
            message_new += "<input type='submit' value='Create'>"
            self.wfile.write(bytes(message_new, 'utf-8'))
            return

        if self.path.endswith("/restaurants"):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = ""
            message += "<html><body><h1>Restaurants</h1></body></html>"
            for res in session.query(Restaurant).all():
                print(type(res.name))
                if type(res.name) == bytes:
                    res.name = res.name.decode("utf-8")
                message += ("<p>" + res.name +
                            "<br><a href ='#'>Edit</a>"
                            "<br><a href ='#'>Delete</a>"
                            "</p>")

            message += " <button type='button'><a href='/restaurants/new'>New Restaurant!</button>"

            """message += ('''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me 
            to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>''')"""
            message += "</body></html>"
            self.wfile.write(bytes(message.encode('utf-8')))
            print(message)
            return
        else:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):

        if self.path.endswith("/restaurants/new"):


            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            print(ctype, pdict)
            if ctype == 'multipart/form-data':
                print(type(self.rfile), type(pdict))
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('newRestaurantName')
                newRestaurant = Restaurant(name=messagecontent[0].decode("utf-8"))
                session.add(newRestaurant)
                session.commit()
                print(messagecontent)

            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.send_header('Location', 'restaurants')
            self.end_headers()




def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("stopping server")
        server.socket.close()


if __name__ == "__main__":
    main()
