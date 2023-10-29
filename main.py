import tkinter as tk
from tkinter import *
from tkinter import ttk
import threading
import subprocess
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DashboardController:
    def __init__(self):
        self.dashboard = tk.Tk()
        self.dashApp = DashboardApp(self.dashboard)
        self.dados = BuscaDados()
        self.buscarDados()
        self.dashboard.mainloop()

    def buscarDados(self):
        thread1 = threading.Thread(target=self.dados.buscaProcessos)
        thread2 = threading.Thread(target=self.dados.buscaInfoSO)
        thread3 = threading.Thread(target=self.dados.buscaParticoes)
        thread4 = threading.Thread(target=self.dados.buscaInfoHardware)
        thread5 = threading.Thread(target=self.dados.buscaInfoMemoria)
        thread6 = threading.Thread(target=self.dados.buscaInformacoesCPU)
        thread7 = threading.Thread(target=self.dados.buscaQuantidadeCPU)

        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread6.start()
        thread7.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()
        thread6.join()
        thread7.join()
        self.dashApp.attInformacoes(self.dados)
        self.dashboard.after(5000, self.buscarDados)


#Model
class BuscaDados:
    def __init__(self):
        self.informacoesCPU = None
        self.quantidadeCPU = None
        self.infoHardware = None
        self.infoMemoria = None
        self.memoriaResumo = None
        self.processos = None
        self.particoes = None
        self.infoSO = None

    def buscaInformacoesCPU(self):
        self.informacoesCPU = subprocess.run(['cat', '/proc/cpuinfo'], stdout=subprocess.PIPE)

    def buscaInfoMemoria(self):
        self.memoriaResumo = subprocess.run(['free'], stdout=subprocess.PIPE)
        self.infoMemoria = subprocess.run(['cat', '/proc/meminfo'], stdout=subprocess.PIPE)

    def buscaQuantidadeCPU(self):
        self.quantidadeCPU = subprocess.run(['nproc'], stdout = subprocess.PIPE)

    def buscaInfoHardware(self):
        self.infoHardware = subprocess.run(['lscpu'], stdout = subprocess.PIPE)

    def buscaProcessos(self):
        self.processos = subprocess.run(['ps', 'aux'], stdout = subprocess.PIPE)

    def buscaParticoes(self):
        self.particoes = subprocess.run(['cat', '/proc/partitions'], stdout = subprocess.PIPE)

    def buscaInfoSO(self):
        self.infoSO = subprocess.run(["uname", '-a'], stdout=subprocess.PIPE)

#View
class DashboardApp:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.dashboard.title("Dashboard Sistemas Operacionais")
        self.dashboard.geometry("960x540")
        self.teste = False
        self.teste2 = False

        nb = ttk.Notebook(self.dashboard)
        nb.place(x=0, y=0)

        self.frame1 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame1, text="Info. SO")

        self.frame2 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame2, text="Info. CPU")

        self.frame3 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame3, text="Info. Hardware")

        self.frame4 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame4, text="Info. Memoria")

        nb2 = ttk.Notebook(self.frame4)
        nb2.place(x=0, y=0)
        self.frame4_1 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_1, text="Valores totais memória")
        self.frame4_2 = Frame(self.frame4, width=960, height=530, bg='#eff5f6')
        nb2.add(self.frame4_2, text="Gráfico memória")

        self.frame5 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame5, text="Info. processos")

        nb3 = ttk.Notebook(self.frame5)
        nb3.place(x=0, y=0)
        self.frame5_1 = Frame(self.frame5, width=960, height=530, bg='#eff5f6')
        nb3.add(self.frame5_1, text="Processos Lista")
        self.frame5_2 = Frame(self.frame5, width=960, height=530, bg='#eff5f6')
        nb3.add(self.frame5_2, text="Gráfico memória processos")

        self.frame6 = Frame(dashboard, width=960, height=530, bg='#eff5f6')
        nb.add(self.frame6, text="Info. partições")

    def attTabelaMemoria(self, dados):
        for widget in self.frame4_1.winfo_children():
            widget.destroy()
        table = ttk.Treeview(self.frame4_1, columns=(1, 2), show="headings", height=10)
        table.pack()

        table.heading(1, text="Tipo")
        table.heading(2, text="Valor usado/disponivel (kb)")
        table.insert('', tk.END, values=['Memoria Total', 2849964])
        table.insert('', tk.END, values=['Memoria Usado', 2380868])
        table.insert('', tk.END, values=['Memoria Livre', 82748])
        table.insert('', tk.END, values=['Buff/Cache', 386348])
        table.insert('', tk.END, values=['Memoria Compartilhada', 28852])
        table.insert('', tk.END, values=['Memoria Disponivel', 273768])


    def attInformacoes(self, dados):
        print(dados.infoSO)
        self.attGraficoMemoria(dados)
        self.attGraficoUsoMemoriaProcessos(dados)
        self.attTabelaMemoria(dados)
        self.attInfoSO(dados)

    def attInfoSO(self, dados):
        for widget in self.frame1.winfo_children():
            widget.destroy()
        labelEXP = ttk.Label(self.frame1, text="Informações sobre o SO:")
        label = "Linux ubuntu22 6.2.0-35-generic #35~22.04.1-Ubuntu SMP PREEMPT_DYNAMIC Fri Oct  6 10:23:26 UTC 2 x86_64 x86_64 x86_64 GNU/Linux"
        infoSOLabel = ttk.Label(self.frame1, text=label)
        labelEXP.pack()
        infoSOLabel.pack()

    def attGraficoMemoria(self, dados):
        for widget in self.frame4_2.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        labels = ['Usado', 'Livre', 'Buffer/Cache']
        if self.teste2 == False:
            sizes = [2380868, 82748, 386348]
            self.teste2 = True
        else:
            sizes = [20, 35, 40]
            self.teste2 = False

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.frame4_2)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def attGraficoUsoMemoriaProcessos(self, dados):
        for widget in self.frame5_2.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        labels = ['Usado', 'Livre', 'Disponivel', 'Shared']
        if self.teste == False:
            sizes = [15, 30, 45, 10]
            self.teste = True
        else:
            sizes = [20, 35, 40, 15]
            self.teste = False

        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        canvas = FigureCanvasTkAgg(fig, master=self.frame5_2)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    dash = DashboardController()
