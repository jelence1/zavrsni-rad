# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'recording_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# IMPORT

from __future__ import print_function
import sys
import os
import time
import datetime
import warnings
import click
import zmq
from abc import abstractmethod
from threading import Thread

import opuslib

from blue_st_sdk.manager import Manager
from blue_st_sdk.manager import ManagerListener
from blue_st_sdk.node import NodeListener
from blue_st_sdk.feature import FeatureListener
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm import FeatureAudioADPCM
from blue_st_sdk.features.audio.adpcm.feature_audio_adpcm_sync import FeatureAudioADPCMSync
from blue_st_sdk.features.audio.opus.feature_audio_opus import FeatureAudioOpus
from blue_st_sdk.features.audio.opus.feature_audio_opus_conf import FeatureAudioOpusConf
from blue_st_sdk.features.feature_beamforming import FeatureBeamforming
from blue_st_sdk.utils.number_conversion import LittleEndian

###Audio Stream#########################################################
import alsaaudio
###Audio Stream#########################################################


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint, Qt, QTimer, QBasicTimer

import time
import globals

# Global Audio Raw file.
audioFile=None
save_audio_flag = 0

# Global stream control index.
n_idx = 0

# Global audio features.
audio_feature = None
audio_sync_feature = None 
beamforming_feature = None

# Global Beamforming control.
beamforming_flag = 0

# Audio stream flag
audio_stream_flag = 0

# INTERFACES

#
# Implementation of the interface used by the Manager class to notify that a new
# node has been discovered or that the scanning starts/stops.
#
class MyManagerListener(ManagerListener):

    #
    # This method is called whenever a discovery process starts or stops.
    #
    # @param manager Manager instance that starts/stops the process.
    # @param enabled True if a new discovery starts, False otherwise.
    #
    def on_discovery_change(self, manager, enabled):
        return

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        return

#
# Implementation of the interface used by the Node class to notify that a node
# has updated its status.
#
class MyNodeListener(NodeListener):

    #
    # To be called whenever a node connects to a host.
    #
    # @param node Node that has connected to a host.
    #
    def on_connect(self, node):
        return

    #
    # To be called whenever a node disconnects from a host.
    #
    # @param node       Node that has disconnected from a host.
    # @param unexpected True if the disconnection is unexpected, False otherwise
    #                   (called by the user).
    #
    def on_disconnect(self, node, unexpected=False):
        return


#
# Implementation of the interface used by the Feature class to notify that a
# feature has updated its data.
#
class MyFeatureListener(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):        
        global n_idx
        ###Audio Stream#################################################
        global stream
        ###Audio Stream#################################################
        ###Save Audio File##############################################
        global audioFile
        global save_audio_flag
        ###Save Audio File##############################################
        ###Audio Stream###
        global audio_stream_flag
        ###Audio Stream###
        if isinstance(feature,FeatureAudioADPCM):
            shortData = sample._data
            if len(shortData) != 0:
                for d in shortData:
                    byteData = LittleEndian.int16_to_bytes(d)
                    ###Save Audio File######################################
                    if save_audio_flag == 1:
                        audioFile.write(byteData)
                    ###Save Audio File######################################
                    ###Audio Stream#########################################
                    if audio_stream_flag == 1:
                        stream.write(byteData)
                    ###Audio Stream#########################################
                n_idx += 1
        elif isinstance(feature,FeatureAudioOpus):
            if sample is not None:
                byteData = sample._data
                if byteData is not None and len(byteData) != 0:
                    ###Save Audio File######################################
                    if save_audio_flag == 1:
                        audioFile.write(byteData)
                    ###Save Audio File######################################
                    ###Audio Stream#########################################
                    if audio_stream_flag == 1:
                        stream.write(byteData)
                    ###Audio Stream#########################################
                    n_idx += 1

