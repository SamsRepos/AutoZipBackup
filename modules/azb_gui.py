import wx
import threading
from time import sleep
from .azb_repository import AzbRepository
from .models.dir_source_model import DirSourceModel
from .models.dir_destination_model import DirDestinationModel

def start_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.daemon = True
    thread.start()

gui_running = False

class GuiPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.repository = AzbRepository()
        self.item_data = {}
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        controls_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_source_button = wx.Button(self, label="Add Source")
        self.add_source_button.Bind(wx.EVT_BUTTON, self.on_add_source)
        controls_sizer.Add(self.add_source_button, 0, wx.ALL, 5)
        
        self.add_destination_button = wx.Button(self, label="Add Destination")
        self.add_destination_button.Bind(wx.EVT_BUTTON, self.on_add_destination)
        controls_sizer.Add(self.add_destination_button, 0, wx.ALL, 5)
        
        self.refresh_button = wx.Button(self, label="Refresh")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        controls_sizer.Add(self.refresh_button, 0, wx.ALL, 5)
        
        main_sizer.Add(controls_sizer)
        
        self.list_ctrl = wx.ListCtrl(
            self, 
            style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_SUNKEN
        )
        
        self.list_ctrl.InsertColumn(0, "Name", width=150)
        self.list_ctrl.InsertColumn(1, "Directory Path", width=300)
        self.list_ctrl.InsertColumn(2, "Active", width=100)
        self.list_ctrl.InsertColumn(3, "Latest Hash", width=200)
        
        main_sizer.Add(self.list_ctrl, 1, wx.EXPAND | wx.ALL, 5)
        
        self.SetSizer(main_sizer)
        self.update_sources_display()
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)

    def update_sources_display(self):
        self.list_ctrl.DeleteAllItems()
        self.item_data.clear()
        
        sources = self.repository.get_all_dir_source_models()
        for source in sources:
            index = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertItem(index, source.task_name)
            self.list_ctrl.SetItem(index, 1, source.dir_path)
            self.list_ctrl.SetItem(index, 2, str(source.task_active))
            self.list_ctrl.SetItem(index, 3, source.latest_hash or "")
            self.item_data[index] = source
            
            self.list_ctrl.SetItemBackgroundColour(index, wx.Colour(240, 240, 240))
            
            # Set text color based on active status
            text_color = wx.Colour(160, 160, 160) if not source.task_active else wx.BLACK
            for col in range(4):
                self.list_ctrl.SetItemTextColour(index, text_color)
            
            destinations = self.repository.get_dir_destination_models(source.id)
            for dest in destinations:
                dest_index = self.list_ctrl.GetItemCount()
                self.list_ctrl.InsertItem(dest_index, "    → Destination")
                self.list_ctrl.SetItem(dest_index, 1, dest.dir_path)
                self.list_ctrl.SetItem(dest_index, 2, str(dest.active))
                self.list_ctrl.SetItem(dest_index, 3, dest.latest_source_hash or "")
                self.item_data[dest_index] = dest
                
                # Set destination text color based on both source and destination active status
                dest_text_color = wx.Colour(160, 160, 160) if not source.task_active or not dest.active else wx.BLACK
                row_is_outdated = (dest.latest_source_hash or "") != (source.latest_hash or "")
                if row_is_outdated:
                    self.list_ctrl.SetItemBackgroundColour(dest_index, wx.Colour(255, 220, 220))
                    dest_text_color = wx.Colour(220, 0, 0)
                else:
                    self.list_ctrl.SetItemBackgroundColour(dest_index, wx.NullColour)
                for col in range(4):
                    self.list_ctrl.SetItemTextColour(dest_index, dest_text_color)

    def on_add_source(self, event):
        dialog = wx.Dialog(self, title="Add Source Directory")
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)

        task_label = wx.StaticText(dialog, label="Task Name:")
        dialog_sizer.Add(task_label, 0, wx.ALL, 5)
        task_input = wx.TextCtrl(dialog)
        dialog_sizer.Add(task_input, 0, wx.EXPAND|wx.ALL, 5)

        dir_label = wx.StaticText(dialog, label="Directory Path:")
        dialog_sizer.Add(dir_label, 0, wx.ALL, 5)
        dir_input = wx.TextCtrl(dialog)
        dialog_sizer.Add(dir_input, 0, wx.EXPAND|wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(dialog, wx.ID_OK, "Save")
        cancel_button = wx.Button(dialog, wx.ID_CANCEL, "Cancel")
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)
        dialog_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        dialog.SetSizer(dialog_sizer)
        dialog.Fit()

        if dialog.ShowModal() == wx.ID_OK:
            try:
                new_source = DirSourceModel({
                    "id": None,
                    "task_name": task_input.GetValue(),
                    "dir_path": dir_input.GetValue(),
                    "active": True,
                    "latest_hash": ""
                })
                self.repository.save_dir_source(new_source)
                self.update_sources_display()
                wx.MessageBox("Source directory added successfully!", "Success", 
                            wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error adding source: {str(e)}", "Error", 
                            wx.OK | wx.ICON_ERROR)

        dialog.Destroy()

    def on_add_destination(self, event):
        sources = self.repository.get_all_dir_source_models()
        if not sources:
            wx.MessageBox("No source directories available. Please add a source first.", 
                        "Error", wx.OK | wx.ICON_ERROR)
            return

        dialog = wx.Dialog(self, title="Add Destination Directory")
        dialog_sizer = wx.BoxSizer(wx.VERTICAL)

        source_label = wx.StaticText(dialog, label="Select Source:")
        dialog_sizer.Add(source_label, 0, wx.ALL, 5)
        source_choices = [f"{s.task_name} ({s.dir_path})" for s in sources]
        source_combo = wx.ComboBox(dialog, choices=source_choices, style=wx.CB_DROPDOWN|wx.CB_READONLY)
        source_combo.SetSelection(0)
        dialog_sizer.Add(source_combo, 0, wx.EXPAND|wx.ALL, 5)

        dir_label = wx.StaticText(dialog, label="Destination Path:")
        dialog_sizer.Add(dir_label, 0, wx.ALL, 5)
        dir_input = wx.TextCtrl(dialog)
        dialog_sizer.Add(dir_input, 0, wx.EXPAND|wx.ALL, 5)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        ok_button = wx.Button(dialog, wx.ID_OK, "Save")
        cancel_button = wx.Button(dialog, wx.ID_CANCEL, "Cancel")
        button_sizer.Add(ok_button, 0, wx.ALL, 5)
        button_sizer.Add(cancel_button, 0, wx.ALL, 5)
        dialog_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 5)

        dialog.SetSizer(dialog_sizer)
        dialog.Fit()

        if dialog.ShowModal() == wx.ID_OK:
            try:
                selected_source = sources[source_combo.GetSelection()]
                new_destination = DirDestinationModel({
                    "id": None,
                    "dir_source_id": selected_source.id,
                    "dir_path": dir_input.GetValue(),
                    "active": True,
                    "latest_source_hash": ""
                })
                self.repository.save_dir_destination(new_destination)
                self.update_sources_display()
                wx.MessageBox("Destination directory added successfully!", "Success", 
                            wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error adding destination: {str(e)}", "Error", 
                            wx.OK | wx.ICON_ERROR)

        dialog.Destroy()

    def on_refresh(self, event):
        self.update_sources_display()

    def update(self):
        pass

    def on_right_click(self, event):
        index = event.GetIndex()
        item = self.item_data.get(index)
        if not item:
            return
        
        menu = wx.Menu()
        
        if isinstance(item, DirSourceModel):
            # Source directory options
            edit_name = menu.Append(-1, "Edit Task Name")
            edit_path = menu.Append(-1, "Edit Source Path")
            toggle_active = menu.Append(-1, "Deactivate" if item.task_active else "Activate")
            
            self.Bind(wx.EVT_MENU, 
                     lambda evt: self.edit_source_name(item), 
                     edit_name)
            self.Bind(wx.EVT_MENU, 
                     lambda evt: self.edit_source_path(item), 
                     edit_path)
            self.Bind(wx.EVT_MENU,
                     lambda evt: self.toggle_source_active(item),
                     toggle_active)
        else:
            # Destination directory options
            edit_path = menu.Append(-1, "Edit Destination Path")
            toggle_active = menu.Append(-1, "Deactivate" if item.active else "Activate")
            
            self.Bind(wx.EVT_MENU, 
                     lambda evt: self.edit_destination_path(item), 
                     edit_path)
            self.Bind(wx.EVT_MENU,
                     lambda evt: self.toggle_destination_active(item),
                     toggle_active)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def edit_source_name(self, source):
        dialog = wx.TextEntryDialog(
            self,
            "Enter new task name:",
            "Edit Task Name",
            source.task_name
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                new_name = dialog.GetValue()
                self.repository.update_source_task_name(source.id, new_name)
                self.update_sources_display()
                wx.MessageBox("Task name updated successfully!", "Success", 
                            wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error updating task name: {str(e)}", "Error", 
                            wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def edit_source_path(self, source):
        dialog = wx.TextEntryDialog(
            self,
            "Enter new source path:",
            "Edit Source Path",
            source.dir_path
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                new_path = dialog.GetValue()
                self.repository.update_source_dir_path(source.id, new_path)
                self.update_sources_display()
                wx.MessageBox("Source path updated successfully!", "Success", 
                            wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error updating source path: {str(e)}", "Error", 
                            wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def edit_destination_path(self, destination):
        dialog = wx.TextEntryDialog(
            self,
            "Enter new destination path:",
            "Edit Destination Path",
            destination.dir_path
        )
        
        if dialog.ShowModal() == wx.ID_OK:
            try:
                new_path = dialog.GetValue()
                self.repository.update_destination_dir_path(destination.id, new_path)
                self.update_sources_display()
                wx.MessageBox("Destination path updated successfully!", "Success", 
                            wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Error updating destination path: {str(e)}", "Error", 
                            wx.OK | wx.ICON_ERROR)
        
        dialog.Destroy()

    def toggle_source_active(self, source):
        try:
            new_status = not source.task_active
            self.repository.update_source_active_status(source.id, new_status)
            self.update_sources_display()
            status_text = "activated" if new_status else "deactivated"
            wx.MessageBox(f"Task {status_text} successfully!", "Success", 
                        wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error updating task status: {str(e)}", "Error", 
                        wx.OK | wx.ICON_ERROR)

    def toggle_destination_active(self, destination):
        try:
            new_status = not destination.active
            self.repository.update_destination_active_status(destination.id, new_status)
            self.update_sources_display()
            status_text = "activated" if new_status else "deactivated"
            wx.MessageBox(f"Destination {status_text} successfully!", "Success", 
                        wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error updating destination status: {str(e)}", "Error", 
                        wx.OK | wx.ICON_ERROR)

class GuiFrame(wx.Frame):
    def __init__(self):
        super().__init__(
            parent=None,
            title="AZB Directory Manager",
            pos=(50, 60),
            size=(800, 600)
        )
        self.panel = GuiPanel(self)
        global gui_running
        gui_running = True
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def on_close(self, event):
        global gui_running
        gui_running = False
        self.Destroy()

SECONDS_BETWEEN_UPDATES = 0.5

def main_loop(frame):
    while gui_running:
        wx.CallAfter(frame.panel.update)
        sleep(SECONDS_BETWEEN_UPDATES)

def run_gui():
    app = wx.App()
    frame = GuiFrame()
    start_thread(main_loop, frame)
    frame.Show()
    app.MainLoop()
  