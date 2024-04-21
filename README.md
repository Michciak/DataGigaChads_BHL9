# Profilowanie Kampanii Marketingowej z Wykorzystaniem Uczenia Maszynowego i Metod XAI

## Opis

Projekt polega na wykorzystaniu modeli uczenia maszynowego do profilowania kampanii marketingowej, a następnie interpretacji tych modeli przy użyciu metod XAI (Explainable Artificial Intelligence). Głównym celem jest zrozumienie, jakie cechy mają największy wpływ na skuteczność kampanii marketingowej.

W projekcie znajduje się:

- Skrypt do eksploracyjnej analizy danych (EDA) - [link](link_do_pliku)
- Skrypt do procesu uczenia modeli - [link](link_do_pliku)
- Webapp pozwalający wybrać liczbę najistotniejszych cech w celu uzyskania opisu grupy docelowej.

## Dokumentacja

Dokumentację poszczególnych etapów można znaleźć w następujących plikach:

- Eksploracyjna analiza danych - [EDA](EDA.md)
- Proces uczenia modeli - [ML](ML.md)

## Aplikacja/UI oraz funkcjonalność

Aplikacja webowa stanowi interfejs do interkacji ze zbudowanymi modelami uczenia maszynowego.
Zawiera ona następujące funkcjonalności:

- Import danych do bazy z pliku csv oraz doszkolenie modeli do nowych obserwacji
- Wybór klasyfikatora podstawie któego dokonywana będzie analiza kampanii
- Podsumowanie metryk wybranego klasyfikatora
- Podsumowanie frkacji sukcesu przeprowadzonych wcześniej kampanii
- Możliwość ręcznego sterowania ilością wpływowych cech
- Wgląd w cechy klienta mające największy wpływ na uzyskanie od niego pozytywnej odpowiedzi
- Wgląd w wykres przebiegu prawdopodobieństwa dla każdej istotnej cechy
- Intuicyjnie zaznaczone obszary na wykresie przedstawiające obszary największego zainteresowania
- Słowny opis zawierający informacje o grupie docelowej

### Screenshots/Video

W sekcji poniżej znajdują się screeny z wyglądem oraz funkcjonalnością aplikacji.

#### Screenshot 1
![Screenshot 1](screenshots/screenshot1.png)

#### Screenshot 2
![Screenshot 2](screenshots/screenshot2.png)

#### Video
[Link do wideo](link_do_wideo)

## Plany rozwoju na przyszłość

- Tworzenie segmentacji obecnych klientów z wykorzystaniem cech uzyskanych z XAI.
- Integracja zewnętrznych danych, takich jak dane demograficzne czy zachowania online, w celu lepszego profilowania grup docelowych.
- Badanie wpływu kampanii marketingowych na różne segmenty klientów i dostosowywanie strategii marketingowej w oparciu o te wyniki.