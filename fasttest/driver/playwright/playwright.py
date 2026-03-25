import time
import platform
from playwright.sync_api import sync_playwright
from xffasttest.driver.playwright.request import Request

DEFAULT_WINDOW = 'DEFAULT_WINDOW'
NEW_WINDOW = 'NEW_WINDOW'
SYSTEM_NAME = platform.system()
SCRIPT_TAG = 'function addClickEvent(t){t.target.addEventListener("click",function(t){lastElement&&(lastElement.style.setProperty("background-color",lastElementColor),lastElementColor=t.target.style.backgroundColor),t.target.style.setProperty("background-color","rgba(204, 51, 51, 0.5)"),lastElement=t.target})}lastElement=null,lastElementColor=null,window.onmousemove=function(t){console.log(t),addClickEvent(t)}'


class PlaywrightDriver(object):

    def __init__(self) -> None:
        playwright = sync_playwright().start()
        self.driver: object = None
        self._playwright: object = playwright
        self._browser: object = None
        self._browser_context: object = None
        self._browser_contexts: dict = {}
        self.config: dict = {}
        self.request = Request()

    def _create_browser(self, config: dict) -> object:
        browser_name = config.browser_name or 'chromium'
        headless = config.headless
        slow_mo = config.slow_mo
        downloads_path = config.downloads_path
        browser = self._playwright[browser_name].launch(headless=headless,
                                                       downloads_path=downloads_path,
                                                       slow_mo=slow_mo)
        return browser

    def _create_context(self, config: dict) -> object:
        base_url = config.base_url
        ignore_https_errors = config.ignore_https_errors
        java_script_enabled = config.java_script_enabled
        bypass_csp = config.bypass_csp
        viewport = config.viewport
        locale = config.locale or 'zh-CN'
        extra_http_headers = config.extra_http_headers
        record_video_dir = config.record_video_dir
        user_agent = config.user_agent
        context = self._browser.new_context(ignore_https_errors=ignore_https_errors,
                                            java_script_enabled=java_script_enabled,
                                            bypass_csp=bypass_csp,
                                            base_url=base_url,
                                            viewport=dict(viewport) if viewport else None,
                                            locale=locale,
                                            extra_http_headers=extra_http_headers,
                                            record_video_dir=record_video_dir,
                                            user_agent=user_agent)
        return context

    def _check_elements(self, selector: str) -> bool:
        elements = self._browser_context.page.query_selector_all(selector)
        for element in elements:
            if element.is_visible() and element.is_enabled():
                break
        else:
            return False
        return True

    def _timed_polling(self, condition_func, selector: str, timeout=10):
        start_time = time.time()
        while True:
            if condition_func(selector):
                break
            time.sleep(0.2)
            if timeout is not None and ((time.time() - start_time) * 1000) > timeout * 1000:
                break

    def browser(self, config: dict) -> None:
        browser_config: dict = config.browser
        self._browser = self._create_browser(browser_config)
        self.config = config

    def window(self, key: str = DEFAULT_WINDOW, config: dict = {}) -> None:
        context_config: dict = config.get('context', {})
        if key not in self._browser_contexts:
            self._browser_context = self._create_context(context_config)
            self._browser_contexts.update({key: self._browser_context})
        else:
            self._browser_context = self._browser_contexts[key]

    def page(self, url: str) -> None:
        page = self._browser_context.new_page()
        self._browser_context.page = page
        self._browser_context.page.on("request", self.request.handle_request)
        self._browser_context.page.on("response", self.request.handle_response)
        self.goto(url)

    def goto(self, url: str) -> None:
        try:
            self._browser_context.page.goto(url)
        except Exception:
            self._browser_context.page.goto(url)
        self._browser_context.page.wait_for_load_state()
        self._browser_context.page.add_script_tag(content=SCRIPT_TAG)

    def set_headers(self, headers: dict) -> None:
        self._browser_context.set_extra_http_headers(headers=headers)

    def reload(self) -> None:
        self._browser_context.page.reload()

    def query_selector_all(self, selector: str, timeout: int) -> list:
        # try:
        #     self._browser_context.page.wait_for_selector(selector, timeout=10000)
        # except:
        #     pass
        self._timed_polling(self._check_elements, selector, timeout)

        return self._browser_context.page.query_selector_all(selector)

    def click(self, element) -> None:
        element.click(force=True)

    def dblclick(self, element) -> None:
        element.dblclick(force=True)

    def check(self, element) -> None:
        element.check()

    def input(self, text: str, clear: bool = False) -> None:
        if clear:
            self.keyboard_press('Control+A')
            self.keyboard_press('Delete')
        self._browser_context.page.keyboard.insert_text(text)

    def waitfor(self, element, state: str)  -> None:
        element.wait_for_element_state(state)

    def hover(self, element) -> None:
        element.hover()

    def get_attribute(self, name: str, element) -> None:
        return element.get_attribute(name)

    def get_text(self, element) -> None:
        return element.text_content()
    
    def mouse_click(self, x: float, y: float, button: str = 'left') -> None:
        self._browser_context.page.mouse.click(x, y, button=button)

    def mouse_dblclick(self, x: float, y: float, button: str = 'left') -> None:
        self._browser_context.page.mouse.dblclick(x, y, button=button)

    def keyboard_press(self, key: str) -> None:
        if SYSTEM_NAME.lower() == 'darwin':
            key = key.replace('Control', 'Meta')
        self._browser_context.page.keyboard.press(key)

    def mouse_move(self, x: float, y: float) -> None:
        self._browser_context.page.mouse.move(x, y)

    def mouse_down(self) -> None:
        self._browser_context.page.mouse.down()

    def mouse_up(self) -> None:
        self._browser_context.page.mouse.up()

    def upload(self, element, file: str) -> None:
        with self._browser_context.page.expect_file_chooser() as fc_info:
            element.click()
        file_chooser = fc_info.value
        file_chooser.set_files(file)

    def download(self, element, file: str) -> None:
        with self._browser_context.page.expect_download() as download_info:
            element.click()
        download = download_info.value
        # wait for download to complete
        download.save_as(file)
        return file

    def cookies(self, url: str) -> list:
        if url:
            return self._browser_context.cookies(url)
        return self._browser_context.cookies()

    def add_cookies(self, cookies: list) -> None:
        self._browser_context.add_cookies(cookies)

    def delete_cookies(self) -> None:
        self._browser_context.clear_cookies()

    def evaluate(self, script: str) -> None:
        return self._browser_context.page.evaluate(script)
    
    def add_init_script(self, script: str = None, file_path: str = None) -> None:
        if script: self._browser_context.add_init_script(script)
        if file_path: self._browser_context.add_init_script(path=file_path)

    def back(self) -> None:
        self._browser_context.page.go_back()

    def video(self) -> str:
        return self._browser_context.page.video.path()

    def url(self) -> str:
        return self._browser_context.page.url

    def title(self) -> str:
        return self._browser_context.page.title

    def iframe(self, domain: str):
        self._browser_context.page.frame(url=domain)
    
    def set_headers(self, headers: dict):
        self._browser_context.page.set_extra_http_headers(headers)

    def close(self) -> str:
        self._browser_context.page.close()
        self._browser_context.close()
        self._browser.close()
        self._browser_contexts.clear()

    def stop(self) -> None:
        self._playwright.stop()
        self._browser_contexts.clear()

    def screenshot(self, path: str, full_page: bool = True) -> None:
        self._browser_context.page.screenshot(path=path,
                                              full_page=full_page)

    def devices(self, device_name: str) -> dict:
        return self._playwright.devices[device_name]
