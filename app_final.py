# app.py — Application SRM complète et corrigée
"""
Application SRM - Maintenance Prédictive pour Eau Potable
Design v2 — Interface moderne & épurée
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px
import plotly.graph_objects as go
import joblib
from datetime import datetime, timedelta
import os
import re
import json
import hashlib
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# INITIALISATION SESSION (VERSION CORRIGÉE)
# ============================================================================

if "initialized" not in st.session_state:
    st.session_state.initialized = True

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "show_change_password" not in st.session_state:
    st.session_state.show_change_password = False

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="SRM · Eau Potable",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CSS — DESIGN SYSTEM COMPLET
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Mono:wght@400;500&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Root Variables ── */
:root {
    --blue-50:  #EFF6FF;
    --blue-100: #DBEAFE;
    --blue-200: #BFDBFE;
    --blue-400: #60A5FA;
    --blue-500: #3B82F6;
    --blue-600: #2563EB;
    --blue-700: #1D4ED8;
    --blue-800: #1E40AF;
    --blue-900: #1E3A8A;

    --slate-50:  #F8FAFC;
    --slate-100: #F1F5F9;
    --slate-200: #E2E8F0;
    --slate-300: #CBD5E1;
    --slate-400: #94A3B8;
    --slate-500: #64748B;
    --slate-600: #475569;
    --slate-700: #334155;
    --slate-800: #1E293B;
    --slate-900: #0F172A;

    --red-50:    #FEF2F2;
    --red-100:   #FEE2E2;
    --red-400:   #F87171;
    --red-500:   #EF4444;
    --red-600:   #DC2626;
    --red-700:   #B91C1C;

    --amber-50:  #FFFBEB;
    --amber-100: #FEF3C7;
    --amber-400: #FBBF24;
    --amber-500: #F59E0B;
    --amber-600: #D97706;

    --green-50:  #F0FDF4;
    --green-100: #DCFCE7;
    --green-400: #4ADE80;
    --green-500: #22C55E;
    --green-600: #16A34A;

    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-xl: 24px;
    --radius-full: 9999px;

    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
    --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.05);
}

/* ── Background ── */
.stApp {
    background: var(--slate-50) !important;
}

.main .block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1400px !important;
}

/* ── Header principal ── */
.srm-header {
    background: linear-gradient(135deg, var(--blue-800) 0%, var(--blue-600) 100%);
    border-radius: var(--radius-xl);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.srm-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
}
.srm-header::after {
    content: '';
    position: absolute;
    bottom: -60px; left: 40%;
    width: 280px; height: 280px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.srm-header h1 {
    color: white !important;
    font-size: 1.75rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}
.srm-header p {
    color: rgba(255,255,255,0.75) !important;
    font-size: 0.9rem !important;
    margin: 0.25rem 0 0 !important;
    font-weight: 300;
}
.srm-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: var(--radius-full);
    padding: 4px 12px;
    color: white !important;
    font-size: 0.75rem;
    font-weight: 500;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(4px);
}

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: white;
    border-radius: var(--radius-lg);
    padding: 1.25rem 1.5rem;
    border: 1px solid var(--slate-200);
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s;
}
.kpi-card:hover { box-shadow: var(--shadow-md); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.kpi-card.blue::before   { background: var(--blue-500); }
.kpi-card.red::before    { background: var(--red-500); }
.kpi-card.amber::before  { background: var(--amber-500); }
.kpi-card.green::before  { background: var(--green-500); }
.kpi-icon {
    width: 40px; height: 40px;
    border-radius: var(--radius-md);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    margin-bottom: 0.75rem;
}
.kpi-card.blue  .kpi-icon { background: var(--blue-50);  color: var(--blue-600); }
.kpi-card.red   .kpi-icon { background: var(--red-50);   color: var(--red-600); }
.kpi-card.amber .kpi-icon { background: var(--amber-50); color: var(--amber-600); }
.kpi-card.green .kpi-icon { background: var(--green-50); color: var(--green-600); }
.kpi-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--slate-900);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.2rem;
}
.kpi-label {
    font-size: 0.78rem;
    color: var(--slate-500);
    font-weight: 400;
}

/* ── Status Badges ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: var(--radius-full);
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
.badge-red    { background: var(--red-50);    color: var(--red-700);    border: 1px solid var(--red-100); }
.badge-amber  { background: var(--amber-50);  color: var(--amber-600);  border: 1px solid var(--amber-100); }
.badge-green  { background: var(--green-50);  color: var(--green-600);  border: 1px solid var(--green-100); }
.badge-blue   { background: var(--blue-50);   color: var(--blue-700);   border: 1px solid var(--blue-100); }

/* ── Section title ── */
.section-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--slate-800);
    margin: 0 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--slate-200);
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: var(--radius-lg);
    border: 1px solid var(--slate-200);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
}
.card-header {
    padding: 1rem 1.25rem;
    border-bottom: 1px solid var(--slate-100);
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--slate-700);
    display: flex;
    align-items: center;
    gap: 8px;
}
.card-body { padding: 1.25rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--slate-900) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: var(--slate-200) !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] .stMetric {
    background: rgba(255,255,255,0.06) !important;
    border-radius: var(--radius-md) !important;
    padding: 0.75rem 1rem !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    margin-bottom: 0.5rem !important;
}
[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    color: white !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
    color: var(--slate-400) !important;
    font-size: 0.75rem !important;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.sidebar-logo-icon {
    width: 36px; height: 36px;
    background: var(--blue-600);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
}
.sidebar-logo-text {
    font-size: 1rem;
    font-weight: 600;
    color: white !important;
    line-height: 1.2;
}
.sidebar-logo-sub {
    font-size: 0.7rem;
    color: var(--slate-400) !important;
}
.sidebar-section {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--slate-500) !important;
    padding: 0.75rem 0 0.5rem;
    margin-top: 0.5rem;
}
.legend-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 6px;
    vertical-align: middle;
}

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: white !important;
    border-radius: var(--radius-lg) !important;
    padding: 4px !important;
    border: 1px solid var(--slate-200) !important;
    gap: 2px !important;
    box-shadow: var(--shadow-sm) !important;
    margin-bottom: 1.5rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: var(--radius-md) !important;
    padding: 0.5rem 1rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    color: var(--slate-500) !important;
    border: none !important;
    transition: all 0.15s !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: var(--blue-600) !important;
    color: white !important;
    box-shadow: 0 1px 3px rgba(37,99,235,0.3) !important;
}
[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* ── Buttons ── */
.stButton > button {
    background: var(--blue-600) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.55rem 1.25rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.1) !important;
    transition: all 0.15s ease !important;
    letter-spacing: -0.01em !important;
}
.stButton > button:hover {
    background: var(--blue-700) !important;
    box-shadow: 0 4px 8px rgba(37,99,235,0.25) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] > div > div {
    font-family: 'DM Sans', sans-serif !important;
    border-radius: var(--radius-md) !important;
    border: 1px solid var(--slate-200) !important;
    background: var(--slate-50) !important;
    font-size: 0.875rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.1) !important;
    background: white !important;
}

/* ── Form ── */
[data-testid="stForm"] {
    background: white !important;
    border-radius: var(--radius-xl) !important;
    border: 1px solid var(--slate-200) !important;
    padding: 1.75rem !important;
    box-shadow: var(--shadow-sm) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-lg) !important;
    overflow: hidden !important;
    border: 1px solid var(--slate-200) !important;
}

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border-left-width: 4px !important;
}

/* ── Diagnostic Result Cards ── */
.diag-card {
    border-radius: var(--radius-xl);
    padding: 2rem;
    text-align: center;
    border: 1px solid;
    position: relative;
    overflow: hidden;
}
.diag-card.critical {
    background: var(--red-50);
    border-color: var(--red-100);
}
.diag-card.warning {
    background: var(--amber-50);
    border-color: var(--amber-100);
}
.diag-card.good {
    background: var(--green-50);
    border-color: var(--green-100);
}
.diag-indicator {
    font-size: 3.5rem;
    margin-bottom: 0.75rem;
    display: block;
}
.diag-title {
    font-size: 1.3rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.diag-card.critical .diag-title { color: var(--red-700); }
.diag-card.warning  .diag-title { color: var(--amber-600); }
.diag-card.good     .diag-title { color: var(--green-600); }
.diag-desc {
    font-size: 0.85rem;
    margin-bottom: 1rem;
}
.diag-card.critical .diag-desc { color: #7f1d1d; }
.diag-card.warning  .diag-desc { color: #78350f; }
.diag-card.good     .diag-desc { color: #14532d; }
.diag-action {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 600;
}
.diag-card.critical .diag-action { background: var(--red-100);   color: var(--red-700); }
.diag-card.warning  .diag-action { background: var(--amber-100); color: var(--amber-600); }
.diag-card.good     .diag-action { background: var(--green-100); color: var(--green-600); }
.diag-score-bar {
    height: 6px;
    border-radius: var(--radius-full);
    background: rgba(0,0,0,0.08);
    margin: 1rem 0 0.5rem;
    overflow: hidden;
}
.diag-score-fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.8s ease;
}
.diag-score-num {
    font-size: 0.78rem;
    font-weight: 600;
    text-align: right;
}

/* ── Planning alert row ── */
.alert-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 0.875rem 1rem;
    border-radius: var(--radius-md);
    margin-bottom: 0.5rem;
    border: 1px solid;
}
.alert-row.crit { background: var(--red-50);   border-color: var(--red-100); }
.alert-row.warn { background: var(--amber-50); border-color: var(--amber-100); }
.alert-row.info { background: var(--blue-50);  border-color: var(--blue-100); }
.alert-row .ar-icon {
    font-size: 1.2rem;
    flex-shrink: 0;
}
.alert-row .ar-body { flex: 1; }
.alert-row .ar-name {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--slate-800);
}
.alert-row .ar-sub {
    font-size: 0.78rem;
    color: var(--slate-500);
}
.alert-row .ar-badge {
    flex-shrink: 0;
    font-size: 0.7rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: var(--radius-full);
}
.alert-row.crit .ar-badge { background: var(--red-100);   color: var(--red-700); }
.alert-row.warn .ar-badge { background: var(--amber-100); color: var(--amber-600); }
.alert-row.info .ar-badge { background: var(--blue-100);  color: var(--blue-700); }

/* ── Footer ── */
.srm-footer {
    text-align: center;
    padding: 2rem 1rem 1rem;
    color: var(--slate-400);
    font-size: 0.75rem;
    border-top: 1px solid var(--slate-200);
    margin-top: 2rem;
}

/* ── Checkbox & radio ── */
[data-testid="stCheckbox"] label,
[data-testid="stRadio"]    label {
    font-size: 0.875rem !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background: var(--blue-600) !important;
}

/* ── Number input label ── */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"]   label,
[data-testid="stTextInput"]   label,
[data-testid="stTextArea"]    label,
[data-testid="stDateInput"]   label {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: var(--slate-600) !important;
    margin-bottom: 2px !important;
}

/* ── Hide default Streamlit header/footer ── */
header[data-testid="stHeader"] { display: none !important; }
#MainMenu, footer { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# LOGIN SYSTEM - VERSION SIMPLE (CONNEXION + CHANGER MOT DE PASSE)
# =============================================================================

import hashlib
import json
import os

# Fichier de stockage des identifiants
CREDENTIALS_FILE = "admin_credentials.json"

def init_credentials():
    if not os.path.exists(CREDENTIALS_FILE):
        default_creds = {
            "username": "admin",
            "password_hash": hashlib.sha256("admin123".encode()).hexdigest()
        }
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(default_creds, f)
    with open(CREDENTIALS_FILE, 'r') as f:
        return json.load(f)

def verify_password(input_password, stored_hash):
    return hashlib.sha256(input_password.encode()).hexdigest() == stored_hash

def update_password(new_password):
    creds = init_credentials()
    creds["password_hash"] = hashlib.sha256(new_password.encode()).hexdigest()
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(creds, f)
    return True

# Initialisation
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "show_change_password" not in st.session_state:
    st.session_state.show_change_password = False

if not st.session_state.logged_in:
    
    creds = init_credentials()
    
    # Pas de CSS pour fond, garder le fond par défaut
    # Centrer le formulaire
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        
        if not st.session_state.show_change_password:
            # Formulaire de connexion
            st.markdown("<h2 style='text-align: center;'>Connexion</h3>", unsafe_allow_html=True)
            st.markdown("<h4 style='text-align: center;'>SRM-Maintenance Prédictive  </h4>", unsafe_allow_html=True)
            
            username = st.text_input("Identifiant", placeholder="admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")
            
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("Se connecter", use_container_width=True):
                    if username == creds["username"] and verify_password(password, creds["password_hash"]):
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Identifiant ou mot de passe incorrect")
            with col_btn2:
                if st.button("Changer mot de passe", use_container_width=True):
                    st.session_state.show_change_password = True
                    st.rerun()
        
        else:
            # Formulaire changement mot de passe
            st.markdown("<h3 style='text-align: center;'>Changer mot de passe</h3>", unsafe_allow_html=True)
            
            current_password = st.text_input("Mot de passe actuel", type="password", placeholder="Mot de passe actuel")
            new_password = st.text_input("Nouveau mot de passe", type="password", placeholder="Nouveau mot de passe")
            confirm_password = st.text_input("Confirmer", type="password", placeholder="Confirmer le mot de passe")
            
            if st.button("Enregistrer", use_container_width=True):
                if not verify_password(current_password, creds["password_hash"]):
                    st.error("Mot de passe actuel incorrect")
                elif len(new_password) < 6:
                    st.error("Minimum 6 caractères")
                elif new_password != confirm_password:
                    st.error("Les mots de passe ne correspondent pas")
                else:
                    update_password(new_password)
                    st.success("Mot de passe modifié avec succès !")
                    st.session_state.show_change_password = False
                    st.rerun()
            
            if st.button("Retour à la connexion", use_container_width=True):
                st.session_state.show_change_password = False
                st.rerun()
    
    st.stop()


# ============================================================================
# LISTES DES CENTRES
# ============================================================================

CENTRES_COMPLETS = sorted([
    "BZOU",
    "IMDAHEN", 
    "FOUM JEMAA",
    "BENI HASAN",
    "TANANT",
    "OUZOUD",
    "AIT ATTAB",
    "TISKI",
    "OUAOULA",
    "TAMDA NPOUMERCID",
    "AIT MHAMED",
    "AZILAL",
    "TIFNI",
    "IMLIL",
    "OUAOUIZEGHT",
    "BENI AYAT",
    "DR BENI AYAT",
    "AFOURER",
    "DEMNATE",
    "RFALA"
])

CENTRES_GPS = {
    "BZOU": (32.1000, -6.5500),
    "IMDAHEN": (32.0833, -6.4500),
    "FOUM JEMAA": (32.1167, -6.4167),
    "BENI HASAN": (32.2000, -6.5000),
    "TANANT": (31.7833, -6.9167),
    "OUZOUD": (32.0167, -6.7167),
    "AIT ATTAB": (31.9833, -6.3500),
    "TISKI": (31.8500, -6.5000),
    "OUAOULA": (32.0500, -6.4500),
    "TAMDA NPOUMERCID": (32.0000, -6.5500),
    "AIT MHAMED": (31.9500, -6.5000),
    "AZILAL": (31.9667, -6.5667),
    "TIFNI": (31.9000, -6.5000),
    "IMLIL": (31.7593, -7.0099),
    "OUAOUIZEGHT": (32.1667, -6.4000),
    "BENI AYAT": (32.2000, -6.4167),
    "DR BENI AYAT": (32.1800, -6.4200),
    "AFOURER": (32.2000, -6.4167),
    "DEMNATE": (31.8500, -7.0167),
    "RFALA": (32.2500, -6.2500),
}

RAPPORTS_FILE = "rapports_interventions.json"

def charger_rapports():
    if os.path.exists(RAPPORTS_FILE):
        with open(RAPPORTS_FILE, 'r', encoding='utf-8') as f:
            return pd.DataFrame(json.load(f))
    return pd.DataFrame(columns=[
        'Date', 'Centre', 'Designation', 'Type_equipement', 'Latitude', 'Longitude',
        'Puissance_kW', 'Debit_l_s', 'Nb_groupes', 'Machine', 'Type_intervention',
        'Operation', 'Description', 'Duree_heures', 'Pieces_Dhs', 'Main_oeuvre_Dhs',
        'Frais_deplacement_Dhs', 'Frais_divers_Dhs', 'Total_Dhs', 'Statut'
    ])

def sauvegarder_rapports(df):
    with open(RAPPORTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(df.to_dict(orient='records'), f, indent=2, default=str)

def extraire_coordonnees(adresse):
    if pd.isna(adresse):
        return None, None
    adresse = str(adresse)
    x_match = re.search(r'X[=\s]*([0-9.]+)', adresse, re.IGNORECASE)
    y_match = re.search(r'Y[=\s]*([0-9.-]+)', adresse, re.IGNORECASE)
    if x_match and y_match:
        try:
            return float(x_match.group(1)), float(y_match.group(1))
        except:
            pass
    coord_match = re.search(r'([0-9.]+)[,\s]+([0-9.-]+)', adresse)
    if coord_match:
        try:
            return float(coord_match.group(1)), float(coord_match.group(2))
        except:
            pass
    return None, None


# ============================================================================
# CHARGEMENT DES MODÈLES ET DONNÉES
# ============================================================================
@st.cache_resource
def charger_modeles():
    try:
        model_class = joblib.load('random_forest_classifier.pkl')
        model_reg = joblib.load('random_forest_regressor.pkl')
        scaler = joblib.load('scaler.pkl')
        return model_class, model_reg, scaler
    except:
        return None, None, None

@st.cache_data
def charger_donnees():
    if os.path.exists("Donnees_fusionnees.xlsx"):
        df_centres = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Centres")
        df_interventions = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Interventions")
        return df_centres, df_interventions
    # Données par défaut si fichier non trouvé
    df_centres = pd.DataFrame({
        'Centre': ['AZILAL', 'OUAOUIZEGHT', 'BENI AYAT', 'FOUM JEMAA', 'DEMNATE'],
        'Priorite': ['Critique', 'Surveillance', 'Bon état', 'Surveillance', 'Bon état'],
        'Cout_total_Dhs': [125000, 45000, 28000, 32000, 15000],
        'Nb_interventions': [12, 5, 2, 4, 1],
        'Score_risque': [85, 55, 25, 45, 18]
    })
    return df_centres, pd.DataFrame()

@st.cache_data
def charger_infrastructures():
    infra_data = {}
    fichier = None
    for p in ["data/Infrastructure eau copie.xlsx", "Infrastructure eau copie.xlsx"]:
        if os.path.exists(p):
            fichier = p
            break
    if not fichier:
        infra_data['reservoirs'] = pd.DataFrame()
        infra_data['stations'] = pd.DataFrame()
        return infra_data

    try:
        df_r = pd.read_excel(fichier, sheet_name="Réservoir", header=7)
        df_r = df_r[df_r['Commune'].notna()].reset_index(drop=True)
        coords = df_r['Adresse/ position GPS'].apply(lambda x: pd.Series(extraire_coordonnees(x)))
        df_r['Latitude'] = coords[0]
        df_r['Longitude'] = coords[1]
        df_r = df_r.dropna(subset=['Latitude', 'Longitude'])
        if 'Capacité' in df_r.columns:
            df_r['Capacite_m3'] = pd.to_numeric(df_r['Capacité'], errors='coerce').fillna(0)
        infra_data['reservoirs'] = df_r
    except:
        infra_data['reservoirs'] = pd.DataFrame()

    try:
        df_s = pd.read_excel(fichier, sheet_name="SP", header=6)
        df_s = df_s[df_s['Commune'].notna()].reset_index(drop=True)
        coords = df_s['Adresse/ position GPS'].apply(lambda x: pd.Series(extraire_coordonnees(x)))
        df_s['Latitude'] = coords[0]
        df_s['Longitude'] = coords[1]
        df_s = df_s.dropna(subset=['Latitude', 'Longitude'])
        if 'Puissance Installée ' in df_s.columns:
            df_s['Puissance_kW'] = pd.to_numeric(df_s['Puissance Installée '], errors='coerce').fillna(0)
        infra_data['stations'] = df_s
    except:
        infra_data['stations'] = pd.DataFrame()

    return infra_data

with st.spinner("📂 Chargement des données..."):
    model_class, model_reg, scaler = charger_modeles()
    df_centres, df_interventions = charger_donnees()
    infra_data = charger_infrastructures()
    df_rapports = charger_rapports()

# Ajouter les coordonnées GPS aux centres
if len(df_centres) > 0:
    if 'Latitude' not in df_centres.columns:
        df_centres['Latitude'] = df_centres['Centre'].apply(lambda x: CENTRES_GPS.get(str(x), (32.0, -6.5))[0])
    if 'Longitude' not in df_centres.columns:
        df_centres['Longitude'] = df_centres['Centre'].apply(lambda x: CENTRES_GPS.get(str(x), (32.0, -6.5))[1])

# ============================================================================
# CALCUL DES KPIs
# ============================================================================
if len(df_centres) > 0:
    nb_critique = int((df_centres['Priorite'] == 'Critique').sum()) if 'Priorite' in df_centres.columns else 0
    total_cout = int(df_centres['Cout_total_Dhs'].sum()) if 'Cout_total_Dhs' in df_centres.columns else 0
    total_int = int(df_centres['Nb_interventions'].sum()) if 'Nb_interventions' in df_centres.columns else 0
else:
    nb_critique = 0
    total_cout = 0
    total_int = 0

nb_reservoirs = len(infra_data.get('reservoirs', pd.DataFrame()))
nb_stations = len(infra_data.get('stations', pd.DataFrame()))


# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">💧</div>
        <div>
            <div class="sidebar-logo-text">SRM</div>
            <div class="sidebar-logo-sub">Eau Potable · Azilal</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">Vue d\'ensemble</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.metric("Centres", len(df_centres))
    with c2: st.metric("Critiques", nb_critique)
    c1, c2 = st.columns(2)
    with c1: st.metric("Réservoirs", nb_reservoirs)
    with c2: st.metric("Stations", nb_stations)

    st.markdown('<div class="sidebar-section">Niveaux de risque</div>', unsafe_allow_html=True)
    st.markdown("""
    <p style="font-size:0.78rem; line-height:2;">
        <span class="legend-dot" style="background:#22C55E"></span> Bon état &nbsp;·&nbsp; < 40 %<br>
        <span class="legend-dot" style="background:#F59E0B"></span> Surveillance &nbsp;·&nbsp; 40–70 %<br>
        <span class="legend-dot" style="background:#EF4444"></span> Critique &nbsp;·&nbsp; > 70 %
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button(" Déconnexion", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.show_change_password = False
        st.rerun()
    
    now = datetime.now()
    st.markdown(f'<p style="font-size:0.7rem;color:#94a3b8;text-align:center;margin-top:0.5rem">{now.strftime("%H:%M:%S")}</p>', unsafe_allow_html=True)


# ============================================================================
# EN-TÊTE (avec date en français)
# ============================================================================
now = datetime.now()

# Dictionnaires pour la conversion en français
jours_fr = {
    'Monday': 'Lundi', 'Tuesday': 'Mardi', 'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi', 'Friday': 'Vendredi', 'Saturday': 'Samedi', 'Sunday': 'Dimanche'
}
mois_fr = {
    'January': 'Janvier', 'February': 'Février', 'March': 'Mars', 'April': 'Avril',
    'May': 'Mai', 'June': 'Juin', 'July': 'Juillet', 'August': 'Août',
    'September': 'Septembre', 'October': 'Octobre', 'November': 'Novembre', 'December': 'Décembre'
}

# Convertir le jour et le mois en français
jour = jours_fr[now.strftime('%A')]
mois = mois_fr[now.strftime('%B')]
jour_numero = now.strftime('%d')
annee = now.strftime('%Y')
heure = now.strftime('%H:%M')

st.markdown(f"""
<div class="srm-header">
    <span class="srm-badge">💧 SRM · Eau Potable</span>
    <h1>Système de Maintenance Prédictive</h1>
    <p>{jour} {jour_numero} {mois} {annee} — {heure}</p>
</div>
""", unsafe_allow_html=True)


# ── KPI BAR ──
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card blue">
    <div class="kpi-icon">📍</div>
    <div class="kpi-value">{len(df_centres)}</div>
    <div class="kpi-label">Centres actifs</div>
  </div>
  <div class="kpi-card red">
    <div class="kpi-icon">🚨</div>
    <div class="kpi-value">{nb_critique}</div>
    <div class="kpi-label">Centres critiques</div>
  </div>
  <div class="kpi-card amber">
    <div class="kpi-icon">🔧</div>
    <div class="kpi-value">{total_int:,}</div>
    <div class="kpi-label">Interventions totales</div>
  </div>
  <div class="kpi-card green">
    <div class="kpi-icon">💰</div>
    <div class="kpi-value">{total_cout:,}</div>
    <div class="kpi-label">Coût total (Dhs)</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ============================================================================
# ONGLETS PRINCIPAUX
# ============================================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    " Cartographie",
    " Diagnostic",
    " Centres",
    " Infrastructures",
    " Rapports",
    " Planning"
])


