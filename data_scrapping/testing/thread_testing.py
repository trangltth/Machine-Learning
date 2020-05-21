import threadingimport time
import logging
from werkzeug.utils import dump_cookie

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] %(threadName)s %(message)s')


# #Signaling between threads
# def wait_for_event(e):
#     logging.debug('is starting')
#     event_start = e.wait()
#     logging.debug('- event is started: %s', event_start)

# def wait_for_a_time(e, t):
#     while not e.is_set():
#         logging.debug('is starting')
#         event_start = e.wait(t)
#         logging.debug('- event is started: %s', event_start)
#         if e.is_set():
#             logging.debug('stopped wait')
#         else:
#             logging.debug('is waitting')

# e = threading.Event()

# thread_1 = threading.Thread(target=wait_for_event, args=(e,))
# thread_1.start()

# thread_2 = threading.Thread(target=wait_for_a_time, args=(e, 1))
# thread_2.start()

# logging.debug('is delayed')
# time.sleep(2)
# e.set()


# # subclass
# class custom_thread(threading.Thread):
#     def __init__(self, name = None, target = None, args=(), kwargs = None):
#         threading.Thread.__init__(self, name=name, target=target)
#         self.args = args
#         self.kwargs = kwargs

#     def run(self):
#         # self.run()
#         logging.debug('is running with %s, %s', self.args, self.kwargs)

# thread_1 = custom_thread(args=(1,2), kwargs={'a':2, 'b':3})
# thread_1.start()

# write a program has 3 threads
# Each thread delay 2 minutes and print start, finish status
# print how main thread work and associate with 3 sub-threads
# understanding threading.enumerate() and apply it.

def _run():
    logging.debug('starting')
    time.sleep(3)


for i in range(3):
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()

main_thread = threading.main_thread()
for thread in threading.enumerate():
    if(thread is main_thread):
        print('this is main_thread: ', thread)
        continue
    logging.debug(' sub_thread is: %s', thread.getName())


######### DEAMON THREAD #############3
# def deamon():
#     """thread worker function"""
#     logging.debug('starting')
#     time.sleep(2)
#     logging.debug('finishing')

# def non_deamon():
#     logging.debug('starting')
#     logging.debug('finishing')

# threads = []
# deamon_thread = threading.Thread(target=deamon, name='worker')
# deamon_thread.setDaemon(True)
# non_deamon_thread = threading.Thread(target=non_deamon, name='proccessor')

# deamon_thread.start()
# non_deamon_thread.start()

# deamon_thread.join(1)
# print('deamon thread is alive: ', deamon_thread.isAlive())
# non_deamon_thread.join()
