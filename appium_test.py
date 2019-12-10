"""
pytest -v -s appium_test.py

Requirements: python 3.8, pytest, appium, android adb + running emulator, dependencies

"""

import pytest
from appium import webdriver
from time import sleep
import socket
from urllib.request import urlopen
import re
from dns_check import check_DNS

class TestSuite:
    
    app = 'com.hmh.api'

    @pytest.fixture(scope="module") 
    def setup(self):
        """Setup for the test"""
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '10'
        desired_caps['deviceName'] = '$ Pixel_Test'
        # Since the app is already installed launching it using package and activity name
        desired_caps['app'] = 'C:\\APIDemos.apk'
        desired_caps['appPackage'] = self.app
        desired_caps['appActivity'] = '.ApiDemos'     
        # Adding appWait Activity since the activity name changes as the focus shifts to the ATP WTA app's first page
        #desired_caps['appWaitActivity'] = '.app.Animation.BouncingBalls'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        # install app from local apk - seems to be done with desired_caps['app']
        # self.driver.install_app('C:\\APIDemos.apk')
        yield
        # remove app
        self.driver.remove_app(self.app)
        self.driver.quit()
        

    def test_android_drafts(self, setup):

        #self.driver.implicitly_wait(10)
        #sleep(10)

        # click on permissions and outdated drivers warning
        self.driver.find_element_by_xpath("//android.widget.Button[@resource-id='com.android.permissioncontroller:id/continue_button']").click()

        sleep(2)

        self.driver.find_element_by_xpath("//android.widget.Button[@resource-id='android:id/button1']").click()

        self.driver.find_element_by_xpath("//android.widget.TextView[@resource-id='android:id/text1']").click()

        # From list of options available click on Accessibility Services by finding element using uiautomator
        access = self.driver.find_element_by_android_uiautomator('new UiSelector().text("Accessibility Service")')
        access.click()

        # Networking checks

        # check ip address using python native
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print('\nInternal IP adress: '+str(s.getsockname()[0])+'\n')
        s.close()

        # check ip address using auxilary web service
        data = str(urlopen('http://checkip.dyndns.com/').read())  # website can be also used to check IP on mobile browser
        # data = '<html><head><title>Current IP Check</title></head><body>Current IP Address: 65.96.168.198</body></html>\r\n'
        print('\nExternal IP adress: ', re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1),'\n')

        # check ip addresses for hostname/url
        print('IP addresses for epam.com: ', list(map(lambda x: x[4][0], socket.getaddrinfo('www.epam.com.',22,type=socket.SOCK_STREAM))))

        # lock and unlock the device
        self.driver.lock()
        sleep(2)
        self.driver.unlock()

        # Check caption text
        expected_text = 'Accessibility/Accessibility Service'
        elmnt = self.driver.find_element_by_xpath("//android.widget.TextView")
        assert expected_text == elmnt.get_attribute('text')

        # run commands on mobile terminal
        result = self.driver.execute_script('mobile: shell', { 'command': 'getprop | grep dns',   # 'ip addr show | grep inet',
                                                               'includeStderr': True,
                                                               'timeout': 10000 })
        print(result)

        # # performance of the app
        # self.driver.activate_app('com.android.chrome')
        # self.driver.press_keycode(3)  # press HOME_KEY
        # sleep(5)
        # perf_stats = self.driver.get_performance_data_types()
        # for stat in perf_stats:
        #     print('\n', stat, ' ', self.driver.get_performance_data('com.android.chrome', stat, 5))
        # self.driver.terminate_app('com.android.chrome')