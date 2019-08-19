#!/usr/bin/env python
# -*- coding: utf-8 -*-
from multiprocessing import Queue, Process, Manager as MultipleProcessingManager
from multiprocessing.managers import BaseManager

from manager import Manager, BarcodeCameraManager, OrderManager, SessionManager
from utils.redis import listener

if __name__ == "__main__":
    BaseManager.register('SessionManager', SessionManager)
    base_manager = BaseManager()
    base_manager.start()

    multiple_processing_manager = MultipleProcessingManager()
    global_dict = multiple_processing_manager.dict()
    global_dict['session_manager'] = base_manager.SessionManager()
    global_dict['test'] = 1


    # user_session = {
    #     'user_info':{},
    #     'snack_info': None,
    #     'session_time': 0
    # }

    face_queue = Queue()
    # encodings = load_all_encoding(env)
    manager = Manager(face_queue)
    # manager.set_known_faces(encodings)
    listener = Process(target=listener.listen, args=(face_queue,))
    listener.daemon = True
    listener.start()
    manager_process = Process(target=manager.run, args=(global_dict,))
    manager_process.start()
    barcode_manager = BarcodeCameraManager()
    barcode_manager_process = Process(target=barcode_manager.run, args=(global_dict,))
    barcode_manager_process.start()
    order_manager = OrderManager()
    order_manager_process = Process(target=order_manager.run, args=(global_dict,))
    order_manager_process.start()
    # listener.join()
    manager_process.join()
    order_manager_process.join()
    barcode_manager_process.join()

