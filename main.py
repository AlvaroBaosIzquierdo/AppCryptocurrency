
import tkinter as tk
import tkinter.messagebox
from tkinter import *

import krakenex
import pandas as pd
import numpy as np
import datetime
import  matplotlib.pyplot as plt
import webbrowser




#Creamos  una clase para almacenar nuestro objeto y mostrar los resultados a través de una interfaz gráfica.
class Product:

    #Definimos los atributos de la clase.
    def __init__(self, root):
        self.wind = root #Almacenamos la ventana que creamos como un atributo de nuestra clase.
        self.wind.title('Criptomonedas')
        self.createwidgets()



    #definimos el primer método en el que vammos a poder conectarnos a la API de kraken
    def connect(self):
        try:
            CCY = self.name.get()
            kraken = krakenex.API()
            date = datetime.datetime.now()
            date = date.replace(year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0, microsecond=0)
            t = date.timestamp() - 60 * 60 * 24 * 720

            data = kraken.query_public('OHLC', data={'pair': CCY, 'since': t, 'interval': 60 * 24})
            df = pd.DataFrame(data['result'][CCY],
                              columns=('date', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count')).set_index(
                'date').astype(float)
            df.index = pd.to_datetime(df.index, unit='s').strftime('%Y-%m-%d')
            texto_aux = Label(root, text="Criptomoneda guardada correctamente. Proceda con el análisis.").grid(row=2, column=2)
            self.prices = df
            self.CCY=CCY
        except:
            tkinter.messagebox.showerror(title = "Error!", message="Ups! Ha ocurrido un error al intentar conectarse a la API, es muy posible que haya introducido incorrectamente el nombre del par de criptomoneda. Le "
                                                                   "recomendamos que visite la pestaña de ayuda.")

    # Definimos la función Analysis como un método dentro de nuestra clase.
    def Analysis(self, window=14):

        df = self.prices

        MA = df.close.rolling(window).mean()
        MA.dropna(inplace=True)

        returns = df.close.pct_change()[1:]
        log_returns = np.log(1 + returns)

        down, up = log_returns.copy(), log_returns.copy()
        up = log_returns.where(log_returns > 0).fillna(0)
        down = log_returns.where(log_returns < 0).fillna(0)

        up_average = up.rolling(window).mean()
        down_average = down.abs().rolling(window).mean()

        RS = up_average / down_average

        RSI = 100 - (100 / (1 + RS[window - 1:]))

        self.RSI = RSI
        self.MA = MA
        self.PAIR=self.CCY
        #print(self.RSI)
        #print(self.MA)
        texto = Label(root, text="¡Se ha ejecutado el análisis correctamente!").grid(row=4, column=2)

    def plot_RSI_MA(self):
        df = self.prices
        RSI = self.RSI
        MA= self.MA
        CCY= self.PAIR
        L = len(df)
        fig, axes = plt.subplots(3, 1, num='RSI y MA')
        axes[0].plot(df.close, color='black')
        axes[1].plot(RSI, color='b')
        # axes[2].plot(df.close, color = 'black')
        axes[2].plot(MA, color='green')

        axes[0].set_title('Precios de cierre de '+CCY)
        axes[1].set_title('RSI de '+CCY)
        axes[2].set_title('MA de '+CCY)

        axes[1].axhline(y=30, color='r', linewidth=3)
        axes[1].axhline(y=70, color='r', linewidth=3)
        axes[0].set_xticks(np.arange(0, L, step=50))
        axes[1].set_xticks(np.arange(0, L, step=50))
        axes[2].set_xticks(np.arange(0, L, step=50))

        plt.tight_layout()
        fig.autofmt_xdate()
        fig.show()



    def plot_MA(self):
        df = self.prices
        MA = self.MA
        CCY=self.PAIR
        L = len(df)
        fig2, axes2 = plt.subplots(1, 1, num='Cierre vs MA')
        axes2.plot(df.close, color='black')
        axes2.plot(MA, color='green')
        axes2.set_title('Precios de cierre vs MA de '+CCY)
        axes2.set_xticks(np.arange(0, L, step=50))

        plt.tight_layout()
        fig2.autofmt_xdate()
        fig2.show()






    def createwidgets(self):

        frame = LabelFrame(self.wind, text = 'Introduzca la criptomoneda a estudiar', bg = "#F1F8EC")
        frame.grid(row = 0, column = 0, columnspan = 4, pady = 20)

        #Definimos otro atributo de nuestro objeto: El nombre de la criptomoneda.
        Label(frame, text = 'Name: ').grid(row  = 1, column = 0)

        #Creamos una variable donde guardar la criptomoneda que introduzcamos.

        self.cryptocurrency = StringVar()

        self.name =  Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1, padx=10, pady=10)
        self.name.config(background="black", fg="#03f943", justify="right")

        #Creamos un botón parguardarla criptomoneda.
        self.button1 = Button(frame , text = 'Save Cryptocurrency', command = self.connect).grid(row = 3, columnspan = 2, sticky = W + E)

        #Botón para hacer el análisis.
        frame2 = LabelFrame(self.wind, text='Pulsa analizar', bg="#F1F8EC")
        frame2.grid(row=4, column=0, columnspan=3, sticky=W + E)
        tk.Button(frame2, text='Analysis', command = self.Analysis).grid(row=5, sticky=W)

        #Ponemos otro frame para ver qué información se quiere obtener.
        frame3 = LabelFrame(self.wind, text='Pulsa en los botones de la información que quiere estudiar', bg="#F1F8EC")
        frame3.grid(row=5, column=0, columnspan=3, sticky = W + E)
        #Introducimos los botones que queremos que nos saque las fráficas
        tk.Button(frame3, text = 'RSI and MA', command = self.plot_RSI_MA).grid(row = 6, sticky = W )
        tk.Button(frame3, text='Stock prices vs MA', command = self.plot_MA).grid(row=6, column=3)




def callback(url):
    webbrowser.open_new(url)
def infoayuda():
    helpWindow = Toplevel(root)
    helpWindow.title("Ayuda")
    helpWindow.geometry("550x50")
    Label(helpWindow,
                    text = "Puede encontrar el nombre de pares de criptomonedas en el siguiente enlace y clickando en result:").grid()
    link1 = Label(helpWindow, text="https://api.kraken.com/0/public/AssetPairs", fg="blue", cursor="hand2")
    link1.grid()
    link1.bind("<Button-1>", lambda e: callback("https://api.kraken.com/0/public/AssetPairs"))

if __name__ == '__main__':
    root = Tk()
    root.geometry("350x300")
    barraMenu = Menu(root)
    root.config(menu=barraMenu)
    menuAyuda = Menu(barraMenu, tearoff=0)
    menuAyuda.add_command(label="Acerca de", command = infoayuda)
    barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
    application = Product(root)
    root.mainloop()



