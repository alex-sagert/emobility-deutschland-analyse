"""
E-Mobilität Deutschland — Interaktives Dashboard
Streamlit-App zur Visualisierung der Analyse-Ergebnisse.

Start: streamlit run streamlit_app/app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Eigene Daten-Loader aus lade_daten.py importieren
from lade_daten import (
    lade_ladesaeulen,
    lade_kba_alle_monate,
    lade_fz1_bestand,
    baue_versorgungstabelle,
)


# ===================================================================
# SEITEN-KONFIGURATION (muss als ERSTES kommen!)
# ===================================================================
st.set_page_config(
    page_title="E-Mobilität Deutschland",
    page_icon="⚡",
    layout="wide",                    # Breites Layout statt schmaler Spalte
    initial_sidebar_state="expanded",
)


# ===================================================================
# DATEN LADEN (gecached - läuft nur einmal beim App-Start)
# ===================================================================
with st.spinner("Lade Daten..."):
    df_ladesaeulen = lade_ladesaeulen()
    df_kba = lade_kba_alle_monate()
    df_bestand = lade_fz1_bestand()
    versorgung = baue_versorgungstabelle()


# ===================================================================
# SIDEBAR (links)
# ===================================================================
with st.sidebar:
    st.title("⚡ E-Mobilität DE")
    st.markdown("**Projektarbeit Woche 4**")
    st.markdown("Python-Weiterbildung educx")
    st.markdown("---")

    st.subheader("ℹ️ Datenquellen")
    st.markdown("""
    - **BNetzA** — Ladesäulenregister (22.04.2026)
    - **KBA FZ 28.9** — Neuzulassungen (15 Monate)
    - **KBA FZ 1.2** — Bestand (01.01.2026)
    """)

    st.markdown("---")

    st.subheader("📊 Kennzahlen")
    st.metric("Ladeeinrichtungen gesamt", f"{len(df_ladesaeulen):,}".replace(",", "."))
    st.metric("Ladepunkte gesamt", f"{int(versorgung['Anzahl_Ladepunkte'].sum()):,}".replace(",", "."))
    st.metric("BEV-Bestand gesamt", f"{int(versorgung['BEV_Bestand'].sum()):,}".replace(",", "."))


# ===================================================================
# HAUPTBEREICH
# ===================================================================
st.title("⚡ E-Mobilität in Deutschland — Dashboard")
st.markdown("""
Interaktive Visualisierung der öffentlichen Ladeinfrastruktur und der E-Auto-Neuzulassungen
in Deutschland auf Bundesländer-Ebene. Zeitraum: **Januar 2025 – März 2026**.
""")

# Tabs anlegen
tab1, tab2, tab3 = st.tabs(["📊 Übersicht", "🗺️ Bundesländer-Vergleich", "📈 Zeitlicher Trend"])

# -------------------------------------------------------------------
# TAB 1 — ÜBERSICHT
# -------------------------------------------------------------------
with tab1:

    # ---- TL;DR / Executive Summary ----
    st.markdown("### 📌 TL;DR — Die fünf wichtigsten Erkenntnisse")

    st.markdown("""
    <style>
    .summary-box {
        background-color: #f0f7ff;
        border-left: 4px solid #0969da;
        padding: 16px 20px;
        margin: 6px 0;
        border-radius: 4px;
    }
    .summary-box-warning {
        background-color: #fff8e1;
        border-left: 4px solid #f59f00;
    }
    .summary-box-success {
        background-color: #e8f5e9;
        border-left: 4px solid #2e7d32;
    }
    </style>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="summary-box summary-box-success">
            <b>1️⃣ Starkes Wachstum der E-Mobilität.</b><br>
            Der BEV-Anteil an Neuzulassungen stieg von <b>17% (Jan 2025) auf 24% (März 2026)</b> —
            mit absolutem Rekord von <b>70.618 BEV-Zulassungen</b> im März 2026.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="summary-box">
            <b>2️⃣ Drei-Länder-Dominanz bei der Infrastruktur.</b><br>
            <b>NRW, Bayern und Baden-Württemberg</b> stellen zusammen über <b>50% aller
            Ladepunkte</b> in Deutschland. Die kleinen Bundesländer liegen eine
            Größenordnung darunter.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="summary-box summary-box-warning">
            <b>3️⃣ Klare Ost-West-Lücke.</b><br>
            Spitze beim BEV-Bestand-Anteil: <b>Hamburg (5,3%)</b>, BW (4,7%).<br>
            Schlusslicht: <b>Sachsen-Anhalt (2,0%)</b>, MV (2,1%), Sachsen (2,2%).
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="summary-box">
            <b>4️⃣ Lineare Beziehung Infrastruktur ↔ E-Auto-Bestand.</b><br>
            Pro zusätzlichem Ladepunkt kommen im Schnitt <b>11 BEVs</b> (lineare Regression).
            Saarland liegt deutlich darüber → <b>höchster Versorgungsdruck</b> in Deutschland.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="summary-box summary-box-warning">
            <b>5️⃣ Bestand und Neuzulassungen klaffen stark auseinander.</b><br>
            Während der BEV-Anteil am bestehenden Fuhrpark deutschlandweit nur bei
            <b>2–5%</b> liegt, ist der Anteil bei Neuzulassungen schon bei <b>13–22%</b>.
            Die Elektrifizierung läuft, ist aber im Bestand noch nicht sichtbar.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="summary-box summary-box-success">
            <b>💡 Bonus-Erkenntnis: Beschleunigung.</b><br>
            Bei Bundesländern wie <b>Saarland und Sachsen wächst der BEV-Anteil
            von Bestand zu Neuzulassungen um den Faktor 5-6x</b>. Der Strukturwandel
            erreicht alle Regionen — wenn auch unterschiedlich schnell.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header("Überblick über die E-Mobilität in Deutschland")

    # KPI-Kacheln (4 Spalten)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Ladepunkte",
            value=f"{int(versorgung['Anzahl_Ladepunkte'].sum()):,}".replace(",", "."),
        )

    with col2:
        st.metric(
            label="BEV-Bestand",
            value=f"{int(versorgung['BEV_Bestand'].sum()):,}".replace(",", "."),
        )

    with col3:
        durchschnitt = (versorgung["BEV_Bestand"].sum() /
                        versorgung["Anzahl_Ladepunkte"].sum())
        st.metric(
            label="BEV je Ladepunkt (Ø)",
            value=f"{durchschnitt:.1f}",
        )

    with col4:
        anteil = (versorgung["BEV_Neuzulassungen_2025"].sum() /
                  versorgung["Pkw_Neuzulassungen_2025"].sum() * 100)
        st.metric(
            label="BEV-Anteil Neuzul. 2025",
            value=f"{anteil:.1f} %",
        )

    st.markdown("---")

    # Zwei Spalten: Ladepunkte + BEV-Bestand
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Ladepunkte pro Bundesland")
        plot_daten = versorgung.sort_values("Anzahl_Ladepunkte", ascending=True)
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.barh(plot_daten["Bundesland"], plot_daten["Anzahl_Ladepunkte"],
                color="#4575b4")
        ax.set_xlabel("Anzahl Ladepunkte")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    with col_right:
        st.subheader("BEV-Bestand pro Bundesland")
        plot_daten = versorgung.sort_values("BEV_Bestand", ascending=True)
        fig, ax = plt.subplots(figsize=(8, 7))
        ax.barh(plot_daten["Bundesland"], plot_daten["BEV_Bestand"],
                color="#fc8d59")
        ax.set_xlabel("BEV-Bestand (Stand 01.01.2026)")
        ax.grid(axis="x", alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)


