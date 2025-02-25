# Data load
DATA_LOAD_TOPIC = 'data_topic'
DATA_LOAD_CONFIG = {'bootstrap.servers': 'localhost:9095,localhost:9096'}
DATA_LOAD_PRODUCER_COUNT = 2

# Dataset

DATASET_FILE_NAME = 'schizophrenia_dataset.csv'

# Data produce

DATA_PRODUCE_TOPIC = 'data_topic'
DATA_PRODUCE_CONFIG = {'bootstrap.servers': 'localhost:9095,localhost:9096',
                       'group.id': 'consumer_group',
                       'auto.offset.reset': 'earliest'}
DATA_PRODUCE_CONSUMER_COUNT = 2
