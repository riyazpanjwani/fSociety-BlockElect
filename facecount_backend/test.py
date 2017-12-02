import multiprocessing
from facecount_stream import CaptureVideo

mgr = multiprocessing.Manager()
val = mgr.Value(int, 1)
cv = CaptureVideo()
job = multiprocessing.Process(target=cv.live_stream_counter, args=(val,))
job.start()
while True:
    if(val.get() == 2):
        print("found two or more faces")
    else:
        print("single face")
jobs.join()
