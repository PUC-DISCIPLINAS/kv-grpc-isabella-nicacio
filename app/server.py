from concurrent import futures
import logging
import grpc

import store_pb2
import store_pb2_grpc

key_value_map = {}


class Store(store_pb2_grpc.StoreServicer):

    def put(self, request, context):
        key_value_map[request.key] = request.value
        return store_pb2.KeyValueModel(key=request.key, value=key_value_map[request.key])

    def get(self, request, context):
        try:
            return store_pb2.KeyValueModel(key=request.key, value=key_value_map[request.key])
        except:
            return store_pb2.KeyValueModel(key="-1", value="-1")

    def getAllKeys(self, request, context):
        return store_pb2.List(map=key_value_map)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    store_pb2_grpc.add_StoreServicer_to_server(Store(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
