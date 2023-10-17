#import statements
import RPi.GPIO as GPIO
import time
import board
import Adafruit_ADS1x15
import Adafruit_DHT
import sys
import adafruit_dht

#initialize sensor values
heartBeat = 0
temp = 0
humid = 0
steps = 0
tilt = 0
move = False

#GPIO Setup
GPIO.setmode(GPIO.BOARD)

#heart
GPIO.setup(40, GPIO.IN)


#step
GPIO.setup(16,GPIO.IN)

#humid
GPIO.setup(3, GPIO.IN)

#electic pads
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)


def callAzure():
  pass
def rCalculation():
  pass

def activate():
   GPIO.output(8, GPIO.HIGH)
   GPIO.output(10, GPIO.HIGH)

#get heart rate
def setHeart():
  if __name__ == '__main__':


    adc = Adafruit_ADS1x15.ADS1015()
    # initialization 
    GAIN = 2/3  
    curState = 0
    thresh = 525 
    P = 512
    T = 512
    stateChanged = 0
    sampleCounter = 0
    lastBeatTime = 0
    firstBeat = True
    secondBeat = False
    Pulse = False
    IBI = 600
    rate = [0]*10
    amp = 100

    lastTime = int(time.time()*1000)

    # Main loop. 
    while True:
        # read from the ADC
        Signal = adc.read_adc(0, gain=GAIN)   
        curTime = int(time.time()*1000)

        sampleCounter += curTime - lastTime;      
        lastTime = curTime
        N = sampleCounter - lastBeatTime;     
        if Signal < thresh and N > (IBI/5.0)*3.0 :
            if Signal < T :                        
              T = Signal;                          

        if Signal > thresh and  Signal > P:           
            P = Signal;                            
                                               
        if N > 250 :                                  
            if  (Signal > thresh) and  (Pulse == False) and  (N > (IBI/5.0)*3.0)  :       
              Pulse = True;                               
              IBI = sampleCounter - lastBeatTime;         
              lastBeatTime = sampleCounter;               

              if secondBeat :                        
                secondBeat = False;                  
                for i in range(0,10):             
                  rate[i] = IBI;                      

              if firstBeat :                        
                firstBeat = False;                   # clear firstBeat flag
                secondBeat = True;                   # set the second beat flag
                continue                              
             
              runningTotal = 0;                    

              for i in range(0,9):                
                rate[i] = rate[i+1];                 
                runningTotal += rate[i];              

              rate[9] = IBI;                          
              runningTotal += rate[9];                
              runningTotal /= 10;                     
              BPM = 60000/runningTotal;               # how many beats can fit into a minute? that's BPM!
              heart = BPM

        if Signal < thresh and Pulse == True :   # when the values are going down, the beat is over
            Pulse = False;                         # reset the Pulse flag so we can do it again
            amp = P - T;                          
            thresh = amp/2 + T;                   
            P = thresh;                            # reset these for next time
            T = thresh;

        if N > 2500 :                          # if 2.5 seconds go by without a beat
            thresh = 512;                         
            P = 512;                               
            T = 512;                              
            lastBeatTime = sampleCounter;                 
            firstBeat = True;                      
            secondBeat = False;                    # when we get the heartbeat back
            
        time.sleep(0.005)
def setTemp():
  dhtDevice = adafruit_dht.DHT22(board.D3)
  while True:
    try:
        # Print the values to the serial port
        temp = temperature_c * (9 / 5) + 32
        humid = dhtDevice.humidity
        
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)

#change step if sensor moved
def setStep():
  GPIO.setmode(GPIO.BCM)
  if GPIO.input(16) != move:
    steps+=1
    move = not move

#function to check if activation needed or not
while True:
  #get sensor values
  setHeart()
  setTemp()
  setStep()

  #AI-system
  if callAzure:
    
    #Check
    if rCalculation():
      
      #activate
      activate()
  else:
    GPIO.output(8, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)