# -------------------------------------------------------------------
# TAB 2 — BUNDESLÄNDER-VERGLEICH
# -------------------------------------------------------------------
with tab2:
    st.header("Bundesländer im Vergleich")
    st.markdown("Wähle eine oder mehrere Kennzahlen und Bundesländer für den Vergleich.")

    col_filter1, col_filter2 = st.columns([1, 2])

    with col_filter1:
        kennzahl = st.selectbox(
            "Welche Kennzahl?",
            options=[
                "Anzahl_Ladepunkte",
                "BEV_Bestand",
                "BEV_je_Ladepunkt",
                "BEV_Anteil_am_Bestand_%",
                "BEV_Anteil_Neuzul_%",
                "Gesamtleistung_kW",
            ],
            index=4,
        )

    with col_filter2:
        ausgewaehlt = st.multiselect(
            "Bundesländer auswählen (leer = alle)",
            options=sorted(versorgung["Bundesland"].tolist()),
            default=[],
        )

    if ausgewaehlt:
        daten_filtered = versorgung[versorgung["Bundesland"].isin(ausgewaehlt)]
    else:
        daten_filtered = versorgung

    st.subheader(f"{kennzahl} pro Bundesland")

    plot_daten = daten_filtered.sort_values(kennzahl, ascending=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.barh(plot_daten["Bundesland"], plot_daten[kennzahl], color="#4575b4")
    ax.set_xlabel(kennzahl)
    ax.grid(axis="x", alpha=0.3)

    for i, wert in enumerate(plot_daten[kennzahl]):
        ax.text(wert, i, f"  {wert:,.1f}".replace(",", "."),
                va="center", fontsize=9)

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("🌡️ Heatmap: Alle Kennzahlen im relativen Vergleich")
    st.markdown("""
    Jede Spalte ist auf 0-1 normalisiert. **Grün** = Spitzenwert der Spalte,
    **rot** = Schlusslicht. Die Beschriftungen zeigen die echten Werte.
    """)

    spalten_heatmap = [
        "Anzahl_Ladepunkte", "Gesamtleistung_kW", "BEV_Bestand",
        "BEV_Neuzulassungen_2025", "BEV_je_Ladepunkt",
        "BEV_Anteil_am_Bestand_%", "BEV_Anteil_Neuzul_%",
    ]

    heatmap_daten = daten_filtered.set_index("Bundesland")[spalten_heatmap]
    heatmap_daten = heatmap_daten.sort_values("BEV_Anteil_Neuzul_%", ascending=False)
    heatmap_norm = (heatmap_daten - heatmap_daten.min()) / (heatmap_daten.max() - heatmap_daten.min())

    fig, ax = plt.subplots(figsize=(11, max(4, len(heatmap_daten) * 0.5)))
    sns.heatmap(
        heatmap_norm,
        annot=heatmap_daten.round(1),
        fmt=".1f",
        cmap="RdYlGn",
        cbar_kws={"label": "Relativ (0 = Schlusslicht, 1 = Spitze)"},
        linewidths=0.5,
        linecolor="white",
        ax=ax,
    )
    plt.xticks(rotation=35, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("📋 Rohdaten")
    st.dataframe(
        daten_filtered.set_index("Bundesland"),
        use_container_width=True,
    )


# -------------------------------------------------------------------
# TAB 3 — ZEITLICHER TREND
# -------------------------------------------------------------------
with tab3:
    st.header("Zeitlicher Trend (Jan 2025 – März 2026)")
    st.markdown("Wie haben sich BEV-Neuzulassungen über die 15 Monate entwickelt?")

    alle_monate = sorted(df_kba["Datum"].unique())
    monate_labels = [pd.Timestamp(m).strftime("%b %Y") for m in alle_monate]

    col_slider1, col_slider2 = st.columns(2)
    with col_slider1:
        start_idx = st.select_slider(
            "Von Monat:",
            options=list(range(len(alle_monate))),
            value=0,
            format_func=lambda i: monate_labels[i],
        )
    with col_slider2:
        ende_idx = st.select_slider(
            "Bis Monat:",
            options=list(range(len(alle_monate))),
            value=len(alle_monate) - 1,
            format_func=lambda i: monate_labels[i],
        )

    if start_idx > ende_idx:
        st.warning("⚠️ Startmonat liegt nach dem Endmonat — bitte korrigieren.")
        st.stop()

    start_datum = pd.Timestamp(alle_monate[start_idx])
    ende_datum = pd.Timestamp(alle_monate[ende_idx])

    df_kba_filtered = df_kba[
        (df_kba["Datum"] >= start_datum) & (df_kba["Datum"] <= ende_datum)
    ]

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

    bev_summe = df_kba_filtered["BEV"].sum()
    pkw_summe = df_kba_filtered["Neuzulassungen_gesamt"].sum()
    anteil = (bev_summe / pkw_summe * 100) if pkw_summe > 0 else 0
    n_monate = ende_idx - start_idx + 1

    with col_kpi1:
        st.metric("Zeitraum (Monate)", n_monate)
    with col_kpi2:
        st.metric("BEV-Neuzulassungen",
                  f"{int(bev_summe):,}".replace(",", "."))
    with col_kpi3:
        st.metric("BEV-Anteil im Zeitraum", f"{anteil:.1f} %")

    st.markdown("---")

    st.subheader("📈 BEV-Trend Deutschland gesamt")

    trend_de = (df_kba_filtered
        .groupby("Datum")
        .agg(BEV=("BEV", "sum"),
             Gesamt=("Neuzulassungen_gesamt", "sum"))
        .reset_index()
    )
    trend_de["Anteil"] = (trend_de["BEV"] / trend_de["Gesamt"] * 100).round(1)

    fig, ax1 = plt.subplots(figsize=(11, 5))
    ax1.bar(trend_de["Datum"], trend_de["BEV"],
            color="#4575b4", alpha=0.7, width=20)
    ax1.set_ylabel("BEV-Neuzulassungen", color="#4575b4")
    ax1.tick_params(axis="y", labelcolor="#4575b4")
    ax1.grid(axis="y", alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(trend_de["Datum"], trend_de["Anteil"],
             color="#d73027", marker="o", linewidth=2)
    ax2.set_ylabel("BEV-Anteil (%)", color="#d73027")
    ax2.tick_params(axis="y", labelcolor="#d73027")

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    st.subheader("🗺️ Bundesländer im Zeitvergleich")

    bundeslaender_vergleich = st.multiselect(
        "Welche Bundesländer vergleichen?",
        options=sorted(df_kba["Bundesland"].unique()),
        default=["Bayern", "Nordrhein-Westfalen", "Baden-Württemberg",
                 "Sachsen", "Berlin"],
    )

    if bundeslaender_vergleich:
        df_vergleich = df_kba_filtered[
            df_kba_filtered["Bundesland"].isin(bundeslaender_vergleich)
        ].copy()
        df_vergleich["Anteil"] = (df_vergleich["BEV"] /
                                   df_vergleich["Neuzulassungen_gesamt"] * 100)
        df_vergleich = df_vergleich.sort_values(["Bundesland", "Datum"])

        fig, ax = plt.subplots(figsize=(11, 6))

        farben = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                  "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

        for i, bl in enumerate(sorted(bundeslaender_vergleich)):
            daten = df_vergleich[df_vergleich["Bundesland"] == bl]
            ax.plot(daten["Datum"], daten["Anteil"].values,
                    marker="o", linewidth=2.2,
                    color=farben[i % len(farben)],
                    label=bl, alpha=0.85)

        ax.set_ylabel("BEV-Anteil an Neuzulassungen (%)", fontsize=11)
        ax.set_xlabel("Monat", fontsize=11)
        ax.legend(loc="upper left", framealpha=0.92, fontsize=9)
        ax.grid(alpha=0.3)
        ax.set_axisbelow(True)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.info("Bitte mindestens ein Bundesland auswählen.")