#!/usr/bin/env python

################################################################################
# COPYRIGHT(c) 2018 STMicroelectronics                                         #
#                                                                              #
# Redistribution and use in source and binary forms, with or without           #
# modification, are permitted provided that the following conditions are met:  #
#   1. Redistributions of source code must retain the above copyright notice,  #
#      this list of conditions and the following disclaimer.                   #
#   2. Redistributions in binary form must reproduce the above copyright       #
#      notice, this list of conditions and the following disclaimer in the     #
#      documentation and/or other materials provided with the distribution.    #
#   3. Neither the name of STMicroelectronics nor the names of its             #
#      contributors may be used to endorse or promote products derived from    #
#      this software without specific prior written permission.                #
#                                                                              #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"  #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE    #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE   #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE    #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR          #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF         #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS     #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN      #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)      #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                                  #
################################################################################


# DESCRIPTION
#
# This application example shows how to connect to a Bluetooth Low Energy (BLE)
# device exporting audio features, and to use it.

# JELENIN KOMENTAR: 
# Audio stream na PC trenutno onemogucen. Za omogucavanje otkomentirati linije sa stream.write().


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


# PRECONDITIONS
#
# In case you want to modify the SDK, clone the repository and add the location
# of the "BlueSTSDK_Python" folder to the "PYTHONPATH" environment variable.
#
# On Linux:
#   export PYTHONPATH=/home/<user>/BlueSTSDK_Python
#
# Moreover, install the following packages:
#   libasound:
#     sudo apt-get install libasound2-dev
#   pyalsaaudio:  
#     sudo pip3 install pyalsaaudio
#
# If you are using the Opus codec
#   libopus:
#     sudo apt-get install libopus0
#   opuslib (wrapper from github):
#     git clone https://github.com/OnBeep/opuslib.git
#     cd opuslib
#     sudo su
#     python3 setup.py install
#
# Troubleshooting:
#   Prevent audio out garbling caused by the audio output peripheral:
#      sudo bash -c "echo disable_audio_dither=1 >> /boot/config.txt"
#      sudo bash -c "echo pwm_mode=2 >> /boot/config.txt" 


# CONSTANTS

INTRO = """##################
# BlueST Example #
##################"""

# Paths and File names
AUDIO_DUMPS_PATH = "audioDumps/"
AUDIO_DUMP_SUFFIX = "_audioDump.raw"
ADPCM_TAG = "_ADPCM"
OPUS_TAG = "_Opus"

# Notifications per second
NPS_ADPCM = 200
NPS_OPUS = 50

# Number of channels.
CHANNELS = 1

# Sampling frequency.
SAMPLING_FREQ_ADPCM = 8000
SAMPLING_FREQ_OPUS = 16000

# Global Audio Raw file.
audioFile=None
save_audio_flag = 0

# Bluetooth Scanning time in seconds (optional).
SCANNING_TIME_s = 5

# Global stream control index.
n_idx = 0

# Global audio features.
audio_feature = None
audio_sync_feature = None 
beamforming_feature = None

# Global Beamforming control.
beamforming_flag = 0;

# Connection to server.
# CONTEXT = zmq.Context()
# SOCKET = CONTEXT.socket(zmq.REQ)
# SOCKET.connect("tcp://localhost:5555")

import globals
CONTEXT = globals.CONTEXT_BLE
SOCKET = globals.SOCKET_BLE

# Audio stream flag
audio_stream_flag = 0

# FUNCTIONS

# Printing intro
def print_intro(socket):
    socket.send(('\n' + INTRO + '\n').encode("utf-8"))
    socket.recv()


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
        global SOCKET
        SOCKET.send(('Discovery %s.' % ('started' if enabled else 'stopped')).encode("utf-8"))
        SOCKET.recv()
        if not enabled:
                #print()
                pass

    #
    # This method is called whenever a new node is discovered.
    #
    # @param manager Manager instance that discovers the node.
    # @param node    New node discovered.
    #
    def on_node_discovered(self, manager, node):
        return
        global SOCKET
        SOCKET.send(('New device discovered: %s.' % (node.get_name())).encode("utf-8"))
        SOCKET.recv()


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
        global SOCKET
        #SOCKET.send(('Device %s connected.' % (node.get_name())).encode("utf-8"))
        SOCKET.send("CONNECTED".encode("utf-8"))
        SOCKET.recv()

    #
    # To be called whenever a node disconnects from a host.
    #
    # @param node       Node that has disconnected from a host.
    # @param unexpected True if the disconnection is unexpected, False otherwise
    #                   (called by the user).
    #
    def on_disconnect(self, node, unexpected=False):
        return
        global SOCKET
        #SOCKET.send(('Device {} disconnected{}.'.format(node.get_name(), ' unexpectedly' if unexpected else '')).encode("utf-8"))
        SOCKET.send("DISCONNECTED".encode("utf-8"))
        SOCKET.recv()


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
                #global SOCKET
                #with open(OUTPUT_PATH, "w") as output_file:
                #    output_file.write("command message received: " + str(sample))  
                
