from utilities.gui import *
from transform.time import *
from datetime import timedelta
import numpy as np

def update_links(obj, links, output_exchange_items, spatial_maps):
    """
    Updates the data from source component exchange items to target component exchange items
    :param obj: a coordinator object
    :param links: the links associated the current model, dict{linkid:link object}
    :param output_exchange_items: All outputs for the source model
    :param spatial_maps: map dictionary object
    """
    for linkid, link in links.iteritems():

        target_model = link.target_component()

        source_item_name = link.source_exchange_item().name()

        # get the auto generated key for this link
        link_key = generate_link_key(link)

        # get the target interpolation time based on the current time of the target model
        target_time = target_model.instance().current_time()

        # get all the datasets of the output exchange item.  These will be used to temporally map the data
        datasets = output_exchange_items[source_item_name].get_all_datasets()

        # build temporal mapping array
        temporal = temporal_nearest_neighbor()
        tmap = temporal.transform(dates,target_time)

        # Temporal data mapping
        mapped = {}
        for geom, datavalues in datasets.iteritems():

            # get the dates and values from the geometry
            dates,values = datavalues.get_dates_values()

            # temporal mapping
            temporal = temporal_nearest_neighbor()
            if temporal and values:
                mapped_dates,mapped_values = temporal.transform(dates,values,target_time)

                if mapped_dates is not None:
                    # save the temporally mapped data by output geometry
                    mapped[geom] = (zip(mapped_dates,mapped_values))

        # update links
        if len(mapped.keys()) > 0:
            obj.update_link(linkid, mapped, spatial_maps[link_key])


def update_links_feed_forward(links, output_exchange_items, spatial_maps):
    """
    Updates the data from source component exchange items to target component exchange items
    :param links: the links associated the current model, dict{linkid:link object}
    :param output_exchange_items: All outputs for the source model.
    :param spatial_maps: map dictionary object
    """

    links_list = links.items()
    sPrint('.. found %d link(s) for this model that need updating ' % len(links_list))

    for linkid, link in links_list:

        # get link source and target info
        target_model = link.target_component()
        target_item_name = link.target_exchange_item().name()
        source_model = link.source_component()
        source_item_name = link.source_exchange_item().name()

        sPrint('.. updating link %s:[%s] --> %s:[%s] ' % (target_model.name(),target_item_name, source_model.name(),
                                                       source_item_name), MessageType.INFO)

        # get the auto generated key for this link
        link_key = generate_link_key(link)

        # get the target interpolation time based on the current time of the target model
        target_st = target_model.instance().simulation_start()
        target_et = target_model.instance().simulation_end()
        target_ts = target_model.instance().time_step()

        t = target_st
        target_times = []
        while t <= target_et:
            # increment time by seconds
            target_times.append(t)
            t += timedelta(seconds=target_ts)


        # get oei data (source)
        oei = output_exchange_items[source_item_name]
        sgeoms = oei.getGeometries2()
        sdateidx, sdates = zip(*oei.getDates2())
        svalues = np.array(oei.getValues2())

        # get iei data (target)
        iei = link.target_exchange_item()
        tgeoms = iei.getGeometries2()

        # build temporal mapping array
        temporal = temporal_nearest_neighbor()
        tmap = temporal.map(sdates, target_times)

        # create empty array to hold mapped data (mimicks the target values array)
        nvals = np.empty((len(target_times), len(tgeoms)))

        # loop throught the source and target geometries in the mapped geoms list
        for sgeom, tgeom in spatial_maps[link_key]:

            # target geometry index
            tidx = tgeoms.index(tgeom)

            # source geometry index
            sidx = sgeoms.index(sgeom)

            # source values for the given index
            svals = svalues[:, sidx]

            # map values
            mvals = transform(tmap, svals)

            # set the source values in the target
            nvals[:, tidx] = mvals

        # do unit conversion
        convert_units(oei, iei, nvals)

        # todo: remove loop to improve efficiency
        # set these data in the iei
        for i in range(0, len(nvals)):
            iei.setValues2(values=nvals[i], timevalue=target_times[i])

        # return success
        return 1
