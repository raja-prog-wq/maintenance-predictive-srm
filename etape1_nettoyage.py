# etape1_nettoyage.py - VERSION CORRIGÉE
"""
ÉTAPE 1: Nettoyage des données + Standardisation des centres
"""

import pandas as pd
import re
from datetime import datetime
import os

print("="*60)
print("📍 ÉTAPE 1: NETTOYAGE DES DONNÉES + STANDARDISATION")
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

print(f"\n📂 Dossier de travail: {os.getcwd()}")

def trouver_fichier(nom_fichier):
    if os.path.exists(nom_fichier):
        return nom_fichier
    for root, dirs, files in os.walk('.'):
        if nom_fichier in files:
            return os.path.join(root, nom_fichier)
    return None

# ============================================================================
# 1.1 NETTOYAGE DES INTERVENTIONS
# ============================================================================
print("\n1.1 Nettoyage du fichier Maintenance_AM3_2_2023.xlsx...")

def nettoyer_interventions():
    fichier = trouver_fichier("Maintenance_AM3_2_2023.xlsx")
    if not fichier:
        print("   ❌ Fichier non trouvé")
        return pd.DataFrame()
    
    # Lire avec les bons en-têtes
    df = pd.read_excel(fichier, sheet_name="Toutes les interventions", header=1)
    
    # Nettoyer les noms de colonnes
    df.columns = df.columns.str.strip()
    
    # Supprimer les lignes vides
    df = df[df['Mois'].notna()]
    df = df.reset_index(drop=True)
    
    # Afficher les noms des colonnes pour debug
    print(f"   📋 Colonnes trouvées: {list(df.columns)}")
    
    # Renommer la colonne Total si nécessaire
    if 'Total Montant (Dhs)' in df.columns:
        df = df.rename(columns={'Total Montant (Dhs)': 'Total_Montant_Dhs'})
    elif 'Total_Montant_Dhs' not in df.columns:
        # Chercher une colonne qui contient 'Total'
        for col in df.columns:
            if 'total' in col.lower():
                df = df.rename(columns={col: 'Total_Montant_Dhs'})
                break
    
    # Convertir la date
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
        df = df.dropna(subset=['Date'])
    
    # Convertir les coûts en nombres
    cols_cout = ['Pièces Rech (Dhs)', 'PVT (Dhs)', 'Frais km (Dhs)', 'Main d\'œuvre (Dhs)', 'Total_Montant_Dhs']
    for col in cols_cout:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    # Standardiser les centres
    if 'Centre' in df.columns:
        df['Centre'] = df['Centre'].astype(str).str.strip().apply(standardiser_centre)
    
    print(f"   ✅ {len(df)} interventions nettoyées")
    return df

df_interventions = nettoyer_interventions()

# ============================================================================
# 1.2 AGRÉGATION PAR CENTRE
# ============================================================================
print("\n1.2 Agrégation des données par centre (fusion des doublons)...")

def creer_fichier_centres(df_interventions):
    if len(df_interventions) == 0:
        return pd.DataFrame()
    
    # Vérifier les colonnes disponibles
    print(f"   Colonnes disponibles: {list(df_interventions.columns)}")
    
    # Trouver la colonne du coût total
    colonne_cout = None
    for col in df_interventions.columns:
        if 'total' in col.lower() or 'montant' in col.lower():
            colonne_cout = col
            break
    
    if colonne_cout is None:
        print("   ❌ Colonne de coût non trouvée")
        return pd.DataFrame()
    
    print(f"   Utilisation de la colonne: {colonne_cout}")
    
    # Grouper par centre
    df_centres = df_interventions.groupby('Centre').agg({
        colonne_cout: 'sum',
        'Date': 'count',
    }).reset_index()
    
    df_centres.columns = ['Centre', 'Cout_total_Dhs', 'Nb_interventions']
    
    # Calculer le nombre d'interventions correctives
    if 'Type' in df_interventions.columns:
        nb_correctives = df_interventions[df_interventions['Type'] == 'Corrective'].groupby('Centre').size()
        df_centres['Nb_correctives'] = df_centres['Centre'].map(nb_correctives).fillna(0)
    else:
        df_centres['Nb_correctives'] = df_centres['Nb_interventions']
    
    # Taux correctif
    df_centres['Taux_correctif'] = (df_centres['Nb_correctives'] / df_centres['Nb_interventions'] * 100).fillna(0)
    
    # Score de risque
    max_int = df_centres['Nb_interventions'].max() if df_centres['Nb_interventions'].max() > 0 else 1
    df_centres['Score_risque'] = (
        (df_centres['Nb_interventions'] / max_int * 50) + 
        (df_centres['Taux_correctif'] * 0.5)
    ).clip(0, 100)
    
    # Priorité
    def get_priorite(score):
        if score >= 70:
            return 'Critique'
        elif score >= 40:
            return 'Surveillance'
        else:
            return 'Bon état'
    
    df_centres['Priorite'] = df_centres['Score_risque'].apply(get_priorite)
    
    # Coordonnées GPS
    gps_default = {
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
    
    df_centres['Latitude'] = df_centres['Centre'].apply(lambda x: gps_default.get(x, (32.0, -6.5))[0])
    df_centres['Longitude'] = df_centres['Centre'].apply(lambda x: gps_default.get(x, (32.0, -6.5))[1])
    
    print(f"   ✅ {len(df_centres)} centres uniques (doublons fusionnés)")
    print("\n   📍 LISTE DES CENTRES UNIQUES:")
    for centre in sorted(df_centres['Centre']):
        print(f"      - {centre}")
    
    return df_centres

df_centres = creer_fichier_centres(df_interventions)

# ============================================================================
# SAUVEGARDE
# ============================================================================
if len(df_centres) > 0:
    print("\n💾 Sauvegarde des données...")
    
    with pd.ExcelWriter("Donnees_fusionnees.xlsx") as writer:
        df_centres.to_excel(writer, sheet_name="Centres", index=False)
        df_interventions.to_excel(writer, sheet_name="Interventions", index=False)
    
    print("   ✅ Fichier 'Donnees_fusionnees.xlsx' créé")
    print("\n" + "="*60)
    print("✅ ÉTAPE 1 TERMINÉE")
    print("="*60)
else:
    print("\n❌ ERREUR: Aucune donnée à sauvegarder")