# ============================================================================
# TAB 1: CARTOGRAPHIE
# ============================================================================
with tab1:
    st.markdown('<p class="section-title"> Carte des infrastructures</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1: show_centres = st.checkbox("📍 Centres", value=True)
    with col2: show_reservoirs = st.checkbox("💧 Réservoirs", value=True)
    with col3: show_stations = st.checkbox("⚡ Stations", value=True)

    m = folium.Map(location=[32.0, -6.5], zoom_start=8, tiles='CartoDB positron')
    mc = MarkerCluster().add_to(m)

    if show_centres and len(df_centres) > 0:
        for _, c in df_centres.iterrows():
            if c.get('Latitude', 0) != 0:
                prio = c.get('Priorite', '')
                color = 'red' if prio == 'Critique' else ('orange' if prio == 'Surveillance' else 'green')
                html = f"""<div style="font-family:DM Sans">
                            <b style="color:{color}">📍 {c['Centre']}</b><br>
                            📊 Interventions: {c.get('Nb_interventions', 0)}<br>
                            ⚠️ Score: {c.get('Score_risque', 0):.0f}%
                        </div>"""
                folium.Marker([c['Latitude'], c['Longitude']],
                              popup=folium.Popup(html, max_width=200),
                              icon=folium.Icon(color=color)).add_to(mc)

    if show_reservoirs and len(infra_data.get('reservoirs', pd.DataFrame())) > 0:
        for _, r in infra_data['reservoirs'].iterrows():
            if pd.notna(r.get('Latitude')):
                html = f"""<div><b style="color:#1D4ED8">💧 {r.get('Désignation', '')}</b><br>
                            Commune: {r.get('Commune', '')}<br>
                            Capacité: {r.get('Capacite_m3', 0):.0f} m³</div>"""
                folium.Marker([r['Latitude'], r['Longitude']],
                              popup=folium.Popup(html, max_width=200),
                              icon=folium.Icon(color='blue', icon='tint', prefix='fa')).add_to(mc)

    if show_stations and len(infra_data.get('stations', pd.DataFrame())) > 0:
        for _, s in infra_data['stations'].iterrows():
            if pd.notna(s.get('Latitude')):
                html = f"""<div><b style="color:#D97706">⚡ {s.get('Désignation', '')}</b><br>
                            Commune: {s.get('Commune', '')}<br>
                            Puissance: {s.get('Puissance_kW', 0):.0f} kW</div>"""
                folium.Marker([s['Latitude'], s['Longitude']],
                              popup=folium.Popup(html, max_width=200),
                              icon=folium.Icon(color='orange', icon='bolt', prefix='fa')).add_to(mc)

    folium_static(m, width=800, height=550)
    st.caption(f" {len(df_centres)} centres ·  {nb_reservoirs} réservoirs ·  {nb_stations} stations")


# ============================================================================
# TAB 2: DIAGNOSTIC
# ============================================================================
with tab2:
    st.markdown('<p class="section-title"> Analyse prédictive de criticité</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("####  Paramètres de l'équipement")
        nb_interventions = st.number_input(" Nombre d'interventions", min_value=0, max_value=50, value=5)
        taux_correctif = st.slider(" Taux correctif (%)", 0, 100, 50)
        anciennete = st.select_slider(" Âge de l'équipement", 
                                      options=["<1 an", "1-3 ans", "3-5 ans", "5-10 ans", ">10 ans"], 
                                      value="3-5 ans")
        type_analyse = st.radio(" Mode d'analyse", 
                                ["📊 Niveau de criticité", "📈 Score détaillé"], 
                                horizontal=True)

        if st.button(" Lancer l'analyse", type="primary", use_container_width=True):
            age_scores = {"<1 an": 0, "1-3 ans": 15, "3-5 ans": 30, "5-10 ans": 50, ">10 ans": 70}
            score = min(100, (nb_interventions * 3) + (taux_correctif * 0.4) + (age_scores.get(anciennete, 30) * 0.3))
            if "Niveau de criticité" in type_analyse:
                st.session_state.diag_classe = 2 if score >= 70 else (1 if score >= 40 else 0)
                st.session_state.diag_score = None
            else:
                st.session_state.diag_score = score
                st.session_state.diag_classe = None

    with col2:
        if st.session_state.get('diag_classe') is not None:
            cl = st.session_state.diag_classe
            if cl == 2:
                st.markdown("""
                <div class="diag-card critical">
                    <span class="diag-indicator">🔴</span>
                    <div class="diag-title">Criticité Élevée</div>
                    <div class="diag-desc">⚠️ Intervention immédiate requise</div>
                    <span class="diag-action">🛠 Intervention urgente</span>
                </div>
                """, unsafe_allow_html=True)
            elif cl == 1:
                st.markdown("""
                <div class="diag-card warning">
                    <span class="diag-indicator">🟠</span>
                    <div class="diag-title">Criticité Modérée</div>
                    <div class="diag-desc">⚠️ Planifier maintenance sous 15 jours</div>
                    <span class="diag-action">📅 Planifier</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="diag-card good">
                    <span class="diag-indicator">🟢</span>
                    <div class="diag-title">Criticité Faible</div>
                    <div class="diag-desc">✅ Équipement en bon état</div>
                    <span class="diag-action">✅ Surveillance normale</span>
                </div>
                """, unsafe_allow_html=True)
        elif st.session_state.get('diag_score') is not None:
            sc = st.session_state.diag_score
            if sc >= 70:
                color, niveau, action = "#DC2626", "Criticité Élevée", "🛠 Intervention immédiate"
            elif sc >= 40:
                color, niveau, action = "#D97706", "Criticité Modérée", "📅 Maintenance sous 15 jours"
            else:
                color, niveau, action = "#16A34A", "Criticité Faible", "✅ Surveillance normale"
            
            st.markdown(f"""
            <div class="diag-card" style="background:{color}08; border-color:{color}30;">
                <div class="diag-title" style="color:{color}">{niveau}</div>
                <div style="font-size:2.5rem;font-weight:700;color:{color};margin:0.5rem 0">{sc:.0f}<span style="font-size:1rem">%</span></div>
                <div class="diag-score-bar">
                    <div class="diag-score-fill" style="width:{sc}%;background:{color}"></div>
                </div>
                <div class="diag-score-num" style="color:{color}">{sc:.0f} / 100</div>
                <span class="diag-action" style="margin-top:1rem;background:{color}15;color:{color}">{action}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(" Ajustez les paramètres et cliquez sur 'Lancer l'analyse'")


# ============================================================================
# TAB 3: CENTRES
# ============================================================================
with tab3:
    st.markdown('<p class="section-title"> Liste des centres</p>', unsafe_allow_html=True)
    if len(df_centres) > 0:
        cols = ['Centre', 'Nb_interventions', 'Cout_total_Dhs', 'Score_risque', 'Priorite']
        st.dataframe(df_centres[[c for c in cols if c in df_centres.columns]], use_container_width=True)
    else:
        st.info("Aucun centre trouvé")


# ============================================================================
# TAB 4: INFRASTRUCTURES
# ============================================================================
with tab4:
    st.markdown('<p class="section-title"> Gestion des infrastructures</p>', unsafe_allow_html=True)

    it1, it2 = st.tabs([" Réservoirs", " Stations de pompage"])

    with it1:
        df_res = infra_data.get('reservoirs', pd.DataFrame())
        if len(df_res) > 0:
            st.dataframe(df_res[['Commune', 'Désignation', 'Capacite_m3', 'Latitude', 'Longitude']], use_container_width=True)
            st.caption(f" {len(df_res)} réservoirs")
        else:
            st.info("Aucune donnée de réservoirs")

    with it2:
        df_st = infra_data.get('stations', pd.DataFrame())
        if len(df_st) > 0:
            st.dataframe(df_st[['Commune', 'Désignation', 'Puissance_kW', 'Latitude', 'Longitude']], use_container_width=True)
            st.caption(f" {len(df_st)} stations")
        else:
            st.info("Aucune donnée de stations")



# ============================================================================
# TAB 5: RAPPORTS 
# ============================================================================
with tab5:
    st.markdown('<p class="section-title"> Saisie d\'un rapport d\'intervention</p>', unsafe_allow_html=True)

    # CSS (nfs l'code, ma tbeddelch)
    st.markdown("""
    <style>
    .required-star { color: #ef4444; font-size: 1.1rem; font-weight: bold; margin-left: 2px; }
    .required-label { font-weight: 500; color: #1e293b; }
    .delete-btn { background-color: #ef4444; color: white; border: none; border-radius: 6px; padding: 4px 12px; font-size: 0.75rem; cursor: pointer; }
    .delete-btn:hover { background-color: #dc2626; }
    </style>
    """, unsafe_allow_html=True)

    # ============================================================================
    # DICTIONNAIRE DES OUVRAGES PAR CENTRE (nfs l'code dyal 9bel, ma tbeddelch)
    # ============================================================================
    OUVRAGES_PAR_CENTRE = {
        "AZILAL": {
            "stations": [
                {"nom": "SR AZILAL", "type": "Station de reprise", "latitude": 31.9611021, "longitude": -6.5517532, "puissance": 33, "debit": 34},
                {"nom": "SR AIT OUAZOUD", "type": "Station de reprise", "latitude": 31.9667, "longitude": -6.5667, "puissance": 22, "debit": 15},
                {"nom": "Step Azilal", "type": "Station d'épuration", "latitude": 31.9600, "longitude": -6.5550, "puissance": 15, "debit": 10}
            ],
            "reservoirs": [
                {"nom": "R1500 Azilal", "type": "Réservoir", "latitude": 31.9650, "longitude": -6.5600, "capacite": 1500},
                {"nom": "R1000+R2000 (Hassan 1er)", "type": "Réservoir", "latitude": 31.9700, "longitude": -6.5580, "capacite": 3000}
            ]
        },
        "OUAOUIZEGHT": {
            "stations": [
                {"nom": "SR2 Ouaouizeght", "type": "Station de reprise", "latitude": 31.964888, "longitude": -6.561908, "puissance": 80, "debit": 16},
                {"nom": "SP1 Assainissement", "type": "Station de pompage", "latitude": 32.1667, "longitude": -6.4000, "puissance": 15, "debit": 5}
            ],
            "reservoirs": [
                {"nom": "R500 Ouaouizeght", "type": "Réservoir", "latitude": 32.1600, "longitude": -6.4050, "capacite": 500},
                {"nom": "R240+R140", "type": "Réservoir", "latitude": 32.1580, "longitude": -6.4080, "capacite": 380}
            ]
        },
        "FOUM JEMAA": {
            "stations": [
                {"nom": "SR1 Foum Jemaa", "type": "Station de reprise", "latitude": 31.8700, "longitude": -6.4000, "puissance": 60, "debit": 40},
                {"nom": "SR2 Foum Jemaa", "type": "Station de reprise", "latitude": 31.8750, "longitude": -6.3950, "puissance": 20, "debit": 3},
                {"nom": "Station Monobloc", "type": "Station de pompage", "latitude": 31.8800, "longitude": -6.3980, "puissance": 45, "debit": 30}
            ],
            "reservoirs": [
                {"nom": "R400 Foum Jemaa", "type": "Réservoir", "latitude": 31.8780, "longitude": -6.4000, "capacite": 400},
                {"nom": "R60 (Station Monobloc)", "type": "Réservoir", "latitude": 31.8820, "longitude": -6.3960, "capacite": 60},
                {"nom": "R30", "type": "Réservoir", "latitude": 31.8850, "longitude": -6.3920, "capacite": 30}
            ]
        },
        "BZOU": {
            "stations": [
                {"nom": "SR Bzou (IMEDDAHEN)", "type": "Station de reprise", "latitude": 32.1000, "longitude": -6.5500, "puissance": 4.1, "debit": 8.76},
                {"nom": "Forage Bzou NF1", "type": "Forage", "latitude": 32.1050, "longitude": -6.5480, "puissance": 30, "debit": 15},
                {"nom": "Forage Bzou NF2", "type": "Forage", "latitude": 32.1080, "longitude": -6.5450, "puissance": 30, "debit": 15}
            ],
            "reservoirs": [
                {"nom": "R80+R300 Bzou", "type": "Réservoir", "latitude": 32.1020, "longitude": -6.5520, "capacite": 380}
            ]
        },
        "IMDAHEN": {
            "stations": [
                {"nom": "SR ZIZ GAZ", "type": "Station de reprise", "latitude": 32.0833, "longitude": -6.4500, "puissance": 22, "debit": 10}
            ],
            "reservoirs": [
                {"nom": "R80+R150+R50", "type": "Réservoir", "latitude": 32.0800, "longitude": -6.4550, "capacite": 280}
            ]
        },
        "BENI AYAT": {
            "stations": [
                {"nom": "SR1 Beni Ayat", "type": "Station de reprise", "latitude": 32.2000, "longitude": -6.4167, "puissance": 11, "debit": 11.66},
                {"nom": "SR2 Beni Ayat", "type": "Station de reprise", "latitude": 32.1950, "longitude": -6.4200, "puissance": 15.5, "debit": 8.32},
                {"nom": "SR3 Beni Ayat", "type": "Station de reprise", "latitude": 32.1900, "longitude": -6.4250, "puissance": 37, "debit": 20},
                {"nom": "Station Monobloc", "type": "Station de pompage", "latitude": 32.1980, "longitude": -6.4180, "puissance": 75, "debit": 50}
            ],
            "reservoirs": [
                {"nom": "R174 Beni Ayat", "type": "Réservoir", "latitude": 32.2020, "longitude": -6.4150, "capacite": 174}
            ]
        },
        "OUZOUD": {
            "stations": [
                {"nom": "SR Ouzoud", "type": "Station de reprise", "latitude": 32.0167, "longitude": -6.7167, "puissance": 33, "debit": 25},
                {"nom": "SR AIT TAGULA", "type": "Station de reprise", "latitude": 32.0200, "longitude": -6.7100, "puissance": 22, "debit": 15}
            ],
            "reservoirs": [
                {"nom": "R200 Ouzoud", "type": "Réservoir", "latitude": 32.0180, "longitude": -6.7140, "capacite": 200},
                {"nom": "R70 Ouzoud", "type": "Réservoir", "latitude": 32.0220, "longitude": -6.7080, "capacite": 70}
            ]
        },
        "TANANT": {
            "stations": [
                {"nom": "SR Tanant", "type": "Station de reprise", "latitude": 31.7833, "longitude": -6.9167, "puissance": 62, "debit": 5}
            ],
            "reservoirs": [
                {"nom": "R250 Tanant", "type": "Réservoir", "latitude": 31.7800, "longitude": -6.9200, "capacite": 250},
                {"nom": "R120 Tanant", "type": "Réservoir", "latitude": 31.7850, "longitude": -6.9150, "capacite": 120}
            ]
        },
        "AIT ATTAB": {
            "stations": [
                {"nom": "Forage Ait Attab", "type": "Forage", "latitude": 31.9833, "longitude": -6.3500, "puissance": 45, "debit": 30}
            ],
            "reservoirs": [
                {"nom": "R600 Ait Attab", "type": "Réservoir", "latitude": 31.9800, "longitude": -6.3550, "capacite": 600},
                {"nom": "R25 Ait Attab", "type": "Réservoir", "latitude": 31.9850, "longitude": -6.3480, "capacite": 25}
            ]
        },
        "TISKI": {
            "stations": [
                {"nom": "Forage Tiski", "type": "Forage", "latitude": 31.8500, "longitude": -6.5000, "puissance": 22, "debit": 10}
            ],
            "reservoirs": [
                {"nom": "R200 Tiski", "type": "Réservoir", "latitude": 31.8550, "longitude": -6.4950, "capacite": 200}
            ]
        },
        "OUAOULA": {
            "stations": [
                {"nom": "Surpresseur Ouaoula", "type": "Station de pompage", "latitude": 32.0500, "longitude": -6.4500, "puissance": 2, "debit": 3.65}
            ],
            "reservoirs": [
                {"nom": "R400 Ouaoula", "type": "Réservoir", "latitude": 32.0450, "longitude": -6.4550, "capacite": 400},
                {"nom": "R200 EL MAHDA", "type": "Réservoir", "latitude": 32.0480, "longitude": -6.4520, "capacite": 200}
            ]
        },
        "DEMNATE": {
            "stations": [
                {"nom": "R1000m3 Surpresseur", "type": "Surpresseur", "latitude": 31.723729, "longitude": -6.993379, "puissance": 4, "debit": 1.11},
                {"nom": "SR3 Demnate", "type": "Station de reprise", "latitude": 31.8500, "longitude": -7.0167, "puissance": 45, "debit": 25},
                {"nom": "SR AIT SEHNOUN", "type": "Station de reprise", "latitude": 31.8600, "longitude": -7.0100, "puissance": 7.5, "debit": 3}
            ]
        },
        "TIFNI": {
            "stations": [
                {"nom": "Forage Tifni", "type": "Forage", "latitude": 31.9000, "longitude": -6.5000, "puissance": 30, "debit": 15}
            ],
            "reservoirs": [
                {"nom": "R100 Tifni", "type": "Réservoir", "latitude": 31.8950, "longitude": -6.5050, "capacite": 100}
            ]
        },
        "IMLIL": {
            "stations": [
                {"nom": "SR7 Imlil", "type": "Station de reprise", "latitude": 31.7593, "longitude": -7.0099, "puissance": 12.6, "debit": 15},
                {"nom": "SR6 Imlil", "type": "Station de reprise", "latitude": 31.7600, "longitude": -7.0050, "puissance": 7.5, "debit": 9}
            ]
        },
        "AFOURER": {
            "stations": [
                {"nom": "SR1 Afourer", "type": "Station de reprise", "latitude": 32.2000, "longitude": -6.4167, "puissance": 20, "debit": 13.5},
                {"nom": "SR2 Afourer", "type": "Station de reprise", "latitude": 32.1950, "longitude": -6.4200, "puissance": 13, "debit": 5.1},
                {"nom": "Station Monobloc Afourer", "type": "Station de pompage", "latitude": 32.1980, "longitude": -6.4180, "puissance": 75, "debit": 50}
            ],
            "reservoirs": [
                {"nom": "R500 Afourer", "type": "Réservoir", "latitude": 32.2020, "longitude": -6.4150, "capacite": 500},
                {"nom": "R150 Afourer", "type": "Réservoir", "latitude": 32.2050, "longitude": -6.4120, "capacite": 150}
            ]
        },
        "BENI HASAN": {
            "stations": [
                {"nom": "Surpresseur SR1 (VER BF)", "type": "Station de pompage", "latitude": 32.2000, "longitude": -6.5000, "puissance": 15, "debit": 8},
                {"nom": "Surpresseur SR2 (vers AIT ABDERRAHMAN)", "type": "Station de pompage", "latitude": 32.2050, "longitude": -6.4950, "puissance": 11, "debit": 6}
            ],
            "reservoirs": [
                {"nom": "R300 Beni Hasan", "type": "Réservoir", "latitude": 32.2020, "longitude": -6.4980, "capacite": 300}
            ]
        },
        "RFALA": {
            "stations": [
                {"nom": "SR OULED MBAREK", "type": "Station de reprise", "latitude": 32.2500, "longitude": -6.2500, "puissance": 22, "debit": 9.4},
                {"nom": "SR OULED RMICH", "type": "Station de reprise", "latitude": 32.2450, "longitude": -6.2550, "puissance": 15, "debit": 5.6}
            ]
        },
        "TAMDA NPOUMERCID": {
            "stations": [
                {"nom": "SR14", "type": "Station de reprise", "latitude": 32.0000, "longitude": -6.5500, "puissance": 15, "debit": 10},
                {"nom": "SR10", "type": "Station de reprise", "latitude": 32.0050, "longitude": -6.5450, "puissance": 6, "debit": 5}
            ]
        },
        "DR BENI AYAT": {
            "stations": [
                {"nom": "Forage DR Beni Ayat", "type": "Forage", "latitude": 32.1800, "longitude": -6.4200, "puissance": 30, "debit": 15}
            ],
            "reservoirs": [
                {"nom": "R100 DR Beni Ayat", "type": "Réservoir", "latitude": 32.1780, "longitude": -6.4220, "capacite": 100},
                {"nom": "R100 Ait Imloul", "type": "Réservoir", "latitude": 32.1750, "longitude": -6.4250, "capacite": 100}
            ]
        }
    }

    if 'centres_dynamiques' not in st.session_state:
        st.session_state.centres_dynamiques = CENTRES_COMPLETS.copy()
    
    # Initialiser les coordonnées
    if 'auto_lat' not in st.session_state:
        st.session_state.auto_lat = 32.0
    if 'auto_lon' not in st.session_state:
        st.session_state.auto_lon = -6.5
    if 'auto_puissance' not in st.session_state:
        st.session_state.auto_puissance = 0
    if 'auto_debit' not in st.session_state:
        st.session_state.auto_debit = 0
    if 'selected_ouvrage' not in st.session_state:
        st.session_state.selected_ouvrage = ""
    
    # Variable pour forcer le reset
    if 'reset_trigger' not in st.session_state:
        st.session_state.reset_trigger = 0
    
    # Pour gérer la suppression
    if 'show_delete_dialog' not in st.session_state:
        st.session_state.show_delete_dialog = False
    if 'rapport_to_delete' not in st.session_state:
        st.session_state.rapport_to_delete = None

    # Fonctions
    def delete_rapport(index):
        global df_rapports
        try:
            df_rapports.drop(index, inplace=True)
            sauvegarder_rapports(df_rapports)
            st.session_state.delete_success = True
            return True
        except Exception as e:
            st.error(f"Erreur lors de la suppression: {e}")
            return False

    def get_coordinates_from_centre(centre_name):
        if not centre_name:
            return 32.0, -6.5
        centre_name_lower = centre_name.lower().strip()
        for key, (lat, lon) in CENTRES_GPS.items():
            if key.lower() == centre_name_lower:
                return lat, lon
        centre_normalized = centre_name_lower.replace('-', ' ').replace('_', ' ').replace("'", " ").replace("’", " ")
        for key, (lat, lon) in CENTRES_GPS.items():
            key_normalized = key.lower().replace('-', ' ').replace('_', ' ').replace("'", " ").replace("’", " ")
            if centre_normalized == key_normalized:
                return lat, lon
        for key, (lat, lon) in CENTRES_GPS.items():
            key_lower = key.lower()
            if centre_name_lower in key_lower or key_lower in centre_name_lower:
                return lat, lon
        mots = centre_name_lower.split()
        for key, (lat, lon) in CENTRES_GPS.items():
            key_lower = key.lower()
            for mot in mots:
                if len(mot) > 3 and mot in key_lower:
                    return lat, lon
        return 32.0, -6.5

    def exporter_pdf(df):
        if len(df) == 0:
            return None
        try:
            from fpdf import FPDF
            import tempfile
            pdf = FPDF(orientation='L', unit='mm', format='A4')
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "SRM - Rapport des Interventions", 0, 1, "C")
            pdf.ln(5)
            pdf.set_font("Arial", "I", 10)
            pdf.cell(0, 10, f"Date d'export: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, "C")
            pdf.ln(8)
            pdf.set_font("Arial", "B", 8)
            pdf.set_fill_color(29, 78, 216)
            pdf.set_text_color(255, 255, 255)
            headers = ['Date', 'Centre', 'Ouvrage', 'Désignation', 'Opération', 'Description', 'Coût pièces', 'Coût total']
            widths = [25, 30, 35, 30, 35, 35, 25, 25]
            for i, h in enumerate(headers):
                pdf.cell(widths[i], 10, h, 1, 0, "C", 1)
            pdf.ln()
            pdf.set_font("Arial", "", 7)
            pdf.set_text_color(0, 0, 0)
            for _, row in df.iterrows():
                pdf.cell(widths[0], 8, str(row.get('Date', ''))[:10], 1)
                pdf.cell(widths[1], 8, str(row.get('Centre', ''))[:20], 1)
                pdf.cell(widths[2], 8, str(row.get('Ouvrage', ''))[:25], 1)
                pdf.cell(widths[3], 8, str(row.get('Designation', ''))[:20], 1)
                pdf.cell(widths[4], 8, str(row.get('Operation', ''))[:25], 1)
                desc = str(row.get('Description', ''))
                if len(desc) > 35:
                    desc = desc[:32] + "..."
                pdf.cell(widths[5], 8, desc, 1)
                pdf.cell(widths[6], 8, f"{row.get('Pieces_Dhs', 0):,.0f}", 1, 0, "R")
                pdf.cell(widths[7], 8, f"{row.get('Total_Dhs', 0):,.0f}", 1, 0, "R")
                pdf.ln()
            pdf.ln(4)
            pdf.set_font("Arial", "B", 10)
            pdf.cell(0, 10, f"Total général: {df['Total_Dhs'].sum():,.2f} Dhs", 0, 1, "R")
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            pdf.output(tmp.name)
            return tmp.name
        except Exception as e:
            st.error(f"Erreur lors de la génération du PDF: {e}")
            return None

    def update_coordinates_from_ouvrage():
        centre = st.session_state.get(f'centre_select_{st.session_state.reset_trigger}', "")
        ouvrage_nom = st.session_state.get(f'ouvrage_select_{st.session_state.reset_trigger}', "")
        if centre and ouvrage_nom and centre in OUVRAGES_PAR_CENTRE:
            tous_ouvrages = []
            if 'stations' in OUVRAGES_PAR_CENTRE[centre]:
                tous_ouvrages.extend(OUVRAGES_PAR_CENTRE[centre]['stations'])
            if 'reservoirs' in OUVRAGES_PAR_CENTRE[centre]:
                tous_ouvrages.extend(OUVRAGES_PAR_CENTRE[centre]['reservoirs'])
            for ouvrage in tous_ouvrages:
                if ouvrage['nom'] == ouvrage_nom:
                    st.session_state.auto_lat = ouvrage['latitude']
                    st.session_state.auto_lon = ouvrage['longitude']
                    st.session_state.auto_puissance = ouvrage.get('puissance', 0)
                    st.session_state.auto_debit = ouvrage.get('debit', ouvrage.get('capacite', 0))
                    break

    def get_ouvrages_for_centre(centre):
        if not centre or centre not in OUVRAGES_PAR_CENTRE:
            return []
        ouvrages = []
        if 'stations' in OUVRAGES_PAR_CENTRE[centre]:
            for s in OUVRAGES_PAR_CENTRE[centre]['stations']:
                ouvrages.append(f"{s['nom']} ({s['type']})")
        if 'reservoirs' in OUVRAGES_PAR_CENTRE[centre]:
            for r in OUVRAGES_PAR_CENTRE[centre]['reservoirs']:
                ouvrages.append(f"{r['nom']} ({r['type']})")
        return ouvrages

    def update_centre():
        centre = st.session_state.get(f'centre_select_{st.session_state.reset_trigger}', "")
        lat, lon = get_coordinates_from_centre(centre)
        st.session_state.auto_lat = lat
        st.session_state.auto_lon = lon
        st.session_state.selected_ouvrage = ""
        st.session_state.auto_puissance = 0
        st.session_state.auto_debit = 0

    # Interface
    st.markdown("#### Informations générales")
    st.caption(" Les champs marqués d'un <span style='color:#ef4444'>*</span> sont obligatoires", unsafe_allow_html=True)
    st.markdown("---")
    
    col1, col2 = st.columns(2)

    # Clé unique basée sur reset_trigger
    widget_key = f"_{st.session_state.reset_trigger}"

    with col1:
        date_rapport = st.date_input(" Date de l'intervention", datetime.now())
        
        st.markdown('<span class="required-label"> Centre / Commune</span> <span class="required-star">*</span>', unsafe_allow_html=True)
        centre = st.selectbox(
            "", 
            [""] + st.session_state.centres_dynamiques,
            key=f"centre_select{widget_key}",
            on_change=update_centre,
            label_visibility="collapsed"
        )
        
        ouvrages_list = get_ouvrages_for_centre(centre) if centre else []
        
        if centre and ouvrages_list:
            st.markdown('<span class="required-label"> Ouvrage / Équipement</span>', unsafe_allow_html=True)
            ouvrage_selectionne = st.selectbox(
                "",
                [""] + ouvrages_list,
                key=f"ouvrage_select{widget_key}",
                on_change=update_coordinates_from_ouvrage,
                label_visibility="collapsed"
            )
            if ouvrage_selectionne:
                st.session_state.selected_ouvrage = ouvrage_selectionne.split(" (")[0] if " (" in ouvrage_selectionne else ouvrage_selectionne
            else:
                st.session_state.selected_ouvrage = ""
        elif centre and not ouvrages_list:
            st.info(f"ℹ️ Aucun ouvrage enregistré pour {centre}")
            st.session_state.selected_ouvrage = ""
        
        st.markdown('<span class="required-label"> Désignation</span> <span class="required-star">*</span>', unsafe_allow_html=True)
        designations = ["", "Pompe immergée", "Pompe axiale", "Pompe centrifuge", 
                       "Station de reprise", "Station de pompage", "Surpresseur",
                       "Réservoir", "Armoire électrique", "Variateur de vitesse", "Vanne"]
        designation = st.selectbox("", designations, key=f"designation{widget_key}", label_visibility="collapsed")
        if designation == "":
            designation = st.text_input(" Autre désignation", key=f"autre_designation{widget_key}", placeholder="Ex: Pompe CP-2000")
        
        type_equipement = st.selectbox(" Type d'équipement", ["", "Pompe", "Station", "Réservoir", "Armoire", "Vanne"], key=f"type_equipement{widget_key}")
        machine = st.text_input(" Machine/Équipement", key=f"machine{widget_key}", placeholder="Ex: SR2, Pompe N°2")

    with col2:
        st.markdown("#### Coordonnées GPS")
        
        if st.session_state.selected_ouvrage:
            st.success(f"✅ Ouvrage sélectionné: **{st.session_state.selected_ouvrage}**")
        elif centre and ouvrages_list:
            st.info("📌 Sélectionnez un ouvrage pour charger ses coordonnées")
        elif centre:
            st.info("ℹ️ Aucun ouvrage enregistré. Saisie manuelle possible.")
        else:
            st.info("📍 Sélectionnez un centre")
        
        col_g1, col_g2 = st.columns(2)
        with col_g1: 
            latitude = st.number_input("Latitude", value=st.session_state.auto_lat, format="%.6f", key=f"lat{widget_key}")
        with col_g2: 
            longitude = st.number_input("Longitude", value=st.session_state.auto_lon, format="%.6f", key=f"lon{widget_key}")
        
        st.markdown("#### Caractéristiques techniques")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            puissance = st.number_input(" Puissance installée (kW)", min_value=0, value=st.session_state.auto_puissance, step=5, key=f"puissance{widget_key}")
        with col_p2:
            debit = st.number_input(" Débit global (l/s)", min_value=0, value=st.session_state.auto_debit, step=5, key=f"debit{widget_key}")
        nb_groupes = st.number_input(" Nombre de groupes", min_value=0, value=1, step=1, key=f"nb_groupes{widget_key}")

    st.markdown("---")
    st.markdown("#### Détails de l'intervention")
    
    col1, col2 = st.columns(2)

    with col1:
        type_intervention = st.selectbox(" Type d'intervention", ["Corrective", "Préventive", "Inspection", "Urgente"], key=f"type_int{widget_key}")
        duree = st.number_input(" Durée (heures)", min_value=0.5, value=2.0, step=0.5, key=f"duree{widget_key}")

    with col2:
        st.markdown('<span class="required-label"> Opération effectuée</span> <span class="required-star">*</span>', unsafe_allow_html=True)
        operation = st.text_input("", key=f"operation{widget_key}", placeholder="Ex: Changement de pompe", label_visibility="collapsed")

    description = st.text_area(" Description détaillée", key=f"description{widget_key}", placeholder="Détails de l'intervention...", height=80)

    st.markdown("---")
    st.markdown("#### Coûts de l'intervention")
    col_a, col_b, col_c, col_d = st.columns(4)

    with col_a: pieces = st.number_input(" Pièces (Dhs)", min_value=0.0, value=0.0, step=100.0, format="%.0f", key=f"pieces{widget_key}")
    with col_b: main_oeuvre = st.number_input(" Main d'œuvre (Dhs)", min_value=0.0, value=0.0, step=100.0, format="%.0f", key=f"main_oeuvre{widget_key}")
    with col_c: frais_deplacement = st.number_input(" Frais déplacement (Dhs)", min_value=0.0, value=0.0, step=50.0, format="%.0f", key=f"frais_dep{widget_key}")
    with col_d: frais_divers = st.number_input(" Frais divers (Dhs)", min_value=0.0, value=0.0, step=50.0, format="%.0f", key=f"frais_div{widget_key}")

    total = pieces + main_oeuvre + frais_deplacement + frais_divers
    st.info(f" **Total calculé automatiquement: {total:,.2f} Dhs**")

    with st.expander(" Aperçu avant sauvegarde"):
        st.markdown(f"""
        <table style="width:100%; font-size:13px">
            <tr><td style="width:35%"><b> Date</b></td>
            <td>{date_rapport.strftime('%d/%m/%Y')}</td>
            </tr>
            <tr><td><b> Centre</b> <span style="color:#ef4444">*</span></td>
            <td>{centre if centre else '⚠️ À remplir'}</td>
            </tr>
            <tr><td><b> Ouvrage</b></td>
            <td>{st.session_state.selected_ouvrage if st.session_state.selected_ouvrage else 'Non spécifié'}</td>
            </tr>
            <tr><td><b> Désignation</b> <span style="color:#ef4444">*</span></td>
            <td>{designation if designation else '⚠️ À remplir'}</td>
            </tr>
            <tr><td><b> Opération</b> <span style="color:#ef4444">*</span></td>
            <td>{operation if operation else '⚠️ À remplir'}</td>
            </tr>
            <tr><td><b> Coordonnées GPS</b></td>
            <td>{latitude:.6f}, {longitude:.6f}</td>
            </tr>
            <tr><td><b> Total</b></td>
            <td><b style="color:#0066cc">{total:,.2f} Dhs</b></td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    # Boutons d'enregistrement
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("💾 Enregistrer le rapport", type="primary", use_container_width=True):
            champs_manquants = []
            if not centre:
                champs_manquants.append("Centre")
            if not designation:
                champs_manquants.append("Désignation")
            if not operation:
                champs_manquants.append("Opération")
            
            if champs_manquants:
                st.error(f"❌ Champs obligatoires manquants : {', '.join(champs_manquants)}")
            else:
                nouveau_rapport = pd.DataFrame([{
                    'Date': date_rapport.strftime('%Y-%m-%d'),
                    'Centre': centre,
                    'Ouvrage': st.session_state.selected_ouvrage,
                    'Designation': designation,
                    'Type_equipement': type_equipement,
                    'Latitude': float(latitude),
                    'Longitude': float(longitude),
                    'Puissance_kW': float(puissance),
                    'Debit_l_s': float(debit),
                    'Nb_groupes': int(nb_groupes),
                    'Machine': machine if machine else designation,
                    'Type_intervention': type_intervention,
                    'Operation': operation,
                    'Description': description,
                    'Duree_heures': float(duree),
                    'Pieces_Dhs': float(pieces),
                    'Main_oeuvre_Dhs': float(main_oeuvre),
                    'Frais_deplacement_Dhs': float(frais_deplacement),
                    'Frais_divers_Dhs': float(frais_divers),
                    'Total_Dhs': float(total),
                    'Statut': 'Terminé'
                }])
                df_rapports = pd.concat([df_rapports, nouveau_rapport], ignore_index=True)
                sauvegarder_rapports(df_rapports)
                
                if centre not in st.session_state.centres_dynamiques:
                    st.session_state.centres_dynamiques.append(centre)
                    st.session_state.centres_dynamiques.sort()
                
                st.success("✅ Rapport enregistré avec succès!")
                st.balloons()
                
                # Reset: incrémenter le compteur
                st.session_state.reset_trigger += 1
                st.rerun()
    
    with col_btn2:
        if st.button("📥 Enregistrer + Exporter Excel", use_container_width=True):
            champs_manquants = []
            if not centre:
                champs_manquants.append("Centre")
            if not designation:
                champs_manquants.append("Désignation")
            if not operation:
                champs_manquants.append("Opération")
            
            if champs_manquants:
                st.error(f"❌ Champs obligatoires manquants : {', '.join(champs_manquants)}")
            else:
                nouveau_rapport = pd.DataFrame([{
                    'Date': date_rapport.strftime('%Y-%m-%d'),
                    'Centre': centre,
                    'Ouvrage': st.session_state.selected_ouvrage,
                    'Designation': designation,
                    'Type_equipement': type_equipement,
                    'Latitude': float(latitude),
                    'Longitude': float(longitude),
                    'Puissance_kW': float(puissance),
                    'Debit_l_s': float(debit),
                    'Nb_groupes': int(nb_groupes),
                    'Machine': machine if machine else designation,
                    'Type_intervention': type_intervention,
                    'Operation': operation,
                    'Description': description,
                    'Duree_heures': float(duree),
                    'Pieces_Dhs': float(pieces),
                    'Main_oeuvre_Dhs': float(main_oeuvre),
                    'Frais_deplacement_Dhs': float(frais_deplacement),
                    'Frais_divers_Dhs': float(frais_divers),
                    'Total_Dhs': float(total),
                    'Statut': 'Terminé'
                }])
                df_rapports = pd.concat([df_rapports, nouveau_rapport], ignore_index=True)
                sauvegarder_rapports(df_rapports)
                
                if centre not in st.session_state.centres_dynamiques:
                    st.session_state.centres_dynamiques.append(centre)
                    st.session_state.centres_dynamiques.sort()
                
                df_rapports.to_excel("rapports_interventions_complet.xlsx", index=False)
                
                st.success("✅ Rapport enregistré et exporté avec succès!")
                st.balloons()
                
                # Reset: incrémenter le compteur
                st.session_state.reset_trigger += 1
                st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Historique des rapports")

    if 'delete_success' in st.session_state and st.session_state.delete_success:
        st.success(" Rapport supprimé avec succès!")
        st.session_state.delete_success = False
        st.rerun()

    if len(df_rapports) > 0:
        df_rapports_display = df_rapports.copy()
        df_rapports_display = df_rapports_display.reset_index()
        
        st.markdown("#### Liste des rapports d'intervention")
        
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.2, 1.2, 1.5, 1.5, 1.8, 1, 1, 0.6])
        
        with col1:
            st.markdown(" Date")
        with col2:
            st.markdown(" Centre")
        with col3:
            st.markdown(" Ouvrage")
        with col4:
            st.markdown(" Désignation")
        with col5:
            st.markdown(" Opération")
        with col6:
            st.markdown(" Pièces")
        with col7:
            st.markdown(" Total")
        with col8:
            st.markdown(" Action")
        
        st.markdown("---")
        
        for idx, row in df_rapports_display.iterrows():
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.2, 1.2, 1.5, 1.5, 1.8, 1, 1, 0.6])
            
            with col1:
                st.write(str(row.get('Date', ''))[:10])
            with col2:
                st.write(str(row.get('Centre', ''))[:15])
            with col3:
                st.write(str(row.get('Ouvrage', ''))[:20])
            with col4:
                st.write(str(row.get('Designation', ''))[:15])
            with col5:
                st.write(str(row.get('Operation', ''))[:25])
            with col6:
                st.write(f"{row.get('Pieces_Dhs', 0):,.0f} Dhs")
            with col7:
                st.write(f"{row.get('Total_Dhs', 0):,.0f} Dhs")
            with col8:
                if st.button(f"❌", key=f"delete_{idx}"):
                    st.session_state.rapport_to_delete = idx
                    st.session_state.show_delete_dialog = True
        
        if st.session_state.show_delete_dialog:
            with st.expander("⚠️ Confirmation de suppression", expanded=True):
                st.warning("⚠️ Êtes-vous sûr de vouloir supprimer ce rapport ? Cette action est irréversible.")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("✅ Oui, supprimer", key="confirm_delete"):
                        if delete_rapport(st.session_state.rapport_to_delete):
                            st.session_state.show_delete_dialog = False
                            st.session_state.rapport_to_delete = None
                            st.rerun()
                with col_no:
                    if st.button("❌ Non, annuler", key="cancel_delete"):
                        st.session_state.show_delete_dialog = False
                        st.session_state.rapport_to_delete = None
                        st.rerun()
        
        with st.expander("📋 Voir le tableau complet"):
            cols_affichage = {
                'Date': ' Date',
                'Centre': ' Centre',
                'Ouvrage': ' Ouvrage',
                'Designation': ' Désignation',
                'Operation': ' Opération',
                'Description': ' Description',
                'Type_intervention': ' Type',
                'Pieces_Dhs': ' Coût pièces',
                'Total_Dhs': ' Coût total'
            }
            
            df_display = df_rapports[list(cols_affichage.keys())].copy()
            df_display = df_display.rename(columns=cols_affichage)
            
            if ' Coût pièces' in df_display.columns:
                df_display[' Coût pièces'] = df_display[' Coût pièces'].apply(lambda x: f"{x:,.0f} Dhs")
            if ' Coût total' in df_display.columns:
                df_display[' Coût total'] = df_display[' Coût total'].apply(lambda x: f"{x:,.0f} Dhs")
            
            st.dataframe(df_display.sort_values(' Date', ascending=False), use_container_width=True)

        col1, col2, col3, col4 = st.columns(4)
        with col1: 
            st.metric(" Total rapports", len(df_rapports))
        with col2: 
            st.metric(" Total coût pièces", f"{df_rapports['Pieces_Dhs'].sum():,.0f} Dhs")
        with col3: 
            st.metric(" Durée totale", f"{df_rapports['Duree_heures'].sum():.1f} h")
        with col4: 
            st.metric(" Coût total moyen", f"{df_rapports['Total_Dhs'].mean():,.0f} Dhs")

        st.markdown("---")
        st.markdown("#### Actions sur les rapports")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("❌ Supprimer TOUS les rapports", use_container_width=True):
                df_rapports = pd.DataFrame(columns=df_rapports.columns)
                sauvegarder_rapports(df_rapports)
                st.rerun()
        with col2:
            df_rapports.to_excel("rapports_interventions.xlsx", index=False)
            with open("rapports_interventions.xlsx", "rb") as f:
                st.download_button("📥 Exporter Excel", f, "rapports_interventions.xlsx")
        with col3:
            pdf_file = exporter_pdf(df_rapports)
            if pdf_file:
                with open(pdf_file, "rb") as f:
                    st.download_button("📄 Exporter PDF", f, "rapports_interventions.pdf")
    else:
        st.info(" Aucun rapport enregistré pour le moment")
# ============================================================================
# TAB 6: PLANNING
# ============================================================================
with tab6:
    st.markdown('<p class="section-title">📅 Planning de maintenance préventive</p>', unsafe_allow_html=True)

    st.markdown("#### 🚨 Centres nécessitant une attention particulière")

    if len(df_rapports) > 0:
        df_rapports['Date'] = pd.to_datetime(df_rapports['Date'])
        dernieres = df_rapports.groupby('Centre')['Date'].max().reset_index()
        dernieres['Jours'] = (datetime.now() - dernieres['Date']).dt.days
        centres_risque = dernieres[dernieres['Jours'] > 30].sort_values('Jours', ascending=False)

        if len(centres_risque) > 0:
            st.warning(f"⚠️ {len(centres_risque)} centre(s) sans intervention depuis plus de 30 jours")
            for _, row in centres_risque.iterrows():
                if row['Jours'] > 90:
                    st.error(f"🔴 **{row['Centre']}** - {int(row['Jours'])} jours - Intervention urgente!")
                elif row['Jours'] > 60:
                    st.warning(f"🟠 **{row['Centre']}** - {int(row['Jours'])} jours - Planifier intervention")
                else:
                    st.info(f"🟡 **{row['Centre']}** - {int(row['Jours'])} jours - À surveiller")
        else:
            st.success("✅ Tous les centres ont eu des interventions récentes")
    else:
        st.info("Aucun rapport d'intervention enregistré pour le moment")

    st.markdown("---")
    st.markdown("#### 📋 Planning d'interventions proposé")

    if len(df_centres) > 0 and 'Nb_interventions' in df_centres.columns:
        moyenne = df_centres['Nb_interventions'].mean()
        df_planning = df_centres[['Centre', 'Nb_interventions', 'Score_risque', 'Priorite']].copy()

        def priorite(row):
            nb = row['Nb_interventions']
            if nb <= moyenne * 0.5:
                return "Haute", "🔴", "Intervenir dans les 15 jours"
            elif nb <= moyenne * 0.8:
                return "Moyenne", "🟠", "Intervenir dans le mois"
            else:
                return "Basse", "🟢", "Maintenance normale"

        df_planning[['Prio', 'Urgence', 'Action']] = df_planning.apply(lambda r: pd.Series(priorite(r)), axis=1)
        planning_urgent = df_planning[df_planning['Prio'] == 'Haute'].sort_values('Nb_interventions')

        if len(planning_urgent) > 0:
            st.markdown("#### 🔴 Interventions à planifier en priorité")
            for _, row in planning_urgent.iterrows():
                st.markdown(f"""
                <div class="alert-row crit">
                    <span class="ar-icon">📍</span>
                    <div class="ar-body">
                        <div class="ar-name">{row['Centre']}</div>
                        <div class="ar-sub">📊 {row['Nb_interventions']} interventions · ⚠️ Risque: {row['Score_risque']:.0f}%</div>
                    </div>
                    <span class="ar-badge">{row['Action']}</span>
                </div>
                """, unsafe_allow_html=True)

        with st.expander("📋 Voir le planning complet"):
            st.dataframe(df_planning[['Centre', 'Nb_interventions', 'Score_risque', 'Priorite', 'Prio', 'Action']], 
                        use_container_width=True,
                        column_config={'Score_risque': st.column_config.ProgressColumn('Risque', format='%d%%')})
    else:
        st.info("Données insuffisantes pour générer le planning")

    st.markdown("---")
    st.markdown("#### 📊 Statistiques des interventions par centre")

    if len(df_rapports) > 0:
        stats = df_rapports.groupby('Centre').agg(
            Nb_rapports=('Machine', 'count'),
            Cout_total=('Total_Dhs', 'sum'),
            Duree_totale=('Duree_heures', 'sum')
        ).reset_index()
        dernieres2 = df_rapports.groupby('Centre')['Date'].max().reset_index()
        stats = stats.merge(dernieres2, on='Centre', how='left')
        stats['Jours_depuis'] = (datetime.now() - pd.to_datetime(stats['Date'])).dt.days
        stats = stats.drop(columns=['Date'])

        st.dataframe(stats.sort_values('Jours_depuis', ascending=False), use_container_width=True)

        # if st.button("📥 Exporter le planning en Excel", use_container_width=True):
        #     stats.to_excel("planning_maintenance.xlsx", index=False)
        #     st.success("Exporté vers 'planning_maintenance.xlsx'")
         # Export du planning
        if st.button("📥 Exporter le planning en Excel", use_container_width=True):
            stats.to_excel("planning_maintenance.xlsx", index=False)
            with open("planning_maintenance.xlsx", "rb") as f:
                st.download_button("💾 Télécharger", f, file_name="planning_maintenance.xlsx", 
                                  mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.info("Aucun rapport pour générer les statistiques")
# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="srm-footer">
    💧 SRM · Système de Régulation et Maintenance · Eau Potable<br>
    Modèles ML | Gestion des infrastructures | Saisie des rapports
</div>
""", unsafe_allow_html=True)