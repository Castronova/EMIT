

import timeit
import datetime



def strftime_index_looping(dt_list):
    conv = []
    for i in range(len(dt_list)):
        conv.append(dt_list[i].strftime('%Y-%m-%d %H:%M:%S.%f'))
    return conv

def strftime_iter_looping(dt_list):
    conv = []
    for dt in dt_list:
        conv.append(dt.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return conv

def strftime_comprehension(dt_list):
    conv = [d.strftime('%Y-%m-%d %H:%M:%S.%f') for d in dt_list]
    return conv

def strftime_str(dt_list):
    conv = [str(d) for d in dt_list]
    return conv


def print_results(text, iter,  time):
    print '%s (%d loops), best time: %3.5f sec' % (text, iter, time)

if __name__ == "__main__":

    now = datetime.datetime.now()
    dt_list = [now + datetime.timedelta(hours=i) for i in range(100000)]

    # benchmark_strftime
    iter = 5

    t = timeit.Timer(lambda: strftime_index_looping(dt_list))
    print_results('strftime_index_looping', iter, t.timeit(iter))

    t = timeit.Timer(lambda: strftime_iter_looping(dt_list))
    print_results('strftime_iter_looping', iter, t.timeit(iter))

    t = timeit.Timer(lambda: strftime_comprehension(dt_list))
    print_results('strftime_comprehension', iter, t.timeit(iter))

    t = timeit.Timer(lambda: strftime_str(dt_list))
    print_results('strftime_str', iter, t.timeit(iter))










