# FIDE Norm Calculator

FIDE Norm Calculator är ett skrivbordsprogram skrivet i Python3 och PySide6, för att beräkna krav för internationella schacknormer enligt FIDE:s regelverk.

Programmet hjälper spelare, arrangörer och domare att analysera, om en turnering uppfyller kraven för IM- och GM-normer.

## Funktioner

- Beräkning av erforderlig poäng för:
  - IM-norm
  - GM-norm
- Beräkning av:
  - Genomsnittsrating (DA)
  - Prestationsrating (TPR)
  - Förväntad poäng enligt Elo-formeln
- Kontroll av federationskrav
- Kontroll av titelkrav
- Stöd för 9–14 motståndare
- Automatisk avrundning enligt FIDE:s normregler
- Grafiskt gränssnitt byggt med PySide6


## Installation

### Klona projektet

Linux

git clone https://github.com/anderskleimark/FIDE_Norm_Calculator.git
cd FIDE_Norm_Calculator

### Skapa virtuell miljö (valfritt)

python -m venv .venv
source .venv/bin/activate


## Starta programmet

python3 FIDE_Norm_Calculator.py


## Användning

1. Ange spelarens:
   - Förnamn
   - Efternamn
   - Federation
   - Elo-tal

2. Ange antal motståndare.

3. Fyll i motståndarnas:
   - Titel
   - Namn
   - Federation
   - Elo-tal

4. Klicka på **Beräkna**.

Programmet visar:

- IM-norm
- GM-norm
- Förväntad poäng
- Titelkrav

## Normkrav som kontrolleras

### Federationskrav

Programmet kan kontrollera att:

- Högst 60 % av motståndarna kommer från spelarens federation.
- Minst två utländska federationer finns representerade.
- Övriga federationskrav enligt FIDE uppfylls.

### Titelkrav

Programmet kontrollerar bland annat:

- Minst 50 % titelspelare.
- Minst 1/3 IM eller GM för IM-norm.
- Minst 1/3 GM för GM-norm.

## Teknisk information

Projektet är utvecklat i:

- Python 3
- PySide6

Huvudkomponenter:

- GUI (PySide6)
- Normberäkningar
- Elo-beräkningar
- Validering av FIDE-krav


## Licens

GPL 3

Copyright (c) 2026 Anders Kleimark
