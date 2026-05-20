"""
Lädt alle Datenquellen für die E-Mobilität-Dashboard-App.
Die Funktionen sind mit @st.cache_data dekoriert, damit Streamlit
die Daten nicht bei jedem User-Klick neu lädt - das macht die App schnell.
"""
import pandas as pd
import os
import streamlit as st


# Pfade zur Datenbasis (relativ zur app.py im streamlit_app/-Ordner)
DATEN_ORDNER = os.path.join(os.path.dirname(__file__), "..", "data")
PFAD_LADESAEULEN = os.path.join(DATEN_ORDNER, "ladesaeulen_bnetza.csv")
PFAD_KBA_ORDNER = os.path.join(DATEN_ORDNER, "kba")
PFAD_FZ1 = os.path.join(PFAD_KBA_ORDNER, "fz1_2026.xlsx")


def lader_kategorie(kw):
    """Klassifiziert Ladepunkte nach Nennleistung."""
    if kw < 22:
        return "Normallader (<22 kW)"
    elif kw < 150:
        return "Schnelllader (22–149 kW)"
    else:
        return "HPC (≥150 kW)"


@st.cache_data
def lade_ladesaeulen():
    """Lädt das BNetzA-Ladesäulenregister und ergänzt Kategorien."""
    df = pd.read_csv(
        PFAD_LADESAEULEN,
        sep=";",
        encoding="cp1252",
        skiprows=10,
        decimal=",",
        thousands=".",
        low_memory=False,
    )
    df["Inbetriebnahmedatum"] = pd.to_datetime(
        df["Inbetriebnahmedatum"], format="%d.%m.%Y", errors="coerce"
    )
    df["Inbetriebnahmejahr"] = df["Inbetriebnahmedatum"].dt.year
    df["Lader_Kategorie"] = df["Nennleistung Ladeeinrichtung [kW]"].apply(lader_kategorie)
    return df


def lese_kba_monatsdatei(pfad):
    """Liest eine einzelne FZ-28.9-Monatsdatei ein."""
    df = pd.read_excel(
        pfad,
        sheet_name="FZ 28.9",
        skiprows=12,
        usecols=[1, 2, 3, 5, 7, 9],
        names=["Bundesland", "Neuzulassungen_gesamt", "Alternativ_gesamt",
               "Elektro_gesamt", "BEV", "Plug_in_Hybrid"],
        header=None,
    )
    df = df.dropna(subset=["Bundesland"])
    df = df[~df["Bundesland"].str.contains("zusammen|Insgesamt|Bundesländer",
                                            case=False, na=False)]

    # Datum aus Dateinamen extrahieren (z.B. fz28_2026_03.xlsx -> 2026-03-01)
    dateiname = os.path.basename(pfad)
    teile = dateiname.replace(".xlsx", "").split("_")
    jahr, monat = teile[1], teile[2]
    df["Datum"] = pd.Timestamp(year=int(jahr), month=int(monat), day=1)

    return df


@st.cache_data
def lade_kba_alle_monate():
    """Lädt alle 15 KBA-Monatsdateien und kombiniert sie."""
    dateien = sorted([
        f for f in os.listdir(PFAD_KBA_ORDNER)
        if f.startswith("fz28_") and f.endswith(".xlsx")
    ])

    dfs = []
    for dateiname in dateien:
        pfad = os.path.join(PFAD_KBA_ORDNER, dateiname)
        dfs.append(lese_kba_monatsdatei(pfad))

    return pd.concat(dfs, ignore_index=True)


@st.cache_data
def lade_fz1_bestand():
    """Lädt FZ 1.2: Pkw-Bestand pro Bundesland zum 01.01.2026."""
    df_roh = pd.read_excel(
        PFAD_FZ1,
        sheet_name="FZ1.2",
        skiprows=9,
        usecols=list(range(12)),
        names=["Land_A", "Bezirk_B", "Bezirk_C", "Bezirk_D",
               "Pkw_gesamt", "Benzin", "Diesel", "Gas",
               "Hybrid_gesamt", "Plug_in_Hybrid", "BEV", "Sonstige"],
        header=None,
    )

    # Bundesländer-Mapping (KBA-Schreibweise -> Standard-Schreibweise)
    bundeslaender_mapping = {
        "Baden-Wuerttemberg": "Baden-Württemberg",
        "Thueringen": "Thüringen",
    }

    maske = df_roh["Bezirk_B"].astype(str).str.contains(
        "INSGESAMT", case=False, na=False)
    df = df_roh[maske].copy()
    df["Bundesland"] = (df["Bezirk_B"]
        .str.replace(" INSGESAMT", "", regex=False)
        .str.title()
        .replace(bundeslaender_mapping)
    )
    df = df[df["Bundesland"] != "Deutschland"].copy()
    df = df.drop(columns=["Land_A", "Bezirk_B", "Bezirk_C", "Bezirk_D"])
    df = df.reset_index(drop=True)
    return df


@st.cache_data
def baue_versorgungstabelle():
    """Baut die finale Versorgungstabelle mit allen Kennzahlen."""
    df_lade = lade_ladesaeulen()
    df_kba = lade_kba_alle_monate()
    df_bestand = lade_fz1_bestand()

    # Ladepunkte pro Bundesland aus BNetzA
    ladepunkte = (df_lade
        .groupby("Bundesland")
        .agg(
            Anzahl_Ladeeinrichtungen=("Bundesland", "size"),
            Anzahl_Ladepunkte=("Anzahl Ladepunkte", "sum"),
            Gesamtleistung_kW=("Nennleistung Ladeeinrichtung [kW]", "sum"),
        )
        .reset_index()
    )

    # BEV-Neuzulassungen Kalenderjahr 2025
    df_2025 = df_kba[df_kba["Datum"].dt.year == 2025].copy()
    bev_2025 = (df_2025
        .groupby("Bundesland")
        .agg(
            BEV_Neuzulassungen_2025=("BEV", "sum"),
            Pkw_Neuzulassungen_2025=("Neuzulassungen_gesamt", "sum"),
        )
        .reset_index()
    )

    # BEV-Bestand pro Bundesland
    bestand_aggr = df_bestand[["Bundesland", "Pkw_gesamt", "BEV",
                                "Plug_in_Hybrid"]].copy()
    bestand_aggr.columns = ["Bundesland", "Pkw_Bestand", "BEV_Bestand",
                            "PHEV_Bestand"]

    # Merge in zwei Schritten
    versorgung = pd.merge(ladepunkte, bestand_aggr, on="Bundesland", how="inner")
    versorgung = pd.merge(versorgung, bev_2025, on="Bundesland", how="inner")

    # Eigene Kennzahlen
    versorgung["BEV_je_Ladepunkt"] = (
        versorgung["BEV_Bestand"] / versorgung["Anzahl_Ladepunkte"]
    ).round(1)
    versorgung["BEV_Anteil_am_Bestand_%"] = (
        versorgung["BEV_Bestand"] / versorgung["Pkw_Bestand"] * 100
    ).round(2)
    versorgung["BEV_Anteil_Neuzul_%"] = (
        versorgung["BEV_Neuzulassungen_2025"] /
        versorgung["Pkw_Neuzulassungen_2025"] * 100
    ).round(1)

    return versorgung