from kafka import KafkaProducer
from datetime import datetime

import time
import sys
import os
import json

libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_TSL2591 import TSL2591

logging.basicConfig(level=logging.INFO)

sensor = TSL2591.TSL2591()
# sensor.SET_InterruptThreshold(0xff00, 0x0010)
# try:

lux = sensor.Lux
print('Lux: %d'%lux)
sensor.TSL2591_SET_LuxInterrupt(50, 200)
infrared = sensor.Read_Infrared
print('Infrared light: %d'%infrared)
visible = sensor.Read_Visible
print('Visible light: %d'%visible)
full_spectrum = sensor.Read_FullSpectrum
print('Full spectrum (IR + visible) light: %d\r\n'%full_spectrum)
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%Y-%m-%d %H:%M:%S.%f")
data = {'Lux': lux,
    'IR': infrared,
    'Visible': visible,
    'Full': full_spectrum,
    'Timestamp': timestampStr}
print(data)
producer = KafkaProducer(bootstrap_servers='charlemagne:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    request_timeout_ms=300000,
    #compression_type=compression,
    # TODO: make these configurable?
    linger_ms=200)
future = producer.send('lightdata', data)
result = future.get(timeout=20)
#time.sleep(30)


    
# except KeyboardInterrupt:    
#     logging.info("ctrl + c:")
#     sensor.Disable()
#     exit()