class MyFeatureListenerBeam(FeatureListener):

    #
    # To be called whenever the feature updates its data.
    #
    # @param feature Feature that has updated.
    # @param sample  Data extracted from the feature.
    #
    def on_update(self, feature, sample):
        return
        global beamforming_feature
        if beamforming_feature is not None:
            global SOCKET
            SOCKET.send(beamforming_feature.encode("utf-8"))
            SOCKET.recv()
                
def terminate(context, socket):
    socket.send("$".encode("utf-8"))
    socket.recv().decode("utf-8")
    socket.close()
    context.term()
    sys.exit(0)

# MAIN APPLICATION

# This application example connects to a Bluetooth Low Energy device, retrieves
# its exported features, and let the user get data from those supporting
# notifications.
def main(argv):
    print("ovdje sam")
    
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

    ###TCP Connection###########################################
    global CONTEXT
    global SOCKET
    ###TCP Connection###########################################
    
    ###Audio Stream###
    global audio_stream_flag
    ###Audio Stream###

    # Printing intro.
    #print_intro(SOCKET)
    
    try:
        # Creating Bluetooth Manager.
            manager = Manager.instance()
            manager_listener = MyManagerListener()
            manager.add_listener(manager_listener)

        #while True:
            manager.discover(SCANNING_TIME_s)

            # Getting discovered devices.
            devices = manager.get_nodes()

            # Listing discovered devices.
            if not devices:
                terminate(context=CONTEXT, socket=SOCKET)
            
            # Selecting a device.
            device = devices[0]
            
            # Connecting to the device.
            node_listener = MyNodeListener()
            device.add_listener(node_listener)
            if not device.connect():
                terminate(socket=SOCKET, context=CONTEXT)
                
            SOCKET.send(("SUCCESS").encode("utf-8"))
            received = SOCKET.recv().decode("utf-8")
            params = [int(ele) for ele in received.split(",")] #STREAM, SAVE, DURATION

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
            
            if all(has_audio_adpcm_features) or all(has_audio_opus_features):
                    save_audio_flag = params[1]
                    
                    if save_audio_flag is not None:
                        if save_audio_flag == 1:
                            ts = time.time()
                            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
                            if not os.path.exists(AUDIO_DUMPS_PATH):
                                os.makedirs(AUDIO_DUMPS_PATH)
                            if all(has_audio_adpcm_features):
                                fileName = AUDIO_DUMPS_PATH + st + ADPCM_TAG + AUDIO_DUMP_SUFFIX
                            elif all(has_audio_opus_features):
                                fileName = AUDIO_DUMPS_PATH + st + OPUS_TAG + AUDIO_DUMP_SUFFIX
                            audioFile = open(fileName,"wb+")
                        
                        
                        number_of_seconds = params[2]
                        
                        if all(has_audio_adpcm_features):
                            number_of_notifications = number_of_seconds * NPS_ADPCM
                        elif all(has_audio_opus_features):
                            number_of_notifications = number_of_seconds * NPS_OPUS

                        if number_of_seconds > 0:
                            SOCKET.send(("STREAMING").encode("utf-8"))
                            SOCKET.recv()
                            
                            if all(has_audio_adpcm_features):
                                ###Audio Stream#####################################
                                stream = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NONBLOCK,'default')
                                stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
                                stream.setchannels(CHANNELS)
                                stream.setrate(SAMPLING_FREQ_ADPCM)
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
                                    stream.setchannels(CHANNELS)
                                    stream.setrate(SAMPLING_FREQ_OPUS)
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
                                    

                        
                            #SOCKET.send(("End of Streaming!").encode("utf-8"))
                            #SOCKET.recv()
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
                        
                        
    except KeyboardInterrupt:
        try:
            # Exiting.
            terminate(context=CONTEXT, socket=SOCKET)
        except SystemExit:
            terminate(context=CONTEXT, socket=SOCKET)
            os._exit(0)


if __name__ == "__main__":

    main(sys.argv[1:])
