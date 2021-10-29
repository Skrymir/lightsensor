from kafka import KafkaProducer

import json

producer = KafkaProducer(bootstrap_servers='192.168.86.7:9092')
producer.send('fizzbuzz', b'wtf')
producer.flush()
