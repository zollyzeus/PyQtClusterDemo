import redis
import time

# List of activation messages to send (deck, card, activation_status)
activation_msgs = [
    (0, 1, True),   # bgnd
    (1, 1, True),   # lane graphics
    (2, 1, True),   # music bgnd
    (3, 1, True),   # music cover
    (4, 1, True),   # mini car
    (5, 1, True),   # ECO
    (6, 1, True),   # weather icon
    (7, 2, True),   # P
    (8, 1, True),   # D
    (9, 2, True),   # N
    (10, 2, True),  # R
    (11, 1, True),  # time
    (12, 1, True),  # temp
    (13, 1, True),  # speedo
    (14, 1, True),  # range
]

def send_activations_to_redis(redis_host='localhost', redis_port=6381, queue_name='restmq'):
    r = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    for deck, card, status in activation_msgs:
        msg = f"{deck},{card},{status}"
        r.rpush(queue_name, msg)
        print(f"Sent: {msg}")
        time.sleep(0.1)  # Optional: small delay between messages

        #r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.rpush('restmq', '0,1,True')
    r.rpush('restmq', '1,1,True')
    r.rpush('restmq', '2,1,True')

if __name__ == "__main__":
    send_activations_to_redis()