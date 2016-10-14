import socket
import os
import threading
import xmlrpclib
import BaseHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from selenium import webdriver

from gauth import GauthManager
import envUtils

THIS_DIR = os.path.dirname(__file__)
SERVER_ADDR = (envUtils.get_ip_address("ens160"), 7060)


class HandleRequest(BaseHTTPRequestHandler):

    def do_GET(self):
        self.gauth_client_html = os.path.join(THIS_DIR, "gauth_client.html")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        gauth_server = GauthManager()
        token, access_token = gauth_server.get_token()
        gauth_server.stop_server()
        self.wfile.write(access_token)


class HTTPGauthServiceServer(BaseHTTPServer.HTTPServer):

    def server_bind(self):
        BaseHTTPServer.HTTPServer.server_bind(self)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.stopped = False

    def serve_forever(self):
        while not self.stopped:
            self.handle_request()

    def force_stop(self):
        self.server_close()
        self.stopped = True
        self.create_dummy_request()

    def create_dummy_request(self):
        driver = webdriver.Firefox()
        driver.get("http://{0}:{1}".format(*self.server_address))
        driver.close()


class GauthServiceManager(object):

    def __init__(self):
        self.httpd = HTTPGauthServiceServer(SERVER_ADDR, HandleRequest)
        threading.Thread(target=self.httpd.serve_forever,
                         name='thread-gauth-service-server').start()

    def stop_server(self):
        self.httpd.force_stop()
