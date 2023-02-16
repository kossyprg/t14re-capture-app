import tkinter as tk
import tkinter.ttk as ttk
from t14re import T14re
from tkcalendar import DateEntry
import datetime
import threading
import time
import os

class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        root.title('t14re capture app')
        root.geometry('800x400+100+100') # width x height
        self.root = root
        self.t14re = T14re()
        self.create_widgets()
        self.rootFoldername = 'data_t14re'

    def create_widgets(self):
        frame_connect = tk.Frame(self.root,relief=tk.GROOVE,bd=2)
        frame_config = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)
        frame_capture = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)
        frame_options = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)

        # COM port label
        self.com_label = tk.Label(frame_connect)
        self.com_label['text'] = 'COM: '

        # Connect button
        connect_btn = tk.Button(frame_connect)
        connect_btn['text'] = 'Connect'
        connect_btn['command'] = self.connect_and_disp_COM_num

        # config label
        self.config_label = tk.Label(frame_config)
        self.config_label['text'] = 'Config: '

        # config entry
        self.config_entry = tk.Entry(frame_config,width=100,state=tk.DISABLED)

        # Load config and setup radar button
        self.load_config_btn = tk.Button(frame_config)
        self.load_config_btn['text'] = 'Load config and setup radar'
        self.load_config_btn['command'] = self.load_config_and_setup_radar
        self.load_config_btn['state'] = 'disabled'

        # Capture mode selection
        self.capture_mode_list = ('Set max files','Endless mode','Scheduled mode')
        self.capture_mode_combobox = ttk.Combobox(frame_capture,state="readonly")
        self.capture_mode_combobox['values'] = self.capture_mode_list
        self.capture_mode_combobox.set('Set max files')
        self.capture_mode_combobox.bind("<<ComboboxSelected>>",self.capture_mode_combobox_selected)

        # Choose folder
        self.choose_folder_btn = tk.Button(frame_options)
        self.choose_folder_btn['text'] = 'Folder'
        self.choose_folder_btn['command'] = self.choose_folder
        self.folder_entry = tk.Entry(frame_options,width=100,state=tk.DISABLED)

        # MaxFiles spinbox
        MaxFiles_label = tk.Label(frame_options)
        MaxFiles_label['text'] = 'Num of files: '
        self.MaxFiles_spinbox = tk.Spinbox(frame_options,format='%4.0f',from_=1,increment=1,to=999999)

        # Entry datetime
        hours_list = [str(x).zfill(2) for x in range(24)]
        minutes_list = [str(x).zfill(2) for x in range(60)]
        seconds_list = [str(x).zfill(2) for x in range(60)]

        ## start datetime
        start_date_label = tk.Label(frame_options)
        start_date_label['text'] = 'start datetime: '
        time_now = datetime.datetime.now().strftime('%H%M%S')
        time_width=3
        self.start_date_dateEntry = DateEntry(frame_options,locale='ja_JP',showweeknumbers=False)
        self.start_time_hour_combobox = ttk.Combobox(frame_options,values=hours_list,width=time_width)
        self.start_time_hour_combobox.set(time_now[0:2])
        self.start_time_minute_combobox = ttk.Combobox(frame_options,values=minutes_list,width=time_width)
        self.start_time_minute_combobox.set(time_now[2:4])
        self.start_time_second_combobox = ttk.Combobox(frame_options,values=seconds_list,width=time_width)
        self.start_time_second_combobox.set(seconds_list[0])

        ## end datetime
        end_date_label = tk.Label(frame_options)
        end_date_label['text'] = 'end datetime: '
        self.end_date_dateEntry = DateEntry(frame_options,locale='ja_JP',showweeknumbers=False)
        self.end_time_hour_combobox = ttk.Combobox(frame_options,values=hours_list,width=time_width)
        self.end_time_hour_combobox.set(time_now[0:2])
        self.end_time_minute_combobox = ttk.Combobox(frame_options,values=minutes_list,width=time_width)
        self.end_time_minute_combobox.set(time_now[2:4])
        self.end_time_second_combobox = ttk.Combobox(frame_options,values=seconds_list,width=time_width)
        self.end_time_second_combobox.set(seconds_list[0])

        # Run/Reserve button
        self.run_btn_list = ('Run','Run','Reserve')
        self.run_btn = tk.Button(frame_capture)
        self.run_btn['text'] = self.run_btn_list[0]
        self.run_btn['state'] = 'disabled'
        self.run_btn['command'] = self.start_capture
        self.stop_btn = tk.Button(frame_capture)
        self.stop_btn['text'] = 'Stop'
        self.stop_btn['state'] = 'disabled'
        self.stop_btn['command'] = self.stop_capture

        # grid 
        frame_connect.grid(row=0,column=0,sticky=tk.NSEW,padx=5,pady=5)
        frame_config.grid(row=0,column=1,sticky=tk.NSEW,padx=5,pady=5)
        frame_capture.grid(row=1,column=0,columnspan=2,sticky=tk.NSEW,padx=5,pady=5)
        frame_options.grid(row=2,column=0,columnspan=2,sticky=tk.NSEW,padx=5,pady=5)

        # ===== arrangement =====
        # COM
        self.com_label.pack(side=tk.TOP)
        connect_btn.pack(side=tk.BOTTOM, ipadx=5, ipady=5, padx=10, pady=5)

        # config
        self.config_label.grid(row=0,column=0)
        self.config_entry.grid(row=0,column=1)
        self.load_config_btn.grid(row=1,column=0,columnspan=2,ipadx=5,ipady=5,padx=10,pady=5)

        # capture
        self.capture_mode_combobox.grid(row=0,column=0)
        self.run_btn.grid(row=1,column=1,ipadx=5, ipady=5,padx=100,pady=10)
        self.stop_btn.grid(row=1,column=2,ipadx=5,ipady=5,padx=100,pady=10)

        # options
        ## Folder
        self.choose_folder_btn.grid(row=0,column=0,ipadx=5, ipady=3, padx=10, pady=5)
        self.folder_entry.grid(row=0,column=1,columnspan=10,sticky=tk.E)

        ## MaxFiles
        mrow = 1
        MaxFiles_label.grid(row=mrow,column=0,pady=5)
        self.MaxFiles_spinbox.grid(row=mrow,column=1)

        ## start date
        srow = 2
        start_date_label.grid(row=srow,column=0,pady=2)
        self.start_date_dateEntry.grid(row=srow,column=1)
        self.label_text_grid(frame_options,row=srow,column=2,text=' ')
        self.start_time_hour_combobox.grid(row=srow,column=3)
        self.label_text_grid(frame_options,row=srow,column=4,text=':')
        self.start_time_minute_combobox.grid(row=srow,column=5)
        self.label_text_grid(frame_options,row=srow,column=6,text=':')
        self.start_time_second_combobox.grid(row=srow,column=7)
        
        ## end date
        erow = 3
        end_date_label.grid(row=erow,column=0,pady=2)
        self.end_date_dateEntry.grid(row=erow,column=1)
        self.label_text_grid(frame_options,row=erow,column=2,text=' ')
        self.end_time_hour_combobox.grid(row=erow,column=3)
        self.label_text_grid(frame_options,row=erow,column=4,text=':')
        self.end_time_minute_combobox.grid(row=erow,column=5)
        self.label_text_grid(frame_options,row=erow,column=6,text=':')
        self.end_time_second_combobox.grid(row=erow,column=7)
    
    def label_text_grid(self,frame,row,column,text):
        label_colon = ttk.Label(frame, text=text)
        label_colon.grid(row=row,column=column)
    
    def capture_mode_combobox_selected(self,event):
        selected_mode = self.capture_mode_combobox.get()
        if selected_mode==self.capture_mode_list[0]:
            self.run_btn['text'] = self.run_btn_list[0]
            self.stop_btn['state'] = 'disabled'
        elif selected_mode==self.capture_mode_list[1]:
            self.run_btn['text'] = self.run_btn_list[1]
            self.stop_btn['state'] = 'normal'
        elif selected_mode==self.capture_mode_list[2]:
            self.run_btn['text'] = self.run_btn_list[2]
            self.stop_btn['state'] = 'disabled'

    def disp_COM_num(self):
        if self.t14re.COM_port_for_MMIC:
            self.com_label['text'] = 'COM: ' + str(self.t14re.COM_port_for_MMIC[3:])
            self.load_config_btn['state'] = 'normal'
        else:
            print('No connection')

    def connect_and_disp_COM_num(self):
        self.t14re.connect_radar()
        self.disp_COM_num()

    def load_config_and_setup_radar(self):
        self.t14re.load_and_send_config()
        CaptureDeviceIndex = 0
        if self.t14re.connect_and_setup_radar(CaptureDeviceIndex):
            self.config_entry['state'] = 'normal'
            self.config_entry.insert(tk.END,self.t14re.config.cfgname)
            self.config_entry['state'] = 'readonly'
            self.run_btn['state'] = 'normal'
        else:
            print('Setup failed')

    def choose_folder(self):
        current_path = os.getcwd()
        folder_name = tk.filedialog.askdirectory(initialdir=current_path)
        print('save folder: ',folder_name)
        self.rootFoldername = folder_name
        self.folder_entry['state'] = 'normal'
        self.folder_entry.insert(tk.END,self.rootFoldername)
        self.folder_entry['state'] = 'readonly'

    def start_capture(self):
        selected_mode = self.capture_mode_combobox.get()
        if selected_mode == self.capture_mode_list[0]:
            MaxFiles = round(float(self.MaxFiles_spinbox.get()))
            startDatetime = 0
            endDatetime = 0
            self.t14re.capture(MaxFiles=MaxFiles, startDatetime=startDatetime, endDatetime=endDatetime,rootFoldername=self.rootFoldername)
        elif selected_mode == self.capture_mode_list[1]:
            MaxFiles = -1
            startDatetime = 0
            endDatetime = 0
            useStopBtn = True
            thread1 = threading.Thread(target=self.t14re.capture,args=(MaxFiles,startDatetime,endDatetime,useStopBtn,self.rootFoldername))
            thread1.start()
        elif selected_mode == self.capture_mode_list[2]:
            MaxFiles = -1
            start_date = self.start_date_dateEntry.get_date()
            start_datetime_str = start_date.strftime('%Y%m%d') + self.start_time_hour_combobox.get() + self.start_time_minute_combobox.get() + self.start_time_second_combobox.get()
            start_datetime = datetime.datetime.strptime(start_datetime_str,'%Y%m%d%H%M%S')
            end_date = self.end_date_dateEntry.get_date()
            end_datetime_str = end_date.strftime('%Y%m%d') + self.end_time_hour_combobox.get() + self.end_time_minute_combobox.get() + self.end_time_second_combobox.get()
            end_datetime = datetime.datetime.strptime(end_datetime_str,'%Y%m%d%H%M%S')
            self.t14re.capture(MaxFiles=MaxFiles, startDatetime=start_datetime, endDatetime=end_datetime,rootFoldername=self.rootFoldername)

    def stop_capture(self):
        print('\nStop!')
        self.t14re.isStopped = True

def main():
    root = tk.Tk()
    app = Application(root=root)
    app.mainloop()

if __name__ == "__main__":
    main()