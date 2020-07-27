import time
import wiringpi

# Pin definitions
ENC_BUTTON = 0 #// RPI Pin 11, BCM 17
ENC_PIN_A = 2  #// RPI Pin 13, BCM 27
ENC_PIN_B = 3  #// RPI Pin 15, BCM 22

count = 0
lastEncUpdate = 0
lastEncoded = 0

def updateButton():
    '''
    uint32_t now = micros();
    if (now - lastBtnupdate < 2000) {
        return;
    }
    lastBtnupdate = now;
    '''
def updateEncoders():
    now = time.time_ns()
    if (lastEncUpdate - now < 500000):
        return
    lastEncUpdate = now

    MSB = wiringpi.digitalRead(ENC_PIN_A)
    LSB = wiringpi.digitalRead(ENC_PIN_B)
    newEncoded = (MSB << 1) | LSB
    encoded = (lastEncoded << 2) | newEncoded
    if (encoded == 0b1011):
        count += 1
    if (encoded == 0b1000):
        count -= 1
    lastEncoded = newEncoded
    print("Count:", count)

    '''
    unsigned int now = micros();
    if (lastEncUpdate - now < 500) {
        return;
    }
    lastEncUpdate = now;

    int MSB = digitalRead(ENC_PIN_A);
    int LSB = digitalRead(ENC_PIN_B);
    int encoded = (MSB << 1) | LSB;
    int sum = (lastEncoded << 2) | encoded;
    if(/*sum == 0b1101 ||  sum == 0b0100 || *//*sum == 0b0010 || */ sum == 0b1011) {
        volume = volman.VolumeUp(1); //m_volume++;
        ROS_INFO("Volume Up = %d", volume);
    }
    if(/*sum == 0b1110 ||  sum == 0b0111 || *//*sum == 0b0001 || */ sum == 0b1000) {
        volume = volman.VolumeDown(1); //m_volume--;
        ROS_INFO("Volume Down = %d", volume);
    }

    lastEncoded = encoded;

    setVolume(volume);
    // if (setvolume(m_volume)) {
    //    ROS_INFO("Volume = %d", m_volume);
    // }
    '''

wiringpi.wiringPiSetup()

wiringpi.pinMode(ENC_PIN_A, wiringpi.GPIO.INPUT)
wiringpi.pinMode(ENC_PIN_B, wiringpi.GPIO.INPUT)
wiringpi.pinMode(ENC_BUTTON, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(ENC_PIN_A, wiringpi.GPIO.PUD_UP)
wiringpi.pullUpDnControl(ENC_PIN_B, wiringpi.GPIO.PUD_UP)
wiringpi.pullUpDnControl(ENC_BUTTON, wiringpi.GPIO.PUD_UP)
wiringpi.wiringPiISR(ENC_PIN_A, wiringpi.GPIO.INT_EDGE_BOTH, updateEncoders)
wiringpi.wiringPiISR(ENC_PIN_B, wiringpi.GPIO.INT_EDGE_BOTH, updateEncoders)
wiringpi.wiringPiISR(ENC_BUTTON, wiringpi.GPIO.INT_EDGE_RISING, updateButton)
while True:
    wiringpi.delay(1500)
