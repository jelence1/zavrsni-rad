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








# MAIN APPLICATION

# This application example connects to a Bluetooth Low Energy device, retrieves
# its exported features, and let the user get data from those supporting
# notifications.

def make_connection():
    


    
    
            

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

        return has_audio_adpcm_features, has_audio_opus_features


def main(audio_feat_flag, opus_feat_flag, params):
    
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
    
    try:

        has_audio_adpcm_features = audio_feat_flag
        has_audio_opus_features = opus_feat_flag

            
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
                    print("Streaming!")
                    # SOCKET.send(("STREAMING").encode("utf-8"))
                    # SOCKET.recv()
                            
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
