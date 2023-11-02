import redis


def main():
    # Connect to Redis server
    redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, password='password')

    # Set a key-value pair
    redis_client.set('test_key', 'Hello, Redis!')

    # Get the value of the key
    value = redis_client.get('test_key')
    print(value.decode('utf-8'))


if __name__ == '__main__':
    main()
