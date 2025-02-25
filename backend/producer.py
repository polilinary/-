import json
import threading
import time
import random

import config
import pandas as pd
from confluent_kafka import Producer, admin


class DataLoader:
    def __init__(self, brokers, topic):
        self.topic = topic
        self.producer = Producer(brokers)

    def produce_message(self, message):
        raw_message = json.dumps(message)
        try:
            self.producer.produce(self.topic, key=str(message['Patient_ID']), value=raw_message)
            self.producer.flush()
        except Exception as e:
            print(f'Failed to produce message: {e}')


def read_data(filename):
    df = pd.read_csv(filename, dtype={"Patient_ID": "int", "Age": "int", "Gender": "int", "Education_Level": "int",
                                      "Marital_Status": "int", "Occupation": "int", "Income_Level": "int",
                                      "Place_of_Residence": "int", "Diagnosis": "int", "Duration_of_Illness": "int",
                                      "Hospitalizations": "int", "Family_History_of_Schizophrenia": "int",
                                      "Substance_Use": "int", "Suicide_Attempts": "int",
                                      "Positive_Symptom_Score": "int", "Negative_Symptom_Score": "int",
                                      "GAF_Score": "int", "Social_Support": "int", "Stress_Factors": "int",
                                      "Medication_Compliance": "int"})
    return df.to_dict('records')


def split_data(data, cnt):
    result = []
    for i in range(cnt):
        result.append([])
    for (i, msg) in enumerate(data):
        result[i % cnt].append(msg)
    return result


def run_produce(dl, data, num):
    for message in data:
        dl.produce_message(message)
        print(f'Produced message by {num}: {message}')
        time.sleep(random.random())


def main():
    admin_client = admin.AdminClient(config.DATA_LOAD_CONFIG)
    data = read_data(config.DATASET_FILE_NAME)
    cnt = config.DATA_LOAD_PRODUCER_COUNT
    admin_client.create_topics([admin.NewTopic(config.DATA_LOAD_TOPIC, cnt)])
    splited = split_data(data, cnt)
    threads = []
    for i in range(cnt):
        dl = DataLoader(config.DATA_LOAD_CONFIG, config.DATA_LOAD_TOPIC)
        threads.append(threading.Thread(target=run_produce, args=(dl, splited[i], i,)))
        threads[-1].start()
    for i in range(cnt):
        threads[i].join()


if __name__ == '__main__':
    main()
