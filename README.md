# E-Mobilität Deutschland — Datenanalyse

**Projektarbeit Woche 4 — Python-Weiterbildung educx**
**Autor:** Alex • **Stand:** Mai 2026

Eine Analyse der öffentlichen Ladeinfrastruktur und der E-Auto-Neuzulassungen in Deutschland auf Bundesländer-Ebene. Verknüpft werden Daten der Bundesnetzagentur (Ladesäulenregister) mit Statistiken des Kraftfahrt-Bundesamts (Neuzulassungen und Bestand).

---

## Fragestellung

Wie hat sich die Elektromobilität in Deutschland im Zeitraum **Januar 2025 bis März 2026** entwickelt, und in welchem Verhältnis steht die öffentliche Ladeinfrastruktur zu den E-Auto-Beständen und Neuzulassungen in den 16 Bundesländern?

Konkret untersucht werden:

1. Verteilung von Ladepunkten und Ladeleistung über die Bundesländer
2. Monatlicher BEV-Anteil an Neuzulassungen über 15 Monate
3. Versorgungsverhältnis "BEV-Bestand pro Ladepunkt" pro Bundesland
4. Lücke zwischen aktuellem Bestand und aktueller Neuzulassungs-Dynamik

---

## Datenquellen

| Quelle | Datei(en) | Stand | Lizenz |
|---|---|---|---|
| Bundesnetzagentur — Ladesäulenregister | `ladesaeulen_bnetza.csv` | 22.04.2026 | OpenData |
| KBA FZ 28.9 — Pkw-Neuzulassungen nach Bundesländern | `kba/fz28_2025_01.xlsx` ... `kba/fz28_2026_03.xlsx` (15 Dateien) | Jan 2025 – März 2026 | OpenData |
| KBA FZ 1.2 — Pkw-Bestand nach Kraftstoffarten | `kba/fz1_2026.xlsx` | 01.01.2026 | OpenData |

---

## Verzeichnisstruktur

```
Projektarbeit Woche 4/
├── .venv/                          (Python virtual environment, lokal)
├── data/
│   ├── ladesaeulen_bnetza.csv      (47 MB, BNetzA-Rohdaten)
│   └── kba/
│       ├── fz28_2025_01.xlsx       (Neuzulassungen Jan 2025)
│       ├── ...                     (... 13 weitere Monate ...)
│       ├── fz28_2026_03.xlsx       (Neuzulassungen März 2026)
│       └── fz1_2026.xlsx           (Bestand zum 01.01.2026)
├── notebooks/
│   └── emobility.ipynb             (Hauptnotebook)
├── output/
│   └── plots/
│       ├── 01_ladepunkte_pro_bundesland.png
│       ├── 02_bev_trend_deutschland.png
│       ├── 03_lader_kategorien_pro_bundesland.png
│       ├── 04_scatter_ladepunkte_vs_bev.png
│       ├── 05_anteil_bestand_vs_neuzulassungen.png
│       ├── 06_korrelations_heatmap.png
│       ├── 07_dashboard.png
│       └── 08_seaborn_bundeslaender_kennzahlen.png
├── docs/
├── emobility_final.html            (HTML-Export für Präsentation/Notion)
├── README.md                       (diese Datei)
└── requirements.txt                (Bibliotheks-Versionen)
```

---

## Reproduktions-Anleitung

### Voraussetzungen

- **Python** ≥ 3.10
- Speicherplatz: ca. 100 MB (Datenfiles + venv)
- Empfohlen: **VS Code mit Jupyter-Extension**

### Schritt 1 — Repository / Projekt aufsetzen

Das Projekt in einen lokalen Ordner kopieren, in dem die `data/`-Struktur wie oben beschrieben vorliegt.

### Schritt 2 — Virtual Environment aufsetzen

In Windows PowerShell (im Projekt-Hauptordner):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Auf macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Schritt 3 — Notebook ausführen

`notebooks/emobility.ipynb` in VS Code öffnen, als Kernel das `.venv` auswählen und mit **"Run All"** alle Zellen von oben nach unten ausführen.

Erwartete Laufzeit: ca. 30 Sekunden bis 2 Minuten je nach Hardware.

---

## Methodik

### Daten-Verknüpfung

Die drei Datenquellen werden über die **Bundesland-Spalte** verknüpft (`pd.merge` mit `how="inner"`). Da die KBA "Baden-Wuerttemberg" mit Umlaut-Ersatz schreibt, die BNetzA dagegen "Baden-Württemberg", werden die Schreibweisen vor dem Merge über ein Mapping harmonisiert.

