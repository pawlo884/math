# 🎯 Matematyka dla Pierwszaków - Aplikacja Streamlit

Prosta aplikacja do nauki dodawania i odejmowania dla dzieci z klas pierwszych.

## 📋 Wymagania

- **Python**: 3.11.9 (pyenv – plik `.python-version`)
- pip

## 🐍 Python (pyenv)

Użyj pyenv do ustawienia wersji Pythona:

```bash
pyenv install 3.11.9   # jeśli nie masz jeszcze tej wersji
pyenv local 3.11.9     # lub po prostu wejdź w katalog – .python-version zadziała
```

## 🚀 Instalacja i uruchomienie (lokalnie)

1. Zainstaluj wymagane biblioteki:

```bash
pip install -r requirements.txt
```

2. Uruchom aplikację:

```bash
streamlit run app.py
```

3. Aplikacja otworzy się automatycznie w przeglądarce na adresie `http://localhost:8502`

## 🐳 Uruchomienie w Dockerze

```bash
docker compose up --build
```

Aplikacja będzie dostępna pod adresem `http://localhost:8502`.

Aby uruchomić w tle:

```bash
docker compose up -d --build
```

## ✨ Funkcjonalności

- ➕ **Tylko dodawanie** - ćwiczenie dodawania liczb do 20
- ➖ **Tylko odejmowanie** - ćwiczenie odejmowania
- ➕➖ **Mieszane** - losowy wybór dodawania lub odejmowania
- 📊 **Śledzenie wyniku** - automatyczne liczenie poprawnych odpowiedzi
- 🎉 **Efekty wizualne** - baloniki za poprawną odpowiedź
- 🎨 **Kolorowy interfejs** - przyjazny dla dzieci

## 🎮 Jak używać

1. Wybierz typ ćwiczenia (dodawanie/odejmowanie/mieszane)
2. Przeczytaj pytanie w kolorowym polu
3. Wpisz odpowiedź w polu tekstowym
4. Kliknij "Sprawdź" aby sprawdzić odpowiedź
5. Kliknij "Następne" aby przejść do kolejnego pytania
6. Kliknij "Nowa gra" aby zresetować wynik

## 💡 Wskazówki

- Używaj ćwiczeń codziennie dla lepszego efektu
- Zacznij od samego dodawania, a potem dodaj odejmowanie
- Śledź swój wynik, aby widzieć postępy
