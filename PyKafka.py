from confluent_kafka import Consumer, Producer

class PyKafka:
    def __init__(self, broker_url, group_id):
        self.broker_url = broker_url
        self.group_id = group_id

    def produce(self, topic, key, value):
        """
        Produce a message to a Kafka topic
        :param topic: topic to produce the message to
        :param key: key of the message
        :param value: value of the message
        """
        conf = {
            'bootstrap.servers': self.broker_url,
            'client.id': 'python-producer'
        }

        producer = Producer(conf)
        producer.produce(topic=topic, key=key, value=value)
        producer.flush()

    def consume(self, topic):
        """
        Consume messages from a Kafka topic
        :param topic: topic to consume messages from
        :return: generator that yields messages
        """
        conf = {
            'bootstrap.servers': self.broker_url,
            'group.id': self.group_id,
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(conf)
        consumer.subscribe([topic])

        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of topic {0} [{1}] at offset {2}".format(
                        msg.topic(), msg.partition(), msg.offset()))
                else:
                    print("Error consuming message from topic {0}: {1}".format(
                        msg.topic(), msg.error()))
            else:
                yield msg.key(), msg.value()
