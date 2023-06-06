import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pandas as pd
from tkintertable import TableCanvas

#função para abrir o explorador de arquivos e escolher um arquivo .csv do computador
def choose_file():
    file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    return file_path

def program():

    #função que abre uma janela para escolha de cor
    def choose_color():
        color = colorchooser.askcolor()
        if color:
            color_label.configure(bg=color[1])

    file_path = choose_file()

    #chamando a função choose_file e abrindo o arquvo definido
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        data = [row for row in csv_reader]

    #variavel para armazenar a quantidade de colunas do arquivo
    colu=[]

    #opções para os combobox
    sacle_options = ['Linear', 'Log Log', 'Mono Log (x)', 'Mono Log (y)']

    points_options = ['Quadrados', 'Circulos', 'Triangulos']

    style_options = ['Pontos', 'Linhas', 'Ambos']

    columns = data[0]

    # faz um frame para colocar a tabela no tk
    table = ttk.Treeview(root, columns=columns, show='headings')

    #define a quatidade de colunas
    for row in data[0:]:
        table.insert('', 'end', values=row)

    #insere os valores nas colunas
    for i, column in enumerate(columns):
        table.heading(i, text=i)
        colu.append(i)
    
    #coloca a tabela no tk
    table.grid(row=12, column=0, columnspan=100)

    def plot():
        #recolhe os valores selecionados em combobox e entry e armazena em variaveis
        eixo_x = x_choose.get()
        eixo_y = y_choose.get()
        graph_color = color_label.cget('bg')
        escala = scale_choose.get()
        titulo = title_dys.get()
        titulo_x = title_x_dys.get()
        titulo_y = title_y_dys.get()
        forma = points_choose.get()
        estilo = style_choose.get()
        grid = var.get()

        #define o gride em true ou false
        if grid == 1:
            grid_fix = True
        elif grid == 0:
            grid_fix = False

        #trnsforma a string em int 
        eixo_x_fix = eval(eixo_x)
        eixo_y_fix = eval(eixo_y)

        #define valores que podem ser interpretados pela biblioteca
        if escala == 'Linear':
            escala_x = 'linear'
            escala_y = 'linear'
        elif escala == 'Log Log':
            escala_x = 'log'
            escala_y = 'log'
        elif escala == 'Mono Log (x)':
            escala_x = 'log'
            escala_y = 'linear'
        elif escala == 'Mono Log (y)':
            escala_x = 'linear'
            escala_y = 'log'

        if forma == 'Quadrados':
            pontos = 's'
        elif forma == 'Circulos':
            pontos = 'o'
        elif forma == 'Triangulos':
            pontos = '^'

        #criando duas listas para adicionar os valores para os eixos
        x = []
        y = []

        #abre novamente o arquivo para ler os valores de cada coluna e inserir nas listas
        with open(file_path) as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                x.append(float(row[eixo_x_fix].replace(',', '.')))
                y.append(float(row[eixo_y_fix].replace(',', '.')))
        
        #sistema de decisão para plotagem do gráfico
        if estilo == 'Linhas':
            fig, ax = plt.subplots()
            ax.plot(x, y, graph_color)
            ax.set_xscale(escala_x)
            ax.set_yscale(escala_y)
            ax.set_title(titulo)
            ax.set_xlabel(titulo_x)
            ax.set_ylabel(titulo_y)
            ax.grid(grid_fix)

        elif estilo == 'Pontos':
            fig, ax = plt.subplots()
            ax.scatter(x, y, marker=pontos, color=graph_color)
            ax.set_xscale(escala_x)
            ax.set_yscale(escala_y)
            ax.set_title(titulo)
            ax.set_xlabel(titulo_x)
            ax.set_ylabel(titulo_y)
            ax.grid(grid_fix)

        elif estilo == 'Ambos':
            fig, ax = plt.subplots()
            ax.plot(x, y, graph_color)
            ax.scatter(x, y, marker=pontos, color=graph_color)
            ax.set_xscale(escala_x)
            ax.set_yscale(escala_y)
            ax.set_title(titulo)
            ax.set_xlabel(titulo_x)
            ax.set_ylabel(titulo_y)
            ax.grid(grid_fix)

        #faz e posiciona o figure do gráfico no tk
        canvas = FigureCanvasTkAgg(fig , master=root)
        canvas.draw()

        canvas.get_tk_widget().grid(row=0, column=2, rowspan=12)

    #configurações de elementos no tk
    x_label = tk.Label(root, text='Eixo X:')
    x_label.grid(row=1, column=0)

    x_choose = tk.StringVar()

    x_combo = ttk.Combobox(root, values=colu, state="readonly", textvariable=x_choose)
    x_combo.grid(row=1, column=1)

    y_label = tk.Label(root, text='Eixo Y:')
    y_label.grid(row=2, column=0)

    y_choose = tk.StringVar()

    y_combo = ttk.Combobox(root, values=colu, state="readonly", textvariable=y_choose)
    y_combo.grid(row=2, column=1)

    color_button = tk.Button(root, text='Escolher cor do gráfico:', command=choose_color)
    color_button.grid(row=3, column=0)

    color_label = tk.Label(root, text='', padx=70)
    color_label.grid(row=3, column=1)

    scale_label = tk.Label(root, text='Escala do gráfico')
    scale_label.grid(row=4, column=0)

    scale_choose = tk.StringVar()

    scale_combo = ttk.Combobox(root, state="readonly", textvariable=scale_choose, values=sacle_options)
    scale_combo.grid(row=4, column=1)

    title_label = tk.Label(root, text='Titulo do gráfico:')
    title_label.grid(row=5, column=0)

    title_dys = tk.Entry(root)
    title_dys.config(font=("Times New Roman", 11))
    title_dys.grid(row=5, column=1)

    title_x_label = tk.Label(root, text='Titulo do eixo x:')
    title_x_label.grid(row=6, column=0)

    title_x_dys = tk.Entry(root)
    title_x_dys.config(font=("Times New Roman", 11))
    title_x_dys.grid(row=6, column=1)

    title_y_label = tk.Label(root, text='Titulo do eixo y:')
    title_y_label.grid(row=7, column=0)

    title_y_dys = tk.Entry(root)
    title_y_dys.config(font=("Times New Roman", 11))
    title_y_dys.grid(row=7, column=1)

    graph_style_label = tk.Label(root, text='Estilo do gráfico:')
    graph_style_label.grid(row=8, column=0)

    style_choose = tk.StringVar()

    graph_style_combo = ttk.Combobox(root, state="readonly", textvariable=style_choose, values=style_options)
    graph_style_combo.grid(row=8, column=1)

    points_label = tk.Label(root, text='Escolha o formato dos pontos')
    points_label.grid(row=9, column=0)

    points_choose = tk.StringVar()

    points_combo = ttk.Combobox(root, state="readonly", textvariable=points_choose, values=points_options)
    points_combo.grid(row=9, column=1)

    var = tk.IntVar()

    grid_check = tk.Checkbutton(root, text='Grid', variable=var)
    grid_check.grid(row=10, column=0, columnspan=2)

    plot_button = tk.Button(root, text='Plotar gráfico', command=plot)
    plot_button.grid(row=11, column=0, columnspan=2)

root = tk.Tk()
root.config(padx=10, pady=10)

choose_button = tk.Button(root, text='Escolher arquivo', command=program)
choose_button.grid(row=0, column=0, columnspan=2)

root.mainloop()