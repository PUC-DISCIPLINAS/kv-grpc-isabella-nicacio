from __future__ import print_function
import logging

import grpc

import store_pb2
import store_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = store_pb2_grpc.StoreStub(channel)


def run():
    while True:
        menu = int(input('\nInform the number of the desired option \n'
                         '1 p/ add key-value | 2 - get key-value | 3 - get all keys \n'))

        put() if menu == 1 else get() if menu == 2 else getAllKeys() if menu == 3 else exit(0)


def put():
    key, value = str(input('\nInform the value of the key: ')), str(input('Inform the value: '))
    response = stub.put(store_pb2.KeyValueModel(key=key, value=value))
    return print(f'Key-value have been stored: {response.key}: {response.value}')


def get():
    key = str(input('\nInform the value of the key: '))
    response = stub.get(store_pb2.KeyValueModel(key=key))
    if response.key != "-1" and response.value != "-1":
        print(f'Key-value selected: {response.key}: {response.value}')
    else:
        print(f'Key not found!')


def getAllKeys():
    response = stub.getAllKeys(store_pb2.Void())
    print("----------- \n Keys list:")
    for key in response.map:
        print(f'{key} \n')
    print("-----------")


if __name__ == '__main__':
    logging.basicConfig()
    run()
