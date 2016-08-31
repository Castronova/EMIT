import datetime
from sprint import *


def check_timehorizons(source_model, target_model):

    ss = source_model.simulation_start()
    se = source_model.simulation_end()
    sts = source_model.time_step()
    ts = target_model.simulation_start()
    te = target_model.simulation_end()

    # reconstruct timelines
    stl = build_timeline(ss, se, sts)


    non_overlapping = 0
    for dt in stl:
        if dt < ts or dt > te:
            non_overlapping += 1

    sPrint('%d of %d source component timesteps are not within the target '
           'component\'s time horizon' % (non_overlapping, len(stl)),
           MessageType.WARNING)

    sPrint('%3.1f%% of the source component timesteps are not within the '
           'target component\'s time horizon' %
           (float(non_overlapping)/float(len(stl)) * 100.), MessageType.WARNING)





def build_timeline(start, end, step_in_seconds):

    th = [start]
    ct = start
    while ct < end:
        ct = ct + datetime.timedelta(seconds=step_in_seconds)
        th.append(ct)
    return th