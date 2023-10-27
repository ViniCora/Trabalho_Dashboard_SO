import tkinter as tk
from tkinter import *
import threading
import sched
import time


class BuscaDados:
    def __init__(self):
        print()

class DashboardApp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")
        self.dashboard.config(background="#eff5f6")

        self.header = Frame(self.dashboard, bg='#333333')
        self.header.place(x=0, y=0, width=960, height=60)
        self.iniciaTela()

    def iniciaTela(self):
        self.buscaDados()

    def buscaProcessos(self):
        print('Processo')

    def buscaMemoria(self):
        print('Memoria')

    def buscaDados(self):
        thread1 = threading.Thread(target=self.buscaProcessos)
        thread2 = threading.Thread(target=self.buscaMemoria)
        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()
        self.dashboard.after(5000, self.buscaDados)



if __name__ == "__main__":
    dashboard = tk.Tk()
    DashboardApp(dashboard)
    dashboard.mainloop()
