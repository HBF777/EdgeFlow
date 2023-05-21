# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/21 12:28
@Auth ： 曾颖
@File ：communicate_gui.py
@IDE ：PyCharm
"""

from core.tools import Logger, ConfigParser
from tornado import web, httpserver, ioloop, websocket
from PIL import Image
import base64
import webbrowser
from .haiKang.main import HKCam
import cv2
import numpy as np

def get_image_dataurl():
    JPEG_HEADER = "data:image/jpeg;base64,"
    # 获取摄像头数据
    hasMoreFrame, frame = HKCam().read()
    r, buf = cv2.imencode(".jpeg", frame)
    dat = Image.fromarray(np.uint8(buf)).tobytes()
    img_date_url = JPEG_HEADER + str(base64.b64encode(dat))[2:-1]

    data = [{
        "img_date_url": img_date_url,
    }]

    return data

class VideoHandler(websocket.WebSocketHandler):
    # 允许跨域请求
    def check_origin(self, origin):
        return True
    # 处理接收数据
    def on_message(self, message):
        self.write_message({"data": get_image_dataurl()})

def web_go():
    app = web.Application(handlers=[(r'/camera', VideoHandler)])
    http_server = httpserver.HTTPServer(app)
    http_server.listen(port=8088, address='127.0.0.1')
    print("URL: http://{}:{}/".format('127.0.0.1', 8088))
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        ioloop.IOLoop.instance().stop()