# -*- coding: utf-8 -*-
"""
@Time ： 2023/5/7 17:04
@Auth ： 曾颖
@File ：main.py
@IDE ：PyCharm
"""
import os
import platform
from HCNetSDK import *
from PlayCtrl import *
import numpy as np
import time
import cv2
from time import  sleep


class HKCam(object):
    def __init__(self, camIP, username, password, devport=8000, recorder=False):
        # 登陆设备信息
        self.DEV_IP = create_string_buffer(camIP.encode())
        self.DEV_PORT = devport
        self.DEV_USER_NAME = create_string_buffer(username.encode())
        self.DEV_PASSWORD = create_string_buffer(password.encode())
        self.WINDOWS_FLAG = False if platform.system() != "Windows" else True
        self.funcRealDataCallBack_V30 = None  # 实时预览回调函数
        self.recent_img = None  # 最新帧
        self.n_stamp = None  # 帧时间戳
        self.last_stamp = None  # 上次时间戳
        # 加载库，先加载依赖库
        if self.WINDOWS_FLAG:
            os.chdir(r'./lib/win')
            self.Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
            self.Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        else:
            os.chdir(r'./lib/linux')
            self.Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
            self.Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')
        # 设置组件库和SSL库加载路径
        self.SetSDKInitCfg()
        # 初始化DLL
        self.Objdll.NET_DVR_Init()
        os.chdir(r'../../')
        # 登陆
        (self.lUserId, self.device_info) = self.LoginDev()
        self.Playctrldll.PlayM4_ResetBuffer(self.lUserId, 1)
        print(self.lUserId)
        if self.lUserId < 0:
            err = self.Objdll.NET_DVR_GetLastError()
            print('Login device fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()
        else:
            print(f'摄像头[{camIP}]登录成功!!')
        self.start_play()
        if recorder:  # 视频录像
            string_buf = f'test{camIP}.mp4'
            if not self.Objdll.NET_DVR_SaveRealData(self.lRealPlayHandle, create_string_buffer(string_buf.encode())):
                print('录像失败')
        time.sleep(1)

    def SetSDKInitCfg(self, ):
        # 设置SDK初始化依赖库路径
        # 设置HCNetSDKCom组件库和SSL库加载路径
        if self.WINDOWS_FLAG:
            strPath = os.getcwd().encode('gbk')
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'\libssl-1_1-x64.dll'))
        else:
            strPath = os.getcwd().encode('utf-8')
            sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
            sdk_ComPath.sPath = strPath
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_ComPath))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(strPath + b'/libcrypto.so.1.1'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(strPath + b'/libssl.so.1.1'))

    def LoginDev(self, ):
        # 登陆注册设备
        device_info = NET_DVR_DEVICEINFO_V30()
        lUserId = self.Objdll.NET_DVR_Login_V30(self.DEV_IP, self.DEV_PORT, self.DEV_USER_NAME, self.DEV_PASSWORD,
                                                byref(device_info))
        return (lUserId, device_info)

    def start_play(self, ):
        self.PlayCtrl_Port = c_long(-1)  # 播放句柄
        # 获取一个播放句柄
        if not self.Playctrldll.PlayM4_GetPort(byref(self.PlayCtrl_Port)):
            print(u'获取播放库句柄失败')

        # 定义码流回调函数
        self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.RealDataCallBack_V30)
        # 开启预览
        self.preview_info = NET_DVR_PREVIEWINFO()
        self.preview_info.hPlayWnd = 0
        self.preview_info.lChannel = 1  # 通道号
        self.preview_info.dwStreamType = 0  # 主码流
        self.preview_info.dwLinkMode = 0  # TCP
        self.preview_info.bBlocked = 1  # 阻塞取流
        # 开始预览并且设置回调函数回调获取实时流数据
        self.lRealPlayHandle = self.Objdll.NET_DVR_RealPlay_V40(self.lUserId, byref(self.preview_info),
                                                                self.funcRealDataCallBack_V30, None)
        if self.lRealPlayHandle < 0:
            print('Open preview fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
            # 登出设备
            self.Objdll.NET_DVR_Logout(self.lUserId)
            # 释放资源
            self.Objdll.NET_DVR_Cleanup()
            exit()

    def DecCBFun(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
        if pFrameInfo.contents.nType == 3:
            t0 = time.time()
            # 解码返回视频YUV数据，将YUV数据转成RGB
            # 如果有耗时处理，需要将解码数据拷贝到回调函数外面的其他线程里面处理，避免阻塞回调导致解码丢帧
            nWidth = pFrameInfo.contents.nWidth
            nHeight = pFrameInfo.contents.nHeight

            nStamp = pFrameInfo.contents.nStamp

            YUV = np.frombuffer(pBuf[:nSize], dtype=np.uint8)
            YUV = np.reshape(YUV, [nHeight + nHeight // 2, nWidth])
            img_rgb = cv2.cvtColor(YUV, cv2.COLOR_YUV2BGR_YV12)
            self.recent_img, self.n_stamp = img_rgb, nStamp

    def RealDataCallBack_V30(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        # 码流回调函数
        if dwDataType == NET_DVR_SYSHEAD:
            # 设置流播放模式
            self.Playctrldll.PlayM4_SetStreamOpenMode(self.PlayCtrl_Port, 0)
            # 打开码流，送入40字节系统头数据
            if self.Playctrldll.PlayM4_OpenStream(self.PlayCtrl_Port, pBuffer, dwBufSize, 1024 * 1024):
                # 设置解码回调，可以返回解码后YUV视频数据
                self.FuncDecCB = DECCBFUNWIN(self.DecCBFun)
                self.Playctrldll.PlayM4_SetDecCallBackExMend(self.PlayCtrl_Port, self.FuncDecCB, None, 0, None)
                # 开始解码播放
                if self.Playctrldll.PlayM4_Play(self.PlayCtrl_Port, None):
                    print(u'播放库播放成功')
                else:
                    print(u'播放库播放失败')
            else:
                print(u'播放库打开流失败')
        elif dwDataType == NET_DVR_STREAMDATA:
            self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, pBuffer, dwBufSize)
        else:
            print(u'其他数据,长度:', dwBufSize)

    def read(self, ):
        while self.n_stamp == self.last_stamp:
            continue
        self.last_stamp = self.n_stamp
        return self.n_stamp, self.recent_img

    def PTZ_control(self, instruct):
        # 开始云台控制
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, instruct, 0)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

        # 转动一秒
        sleep(0.5)

        # 停止云台控制
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, instruct, 1)
        if lRet == 0:
            print('Stop ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Stop ptz control success')

    def release(self):
        self.Objdll.NET_DVR_StopRealPlay(self.lRealPlayHandle)
        if self.PlayCtrl_Port.value > -1:
            self.Playctrldll.PlayM4_Stop(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_CloseStream(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_FreePort(self.PlayCtrl_Port)
            PlayCtrl_Port = c_long(-1)
            self.Objdll.NET_DVR_Logout(self.lUserId)
            self.Objdll.NET_DVR_Cleanup()
        print('释放资源结束')

if __name__ == '__main__':
    camIP = '192.168.100.45'
    DEV_PORT = 8000
    username = 'admin'
    password = 'zsc123321'
    hkclass = HKCam(camIP, username, password)
    last_stamp = 0
    while True:
        t0 =time.time()
        n_stamp,img = hkclass.read()
        last_stamp=n_stamp
        cv2.imshow('1',cv2.resize(img,(800,600)))
        kkk = cv2.waitKey(1)
        if kkk ==ord('q'):
            break

    hkclass.PTZ_control(21)
    hkclass.release()
