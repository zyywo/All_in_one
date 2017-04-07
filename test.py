#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import json

# TODO:
# 1.新增/删除功能
# 2.使程序在没有配置文件时也可以编辑配置文件并保存
# 3.倒计时自动开始

class Add_router_window(tk.Toplevel):
    def __init__(self,index=None,config=None):
        self.config = config
        self.index = index
        self.router = self.config['routers'][self.index]
        super().__init__()
        self.createwidget()

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

        self.save_button = tk.Button(self, text='保存', command=self.save_button_clicked).grid(row=3, sticky=tk.E)
        self.cancel_button = tk.Button(self,text='取消',command=self.cancle_button_clicked).grid(row=3,column=1,sticky=tk.W)


    def save_button_clicked(self):
        s = {'ip':self.ip_entry.get(),'username':self.username_entry.get(),'password':self.password_entry.get()}

        self.config['routers'][self.index]=s

        print(self.config)

        with open('test.json','w') as jf:
            json.dump(self.config,jf)

        self.destroy()

    def cancle_button_clicked(self):
        self.destroy()


class MainWindow(tk.Frame):
    def __init__(self,mast=None):
        super().__init__(mast)
        self.pack()

        self.update()

        print(self._config)

    def creatwidgets(self):
        self.mail_from_label = tk.Label(self,text='发件人邮箱：')
        self.mail_password_label = tk.Label(self, text='发件人邮箱密码：')
        self.mail_server_label = tk.Label(self,text='邮箱服务器：')
        self.mail_to_label = tk.Label(self,text='收件人邮箱：')
        self.base_dir_label = tk.Label(self,text='工作目录')
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
            for item in self._config['routers']:
                self.routers_list_box.insert(tk.END,item['ip'])

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
        self.routers_list_box.grid(row=5,column=1)

        self.routers_list_box.bind("<Double-Button-1>",lambda e:self.create_window())

    def create_window(self):
        index = self.routers_list_box.curselection()[0]

        t = Add_router_window(index,self._config)

    @staticmethod
    def load_config():
        _s = None
        try:
            with open('test.json') as jf:
                _s = json.load(jf)
        except Exception as e:
            print(e)

        return _s

    def update(self):
        self._config = self.load_config()
        self.creatwidgets()

if __name__ == '__main__':

    root = tk.Tk()

    app = MainWindow(root)

    # app.master.maxsize(200,200)

    app.mainloop()