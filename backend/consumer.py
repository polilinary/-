import json
import random
import threading
import time
import pandas as pd

from confluent_kafka import Consumer

import config


class ProduceData:
    data = []

    def __init__(self, consumer_config, topic, num):
        self.consumer = Consumer(consumer_config)
        self.topic = topic
        self.consumer.subscribe([self.topic])
        self.num = num

    def run(self):
        while True:
            msg = self.consumer.poll(10)
            if msg is None:
                print("Stop pooling")
                break
            print(f"Consume by {self.num}: {msg.key().decode('utf-8')}")
            value = msg.value().decode('utf-8')
            data = json.loads(value)
            self.data.append(data)

    def get_data(self):
        return self.data


def main():
    cnt = config.DATA_PRODUCE_CONSUMER_COUNT
    consumers = []
    threads = []
    for i in range(cnt):
        consumer = ProduceData(config.DATA_PRODUCE_CONFIG, config.DATA_PRODUCE_TOPIC, i)
        consumers.append(consumer)
        threads.append(threading.Thread(target=consumer.run))
        threads[-1].start()
    full_data = []
    for i in range(cnt):
        threads[i].join()
        data = consumers[i].get_data()
        if len(data) == 0:
            print("No data")
            break
        full_data = full_data + data
    if len(full_data) == 0:
        print("No data in all consumers")
        return
    full_data.sort(key=lambda x: x['Patient_ID'], reverse=True)
    df = pd.DataFrame(data=full_data)
    df.set_index('Patient_ID', inplace=True)
    df.to_csv('consumed_data.csv')


if __name__ == '__main__':
    main()
