#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import json
import os

# TODO:
# 1.新增/删除功能
# 2.使程序在没有配置文件时也可以编辑配置文件并保存
# 3.倒计时自动开始

class Add_router_window(tk.Toplevel):
    def __init__(self,index=None,config=None):
        self.config = config
        self.index = index
        self.router = None

        if self.index is not len(self.config['routers']):
            self.router = self.config['routers'][self.index]
        super().__init__()
        self.createwidget()
        self.title('编辑IP')

    def createwidget(self):
        self.ip_label = tk.Label(self,text='IP：').grid(row=0,sticky=tk.W)
        self.username_label = tk.Label(self, text='用户名：').grid(row=1, sticky=tk.W)
        self.password_label = tk.Label(self, text='密码：').grid(row=2, sticky=tk.W)

        self.ip_entry = tk.Entry(self)
        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self)

        self.ip_entry.grid(row = 0,column=1)
        self.username_entry.grid(row=1,column=1)
        self.password_entry.grid(row=2,column=1)

        if self.router is not None:
            self.ip_entry.insert(0,self.router['ip'])
            self.username_entry.insert(0,self.router['username'])
            self.password_entry.insert(0,self.router['password'])

        self.save_button = tk.Button(self, text='添加', command=self.save_button_clicked).grid(row=3, sticky=tk.E)
        self.cancel_button = tk.Button(self,text='取消',command=self.cancle_button_clicked).grid(row=3,column=1,sticky=tk.W)

    def save_button_clicked(self):
        temp_router = {'ip':self.ip_entry.get(),'username':self.username_entry.get(),'password':self.password_entry.get()}

        print('Class Add_router_windows:save_button_clicked(): ',self.config['routers'])

        if self.index == len(self.config['routers']):
            self.config['routers'].append(temp_router)
        else:
            self.config['routers'][self.index] = temp_router

        with open('test.json','w') as jf:
            json.dump(self.config,jf)

        self.destroy()

    def cancle_button_clicked(self):
        self.destroy()


class MainWindow(tk.Frame):
    def __init__(self,mast=None):
        super().__init__(mast)
        self.pack()

        self._update()

    def creatwidgets(self):
        self.mail_from_label = tk.Label(self,text='发件人邮箱：')
        self.mail_password_label = tk.Label(self, text='发件人邮箱密码：')
        self.mail_server_label = tk.Label(self,text='邮箱服务器：')
        self.mail_to_label = tk.Label(self,text='收件人邮箱：')
        self.base_dir_label = tk.Label(self,text='工作目录')
        self.new_button = tk.Button(self,text='添加IP',command=self.new_button_clicked)
        self.delete_button = tk.Button(self,text='删除IP')
        self.save_button= tk.Button(self,text='保存配置',command=self.save_button_clicked)
        self.routers_list_box = tk.Listbox(self)

        self.mail_from_entry = tk.Entry(self)
        self.mail_password_entry = tk.Entry(self)
        self.mail_server_entry = tk.Entry(self)
        self.mail_to_entry = tk.Entry(self)
        self.base_dir_entry = tk.Entry(self)

        # 设置组件的默认内容
        if self._config is not None:
            self.mail_from_entry.insert(0, self._config['mail_from'])
            self.mail_password_entry.insert(0,self._config['mail_password'])
            self.mail_server_entry.insert(0,self._config['mail_server'])
            self.mail_to_entry.insert(0,self._config['mail_to'])
            self.base_dir_entry.insert(0,self._config['base_dir'])
            for _Trouter in self._config['routers']:
                self.routers_list_box.insert(tk.END,_Trouter['ip'])

        #设置组件的位置
        self.mail_from_label.grid(row=0)
        self.mail_from_entry.grid(row=0,column=1)
        self.mail_password_label.grid(row=1)
        self.mail_password_entry.grid(row=1,column=1)
        self.mail_server_label.grid(row=2)
        self.mail_server_entry.grid(row=2,column=1)
        self.mail_to_label.grid(row=3)
        self.mail_to_entry.grid(row=3,column=1)
        self.base_dir_label.grid(row=4)
        self.base_dir_entry.grid(row=4,column=1)
        self.new_button.grid(row=5)
        self.delete_button.grid(row=6)
        self.save_button.grid(row=7)
        self.routers_list_box.grid(row=5, column=1,rowspan=3)

        # 设置组建的动作
        self.routers_list_box.bind("<Double-Button-1>", lambda e:self.list_box_double_clicked())

    def list_box_double_clicked(self):
        index = self.routers_list_box.curselection()[0]

        t = Add_router_window(index,self._config)
        self.update_idletasks()

    @staticmethod
    def load_config():
        """读取配置文件，返回值是字典类型"""

        _s = None

        if not os.path.exists('test.json'):
            _s = {'mail_from':'','mail_to':'','mail_password':'','mail_server':'','base_dir':'','routers':[]}
            print('Class MainWindow:load_config():Not exists file: test.json')
        else:
            try:
                with open('test.json') as jf:
                    _s = json.load(jf)
            except Exception as e:
                print('class MainWindow:load_config():',e)
        return _s

    def _update(self):
        """读取配置文件，并更新窗口的内容"""

        self._config = self.load_config()
        self.creatwidgets()

    def new_button_clicked(self):
        index = len(self._config['routers'])
        w = Add_router_window(index,self._config)

    def save_button_clicked(self):
        self._config['mail_from'] = self.mail_from_entry.get()
        self._config['mail_password'] = self.mail_password_entry.get()
        self._config['mail_server'] = self.mail_server_entry.get()
        self._config['mail_to'] = self.mail_to_entry.get()
        self._config['base_dir'] = self.base_dir_entry.get()

        with open('test.json','w') as jf:
            json.dump(self._config,jf)

        print('Class MainWindow:save_button_clicked(): ',self._config)

if __name__ == '__main__':

    root = tk.Tk()

    app = MainWindow(root)
    app.master.title('配置编辑器')

    # app.master.maxsize(200,200)

    app.mainloop()

# from tkinter import *
#
# class Tl(Toplevel):
#     def __init__(self):
#         super().__init__()
#         self.title('子窗口')
#         self.button = Button(self,text='关闭',command=self.close).pack()
#
#     def close(self):
#         self.destroy()
#
# class MainWindow(Frame):
#     def __init__(self):
#         super().__init__()
#         self.pack()
#
#         self.button = Button(self, text='show child window', command=self.show_child_window)
#         self.entry = Entry(self)
#
#         self.entry.pack()
#         self.button.pack()
#
#     def show_child_window(self):
#         child_window = Tl()
#
#     def done(self):
#         self.entry.insert(0,'子窗口已关闭')
#
# a = MainWindow()
# a.mainloop()