#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def oblicz():
    try:
        # Wczytanie danych z pola tekstowego
        dane = [float(x) for x in entry.get().replace(',', '.').split()]
        dane = np.array(dane)

        # Obliczenia statystyczne
        srednia = np.mean(dane)
        odchylenie = np.std(dane, ddof=1)
        N = len(dane)
        niepewnosc_sredniej = odchylenie / np.sqrt(N)
        niepewnosc_calkowita = np.sqrt(odchylenie**2 + niepewnosc_sredniej**2)

        # Filtrowanie punktów w granicach niepewności
        maska = (dane >= srednia - niepewnosc_calkowita) & (dane <= srednia + niepewnosc_calkowita)
        dane_filtrowane = dane[maska]
        x = np.arange(1, N + 1)
        x_filtrowane = x[maska]

        # Regresja liniowa tylko dla zaakceptowanych punktów
        if len(dane_filtrowane) > 1:
            slope, intercept, r_value, p_value, std_err = linregress(x_filtrowane, dane_filtrowane)
            y_fit = slope * x + intercept
        else:
            slope, intercept, y_fit = 0, srednia, np.ones_like(x) * srednia

        # Aktualizacja wyników
        wynik_label.config(
            text=(
                f"Średnia: {srednia:.4f}\n"
                f"Odchylenie standardowe: {odchylenie:.4f}\n"
                f"Niepewność średniej: {niepewnosc_sredniej:.4f}\n"
                f"Niepewność całkowita: {niepewnosc_calkowita:.4f}\n"
                f"Liczba punktów po odrzuceniu: {len(dane_filtrowane)} / {N}"
            )
        )

        # Wykres
        plt.figure(figsize=(8, 5))
        plt.errorbar(x, dane, yerr=odchylenie, fmt='o', label='Wszystkie pomiary', alpha=0.4, capsize=5)
        plt.errorbar(x_filtrowane, dane_filtrowane, yerr=odchylenie, fmt='o', color='blue', label='Użyte punkty', capsize=5)
        plt.plot(x, y_fit, 'r-', label=f'Regresja: y={slope:.3f}x+{intercept:.3f}')
        plt.axhline(srednia + niepewnosc_calkowita, color='gray', linestyle='--', label='Granice niepewności')
        plt.axhline(srednia - niepewnosc_calkowita, color='gray', linestyle='--')
        plt.xlabel('Numer pomiaru')
        plt.ylabel('Wartość')
        plt.title('Wykres pomiarów z regresją liniową (po filtracji)')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        messagebox.showerror("Błąd", f"Niepoprawne dane: {e}")

# GUI
root = tk.Tk()
root.title("Analiza pomiarów z regresją liniową i filtrowaniem punktów")

tk.Label(root, text="Podaj wartości pomiarów (oddzielone spacją):").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Oblicz i narysuj wykres", command=oblicz).pack(pady=10)

wynik_label = tk.Label(root, text="", justify="left", font=("Consolas", 10))
wynik_label.pack(pady=10)

root.mainloop()
