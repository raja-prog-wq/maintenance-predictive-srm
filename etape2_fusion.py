# etape2_fusion.py - VERSION AVEC STANDARDISATION DES CENTRES
"""
ÉTAPE 2: FUSION DES DONNÉES + STANDARDISATION
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🔗 ÉTAPE 2: FUSION DES DONNÉES + STANDARDISATION")
print("="*60)

# ============================================================================
# DICTIONNAIRE POUR STANDARDISER LES CENTRES
# ============================================================================
MAPPING_CENTRES = {
    # BZOU
    "BZOU": "BZOU", "Bzou": "BZOU", "bzou": "BZOU",
    
    # IMDAHEN
    "IMDAHEN": "IMDAHEN", "imdahen": "IMDAHEN", "Imedahen": "IMDAHEN",
    
    # FOUM JEMAA
    "FOUM JEMAA": "FOUM JEMAA", "foum jemaa": "FOUM JEMAA", "Foum Jemaâ": "FOUM JEMAA",
    "FOM JEMAA": "FOUM JEMAA", "fom jemaa": "FOUM JEMAA",
    
    # BENI HASAN
    "BENI HASAN": "BENI HASAN", "beni hasan": "BENI HASAN",
    
    # TANANT
    "TANANT": "TANANT", "Tanant": "TANANT", "tanant": "TANANT",
    
    # OUZOUD
    "OUZOUD": "OUZOUD", "Ouzoud": "OUZOUD", "ouzoud": "OUZOUD", "OZOUD": "OUZOUD", "ozoud": "OUZOUD",
    
    # AIT ATTAB
    "AIT ATTAB": "AIT ATTAB", "ait attab": "AIT ATTAB", "ait attb": "AIT ATTAB", "aitattb": "AIT ATTAB",
    
    # TISKI
    "TISKI": "TISKI", "tiski": "TISKI", "TISQUI": "TISKI", "tisqui": "TISKI",
    
    # OUAOULA
    "OUAOULA": "OUAOULA", "Ouaoula": "OUAOULA", "ouaoula": "OUAOULA",
    
    # TAMDA NPOUMERCID
    "TAMDA NPOUMERCID": "TAMDA NPOUMERCID", "Tamda Npoumercid": "TAMDA NPOUMERCID",
    
    # AIT MHAMED
    "AIT MHAMED": "AIT MHAMED", "ait mhammed": "AIT MHAMED", "ait M'hamed": "AIT MHAMED",
    
    # AZILAL
    "AZILAL": "AZILAL", "Azilal": "AZILAL", "azilal": "AZILAL",
    
    # TIFNI
    "TIFNI": "TIFNI", "Tifni": "TIFNI", "tifni": "TIFNI",
    
    # IMLIL
    "IMLIL": "IMLIL", "Imlil": "IMLIL", "imlil": "IMLIL",
    
    # OUAOUIZEGHT
    "OUAOUIZEGHT": "OUAOUIZEGHT", "Ouaouizeght": "OUAOUIZEGHT", "ouaouizeght": "OUAOUIZEGHT",
    
    # BENI AYAT
    "BENI AYAT": "BENI AYAT", "beni ayat": "BENI AYAT", "beni ayyat": "BENI AYAT", "béni Ayat": "BENI AYAT",
    
    # DR BENI AYAT
    "DR BENI AYAT": "DR BENI AYAT", "Dr Beni Ayat": "DR BENI AYAT",
    
    # AFOURER
    "AFOURER": "AFOURER", "Afourer": "AFOURER", "afourer": "AFOURER",
    
    # DEMNATE
    "DEMNATE": "DEMNATE", "Demnate": "DEMNATE", "demnat": "DEMNATE",
    
    # RFALA
    "RFALA": "RFALA", "Rfala": "RFALA", "refala": "RFALA", "REFALA": "RFALA",
}
def standardiser_centre(nom):
    if pd.isna(nom):
        return nom
    nom_str = str(nom).strip()
    return MAPPING_CENTRES.get(nom_str, nom_str.upper())

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================
def trouver_fichier(nom_fichier):
    if os.path.exists(nom_fichier):
        return nom_fichier
    for root, dirs, files in os.walk('.'):
        if nom_fichier in files:
            return os.path.join(root, nom_fichier)
    return None

def extraire_coordonnees(adresse):
    if pd.isna(adresse):
        return None, None
    adresse = str(adresse)
    x_match = re.search(r'X[=\s]*([0-9.]+)', adresse, re.IGNORECASE)
    y_match = re.search(r'Y[=\s]*([0-9.-]+)', adresse, re.IGNORECASE)
    if x_match and y_match:
        return float(x_match.group(1)), float(y_match.group(1))
    coord_match = re.search(r'([0-9.]+)[,\s]+([0-9.-]+)', adresse)
    if coord_match:
        return float(coord_match.group(1)), float(coord_match.group(2))
    return None, None

# ============================================================================
# 1. CHARGEMENT DES INTERVENTIONS
# ============================================================================
print("\n📂 1. Chargement des interventions...")

fichier_maintenance = trouver_fichier("Maintenance_AM3_2_2023.xlsx")
if not fichier_maintenance:
    print("   ❌ Fichier non trouvé")
    exit()

df_raw = pd.read_excel(fichier_maintenance, sheet_name="Toutes les interventions", header=1)
df_interventions = df_raw[df_raw['Mois'].notna()].copy()
df_interventions = df_interventions.reset_index(drop=True)

# Nettoyer les colonnes
df_interventions.columns = df_interventions.columns.str.strip()
df_interventions['Date'] = pd.to_datetime(df_interventions['Date'], format='%d/%m/%Y', errors='coerce')
df_interventions = df_interventions.dropna(subset=['Date'])

# Convertir les coûts
if 'Total Montant (Dhs)' in df_interventions.columns:
    df_interventions['Total_Montant_Dhs'] = pd.to_numeric(df_interventions['Total Montant (Dhs)'], errors='coerce').fillna(0)

# STANDARDISER LES CENTRES
if 'Centre' in df_interventions.columns:
    df_interventions['Centre'] = df_interventions['Centre'].astype(str).str.strip().apply(standardiser_centre)

print(f"   ✅ {len(df_interventions)} interventions chargées")

# ============================================================================
# 2. AGRÉGATION PAR CENTRE (FUSION DES DOUBLONS)
# ============================================================================
print("\n📊 2. Agrégation par centre (fusion des doublons)...")

if 'Centre' in df_interventions.columns:
    # Grouper par centre standardisé
    interventions_par_centre = df_interventions.groupby('Centre').agg({
        'Total_Montant_Dhs': 'sum',
        'Date': 'count'
    }).reset_index()
    interventions_par_centre.columns = ['Centre', 'Cout_total_Dhs', 'Nb_interventions']
    
    # Compter les correctives
    if 'Type' in df_interventions.columns:
        correctives = df_interventions[df_interventions['Type'] == 'Corrective'].groupby('Centre').size().reset_index(name='Nb_correctives')
        interventions_par_centre = interventions_par_centre.merge(correctives, on='Centre', how='left')
        interventions_par_centre['Nb_correctives'] = interventions_par_centre['Nb_correctives'].fillna(0)
        interventions_par_centre['Taux_correctif'] = (interventions_par_centre['Nb_correctives'] / interventions_par_centre['Nb_interventions'] * 100).round(1)
    else:
        interventions_par_centre['Taux_correctif'] = 0
    
    print(f"   ✅ {len(interventions_par_centre)} centres uniques (doublons fusionnés)")
    print("\n   📍 CENTRES TROUVÉS:")
    for c in sorted(interventions_par_centre['Centre']):
        print(f"      - {c}")
else:
    print("   ❌ Colonne 'Centre' non trouvée")
    exit()

# ============================================================================
# 3. CHARGEMENT DES INFRASTRUCTURES (optionnel)
# ============================================================================
print("\n 3. Chargement des infrastructures (optionnel)...")

fichier_dp = trouver_fichier("Infrastructure eau DP AZILAL.xlsx")
if fichier_dp:
    print(f"   📂 Fichier trouvé: {fichier_dp}")
    try:
        df_reservoirs = pd.read_excel(fichier_dp, sheet_name="Réservoir", header=5)
        df_reservoirs = df_reservoirs[df_reservoirs['Commune'].notna()]
        # Standardiser les communes
        df_reservoirs['Commune'] = df_reservoirs['Commune'].astype(str).str.strip().apply(standardiser_centre)
        
        # Extraire coordonnées
        df_reservoirs[['Latitude', 'Longitude']] = df_reservoirs['Adresse/ position GPS'].apply(
            lambda x: pd.Series(extraire_coordonnees(x))
        )
        df_reservoirs['Capacite_m3'] = pd.to_numeric(df_reservoirs['Capacité'], errors='coerce').fillna(0)
        
        # Grouper par commune standardisée
        stats_reservoirs = df_reservoirs.groupby('Commune').agg({
            'Capacite_m3': 'sum',
            'Latitude': 'first',
            'Longitude': 'first'
        }).reset_index()
        stats_reservoirs.columns = ['Centre', 'Capacite_totale_m3', 'Latitude_reservoir', 'Longitude_reservoir']
        interventions_par_centre = interventions_par_centre.merge(stats_reservoirs, on='Centre', how='left')
        print(f"   ✅ Données réservoirs ajoutées")
    except Exception as e:
        print(f"   ⚠️ Erreur: {e}")
else:
    print("   ⚠️ Fichier infrastructure non trouvé (optionnel)")

# ============================================================================
# 4. COORDONNÉES GPS
# ============================================================================
print("\n📍 4. Définition des coordonnées GPS...")

centres_gps = {
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

def get_coordinates(row):
    centre = row['Centre']
    if 'Latitude_reservoir' in row and pd.notna(row['Latitude_reservoir']) and row['Latitude_reservoir'] != 0:
        return row['Latitude_reservoir'], row['Longitude_reservoir']
    return centres_gps.get(centre, (32.0, -6.5))

interventions_par_centre[['Latitude', 'Longitude']] = interventions_par_centre.apply(
    lambda row: pd.Series(get_coordinates(row)), axis=1
)

# ============================================================================
# 5. CALCUL DU SCORE DE RISQUE
# ============================================================================
print("\n⚠️ 5. Calcul du score de risque...")

def calculer_score_risque(row):
    score = 0
    score += min(50, row['Nb_interventions'] * 5)
    if 'Taux_correctif' in row:
        score += row['Taux_correctif'] * 0.3
    if 'Capacite_totale_m3' in row and row['Capacite_totale_m3'] > 1000:
        score += 10
    return min(100, score)

interventions_par_centre['Score_risque'] = interventions_par_centre.apply(calculer_score_risque, axis=1)

def get_priorite(score):
    if score >= 70: return "Critique"
    elif score >= 40: return "Surveillance"
    else: return "Bon état"

interventions_par_centre['Priorite'] = interventions_par_centre['Score_risque'].apply(get_priorite)

print(f"\n   📊 Distribution des priorités:")
print(interventions_par_centre['Priorite'].value_counts().to_string())

# ============================================================================
# 6. CRÉATION DU DATASET ML
# ============================================================================
print("\n🤖 6. Création du dataset ML...")

df_ml = interventions_par_centre[[
    'Centre', 'Nb_interventions', 'Cout_total_Dhs', 'Taux_correctif',
    'Score_risque', 'Priorite', 'Latitude', 'Longitude'
]].copy()

df_ml['Cible'] = (df_ml['Score_risque'] >= 50).astype(int)

print(f"   ✅ {len(df_ml)} échantillons")
print(f"   🎯 Cible=1 (risque élevé): {df_ml['Cible'].sum()}")
print(f"   🎯 Cible=0 (risque faible): {len(df_ml) - df_ml['Cible'].sum()}")

# ============================================================================
# 7. SAUVEGARDE
# ============================================================================
print("\n💾 7. Sauvegarde des données...")

with pd.ExcelWriter("Donnees_fusionnees.xlsx") as writer:
    interventions_par_centre.to_excel(writer, sheet_name="Centres", index=False)
    df_ml.to_excel(writer, sheet_name="ML_dataset", index=False)
    df_interventions.to_excel(writer, sheet_name="Interventions", index=False)

df_ml.to_csv("dataset_ml.csv", index=False, encoding='utf-8-sig')
print("   ✅ Fichiers sauvegardés")

# ============================================================================
# RÉCAPITULATIF
# ============================================================================
print("\n" + "="*60)
print("✅ ÉTAPE 2 TERMINÉE")
print("="*60)

print(f"\n📊 RÉCAPITULATIF:")
print(f"   - Centres uniques: {len(interventions_par_centre)}")
print(f"   - Interventions totales: {interventions_par_centre['Nb_interventions'].sum():.0f}")
print(f"   - Coût total: {interventions_par_centre['Cout_total_Dhs'].sum():,.0f} Dhs")

print("\n📋 LISTE FINALE DES CENTRES:")
for centre in sorted(interventions_par_centre['Centre']):
    row = interventions_par_centre[interventions_par_centre['Centre'] == centre].iloc[0]
    print(f"   - {centre}: {row['Nb_interventions']:.0f} interventions, {row['Score_risque']:.0f}%")