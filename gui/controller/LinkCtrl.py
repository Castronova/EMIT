import collections
import uuid

import wx
import wx.grid as gridlib
import wx.lib.newevent as ne
from sprint import *
import coordinator.engineAccessors as engine
from emitLogging import elog
from gui.views.LinkView import LinkView
from gui.controller.SpatialCtrl import SpatialCtrl

LinkUpdatedEvent, EVT_LINKUPDATED = ne.NewEvent()


class LinkCtrl(LinkView):
    odesc = ""
    idesc = ""

    def __init__(self, parent, outputs, inputs, link_obj=None, swap=False):
        LinkView.__init__(self, parent, outputs, inputs)

        # link_obj must be a CanvasObjectsCtrl.SmoothLineWithArrow object
        self.link_obj = link_obj

        # self.l = None
        self.swap = swap
        self.swap_was_clicked = False

        # save parent (used in onplot)
        self.parent = parent

        # class link variables used to save link
        self.__selected_link = None

        #  holds the links that will be deleted when deleting->save and close
        self.links_to_delete = []

        self.__link_source_id = self.output_component['id']
        self.__link_target_id = self.input_component['id']
        self.__links = collections.OrderedDict()
        self.link_obj_hit = False

        self.on_start_up(self.output_component, self.input_component)

        self.InitBindings()

        self.__checkbox_states = [None, None]

    def InitBindings(self):
        self.link_name_list_box.Bind(wx.EVT_LISTBOX, self.on_change)
        self.link_name_list_box.Bind(wx.EVT_LEFT_UP, self.on_left_up)

        self.new_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.new_button.Bind(wx.EVT_BUTTON, self.on_new_button)
        self.delete_button.Bind(wx.EVT_BUTTON, self.on_delete)
        self.swap_button.Bind(wx.EVT_BUTTON, self.on_swap)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_plot_geometries)
        self.Bind(EVT_LINKUPDATED, self.on_link_selected)
        self.Bind(wx.EVT_CLOSE, self.on_cancel)
        self.output_grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.on_output_grid_hover)
        self.input_grid.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.on_input_grid_hover)

        self.output_combo.Bind(wx.EVT_COMBOBOX, self.on_select_output)
        self.input_combo.Bind(wx.EVT_COMBOBOX, self.on_select_input)
        self.temporal_combo.Bind(wx.EVT_COMBOBOX, self.on_select_temporal)
        self.spatial_combo.Bind(wx.EVT_COMBOBOX, self.on_select_spatial)

        self.Bind(wx.EVT_SIZE, self.frame_resizing)

    def activate_swap(self):
        if self.swap:
            self.swap_button.Enable()
        else:
            self.swap_button.Disable()

    def activate_controls(self, activate=True):
        if activate:
            self.save_button.Enable()
            self.spatial_combo.Enable()
            self.temporal_combo.Enable()
            self.input_combo.Enable()
            self.output_combo.Enable()
            self.plot_button.Enable()
            self.activate_swap()
        else:
            self.save_button.Disable()
            self.spatial_combo.Disable()
            self.temporal_combo.Disable()
            self.input_combo.Disable()
            self.output_combo.Disable()
            self.plot_button.Disable()
            self.swap_button.Disable()

    def create_one_way_arrow(self, image, models):
        #  Only call this method if all the links go the same direction
        #  Draws the arrow based off the direction of the links
        if engine.getModelById(models[0].ID)["name"] == engine.getModelById(self.__links.values()[0].source_id)["name"]:
            self.parent.Parent.createLine(R1=models[0], R2=models[1], image_name=image)
        else:
            self.parent.Parent.createLine(R1=models[1], R2=models[0], image_name=image)

    def find_link_direction(self):
        # returns None if no link. Show question mark
        # return true if link goes one. Show one-way arrow
        # return false if links goes two ways. Show two-way arrow
        if len(self.__links) == 0:
            return None

        items = []
        for key, value in self.__links.iteritems():
            items.append(engine.getModelById(value.source_id)["name"])

        return all_same(items)

    def frame_resizing(self, event):
        self.resize_grid_to_fill_white_space(self.input_grid)
        self.resize_grid_to_fill_white_space(self.output_grid)
        event.Skip()  # In a sizer-based layout, event.Skip() will catch all size events

    def get_input_model_text(self):
        if self.input_component['id'] == self.__selected_link.target_id:
            return self.input_component['name']
        else:
            return self.output_component['name']

    def get_link_by_name(self, name):
        for l in self.__links.values():
            if l.name() == name:
                return l
        return None

    def get_model_from(self):
        if 'name' in self.output_component:
            return self.output_component['name']
        else:
            return None

    def get_model_to(self):
        if 'name' in self.input_component:
            return self.input_component['name']
        else:
            return None

    def get_output_model_text(self):
        if self.output_component['id'] == self.__selected_link.source_id:
            return self.output_component['name']
        else:
            return self.input_component['name']

    def get_selected_link_id(self):
        selection = self.link_name_list_box.GetStringSelection()
        link_id = selection.split('|')[0].strip()
        return link_id

    def on_start_up(self, component1, component2):
        self.input_combo.SetItems(['---'] + self.input_combo_choices())
        self.output_combo.SetItems(['---'] + self.output_combo_choices())

        links = []
        x = engine.getLinksBtwnModels(component1['id'], component2['id'])
        y = engine.getLinksBtwnModels(component2['id'], component1['id'])
        if x:
            for l in x:
                links.append(l)
        if y:
            for l in y:
                links.append(l)

        if links:
            for l in links:
                link = LinkInfo(l['source_item'],
                                l['target_item'],
                                l['source_id'],
                                l['target_id'],
                                l['id'],
                                l['spatial_interpolation'],
                                l['temporal_interpolation'])


                self.__links[l['id']] = link

            # select the first value
            self.refresh_link_name_box()
            self.link_name_list_box.SetSelection(0)
            self.__selected_link = self.__links.keys()[0]
            self.on_change(None)
        else:
            # if no links are found, need to deactivate controls
            self.activate_controls(False)

    def populate_output_metadata(self, l):

        # get the link object
        outputs = l.output_metadata
        if l.oei in outputs:
            o = outputs[l.oei]

            self.output_grid.SetCellValue(1, 1, o['variable'].VariableNameCV())
            self.output_grid.SetCellValue(2, 1, o['variable'].VariableDefinition())
            self.odesc = o['variable'].VariableDefinition()

            self.output_grid.SetCellValue(4, 1, o['unit'].UnitName())
            self.output_grid.SetCellValue(5, 1, o['unit'].UnitTypeCV())
            self.output_grid.SetCellValue(6, 1, o['unit'].UnitAbbreviation())
        else:
            self.odesc = ""
            self.reset_grid(self.output_grid)

    def populate_input_metadata(self, l):

        # get the link object
        inputs = l.input_metadata
        if l.iei in inputs:
            i = inputs[l.iei]

            self.input_grid.SetCellValue(1, 1, i['variable'].VariableNameCV())
            self.input_grid.SetCellValue(2, 1, i['variable'].VariableDefinition())
            self.idesc = i['variable'].VariableDefinition()

            self.input_grid.SetCellValue(4, 1, i['unit'].UnitName())
            self.input_grid.SetCellValue(5, 1, i['unit'].UnitTypeCV())
            self.input_grid.SetCellValue(6, 1, i['unit'].UnitAbbreviation())
        else:
            self.idesc = ""
            self.reset_grid(self.input_grid)

    def reset_grid(self, grid):
        if not isinstance(grid, wx.grid.Grid):
            sPrint("grid must be type wx.grid.Grid", MessageType.DEBUG)
            return

        grid.SetCellValue(1, 1, "")
        grid.SetCellValue(2, 1, "")

        grid.SetCellValue(4, 1, "")
        grid.SetCellValue(5, 1, "")
        grid.SetCellValue(6, 1, "")

    def refresh_link_name_box(self):

        self.link_name_list_box.Clear()
        for key, value in self.__links.iteritems():
            if key in self.links_to_delete:
                pass
            else:
                self.link_name_list_box.Append(value.name())

    def replace_canvas_image(self, image, one_way=False):
        self.parent.Parent.remove_link_image(link_object=self.link_obj.line)

        models = self.parent.Parent.arrows[self.link_obj]
        if one_way:
            #  Determine the direction of the arrow
            self.create_one_way_arrow(image, models)
        else:
            self.parent.Parent.createLine(R1=models[0], R2=models[1], image_name=image)

    def remove_warning_links(self, warnings):
        # If warnings is in __links
        if set(warnings).issubset(set(self.__links.values())):
            new_list = collections.OrderedDict()
            for key, value in self.__links.items():
                if value not in warnings:
                    new_list[key] = value

            self.__links = new_list
            self.refresh_link_name_box()

    ######################################
    # EVENTS
    ######################################

    def on_cancel(self, event):
        self.Destroy()

    def on_change(self, event):
        link_name = self.link_name_list_box.GetStringSelection()

        # get the selected link
        l = self.get_link_by_name(link_name)

        # set the currently selected link
        self.__selected_link = l

        # update the combobox selections
        self.output_combo.SetStringSelection(l.oei)
        self.input_combo.SetStringSelection(l.iei)

        if l.temporal_interpolation is not None:
            self.temporal_combo.SetStringSelection(l.temporal_interpolation)
        else:
            # set default value
            self.temporal_combo.SetSelection(0)

        if l.spatial_interpolation is not None:
            self.spatial_combo.SetStringSelection(l.spatial_interpolation)
        else:
            # set default value
            self.spatial_combo.SetSelection(0)

        # set the state of link_obj_hit
        self.link_obj_hit = True

        wx.PostEvent(self, LinkUpdatedEvent())

    def on_delete(self, event):
        #  Links are placed in a queue that will be deleted permanently when clicking on save and close.

        if self.link_name_list_box.GetSelection() < 0:
            elog.info("Please select a link to delete")
            return

        # get the link id
        linkid = self.get_selected_link_id()

        self.links_to_delete.append(linkid)

        index = self.link_name_list_box.GetSelection()
        self.link_name_list_box.Delete(index)

    def on_input_grid_hover(self, e):
        self.on_input_grid_tool_tip(e)

    def on_input_grid_tool_tip(self, e):
        if e.GetRow() == 2 and e.GetCol() == 1:
            self.input_grid.SetToolTip(wx.ToolTip(self.idesc))
        else:
            self.input_grid.SetToolTip(wx.ToolTip(""))
        e.Skip()

    def on_left_up(self, event):

        if not self.link_obj_hit:
            link_name = self.__selected_link.name()

            selected_index = self.link_name_list_box.Items.index(link_name)
            self.link_name_list_box.SetSelection(selected_index)

        # reset the state of link_obj_hit
        self.link_obj_hit = False

    def on_link_selected(self, event):

        # get the selected link object
        selected = self.link_name_list_box.GetStringSelection()
        selected_id = selected.split('|')[0].strip()

        # make sure a link is selected
        if selected_id in self.__links.keys():

            # get the selected link object
            self.__selected_link = self.__links[selected_id]

            # activate controls
            self.activate_controls(True)

            # populate the link metadata
            self.populate_output_metadata(self.__selected_link)
            self.populate_input_metadata(self.__selected_link)

            #  Setting the labels that indicate which metadata is input and output
            self.input_label.SetLabel("Input of: " + str(self.get_input_model_text()))
            self.output_label.SetLabel("Output of: " + str(self.get_output_model_text()))

        else:
            # deactivate controls if nothing is selected
            self.activate_controls(False)

    def on_new_button(self, event):

        # set the exchange item values to ---
        self.input_combo.SetSelection(0)
        self.output_combo.SetSelection(0)

        # generate a unique name for this link
        oei = self.output_combo.GetValue()
        iei = self.input_combo.GetValue()

        # create a link object and save it at the class level
        l = LinkInfo(oei, iei, self.__link_source_id, self.__link_target_id)
        self.__links[l.uid] = l

        # add the link name to the links list box
        self.refresh_link_name_box()

        # set the currently selected link
        self.__selected_link = l

        # select the last value
        self.link_name_list_box.SetSelection(self.link_name_list_box.GetCount() - 1)

        self.on_change(None)

        self.output_label.SetLabel("Output of " + self.get_model_from())
        self.input_label.SetLabel("Input of " + self.get_model_to())

    def on_output_grid_hover(self, e):
        self.on_output_grid_tool_tip(e)

    def on_output_grid_tool_tip(self, e):
        if e.GetRow() == 2 and e.GetCol() == 1:
            self.output_grid.SetToolTip(wx.ToolTip(self.odesc))
        else:
            self.output_grid.SetToolTip(wx.ToolTip(""))
        e.Skip()

    def on_plot_geometries(self, event):
        """
        Launches the spatial plot view that displays the geographic representations and metadata associated with
        various input and output exchange items
        Args:
            event: wx.EVT_BUTTON

        Returns: None

        """
        frame = wx.Frame(self.parent, size=(630, 685), style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        title = self.get_output_model_text() + " --> " + self.get_input_model_text()
        controller = SpatialCtrl(frame)

        # input exchange item -> iei
        iei = controller.get_input_exchange_item_by_id(self.__selected_link.target_id)
        igeom = controller.get_geometries(iei)

        # output exchange item -> oei
        oei = controller.get_output_exchange_item_by_id(self.__selected_link.source_id)
        ogeom = controller.get_geometries(oei)

        controller.set_data(target=igeom, source=ogeom)
        controller.raw_input_data = iei
        controller.raw_output_data = oei

        controller.add_input_combo_choices(igeom.keys())
        controller.add_output_combo_choices(ogeom.keys())

        frame.SetTitle(title)
        frame.Show()

    def on_save(self, event):
        """
        Saves all link objects to the engine and then closes the link creation window
        """

        # Deleting the links that are in the delete queue
        for link_id in self.links_to_delete:
            engine.removeLinkById(link_id)
            if link_id in self.__links:
                self.__links.pop(link_id)

        warnings = []
        errors = []
        for l in self.__links.values():

            if l.iei == '---' or l.oei == '--':
                warnings.append(l)
            else:

                try:
                    kwargs = dict(source_id=l.source_id,
                                  source_item=l.oei,
                                  target_id=l.target_id,
                                  target_item=l.iei,
                                  spatial_interpolation=l.spatial_interpolation,
                                  temporal_interpolation=l.temporal_interpolation,
                                  uid=l.uid)

                    # remove the existing link, if there is one
                    engine.removeLinkById(l.uid)

                    # add a new link inside the engine
                    link_id = engine.addLink(**kwargs)

                    if link_id:
                        l.saved = True

                    wx.PostEvent(self, LinkUpdatedEvent())
                except:
                    elog.error('ERROR|Could not save link: %s' % l.name)
                    errors.append(l)

        if len(warnings) > 0:
            warning_links = '\n'.join(l.name() for l in warnings)
            warning = wx.MessageDialog(self,
                                       "Could not save the following links because they lacking either input or output items: \n\n " + warning_links + "\n\n Would you like to discard these partial link objects?",
                                       'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING)

            if warning.ShowModal() == wx.ID_YES:
                self.remove_warning_links(warnings=warnings)
                self.Destroy()
            else:
                return
        result = self.find_link_direction()
        if result:
            # todo: these images need to be coming from config instead of hardcoded
            self.replace_canvas_image(image="rightArrowBlue60.png", one_way=True)
        elif result is False:
            self.replace_canvas_image(image="multiArrow.png")
        else:
            self.replace_canvas_image(image="questionMark.png")

        self.Destroy()

    def on_select_input(self, event):
        """
        sets the metadata for the selected input exchange item and populates a tree view
        """

        # get selected value
        input_name = self.input_combo.GetValue()

        # get the current link
        l = self.__selected_link

        # change the link name to reflect output -> input
        l.iei = input_name
        l.refresh('input')

        # update the name in the links list
        self.__links[l.uid] = l

        # refresh the link name box
        self.refresh_link_name_box()

        # populate metadata
        self.populate_input_metadata(l)

    def on_select_output(self, event):
        """
        sets the metadata for the selected output exchange item and populates a tree view
        """

        # get selected value
        output_name = self.output_combo.GetValue()

        # get the current link
        selected_link = self.__selected_link

        # change the link name to reflect output -> input
        selected_link.oei = output_name
        selected_link.refresh('output')

        # update the name in the links list
        self.__links[selected_link.uid] = selected_link

        # refresh the link name box
        self.refresh_link_name_box()

        # populate metadata
        self.populate_output_metadata(selected_link)

    def on_select_spatial(self, event):
        # get the current link---
        l = self.__selected_link

        spatial_value = self.spatial_combo.GetValue()
        if spatial_value == 'None Specified':
            l.spatial_interpolation = None
        else:
            l.spatial_interpolation = self.spatial_transformations[spatial_value]

    def on_select_temporal(self, event):
        # get the current link
        l = self.__selected_link

        temporal_value = self.temporal_combo.GetValue()
        if temporal_value == 'None Specified':
            l.temporal_interpolation = None
        else:
            l.temporal_interpolation = self.temporal_transformations[temporal_value]

    def on_swap(self, event):
        try:
            selected = self.get_selected_link_id()
            engine.removeLinkById(selected)
            self.__links.pop(selected)

        except Exception as e:
            elog.debug(e)
            elog.warning("Please select which link to swap")
            return

        self.swap_was_clicked = True

        #  Swapping components of models
        temp = self.output_component
        self.output_component = self.input_component
        self.input_component = temp

        self.__link_source_id = self.output_component['id']
        self.__link_target_id = self.input_component['id']

        self.input_combo.SetItems(['---'] + self.input_combo_choices())
        self.output_combo.SetItems(['---'] + self.output_combo_choices())
        self.input_combo.SetSelection(0)
        self.output_combo.SetSelection(0)

        self.on_new_button(1)


class LinkInfo:
    def __init__(self, oei, iei, source_id, target_id, uid=None, spatial_interpolation=None, temporal_interpolation=None):


        self.uid = 'L' + uuid.uuid4().hex if uid is None else uid
        # self.name = self.generate_link_name(oei,iei,self.uid)
        self.oei = oei
        self.iei = iei
        self.source_id = source_id
        self.target_id = target_id
        self.spatial_interpolation = spatial_interpolation
        self.temporal_interpolation = temporal_interpolation

        self.saved = False

        self.output_metadata = {}
        self.input_metadata = {}

        self.get_input_and_output_metadata()

    def refresh(self, type):
        self.get_input_and_output_metadata(type)

    def name(self):
        iei_name = self.iei if self.iei != '---' else '?'
        oei_name = self.oei if self.oei != '---' else '?'

        if iei_name == '?' and oei_name == '?':
            return '%s' % self.uid
        else:
            return '%s | %s -> %s ' % (self.uid, oei_name, iei_name)

    def get_input_and_output_metadata(self, type=None):

        if type == 'output' or type is None:
            # get output information
            outputs = engine.getExchangeItems(self.source_id, 'OUTPUT')
            if outputs is not None:
                for output in outputs:
                    self.output_metadata[output['name']] = output
        if type == 'input' or type is None:
            # get input information
            inputs = engine.getExchangeItems(self.target_id, 'INPUT')
            if inputs is not None:
                for input in inputs:
                    self.input_metadata[input['name']] = input


def all_same(items):
        return all(x == items[0] for x in items)
