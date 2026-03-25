import os
import json
import time
import pyperclip
from xffasttest.common import action
from xffasttest.driver.selector import selector_formatting
from xffasttest.driver.playwright import playwright_driver


class Driver(object):

    def __init__(self) -> None:
        pass

    @staticmethod
    @action
    def browser(config: dict = {}) -> None:
        playwright_driver.browser(config)

    @staticmethod
    @action
    def window(key: str = '', config: dict = {}) -> None:
        playwright_driver.window(key=key, config=config)

    @staticmethod
    @action
    def set_headers(headers: dict = {}) -> None:
        playwright_driver.set_headers(headers)

    @staticmethod
    @action
    def reload() -> None:
        playwright_driver.reload()

    @staticmethod
    @action
    def page(url: str) -> None:
        playwright_driver.page(url=url)

    @staticmethod
    @action
    def goto(url: str) -> None:
        playwright_driver.goto(url=url)

    @staticmethod
    def get_element(selector: str, index: int = 0, options: dict = {}) -> None:
        visible_elements = Driver.get_elements(selector, options)
        try:
            return visible_elements[index]
        except:
            raise Exception(f'waiting for locator(selector="{selector}", index={index}) to be visible')

    @staticmethod
    def get_elements(selector: str, options: dict = {}) -> None:
        selector = selector_formatting(selector, options)
        timeout = options.get('timeout', 10)
        elements = playwright_driver.query_selector_all(selector, timeout)
        visible_elements = [element for element in elements if element.is_visible()]
        return visible_elements

    @staticmethod
    @action
    def click(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        playwright_driver.click(element=element)
        time.sleep(0.5)

    @staticmethod
    @action
    def dblclick(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        playwright_driver.dblclick(element=element)

    @staticmethod
    @action
    def check(selector: str, index: int = 0, options: dict = {}) -> None:
        Driver.get_element(selector=selector, index=index, options=options)

    @staticmethod
    @action
    def not_exist(selector: str, index: int = 0, options: dict = {}) -> None:
        try:
            options.update({'timeout': 3 })
            visible_elements = Driver.get_elements(selector, options)
            visible_elements[index]
            return False
        except:
            return True

    @staticmethod
    @action
    def exist(selector: str, index: int = 0, options: dict = {}) -> None:
        try:
            visible_elements = Driver.get_elements(selector, options)
            visible_elements[index]
            return True
        except:
            return False

    @staticmethod
    @action
    def waitfor(state: str, selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        playwright_driver.waitfor(element=element, state=state)

    @staticmethod
    @action
    def input(text: str, clear: bool = False) -> None:
        playwright_driver.input(text=text, clear=clear)

    @staticmethod
    @action
    def hover(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        playwright_driver.hover(element)

    @staticmethod
    @action
    def get_attribute(name: str, selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        return playwright_driver.get_attribute(name, element)

    @staticmethod
    @action
    def get_text(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        return playwright_driver.get_text(element)

    @staticmethod
    @action
    def keyboard_press(key: str) -> None:
        playwright_driver.keyboard_press(key)

    @staticmethod
    @action
    def mouse_click(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        bounding_box = element.bounding_box()
        x, y, width, height = bounding_box.values()
        offset_x = options.get('x', 0)
        offset_y = options.get('y', 0)
        button =  options.get('button', 'left')
        playwright_driver.mouse_click(x + offset_x, y + offset_y, button)

    @staticmethod
    @action
    def mouse_dblclick(selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index, options=options)
        bounding_box = element.bounding_box()
        x, y, width, height = bounding_box.values()
        offset_x = options.get('x', 0)
        offset_y = options.get('y', 0)
        button =  options.get('button', 'left')
        playwright_driver.mouse_dblclick(x + offset_x, y + offset_y, button)

    @staticmethod
    @action
    def mouse_move(x: float, y: float) -> None:
        playwright_driver.mouse_move(x, y)

    @staticmethod
    @action
    def mouse_down() -> None:
        playwright_driver.mouse_down()

    @staticmethod
    @action
    def mouse_up() -> None:
        playwright_driver.mouse_up()

    @staticmethod
    @action
    def upload(file_path: str, selector: str, index: int = 0, options: dict = {}) -> None:
        element = Driver.get_element(selector=selector, index=index)
        playwright_driver.upload(element=element, file=file_path)

    @staticmethod
    @action
    def download(file_path: str, selector: str, index: int = 0, options: dict = {}) -> str:
        element = Driver.get_element(selector=selector, index=index)
        return playwright_driver.download(element=element, file=file_path)

    @staticmethod
    @action
    def cookies(url: str = None) -> list:
        return playwright_driver.cookies(url)

    @staticmethod
    @action
    def add_cookies(cookies: list) -> None:
        playwright_driver.add_cookies(cookies)

    @staticmethod
    @action
    def delete_cookies() -> None:
        playwright_driver.delete_cookies()

    @staticmethod
    @action
    def back() -> None:
        playwright_driver.back()

    @staticmethod
    @action
    def url() -> None:
        return playwright_driver.url()

    @staticmethod
    @action
    def title() -> None:
        return playwright_driver.title()

    @staticmethod
    @action
    def evaluate(script: str) -> None:
        return playwright_driver.evaluate(script)

    @staticmethod
    @action
    def add_init_script(script: str = None, file_path: str = None) -> None:
        playwright_driver.add_init_script(script, file_path=file_path)

    @staticmethod
    @action
    def sleep(s: int) -> None:
        time.sleep(s)

    @staticmethod
    @action
    def iframe(domain: str):
        playwright_driver.iframe(domain)

    @staticmethod
    @action
    def set_headers(headers: dict):
        playwright_driver.set_headers(headers)

    @staticmethod
    @action
    def paste():
        clipboard_content = pyperclip.paste()
        return clipboard_content

    @staticmethod
    def close() -> None:
        playwright_driver.close()

    @staticmethod
    @action
    def screenshot(path: str, full_page: bool = True) -> None:
        playwright_driver.screenshot(path=path, full_page=full_page)

    @staticmethod
    def video() -> str:
        return playwright_driver.video()

    @staticmethod
    def save_request(domains: list = []) -> str:

        request_list = playwright_driver.request.request_list

        if not domains:
            return json.dumps(request_list)
        else:
            _domains = [domain for _domains in domains for domain in _domains]
            data = []
            for request in request_list:
                for domain in _domains:
                    if domain in request['url']:
                        data.append(request)

            return json.dumps(data)

    @staticmethod
    @action
    def get_response(url: str, index: int = 5) -> dict:
        while index:
            request_list = playwright_driver.request.request_list
            request_list.reverse()
            for request in request_list:
                if url in request.get('url', ''):
                    return request
            time.sleep(1)
            index -= 1

    @staticmethod
    def stop() -> None:
        playwright_driver.stop()

    @staticmethod
    def devices(device_name: str) -> dict:
        return playwright_driver.devices(device_name)