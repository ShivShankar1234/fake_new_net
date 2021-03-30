import time
from threading import Lock

class ResourceAllocator:
    def __init__(self, num_keys=34, time_window=900, window_limit=15):
        self._lock = Lock()
        self.val = None
        self.num_keys = num_keys        # we have num_keys threads to process requests
        self.timers = dict()
        self.time_window = time_window
        self.window_limit = window_limit

        for i in range(0, self.num_keys):
            self.timers[i] = [0, 0]         # [time_last_woken_up, num_windows_open]

    def change_params(self, window_limit, time_window):
        self.time_window = time_window
        self.window_limit = window_limit

    def get_resource_index(self):
        """
        Return index of the resource to use for making requests to get data
        if none of the resources are available, then send number of seconds until the resource is not available

        :return: Index resource is available otw time until none of the resources are available
        """

        result = -1
        max_sleep_time = self.time_window
        with self._lock:
            while result == -1:
                for i in range(0, self.num_keys):
                    # calculate the time needed to sleep (this is positive if we are currently processing something)
                    curr_sleep_time = max((self.timers[i][0] + self.time_window) - time.time(), 0)
                    max_sleep_time = min(max_sleep_time, curr_sleep_time)

                    # If we have reached window_limit parallel windows and have completed our last task,
                    # reset timer at this index
                    if self.timers[i][1] >= self.window_limit and self.timers[i][0] + self.time_window < time.time():
                        self.timers[i][0] = 0
                        self.timers[i][1] = 0

                    # If timer at index can accept new task, this is the result index
                    if self.timers[i][1] < self.window_limit:
                        result = i
                        break
                if result == -1:    # if all streams are rate limited
                    return -1 * max_sleep_time
            # Wake up thread (and set first element of its timer to current time)
            if self.timers[result][0] == 0:
                self.timers[result][0] = time.time()

            self.timers[result][1] += 1
            return result
