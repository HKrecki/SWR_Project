Projekt realizowany w ramach pracy magisterskiej.
Temat: Zrobotyzowane stanowisko do badania parametrów zgrzewania punktowego.

Plan - sieć czujników (Software/Hardware):
- Komunikacja STM32 <-> Qt (proste wysyłanie danych w pętli i wyświetlenie w konsoli)
- Sygnał start - stop pomiaru wysyłane z Qt do STM (czy pomiar czasowy?)
- Okno z 3 zakładkami: pulpit, wykresy ustawienia
- Przygotowanie zakładki ustawień (dane ustawienia UART, przyciski i wybór portu, podgląd wysyłanych danych)
- Odczyt danych z czujnika wstrząsów
- Przygotowanie zakładki wykresy (wykres z przesyłanych danych)
- Odczyt danych z pozostałych czujników (wstrząsów, fotorezystorów, natężenia pola E-M)
- Odczyt danych z kamery przez STM32
- Wyświetlenie danych z kamery w Qt
- Uporządkowanie GUI