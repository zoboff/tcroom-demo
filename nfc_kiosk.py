# coding=utf8
import string
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import screeninfo
import serial
import re
import threading
import queue
import tcroom
import asyncio
import time
from enum import Enum

ContactsNumber: int = 3
DeltaTime = 1
HeightPercentage: float = 0.8
WidthPercentage: float = 0.7
PleaseLoginButtonPercentage: float = 0.25
SpacingPercentage: float = 0.15
RegexForCardNumber = rb'[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}'
Ip: str = "127.0.0.1"
Pin: str = "123"


class State(Enum):
    Unknown = 0
    NeedLogin = 1
    Normal = 2
    Calling = 3


dictData = {
    'DA-8B-25-B4':
        {
            "ContactList":
                [
                    {
                        'DisplayName': 'Contact123',
                        'Login2Call': 'novikov@team.trueconf.com'
                    },
                    {
                        'DisplayName': 'Contact2',
                        'Login2Call': 'novikov@team.trueconf.com'
                    },
                    {
                        'DisplayName': 'Contact3',
                        'Login2Call': 'novikov@team.trueconf.com'
                    }
                ]
        },
    'CA-C7-37-B3':
        {
            "ContactList":
                [
                    {
                        'DisplayName': 'Contact4',
                        'Login2Call': 'novikov@team.trueconf.com'
                    },
                    {
                        'DisplayName': 'Contact5',
                        'Login2Call': 'novikov@team.trueconf.com'
                    },
                    {
                        'DisplayName': 'Contact6',
                        'Login2Call': 'novikov@team.trueconf.com'
                    }
                ]
        }
}


def threadFunction_catchCardNumber(callbackQueue, stringFromCOMPort, appLayout) -> bool:
    result = re.search(RegexForCardNumber, stringFromCOMPort)
    if result is not None:
        callbackQueue.put(result.group().decode('UTF-8'))
        # It is necessary to work with the layout ONLY from the main thread
        print(result.group().decode('UTF-8'))
        QMetaObject.invokeMethod(appLayout, "setupButton", Qt.QueuedConnection)

    return False


