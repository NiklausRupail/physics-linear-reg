#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import linregress

def oblicz():
    try:
        # wczytanie wartości pomiarów
        dane = [float(x) for x in entry_dane.get().replace(',', '.').split()]
        dane = np.array(dane)

        # wczytanie niepewności
        UA = float(entry_UA.get().replace(',', '.'))
        UB = float(entry_UB.get().replace(',', '.'))

        # obliczenia statystyczne
        srednia = np.mean(dane)
        odchylenie = np.std(dane, ddof=1)
        N = len(dane)
        niepewnosc_sredniej = odchylenie / np.sqrt(N)
        niepewnosc_calkowita = np.sqrt(UA**2 + UB**2)

        # filtrowanie punktów w granicach niepewności całkowitej
        maska = (dane >= srednia - niepewnosc_calkowita) & (dane <= srednia + niepewnosc_calkowita)
        dane_filtrowane = dane[maska]
        x = np.arange(1, N + 1)
        x_filtrowane = x[maska]

        # regresja liniowa tylko dla zaakceptowanych punktów
        if len(dane_filtrowane) > 1:
            slope, intercept, r_value, p_value, std_err = linregress(x_filtrowane, dane_filtrowane)
            y_fit = slope * x + intercept
        else:
            slope, intercept, y_fit = 0, srednia, np.ones_like(x) * srednia

        # wyświetlenie wyników
        wynik_label.config(
            text=(
                f"Średnia: {srednia:.4f}\n"
                f"Odchylenie standardowe: {odchylenie:.4f}\n"
                f"Niepewność średniej: {niepewnosc_sredniej:.4f}\n"
                f"Niepewność całkowita (A+B): {niepewnosc_calkowita:.4f}\n"
                f"Punkty użyte po filtracji: {len(dane_filtrowane)}/{N}"
            )
        )

        # wykres w oknie GUI
        fig.clear()
        ax = fig.add_subplot(111)
        ax.errorbar(x, dane, yerr=niepewnosc_calkowita, fmt='o', alpha=0.4, capsize=5, label='Wszystkie pomiary')
        ax.errorbar(x_filtrowane, dane_filtrowane, yerr=niepewnosc_calkowita, fmt='o', color='blue', capsize=5, label='Użyte punkty')
        ax.plot(x, y_fit, 'r-', label=f'Regresja: y={slope:.3f}x+{intercept:.3f}')
        ax.axhline(srednia + niepewnosc_calkowita, color='gray', linestyle='--', label='Granice niepewności')
        ax.axhline(srednia - niepewnosc_calkowita, color='gray', linestyle='--')
        ax.set_xlabel('Numer pomiaru')
        ax.set_ylabel('Wartość')
        ax.set_title('Pomiary z niepewnościami i regresją')
        ax.legend()
        ax.grid(True)
        canvas.draw()

    except Exception as e:
        messagebox.showerror("Błąd", f"Niepoprawne dane: {e}")

# GUI
root = tk.Tk()
root.title("Analiza pomiarów z niepewnościami A i B")

tk.Label(root, text="Podaj wartości pomiarów (oddzielone spacją):").pack(pady=2)
entry_dane = tk.Entry(root, width=50)
entry_dane.pack(pady=2)

tk.Label(root, text="Podaj niepewność typu A:").pack(pady=2)
entry_UA = tk.Entry(root, width=10)
entry_UA.pack(pady=2)

tk.Label(root, text="Podaj niepewność typu B:").pack(pady=2)
entry_UB = tk.Entry(root, width=10)
entry_UB.pack(pady=2)

tk.Button(root, text="Oblicz i narysuj wykres", command=oblicz).pack(pady=5)

wynik_label = tk.Label(root, text="", justify="left", font=("Consolas", 10))
wynik_label.pack(pady=5)

# matplotlib w GUI
fig = plt.Figure(figsize=(6,4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=5)

root.mainloop()
