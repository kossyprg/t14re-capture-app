import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import os
import glob
import scipy.io
from t14re import Config
from tkinter import filedialog
import threading
import datetime
import math

class Application(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root)
        root.title('t14re bin2mat converter app')
        root.geometry('800x400+100+100') # width x height
        self.root = root
        self.path_cfg = 0
        self.path_data_folder = 0
        self.n = 0 # number of converted files
        self.N = 0 # number of all files
        self.config = Config()
        self.create_widgets()
        self.configIsLoaded = False
        self.dataIsDefined = False
    
    def create_widgets(self):
        frame_config = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)
        frame_data_folder = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)
        frame_main = tk.Frame(self.root,relief=tk.GROOVE,bd=2,padx=10,pady=10)

        # Load config button
        load_config_btn = tk.Button(frame_config)
        load_config_btn['text'] = 'Config file'
        load_config_btn['command'] = self.load_configfile
        self.config_entry = tk.Entry(frame_config,width=100,state=tk.DISABLED)

        # choose data folder
        choose_folder_btn = tk.Button(frame_data_folder,
                                    text='Folder',
                                    command=self.choose_data_folder)
        self.folder_entry = tk.Entry(frame_data_folder,width=100,state=tk.DISABLED)
        self.folder_num_label = tk.Label(frame_data_folder,text='Number of files: ')

        # main
        self.progress_condition_label = tk.Label(frame_main)
        self.progressbar = ttk.Progressbar(frame_main,
                                            mode="determinate",
                                            variable=self.n)
        self.progress_percentage_label = tk.Label(frame_main)
        self.progress_remaining_time_label = tk.Label(frame_main)
        self.convert_btn = tk.Button(frame_main,
                                    command=self.main_convert,
                                    text='Convert',
                                    state='disabled')

        # Set frames
        frame_config.grid(row=0,column=0,sticky=tk.NSEW,padx=5,pady=5)
        frame_data_folder.grid(row=1,column=0,sticky=tk.NSEW,padx=5,pady=5)
        frame_main.grid(row=2,column=0,sticky=tk.NSEW,padx=5,pady=5)

        # ===== arrangement =====
        load_config_btn.pack(side=tk.LEFT,padx=5)
        self.config_entry.pack(side=tk.TOP,expand=True,fill=tk.X)

        choose_folder_btn.pack(side=tk.LEFT,padx=5,pady=(0,20))
        self.folder_entry.pack(side=tk.TOP,expand=True,fill=tk.X)
        self.folder_num_label.pack(side=tk.BOTTOM)

        self.progress_condition_label.pack(anchor=tk.N)
        self.progressbar.pack(anchor=tk.N,expand=True,fill=tk.X)
        self.progress_percentage_label.pack(anchor=tk.N)
        self.progress_remaining_time_label.pack(anchor=tk.N)
        self.convert_btn.pack(anchor=tk.N,ipadx=10,ipady=5)

    def load_configfile(self):
        path = os.getcwd()
        typ = [('configuration file','*.cfg')]
        self.path_cfg = filedialog.askopenfilename(filetypes=typ,initialdir=path)
        if not self.path_cfg:
            print('Canceled')
        else:
            self.config_entry['state'] = 'normal'
            self.config_entry.insert(tk.END,self.path_cfg)
            self.config_entry['state'] = 'readonly'
            self.config.load_config(self.path_cfg)
            self.configIsLoaded = True
        if self.configIsLoaded and self.dataIsDefined:
            self.convert_btn['state'] = 'normal'

    def choose_data_folder(self):
        current_path = os.getcwd()
        self.path_data_folder = tk.filedialog.askdirectory(initialdir=current_path)
        if not self.path_data_folder:
            print('Canceled')
        else:
            print('target folder: ',self.path_data_folder)
            files = glob.glob(self.path_data_folder + "*/*.bin")
            N = len(files)
            if N < 1:
                print('No binary files. Check the folder.')
            else:
                self.folder_entry['state'] = 'normal'
                self.folder_entry.insert(tk.END,self.path_data_folder)
                self.folder_entry['state'] = 'readonly'
                self.N = N
                self.n = 0
                self.bin_files = files
                self.folder_num_label['text'] = 'Number of files: ' + str(self.N)
                self.progressbar.configure(maximum=self.N,value=self.n)
                print('Num of files: ',self.N)
                self.dataIsDefined = True
        if self.configIsLoaded and self.dataIsDefined:
            self.convert_btn['state'] = 'normal'
    
    def convert_data_bin2mat(self):
        self.progress_condition_label['text'] = 'Converting...'
        for i in range(self.N):
            print('\rfilenum: '+str(i+1)+'/'+str(self.N), end='')
            fname = self.bin_files[i]
            fr = open(fname, 'rb')
            data = np.frombuffer(fr.read(),np.uint8)
            
            data2 = data.reshape(self.config.FramesPerData,self.config.frameCfg['ChirpsetsPerFrame'],self.config.NTx*self.config.NRx,self.config.profileCfg['numAdcSamples'],2,2)
            
            I_data = (data2[:, :, :, :, 0, 0] + data2[:, :, :, :, 0, 1] * 256).astype(np.int16)
            Q_data = (data2[:, :, :, :, 1, 0] + data2[:, :, :, :, 1, 1] * 256).astype(np.int16)
            
            I_data[I_data >= 0x8000] -= 0x10000
            Q_data[Q_data >= 0x8000] -= 0x10000
            
            data_reshape = I_data + 1j * Q_data
            
            # save mat file
            scipy.io.savemat(fname.replace('.bin','') + ".mat", {'signals': data_reshape})
            self.n += 1
        self.progress_condition_label['text'] = 'Done!'
        return True

    def update_progressbar(self):
        delay = 5 # ms
        while self.n <= self.N:
            if self.n==self.N:
                self.progressbar.after(delay,self.progressbar.configure(value=self.n))
                self.progressbar.update()
                self.progress_percentage_label['text'] = '100%'
                self.progress_remaining_time_label['text'] = ''
                break
            else:
                if self.n > 5:
                    self.progress_remaining_time_label['text'] = self.output_rest_time_log()
                self.progressbar.after(delay,self.progressbar.configure(value=self.n))
                self.progressbar.update()
                self.progress_percentage_label['text'] = str(round(self.n/self.N*100)) + '%'
        return True

    def main_convert(self):
        self.n = 0
        self.start_time = datetime.datetime.now()
        thread1 = threading.Thread(target=self.convert_data_bin2mat)
        thread2 = threading.Thread(target=self.update_progressbar)
        thread1.start()
        thread2.start()

    def output_rest_time_log(self):
        dt = datetime.datetime.now() - self.start_time
        dt_sec = dt.total_seconds()
        v = self.n/dt_sec # files/sec
        time_remain = math.ceil((self.N-self.n)/v) # ex) 0.5 sec -> 1 sec
        if time_remain>3600:
            hours = math.floor(time_remain/3600)
            minutes = math.floor((time_remain-hours*3600)/60)
            out_log = str(hours) + ' h ' + str(minutes) + ' min remaining'
        elif time_remain>60:
            minutes = math.floor(time_remain/60)
            seconds = round(time_remain-minutes*60)
            out_log = str(minutes) + ' min ' + str(seconds) + ' sec remaining'
        else:
            out_log = str(time_remain) + ' sec remaining'
        return out_log

def main():
    root = tk.Tk()
    app = Application(root=root)
    app.mainloop()

if __name__ == "__main__":
    main()