#
# Implementation of the interface used by the Feature class to notify that a
# feature has updated its data.
#
class MyFeatureListenerSync(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        global audio_feature
        if audio_feature is not None:
            if isinstance(feature, FeatureAudioADPCMSync):
                audio_feature.set_audio_sync_parameters(sample)
            elif isinstance(feature, FeatureAudioOpusConf):
                return
                
class MyFeatureListenerBeam(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        return

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(20, 20, 750, 550))
        self.widget.setStyleSheet("QPushButton {\n"
"    font: 14pt \"Arial Rounded MT Bold\";\n"
"border-radius: 20px;\n"
"}\n"
"\n"
"QPushButton#recordBtn {\n"
"background-color: qlineargradient(spread:reflect, x1:0, y1:0, x2:0.553, y2:0.533409, stop:0.00497512 rgba(78, 75, 108, 255), stop:0.935323 rgba(151, 180, 209, 255))\n"
"}\n"
"\n"
"QPushButton#editBtn {\n"
"color: white;\n"
"background-color:qlineargradient(spread:reflect, x1:0, y1:0, x2:0.513, y2:0.499318, stop:0 rgba(160, 193, 221, 255), stop:0.955224 rgba(74, 99, 119, 255))\n"
"}\n"
"\n"
"QPushButton#editBtn:hover, #recordBtn:hover, #exitBtn:hover {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.731905, y2:0.755, stop:0 rgba(255, 221, 221, 255), stop:0.955224 rgba(238, 103, 100, 255))\n"
"}\n"
"\n"
"QPushButton#exitBtn {\n"
"background-color: rgba(195, 195, 195, 0.3);\n"
"border-radius: 10px; \n"
"}")
        self.widget.setObjectName("widget")
        self.mainLabel = QtWidgets.QLabel(self.widget)
        self.mainLabel.setGeometry(QtCore.QRect(0, 0, 750, 550))
        self.mainLabel.setStyleSheet("border-radius: 50px;\n"
"background-color: rgb(191, 204, 228);")
        self.mainLabel.setText("")
        self.mainLabel.setObjectName("mainLabel")
        self.micLabel = QtWidgets.QLabel(self.widget)
        self.micLabel.setGeometry(QtCore.QRect(30, 130, 80, 80))
        self.micLabel.setText("")
        self.micLabel.setPixmap(QtGui.QPixmap("imgs/microphone.png"))
        self.micLabel.setScaledContents(True)
        self.micLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.micLabel.setObjectName("micLabel")
        self.header = QtWidgets.QLabel(self.widget)
        self.header.setGeometry(QtCore.QRect(0, 0, 750, 70))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(28)
        self.header.setFont(font)
        self.header.setStyleSheet("border-top-left-radius: 50px;\n"
"border-top-right-radius: 50px;\n"
"background-color: rgb(64, 69, 79);\n"
"")
        self.header.setText("")
        self.header.setAlignment(QtCore.Qt.AlignCenter)
        self.header.setObjectName("header")
        self.headerLabel = QtWidgets.QLabel(self.widget)
        self.headerLabel.setGeometry(QtCore.QRect(200, 10, 352, 71))
        self.headerLabel.setText("")
        self.headerLabel.setPixmap(QtGui.QPixmap("imgs/header.png"))
        self.headerLabel.setScaledContents(True)
        self.headerLabel.setObjectName("headerLabel")
        self.headerFade = QtWidgets.QLabel(self.widget)
        self.headerFade.setGeometry(QtCore.QRect(0, 70, 750, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(28)
        self.headerFade.setFont(font)
        self.headerFade.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.511975, y1:0.443, x2:0.522, y2:1, stop:0 rgba(64, 69, 79, 255), stop:1 rgba(64, 69, 79, 0))")
        self.headerFade.setText("")
        self.headerFade.setAlignment(QtCore.Qt.AlignCenter)
        self.headerFade.setObjectName("headerFade")
        self.exitBtn = QtWidgets.QPushButton(self.widget)
        self.exitBtn.setGeometry(QtCore.QRect(690, 30, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.exitBtn.setFont(font)
        self.exitBtn.setObjectName("exitBtn")
        self.recordBtn = QtWidgets.QPushButton(self.widget)
        self.recordBtn.setGeometry(QtCore.QRect(240, 130, 291, 85))
        self.recordBtn.setStyleSheet("")
        self.recordBtn.setObjectName("recordBtn")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(70, 250, 621, 251))
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.mainLabel.raise_()
        self.micLabel.raise_()
        self.header.raise_()
        self.headerFade.raise_()
        self.headerLabel.raise_()
        self.exitBtn.raise_()
        self.label.raise_()
        self.recordBtn.raise_()

        self.exitBtn.clicked.connect(self.exit)
        self.recordBtn.clicked.connect(self.start)

        self.timer = QTimer()
        self.timer.timeout.connect(self.finished)
        self.basic = QBasicTimer()

        self.labeltext = "<html><head/><body><p>Trying to connect to the STM32...</p><p>Please do not exit the application.</p></body></html>"

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.exitBtn.setText(_translate("Form", "X"))
        self.label.setText(_translate("Form", self.labeltext))
        self.recordBtn.setText(_translate("Form", "START"))

    def exit(self):
        sys.exit(0)

    def start(self):
        self.recordBtn.setEnabled(False)
        self.make_connection()

    def terminate(self):
        time.sleep(5000)
        sys.exit(0)

    def update_gui(self):
        _translate = QtCore.QCoreApplication.translate
        self.labeltext = '''<html><head/><body><p>Streaming has started!</p>
        <p>Streaming enabled: {}</p>
        <p>Audio will be saved: {}</p>
        <p>Time left: {} seconds</p></body></html>'''.format(self.stream, self.save, self.timer.remainingTime()//1000)
        self.retranslateUi()

    def finished(self):
        self.basic.stop()
        _translate = QtCore.QCoreApplication.translate
        self.labeltext =  "Recording is finished! You can now exit the application."
        self.retranslateUi()

    def timerEvent(self, event):
        self.update_gui()
        super().timerEvent(event)

    def get_data(self, r):
        self.data = r
        r = r.split(",") #stream, save, duration
        if r[0] == "0":
            self.stream = "No"
        else:
            self.stream = "Yes"
        if r[1] == "0":
            self.save = "No"
        else:
            self.save = "Yes"
        self.duration = int(r[2])

    def make_connection(self):
        _translate = QtCore.QCoreApplication.translate

        global n_idx
        ###Audio Stream#####################################################
        global stream
        ###Audio Stream#####################################################
        ###Save Audio File##################################################
        global audioFile
        global save_audio_flag
        global beamforming_flag
        ###Save Audio File##################################################
        
        global audio_feature
        global audio_sync_feature
        global beamforming_feature
        
        ###Audio Stream###
        global audio_stream_flag
        ###Audio Stream###

        # Creating Bluetooth Manager.
        manager = Manager.instance()
        manager_listener = MyManagerListener()
        manager.add_listener(manager_listener)

        self.labeltext = "Scanning for Bluetooth devices..."
        self.retranslateUi()

        manager.discover(globals.SCANNING_TIME_s)

        # Getting discovered devices.
        devices = manager.get_nodes()

        # Listing discovered devices.
        if not devices:
            self.label.setText(_translate("Form", "<html><head/><body><p>No Bluetooth devices found.</p><p>Check the STM32's connection.</p><p>The application will now shut down.</p></body></html>"))
            self.terminate()
            
        # Selecting a device.
        device = devices[0]
        
        # Connecting to the device.
        text = "Device found: " +  device.get_name() + "\n" + "Trying to connect..."
        self.label.setText(_translate("Form", text))
        node_listener = MyNodeListener()
        device.add_listener(node_listener)
        if not device.connect():
            self.label.setText(_translate("Form", "<html><head/><body><p>Connection failed.</p><p>Check the STM32's connection.</p><p>The application will now shut down.</p></body></html>"))
            self.terminate()

        self.label.setText(_translate("Form", "<html><head/><body><p>Connection successful!</p><p>Streaming will start in a few seconds.</p></body></html>"))
        time.sleep(300)

        has_audio_adpcm_features = [False,False]
        has_audio_opus_features = [False,False]

        i = 1
        features = device.get_features()
        for feature in features:
            if isinstance(feature, FeatureAudioADPCM):
                audio_feature = feature
                has_audio_adpcm_features[0] = True
            elif isinstance(feature, FeatureAudioADPCMSync):
                audio_sync_feature = feature
                has_audio_adpcm_features[1] = True
            elif isinstance(feature, FeatureAudioOpus):
                audio_feature = feature
                has_audio_opus_features[0] = True
            elif isinstance(feature, FeatureAudioOpusConf):
                audio_sync_feature = feature
                has_audio_opus_features[1] = True
            elif isinstance(feature,FeatureBeamforming):
                beamforming_feature = feature
            i += 1


        self.streaming(has_audio_adpcm_features, has_audio_opus_features, device)
        
    def streaming(self, audio_feat_flag, opus_feat_flag, device):
        global n_idx
        ###Audio Stream#####################################################
        global stream
        ###Audio Stream#####################################################
        ###Save Audio File##################################################
        global audioFile
        global save_audio_flag
        global beamforming_flag
        ###Save Audio File##################################################
        
        global audio_feature
        global audio_sync_feature
        global beamforming_feature
        
        ###Audio Stream###
        global audio_stream_flag
        ###Audio Stream###        


        has_audio_adpcm_features = audio_feat_flag   
        has_audio_opus_features = opus_feat_flag

        self.timer.start(self.duration*1000)
        self.basic.start(1000, self)

        if all(has_audio_adpcm_features) or all(has_audio_opus_features):
            save_audio_flag = self.save
                    
            if save_audio_flag is not None:
                if save_audio_flag == 1:
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
                    if not os.path.exists(globals.AUDIO_DUMPS_PATH):
                        os.makedirs(globals.AUDIO_DUMPS_PATH)
                    if all(has_audio_adpcm_features):
                        fileName = globals.AUDIO_DUMPS_PATH + st + globals.ADPCM_TAG + globals.AUDIO_DUMP_SUFFIX
                    elif all(has_audio_opus_features):
                        fileName = globals.AUDIO_DUMPS_PATH + st + globals.PUS_TAG + globals.AUDIO_DUMP_SUFFIX
                    audioFile = open(fileName,"wb+")
                        
                        
                number_of_seconds = self.duration
                        
                if all(has_audio_adpcm_features):
                    number_of_notifications = number_of_seconds * globals.NPS_ADPCM
                elif all(has_audio_opus_features):
                    number_of_notifications = number_of_seconds * globals.NPS_OPUS

                if number_of_seconds > 0:
                    # START OF STREAMING
                    self.timer.start(self.duration*1000)
                    self.basic.start(1000, self)
                            
                    if all(has_audio_adpcm_features):
                        ###Audio Stream#####################################
                        stream = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NONBLOCK,'default')
                        stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                        stream.setchannels(globals.CHANNELS)
                        stream.setrate(globals.SAMPLING_FREQ_ADPCM)
                        ###Audio Stream#####################################
                                
                        #Enabling Notifications
                        audio_feature_listener = MyFeatureListener()
                        audio_feature.add_listener(audio_feature_listener)
                        device.enable_notifications(audio_feature)
                        audio_sync_feature_listener = MyFeatureListenerSync()
                        audio_sync_feature.add_listener(audio_sync_feature_listener)
                        device.enable_notifications(audio_sync_feature)
                    elif all(has_audio_opus_features):
                        ###Audio Stream#########################################
                        #SuppressING warnings.
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            stream = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL,'default')
                            stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                            stream.setchannels(globals.CHANNELS)
                            stream.setrate(globals.SAMPLING_FREQ_OPUS)
                            stream.setperiodsize(160)
                        ###Audio Stream#########################################
                                            
                        #Enabling Notifications
                        audio_sync_feature_listener = MyFeatureListenerSync()
                        audio_sync_feature.add_listener(audio_sync_feature_listener)
                        # Suppressing warnings.
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            device.enable_notifications(audio_sync_feature)
                            audio_feature_listener = MyFeatureListener()
                            audio_feature.add_listener(audio_feature_listener)
                            device.enable_notifications(audio_feature)
                            
                    n_idx = 0
                    while n_idx < number_of_notifications:
                        device.wait_for_notifications(0.05)
                                    

                        
                    # END OF STREAMING 

                    # Disabling notifications.
                    device.disable_notifications(audio_feature)
                    audio_feature.remove_listener(audio_feature_listener)
                    device.disable_notifications(audio_sync_feature)
                    audio_sync_feature.remove_listener(audio_sync_feature_listener)
                            
                    ###Save Audio File##################################
                    if save_audio_flag == 1:
                        audioFile.close()
                    ###Save Audio File##################################
                    ###Audio Stream#####################################
                    stream.close()
                    ###Audio Stream#####################################
                        
            

        

    
    


class Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setupUi(self)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.oldPosition)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPosition = event.globalPos()

    

    

    

    

        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Form()

    w.get_data(sys.argv[1])
    
    w.show()
    
    sys.exit(app.exec_())

    


