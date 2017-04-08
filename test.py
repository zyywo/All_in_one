#!/usr/bin/python3
# -*- coding: utf-8 -*-
from RouterShot import SaveScreenShot
import tkinter as tk
import json
import os

config_file = 'test.json'

# TODO:
# 3.倒计时自动开始

class Add_router_window(tk.Toplevel):
    def __init__(self,index=None,config=None):
        super(Add_router_window, self).__init__()
        self.config = config
        self.index = index
        self.router = None

        if self.index is not len(self.config['routers']):
            self.router = self.config['routers'][self.index]
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

        with open(config_file,'w') as jf:
            json.dump(self.config,jf)


        try:
            self.destroy()
        except Exception as e:
            print(e)

    def cancle_button_clicked(self):
        try:
            self.destroy()
        except Exception as e:
            print(e)


class MainWindow(tk.Frame):

    def __init__(self,mast=None):
        self.child_window = None
        super().__init__(mast)
        self.pack()
        self._config = self.load_config()

        # s = SaveScreenShot(self._config)
        self.creatwidgets()

    def creatwidgets(self):
        self.mail_from_label = tk.Label(self,text='发件人邮箱：')
        self.mail_password_label = tk.Label(self, text='发件人邮箱密码：')
        self.mail_server_label = tk.Label(self,text='邮箱服务器：')
        self.mail_to_label = tk.Label(self,text='收件人邮箱：')
        self.base_dir_label = tk.Label(self,text='工作目录')
        self.new_button = tk.Button(self,text='添加IP',command=self.new_button_clicked)
        self.delete_button = tk.Button(self,text='删除IP',command=self.delete_button_clicked)
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

    @staticmethod
    def load_config():
        """读取配置文件，返回值是字典类型"""

        _s = None

        if not os.path.exists(config_file):
            _s = {'mail_from':'','mail_to':'','mail_password':'','mail_server':'','base_dir':'','routers':[]}
            print('Class MainWindow:load_config():Not exists file: {}'.format(config_file))
        else:
            try:
                with open(config_file) as jf:
                    _s = json.load(jf)
            except Exception as e:
                print('class MainWindow:load_config():',e)
        return _s

    def _update(self):
        """读取配置文件，更新窗口内容,并把child_window赋值为None"""
        self._config = self.load_config()
        self.creatwidgets()
        self.child_window=None
        print('updated')

    def list_box_double_clicked(self):
        if not self.child_window:
            try:
                index = self.routers_list_box.curselection()[0]

                self.child_window = Add_router_window(index,self._config)

                self.child_window.ip_entry.bind('<Destroy>',lambda anym:self._update())
                '''如果使用w.bind('<Destroy>',func)的方式，那么窗口中有多少个部件，就会destroy多少次，每个部件destroy时都会触发func，从而导致func调用多次'''
            except Exception as e:
                print(e)

    def new_button_clicked(self):
        if not self.child_window:
            index = len(self._config['routers'])
            self.child_window = Add_router_window(index,self._config)
            self.child_window.ip_entry.bind('<Destroy>',lambda anym:self._update())

    def delete_button_clicked(self):
        index = self.routers_list_box.curselection()[0]
        print(index)
        self._config['routers'].pop(index)

        self.save_button_clicked()

        self.creatwidgets()

    def save_button_clicked(self):
        self._config['mail_from'] = self.mail_from_entry.get()
        self._config['mail_password'] = self.mail_password_entry.get()
        self._config['mail_server'] = self.mail_server_entry.get()
        self._config['mail_to'] = self.mail_to_entry.get()
        self._config['base_dir'] = self.base_dir_entry.get()

        with open(config_file,'w') as jf:
            json.dump(self._config,jf)

        print('Class MainWindow:save_button_clicked(): ',self._config)

if __name__ == '__main__':

    root = tk.Tk()

    app = MainWindow(root)
    app.master.title('配置编辑器')

    app.mainloop()