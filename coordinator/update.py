__author__ = 'tonycastronova'

from utilities.gui import *
from transform.time import *
from datetime import timedelta

def update_links(obj, links, output_exchange_items, spatial_maps):
    """
    Updates the data from source component exchange items to target component exchange items
    :param obj: a coordinator object
    :param links: the links associated the current model, dict{linkid:link object}
    :param output_exchange_items: All outputs for the source model.
    :param spatial_maps: map dictionary object
    """


    for linkid, link in links.iteritems():

        #target_model  = target[0]
        target_model = link.target_component()

        source_item_name = link.source_exchange_item().name()

        # get the auto generated key for this link
        link_key = generate_link_key(link)

        # get the target interpolation time based on the current time of the target model
        target_time = target_model.get_instance().current_time()

        # get all the datasets of the output exchange item.  These will be used to temporally map the data
        datasets = output_exchange_items[source_item_name].get_all_datasets()

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

def update_links_feed_forward(obj, links, output_exchange_items, spatial_maps):
    """
    Updates the data from source component exchange items to target component exchange items
    :param obj: a coordinator object
    :param links: the links associated the current model, dict{linkid:link object}
    :param output_exchange_items: All outputs for the source model.
    :param spatial_maps: map dictionary object
    """


    for linkid, link in links.iteritems():

        #target_model  = target[0]
        target_model = link.target_component()

        source_item_name = link.source_exchange_item().name()

        # get the auto generated key for this link
        link_key = generate_link_key(link)

        # get the target interpolation time based on the current time of the target model
        target_st = target_model.get_instance().simulation_start()
        target_et = target_model.get_instance().simulation_end()
        target_ts = target_model.get_instance().time_step()

        t = target_st
        target_times = []
        while t <= target_et:
            target_times.append(t)
            t += timedelta(**{target_ts[1]:target_ts[0]})

        # get all the datasets of the output exchange item.  These will be used to temporally map the data
        datasets = output_exchange_items[source_item_name].get_all_datasets()

        # Temporal data mapping
        mapped = {}
        for geom, datavalues in datasets.iteritems():

            # get the dates and values from the geometry
            dates,values = datavalues.get_dates_values()

            # temporal mapping
            temporal = temporal_nearest_neighbor()
            if temporal and values:
                mapped_dates,mapped_values = temporal.transform(dates,values,target_times)

                if mapped_dates is not None:
                    # save the temporally mapped data by output geometry
                    mapped[geom] = (zip(mapped_dates,mapped_values))

        # update links
        if len(mapped.keys()) > 0:
            # get spatially mapped data for the current link
            spatial_mapping = spatial_maps[link_key] if link_key in spatial_maps else None
            if spatial_mapping is None:
                raise Exception('Spatial Mapping was not set!')
            obj.update_link(linkid, mapped, spatial_mapping)