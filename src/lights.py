# Turn the lights off and on
#
# Makes a call to an X10 Pyro server connected to an X10 Firecracker (rs-232):
# https://github.com/cmang/x10-pyro
#
# X10 Pyro format:
# http://url:5000/<house>/<id>/OFF
# http://url:5000/<house>/<id>/ON
#
# eg, for house C, light 2:
# http://10.0.0.99:5000/c/2/OFF

#import requests
import urllib.request

class LightsX10():
    def __init__(self):
        self.house = 'c'
        self.main_light_id = '1'
        self.url = f'http://10.0.0.99:5000/{self.house}/{self.main_light_id}/'

    def on(self):
        print(f"X10 Pyro: Turning {self.house}/{self.main_light_id} ON")
        url = self.url + 'ON'
        print(f"Calling url: {url}")
        #r = requests.post(url)
        try:
            with urllib.request.urlopen(url) as response:
                   r = response.read()
        except Exception as E:
            print(f"There was an error opening the URL: {E}")
        print(f"X10 Pyro: Results: {r}")
        return True

    def off(self):
        print(f"X10 Pyro: Turning {self.house}/{self.main_light_id} OFF")
        url = self.url + 'OFF'
        print(f"Calling url: {url}")
        #r = requests.post(url)
        try:
            with urllib.request.urlopen(url) as response:
                   r = response.read()
        except Exception as E:
            print(f"There was an error opening the URL: {E}")
        print(f"X10 Pyro Results: {r}")
        return True
