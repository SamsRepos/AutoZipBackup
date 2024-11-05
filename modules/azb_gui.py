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

    def update_sources_display(self):
        self.list_ctrl.DeleteAllItems()
        
        sources = self.repository.get_all_dir_source_models()
        for source in sources:
            index = self.list_ctrl.GetItemCount()
            self.list_ctrl.InsertItem(index, source.task_name)
            self.list_ctrl.SetItem(index, 1, source.dir_path)
            self.list_ctrl.SetItem(index, 2, str(source.task_active))
            self.list_ctrl.SetItem(index, 3, source.latest_hash or "")
            
            self.list_ctrl.SetItemBackgroundColour(index, wx.Colour(240, 240, 240))
            
            destinations = self.repository.get_dir_destination_models(source.id)
            for dest in destinations:
                dest_index = self.list_ctrl.GetItemCount()
                self.list_ctrl.InsertItem(dest_index, "    → Destination")
                self.list_ctrl.SetItem(dest_index, 1, dest.dir_path)
                self.list_ctrl.SetItem(dest_index, 2, str(dest.active))
                self.list_ctrl.SetItem(dest_index, 3, dest.latest_source_hash or "")

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
  