def threadFunction_ListeningComPort(callbackQueue, appLayout):
    ser = serial.Serial(
        # Look where to which port the NSF reader is connected it was be ttyUSB0 or ttyUSB1
        # To check this, do in command line
        # cd /dev
        # ls ttyUSB* <----- need this number
        # And С‹ee what number is indicated at the end of the remaining line
        port='/dev/ttyUSB0',
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
    while True:
        stringFromCOMPort = ser.readline()
        threadFunction_catchCardNumber(callbackQueue, stringFromCOMPort, appLayout)


class ButtonWithInfo(QPushButton):

    def __init__(self, textButton, callId: string):
        super().__init__(textButton)
        self.callId = callId


class Button2Call(QWidget):
    previousCard: str

    def __init__(self, monitor: int, callbackQueue: queue):
        super().__init__()

        self.layout = None
        self.previousCard = "None"
        self.previousStateFromRoom = 0
        self.room = None
        self.callback_queue = callbackQueue
        if monitor >= len(screeninfo.get_monitors()) or monitor < 0:
            monitor = 0
        self.monitor = screeninfo.get_monitors()[monitor]
        self.state = State.Unknown
        self.lastTimeNFCCallBack = 0
        self.initUI()

    def initUI(self):
        # Setting layout
        self.layout = QVBoxLayout(self)
        self.setupButton()
        # Position
        self.setPosition()

        # Frameless window
        # | Qt.WindowStaysOnTopHint
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # Show
        self.show()

    def connectToRoom(self):
        async def on_change_state(state: int):
            print(f"New state is {state}")
            QMetaObject.invokeMethod(layout, "setButtonFromNewState", Qt.QueuedConnection)
            await asyncio.sleep(0.3)

        async def on_method(method, response):
            print(f"Method: {method}")
            print(f"  Response: {response}")
            await asyncio.sleep(0.3)

        # ==========================================================
        while True:
            try:
                print("Connecting to TrueConf Room...")
                self.room = tcroom.make_connection(pin=Pin, room_ip=Ip,
                                                   cb_OnChangeState=on_change_state, cb_OnMethod=on_method,
                                                   debug_mode=True)
                print("Successfully connected")
                return True
            # try again
            except tcroom.ConnectToRoomException as e:
                print(f'ConnectToRoomException.')
                print('Try again...')
                time.sleep(1)
                continue  # connection again
            #
            except Exception as e:
                print(f'Exception "{e.__class__.__name__}" in {__file__}:{sys._getframe().f_lineno}: {e}')
                return False
            #
            except KeyboardInterrupt:
                print('Exit by the Ctrl + c')
                return False
        # ==========================================================
        # end of while
        # ==========================================================

    @pyqtSlot()
    def setButtonFromNewState(self):
        newState = self.room.getAppState()
        if self.previousStateFromRoom == newState:
            return
        else:
            self.previousStateFromRoom = newState
        if newState > 3:
            if self.state != State.Calling:
                self.callingState()
        if newState == 3:
            if self.state != State.Normal:
                if self.previousCard == "":
                    self.loginState()
                else:
                    self.normalState(dictData[self.previousCard]["ContactList"])
        if newState < 3:
            if self.state != State.NeedLogin:
                self.loginState()

    @pyqtSlot()
    def setupButton(self, cardNum: str = ""):
        # Try to get card from com port
        try:
            cardNum = self.callback_queue.get(False)
            if time.time() - self.lastTimeNFCCallBack < DeltaTime:
                cardNum = ""
            self.lastTimeNFCCallBack = time.time()
            callback_queue.queue.clear()
        except queue.Empty:
            print('Not from NFC call')

        # If we get card from COM port compare with the previous using card
        # and if the cards are the same disconnect from Room
        if cardNum == self.previousCard:
            if self.room.getAppState() > 3:
                self.room.hangUp()
            self.loginState()
            return
        else:
            if self.state == State.Normal or self.state == State.Calling:
                print("Please logout with old card")
                return

        # Check on cardNum in dictionary
        # if we found one make connect to Room and display call button
        if cardNum in dictData:
            self.previousCard = cardNum
            self.connectToRoom()
        else:
            self.loginState()
            return
        if self.room.getAppState() > 3:
            self.callingState()
            return

        layoutList = dictData[cardNum]["ContactList"]
        self.normalState(layoutList)

    def normalState(self, layoutList: list):
        self.clearLayout()
        self.state = State.Normal
        for fillData in layoutList:
            displayName = fillData['DisplayName']
            login2call = fillData['Login2Call']
            button = ButtonWithInfo(displayName, login2call)
            button.setStyleSheet("background-color: #0097a7;"
                                 "text-align: left;"
                                 "padding: 10px;"
                                 "color: white;"
                                 "font: bold 148px;")
            button.setIcon(QIcon('ic_addressbook_inv.png'))
            sizeIcon: int = round(button.geometry().height() * 0.3)
            button.setIconSize(QSize(sizeIcon, sizeIcon))
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(self.on_click)
            self.layout.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(button)

    def loginState(self):
        self.clearLayout()
        if self.state == State.Calling:
            self.room.hangUp()
        if self.room is not None and self.room.isConnected():
            self.room.disconnect()
        self.previousCard = ""
        self.state = State.NeedLogin
        button = QPushButton("Приложите пропуск")
        button.setStyleSheet("background-color: #0097a7;"
                             "padding: 10px;"
                             "color: white;"
                             "font: bold 148px;")
        button.setEnabled(False)
        width: int = round(self.monitor.width * WidthPercentage)
        height: int = round(self.monitor.height * PleaseLoginButtonPercentage)
        leftCoord: int = self.monitor.x + round((self.monitor.width - width) / 2)
        topCoord: int = self.monitor.y + round((self.monitor.height - height) / 2)
        button.setGeometry(leftCoord, topCoord, width, height)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(button)

    def callingState(self):
        self.clearLayout()
        self.state = State.Calling
        button = QPushButton("HangUp")
        button.setStyleSheet("background-color: red;"
                             "padding: 10px;"
                             "color: white;"
                             "font: bold 148px;")
        width: int = round(self.monitor.width * WidthPercentage)
        height: int = round(self.monitor.height * PleaseLoginButtonPercentage)
        leftCoord = self.monitor.x + round((self.monitor.width - width) / 2)
        topCoord = self.monitor.y + round((self.monitor.height - height) / 2)
        button.setGeometry(leftCoord, topCoord, width, height)
        button.clicked.connect(self.on_hangup_click)
        self.layout.setAlignment(Qt.AlignBottom)
        self.layout.addWidget(button)

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def setPosition(self):
        # calc window size & position
        width: int = round(self.monitor.width * WidthPercentage)
        height: int = round(self.monitor.height * HeightPercentage)
        leftCoord: int = self.monitor.x + round((self.monitor.width - width) / 2)
        topCoord: int = self.monitor.y + round((self.monitor.height - height) / 2)

        # set position
        self.setGeometry(leftCoord, topCoord, width, height)

        # set spacing between buttons
        self.layout.setSpacing(round(self.monitor.height * SpacingPercentage))

    @pyqtSlot()
    def on_click(self):
        self.room.call(self.sender().callId)
        self.state = State.Calling
        print(self.sender().callId)
        self.callingState()

    @pyqtSlot()
    def on_hangup_click(self):
        self.room.hangUp()

        if self.previousCard == "":
            self.room.disconnect()
            self.state = State.NeedLogin
            self.needLoginState()
        else:
            self.normalState(dictData[self.previousCard]["ContactList"])
            self.state = State.Normal


if __name__ == '__main__':
    app = QApplication(sys.argv)
    callback_queue = queue.Queue()
    layout = Button2Call(monitor=0, callbackQueue=callback_queue)
    callbackThread = threading.Thread(target=threadFunction_ListeningComPort, args=(callback_queue, layout,),
                                      daemon=True)
    callbackThread.start()
    sys.exit(app.exec_())
