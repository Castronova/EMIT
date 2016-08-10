import numpy as np
import timeit



def test_sat_deficit_list_comp(num_elements, num_loops):


    # calculate saturation deficit
    s_average = 2182.8788
    c = 180.0
    lambda_average = 9.11
    step = (17.78 - 3.11) / float(num_elements)
    et = 0
    p = 0
    ti = np.arange(3.11, 17.78, step)
    print 'Step: %3.5f, Num Elements: %d' % (step, len(ti))

    for i in range(num_loops):
        sat_deficit = [s_average + c * (lambda_average - t) for t in ti]
        sat_deficit = [s - p + et for s in sat_deficit]


def test_sat_deficit_numpy(num_elements, num_loops):

    # calculate saturation deficit
    s_average = 2182.8788
    c = 180.0
    lambda_average = 9.11
    step = (17.78 - 3.11) / float(num_elements)
    et = 0
    p = 0

    ti = np.arange(3.11, 17.78, step)
    print 'Step: %3.5f, Num Elements: %d' % (step, len(ti))

    for i in range(num_loops):
        sat_deficit = np.add(s_average, np.multiply(c, np.subtract(lambda_average, ti)))
        sat_deficit = np.subtract(sat_deficit, (p + et))



t = timeit.Timer(lambda: test_sat_deficit_list_comp(7820, 5809))
comp_time = t.timeit(number=1)
print '\n%3.5f sec:\t\ttest_sat_deficit_list_comp' % comp_time

t = timeit.Timer(lambda: test_sat_deficit_numpy(7820, 5809))
np_time = t.timeit(number=1)
print '\n%3.5f sec:\t\ttest_sat_deficit_numpy' % np_time
