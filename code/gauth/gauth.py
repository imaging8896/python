import socket
import os
import requests
import threading
import time

import BaseHTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re

import envUtils

THIS_DIR = os.path.dirname(__file__)
SERVER_ADDR = (envUtils.get_ip_address("ens160"), 7070)

EMAIL = "hopebaytest1@gmail.com"
PWD = "4nXiC9X6"


class HandleGauth(BaseHTTPRequestHandler):

    def do_GET(self):
        self.gauth_client_html_page = os.path.join(
            THIS_DIR, "gauth_client.html")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(self.gauth_client_html_page, "rb") as f:
            self.wfile.write(f.read())


class HTTPGauthServer(BaseHTTPServer.HTTPServer):

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


class GauthManager(object):

    def __init__(self):
        self.httpd = HTTPGauthServer(SERVER_ADDR, HandleGauth)
        threading.Thread(target=self.httpd.serve_forever,
                         name='thread-gauth-server').start()

    def get_token(self):
        driver = webdriver.Firefox()
        driver.get("http://localhost:7070")
        selenium_gauth_client_html_scrip(driver)
        token = driver.find_element_by_id('token').text
        access_token = driver.find_element_by_id('access_token').text
        driver.close()
        return token, access_token

    def stop_server(self):
        self.httpd.force_stop()

########### private ###########


def selenium_gauth_client_html_scrip(driver):
    elem = driver.find_element_by_class_name("abcRioButtonIcon").click()
    time.sleep(5)   # magic sleep

    handles = driver.window_handles
    for handle in handles:
        driver.switch_to_window(handle)
        if re.search("Google", driver.title):
            google_page = handle
        else:
            original_page = handle

    google_popup_page_script(driver, google_page)

    driver.switch_to_window(original_page)
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "token")))


def google_popup_page_script(driver, page):
    driver.switch_to_window(page)
    insert_email_script(driver)
    insert_pwd_script(driver)
    time.sleep(5)
    submit_approve_script(driver)


def insert_email_script(driver):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "Email")))
    driver.find_element_by_id("Email").send_keys(EMAIL)
    driver.find_element_by_name("signIn").click()


def insert_pwd_script(driver):
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "Passwd")))
    driver.find_element_by_id("Passwd").send_keys(PWD)
    driver.find_element_by_id("signIn").click()


def submit_approve_script(driver):
    if len(driver.window_handles) == 2:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "submit_approve_access")))
        driver.find_element_by_id("submit_approve_access").click()
