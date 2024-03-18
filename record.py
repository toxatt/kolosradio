import os.path
from locale import currency
from threading import Thread
from tool import getDateTimeNow
import audioop
import pyaudio
import wave
import time
import sys

class Record(Thread):
    def __init__(self,params):
        Thread.__init__(self)
        self.x = 0
        self.chunk = 32
        self.p = pyaudio.PyAudio()
        self.threshold_on = params['audio-threshold-on']
        self.threshold_off = params['audio-threshold-off']
        self.time_low = params['audio-time-low']
        self.time_hi = params['audio-time-hi']
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.path_sound = params['path-sound']

    def run(self):
        chunk = self.chunk
        try:
            print("Start searching for devices")
            for i in range(self.p.get_device_count()):
                print(i, self.p.get_device_info_by_index(i)['name'])
                #   info = self.p.get_device_info_by_index(i)
                # print("Device {} ----------- {}".format(info["index"], info["name"]))
            print("default device -> ", self.p.get_default_input_device_info()['index'])
            index = self.p.get_default_input_device_info()['index']
            stream = self.p.open(format=pyaudio.paInt16,
                                 channels=2, rate=44100,
                                 input=True,
                                 input_device_index=index,
                                 frames_per_buffer=self.chunk)
            print(stream)
            frames = []  # Инициализировать массив для хранения кадров
            record = 0
            time_on = 0
            time_off = 0
            trigger = 0
            time_p = 0
        except:
            print('error sound device')
            #            sys.exit('sound device open error ')
            sys.exit()
            
        try:
            if not os.path.isdir("%s" % self.path_sound):
                os.makedirs("%s" % self.path_sound)
            while True:
                data = stream.read(chunk)
                rms = audioop.rms(data, 2)
               # print(rms)
                curr_time = round(time.time() * 1000)
#                if (curr_time > time_p + 5000 ):
#                    print("rms",rms)
#                    time_p = curr_time
# ------------- Hi volume   -------------------------
                if (rms > self.threshold_on):
                    if (trigger == 0 ):
                        trigger = 1
                        time_on = curr_time

                    if (curr_time > (time_on + self.time_hi)):
                        if not record:
                            record = 1
                            print("current tome:",curr_time)
                            print("time on", time_on)
                            print("start record")

# ---------- low volume  ------------------
                if (rms < self.threshold_off):
                    if trigger == 1:
                        trigger = 0
                        time_off = curr_time
                    if record:
                        if (curr_time >  time_off + self.time_low):
                            print("stop record")
                           # stop recording
                            # Stop and close the stream
                           # stream.stop_stream()
                           # stream.close()
                            # Terminate the PortAudio interface
                           # self.p.terminate()
                            filename = getDateTimeNow()+".wav"
                            wf = wave.open(os.path.join(self.path_sound, filename), 'wb')
                            wf.setnchannels(2)
                            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
                            wf.setframerate(44100)
                            wf.writeframes(b''.join(frames))
                            wf.close()
                            frames = []
                            record = 0
                #print(record)
                if (record):
                    frames.append(data)

            print("ok")
        except:
            print('error recording')

        finally:
            print("done")