### Eigene Kennzahlen

Aus den Rohdaten werden drei abgeleitete Kennzahlen berechnet:

| Kennzahl | Formel | Aussage |
|---|---|---|
| **BEV je Ladepunkt** | BEV-Bestand ÷ Ladepunkte | Versorgungsdruck (hoch = knapp) |
| **BEV-Anteil am Bestand (%)** | BEV-Bestand ÷ Pkw-Bestand × 100 | Ist-Stand der Elektrifizierung |
| **BEV-Anteil bei Neuzulassungen (%)** | BEV-Neuzul. 2025 ÷ Gesamt-Neuzul. 2025 × 100 | Aktuelle Marktdynamik |

### Zeitliche Aggregation

- Für **Trend-Visualisierungen** wird der gesamte verfügbare Zeitraum (15 Monate, Jan 2025 – März 2026) genutzt.
- Für **Bundesländer-Vergleiche** wird das abgeschlossene Kalenderjahr 2025 (12 Monate) verwendet, damit alle Bundesländer denselben Zeitraum abbilden.

### Verwendete Methoden

- **`pd.read_csv`** mit `skiprows`, deutscher Zahlenformatierung (Komma als Dezimaltrennzeichen)
- **`pd.read_excel`** mit `sheet_name`, `skiprows`, `usecols`-Filter
- **`.groupby` + `.agg`** für Aggregationen
- **`.apply` mit eigenen Funktionen** zur Klassifikation
- **`pd.merge`** zur Verknüpfung der Datenquellen
- **`np.polyfit`** für lineare Regression (Trendlinie im Streudiagramm)
- **`matplotlib.gridspec`** für Multi-Panel-Dashboard
- **`seaborn.heatmap`** mit Min-Max-Normalisierung

---

## Wichtigste Erkenntnisse

1. **Drei-Länder-Dominanz:** NRW, Bayern und Baden-Württemberg stellen zusammen über 50% aller öffentlichen Ladepunkte in Deutschland.
2. **Starker Wachstumstrend:** Der BEV-Anteil bei Neuzulassungen steigt von 17% (Jan 2025) auf 24% (März 2026), mit absolutem Rekord von 70.618 BEVs im März 2026.
3. **Lücke Bestand vs. Neuzulassungen:** Bundesweit liegt der BEV-Anteil am Bestand bei 2–5%, der Neuzulassungs-Anteil bei 13–22% — der Fuhrpark elektrifiziert sich rasant.
4. **Ost-West-Gefälle:** Sachsen-Anhalt, MV, Sachsen und Thüringen bilden das Schlusslicht beim BEV-Bestand-Anteil; Niedersachsen, Schleswig-Holstein und Baden-Württemberg führen.
5. **Lineare Beziehung Infrastruktur ↔ Bestand:** Pro zusätzlichem Ladepunkt kommen im Durchschnitt 11 BEVs (Trendlinie aus Streudiagramm).

---

## Limitationen

- **Nur öffentliche Ladepunkte.** Private Wallboxen (geschätzt >700.000 in Deutschland) sind im BNetzA-Register nicht erfasst.
- **Stichtage divergieren.** BEV-Bestand 01.01.2026, Ladepunkte 22.04.2026 — Differenz ca. 4 Monate.
- **Keine Nutzungsdaten.** Wir wissen nicht, wie ausgelastet die Ladepunkte sind.
- **Pendler-Dynamik nicht abgebildet.** Autos werden am Wohnort registriert, geladen wird teilweise am Arbeitsort.

---

## Mögliche Weiterführungen

- **Prognose-Modell** mit `np.polyfit` — ab wann erreicht der BEV-Anteil 50%?
- **FZ 2.0** — BEV-Marktanteile nach Hersteller
- **Geo-Visualisierung** mit `geopandas` — Choroplethen-Karte Deutschland
- **Normalisierung auf Einwohnerzahlen** — Ladepunkte pro 1.000 Einwohner
- **Erweiterung um Stromnetz-Daten** — Versorgungssicherheit bei wachsender E-Mobilität

---

## Verwendete Software

- Python 3.11
- pandas, numpy, matplotlib, seaborn (Versionen in `requirements.txt`)
- VS Code mit Jupyter-Extension

---

## Kontakt

Bei Fragen oder Anregungen: Erstellt im Rahmen der educx Python-Weiterbildung, Mai 2026.
