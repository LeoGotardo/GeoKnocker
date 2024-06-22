import threading
import ctypes

class CustomThread(threading.Thread):
    """
    Initialize CustomThread Object
    
    Args:
        group(object): Thread Group.
        target(callabe): Target Function to call when thread starts.
        name(str): Thread name.
        args(tuple): arguments to pass to the target function
        kwargs(dict): keyword arguments to pass to the target function.
        verbose(bool): Verbosity level.
        
    Returns:
        The return value of the target function if it exists.
    """
    def __init__(self, group=None, target= None, name=None, args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
        self._stop_event = threading.Event()

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        threading.Thread.join(self)
        return self._return
    
    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')