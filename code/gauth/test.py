import urllib

from gauth import GauthManager
from gauthService import GauthServiceManager


if __name__ == '__main__':
    # gauth_mgr = GauthManager()
    # print gauth_mgr.get_token()
    # print gauth_mgr.get_token()
    # time.sleep(5)
    # gauth_mgr.stop_server()
    gsuth_service = GauthServiceManager()
    web_in = urllib.urlopen("http://127.0.0.1:7060")
    for line in web_in:
        print line
    web_in = urllib.urlopen("http://127.0.0.1:7060")
    for line in web_in:
        print line
    gsuth_service.stop_server()
