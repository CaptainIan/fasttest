#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import datetime
import platform
from colorama import init, Fore


if platform.system() != 'Windows':
    init(wrap=True)
init(autoreset=True)

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        pass

    def __write(self, message: str) -> None:
        try:
            self.log_path = os.path.join(self.reports, 'report.log')
            with open(self.log_path, 'a+', encoding='UTF-8') as f:
                f.write(f'{message}\n')
        except:
            pass
        
    def log_info(self, message: str, color: str = '', end = '\n') -> None:

        if not isinstance(message, str): message = str(message)
        date_info: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S INFO :")
        if color:
            print(date_info + color + message, end=end)
        else:
            print(date_info + message, end=end)
        self.__write(date_info + message)

    def log_error(self, message: str, exit: bool = False) -> None:

        if not isinstance(message, str): message = str(message)
        date_error: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ERROR :")
        print(date_error + Fore.RED + message)
        self.__write(date_error + message)
        if exit: os._exit(0)

    def log_print(self, message: str, color: str = '', end = '\n') -> None:

        if color:
            print(color + message, end=end)
        else:
            print(message, end=end)
        self.__write(message)
