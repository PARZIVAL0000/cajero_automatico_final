#!/usr/bin/env python
#_*_ coding:utf-8 _*_ 

from cajero import Login

def main():
    Login.login()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("[>] Saliendo Del Programa...")
        exit()