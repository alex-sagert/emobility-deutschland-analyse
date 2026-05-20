"""
Lädt vor-aggregierte Daten für die Streamlit-App.
Statt der großen Rohdaten (47 MB CSV, 16 Excel-Dateien) werden hier
kleine CSV-Dateien geladen, die mit dem Notebook erstellt wurden.

Vorteile:
- Schneller App-Start (<1 Sekunde statt mehreren)
- Funktioniert auf Streamlit Cloud ohne die Rohdaten ins Repo zu pushen
- Reduziert auf ~20 KB statt 50 MB
"""
import pandas as pd
import os
import streamlit as st


# Pfade relativ zur app.py / lade_daten.py
DATEN_ORDNER = os.path.join(os.path.dirname(__file__), "data")
PFAD_VERSORGUNG = os.path.join(DATEN_ORDNER, "versorgung.csv")
PFAD_KBA = os.path.join(DATEN_ORDNER, "kba_neuzulassungen.csv")
PFAD_PIVOT = os.path.join(DATEN_ORDNER, "pivot_kategorie.csv")


@st.cache_data
def lade_versorgungstabelle():
    """Lädt die vor-berechnete Versorgungstabelle (16 Bundesländer × 11 Kennzahlen)."""
    return pd.read_csv(PFAD_VERSORGUNG, sep=";", decimal=",", encoding="utf-8")


@st.cache_data
def lade_kba_alle_monate():
    """Lädt die KBA-Neuzulassungen über 15 Monate (240 Zeilen)."""
    df = pd.read_csv(PFAD_KBA, sep=";", decimal=",", encoding="utf-8")
    df["Datum"] = pd.to_datetime(df["Datum"])
    return df


@st.cache_data
def lade_pivot_kategorie():
    """Lädt die Lader-Kategorien pro Bundesland."""
    return pd.read_csv(PFAD_PIVOT, sep=";", decimal=",",
                       encoding="utf-8", index_col=0)


# Aliases für Rückwärts-Kompatibilität (alte App-Code-Stellen funktionieren weiter)
baue_versorgungstabelle = lade_versorgungstabelle