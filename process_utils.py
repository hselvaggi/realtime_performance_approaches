import multiprocessing as mp


request = mp.Queue()
response = mp.Queue()
stopped = False


def execution_engine():
    global stopped
    while not stopped:
        if not request.empty():
            fn, data = request.get_nowait()
            result = fn(data)
            response.put(result)


process = mp.Process(target=execution_engine)
process.start()


def forked_function(fn):
    def wrapper(obj, default):
        request.put((fn, obj))

        if not response.empty():
            return response.get_nowait()

        return default

    return wrapper


def cleanup():
    global process
    global stopped

    print()

    stopped = True
    process.terminate()
