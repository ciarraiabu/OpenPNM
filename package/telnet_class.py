from log import Log
from constants import *

import os
import sys
import telnetlib
import re
import getpass
import socket
import time


class Tnet():

    PROMPT_CHECK_TIMEOUT_SEC = 2
    NON_LOGIN_PROMPTS = [b">>>", b"^", b"@", b"$", b"#", b"%"]
    CONNECTION_PROMPT = b">>>"
    LOGIN_PROMPTS = [b"ogin:", b"assword:"]
    READ_UNTIL_WAIT_TIMEOUT = 5

    SESSION_PROMPT_CHG = "export PS1=\'>>>\';"
    REVERT_SESSION_PROMPT = "source ~/.bashrc"
    MAX_CONNECITON_TRIES = 5
    connStatus = STATUS_OK

    TELNET_AVALIABLE_PORTS = [8008, 8009]

    def __init__(self, host, user, pw, port=23):

        connectTries = 1

        while (connectTries < Tnet.MAX_CONNECITON_TRIES):

            try:
                self.conn = telnetlib.Telnet(host, port)

            except:
                Log.error("Unable to Connect to: " + host + " - Retry count(" + str(connectTries) + ")")
                self.connStatus = STATUS_NOK

            else:
                self.connStatus = STATUS_OK
                break

            connectTries += 1
            time.sleep(1)

        if self.connStatus is STATUS_NOK:
            return

        if Log.isDebugEnable():
            self.conn.set_debuglevel(1)

        self.conn.write(b"\r\r\r")

        # Check for Type of Prompt (Already logged in Terminal Server)
        rtn = self.conn.expect( self.LOGIN_PROMPTS,
                                self.PROMPT_CHECK_TIMEOUT_SEC)

        Log.debug("Prompt Detection: " + str(rtn))

        # Login Prompt (Could be login or password prompt)
        if rtn[0] == 0:
            Log.debug("LOGIN PROMPT DETECTED")
            self.conn.write(bytes(user + "\r", 'utf-8'))
            self.conn.read_until(b"assword: ")
            self.conn.write(bytes(pw + "\r", 'utf-8'))
        else:
            Log.debug("SHELL PROMPT DETECTED")

        self.cmd_Rtn(self.SESSION_PROMPT_CHG)
        self.clearPrompt()
        Log.debug("ClearBuffer: " + self.clearBuffer())

    def __del__(self):
        Log.debug("Destroying Tnet Object")

    def status(self):
        return self.connStatus

    def cmd(self, cmd):
        Log.debug("CMD: " + cmd)
        self.conn.write(bytes(cmd, 'utf-8'))

    def cmd_Rtn(self, cmd):
        Log.debug("CMD: " + cmd)
        self.conn.write(bytes(cmd + "\r\n", 'utf-8'))

    def sendRtn(self):
        Log.debug("SEND-RTN:")
        return self.conn.write(bytes("\r\n", 'utf-8'))

    def read(self):
        Log.debug("Getting Telnet Response, waiting for : " + str(self.CONNECTION_PROMPT))

        return self.conn.read_until(self.CONNECTION_PROMPT,
                                    self.READ_UNTIL_WAIT_TIMEOUT).decode('ascii')

    def readGetList(self, forceRetrySearch=""):
        Log.debug("Getting Telnet Responses, waiting for : " + str(self.CONNECTION_PROMPT))

        if forceRetrySearch:
            rtn = self.read()
            while (str(rtn).find(forceRetrySearch) is -1):
                time.sleep(1)
                Log.debug("Checking for Force Retry Search Response...")
                rtn = self.read()
            Log.debug("Force Retry Search Found: " + str(rtn))
            return rtn.split("\r\n")

        return self.conn.read_until(self.CONNECTION_PROMPT,
                                    self.READ_UNTIL_WAIT_TIMEOUT).decode('ascii').split("\r\n")

    def readAll(self):
        return self.conn.read_all().decode('ascii')

    def clearBuffer(self):
        return self.conn.read_very_lazy().decode('ascii')
    
    def clearPrompt(self):
        self.sendRtn()
        r = self.read()
        Log.debug("ClearPrompt: " + r)

    def close(self):
        self.cmd_Rtn(self.REVERT_SESSION_PROMPT)
        self.sendRtn()
        self.conn.get_socket().shutdown(socket.SHUT_WR)
        self.conn.close()
        self.connStatus = STATUS_NOK
        return STATUS_OK
