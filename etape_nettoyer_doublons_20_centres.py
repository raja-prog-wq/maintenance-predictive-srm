# etape_nettoyer_doublons_20_centres.py
"""
Nettoyer les doublons et garder uniquement les 20 centres standards
"""

import pandas as pd
import os

# Les 20 centres standards (d'après attachement type.xlsx)
CENTRES_STANDARDS_20 = [
    "AIT ATTAB",
    "AIT MHAMED",
    "AZILAL",
    "BENI AYAT",
    "BENI HASAN",
    "BZOU",
    "DEMNATE",
    "DR BENI AYAT",
    "FOUM JEMAA",
    "IMDAHEN",
    "IMLIL",
    "OUAOUIZEGHT",
    "OUAOULA",
    "OUZOUD",
    "RFALA",
    "TAMDA NPOUMERCID",
    "TANANT",
    "TIFNI",
    "TISKI",
    "AFOURER"
]

# Mapping des noms (variantes → nom standard)
MAPPING_STANDARD = {
    # AIT ATTAB
    "AIT ATTAB": "AIT ATTAB", "ait attab": "AIT ATTAB", "ait attb": "AIT ATTAB", "aitattb": "AIT ATTAB",
    
    # AIT MHAMED
    "AIT MHAMED": "AIT MHAMED", "ait mhammed": "AIT MHAMED", "ait M'hamed": "AIT MHAMED",
    
    # AZILAL
    "AZILAL": "AZILAL", "Azilal": "AZILAL", "azilal": "AZILAL",
    
    # BENI AYAT
    "BENI AYAT": "BENI AYAT", "beni ayat": "BENI AYAT", "beni ayyat": "BENI AYAT", "béni Ayat": "BENI AYAT",
    
    # BENI HASAN
    "BENI HASAN": "BENI HASAN", "beni hasan": "BENI HASAN",
    
    # BZOU
    "BZOU": "BZOU", "Bzou": "BZOU", "bzou": "BZOU",
    
    # DEMNATE
    "DEMNATE": "DEMNATE", "Demnate": "DEMNATE", "demnat": "DEMNATE",
    
    # DR BENI AYAT
    "DR BENI AYAT": "DR BENI AYAT", "Dr Beni Ayat": "DR BENI AYAT",
    
    # FOUM JEMAA
    "FOUM JEMAA": "FOUM JEMAA", "foum jemaa": "FOUM JEMAA", "Foum Jemaâ": "FOUM JEMAA", "fom jemaa": "FOUM JEMAA", "FOM JEMAA": "FOUM JEMAA",
    
    # IMDAHEN
    "IMDAHEN": "IMDAHEN", "imdahen": "IMDAHEN", "Imedahen": "IMDAHEN",
    
    # IMLIL
    "IMLIL": "IMLIL", "Imlil": "IMLIL", "imlil": "IMLIL",
    
    # OUAOUIZEGHT
    "OUAOUIZEGHT": "OUAOUIZEGHT", "Ouaouizeght": "OUAOUIZEGHT", "ouaouizeght": "OUAOUIZEGHT",
    
    # OUAOULA
    "OUAOULA": "OUAOULA", "Ouaoula": "OUAOULA", "ouaoula": "OUAOULA",
    
    # OUZOUD
    "OUZOUD": "OUZOUD", "Ouzoud": "OUZOUD", "ouzoud": "OUZOUD", "OZOUD": "OUZOUD", "ozoud": "OUZOUD",
    
    # RFALA
    "RFALA": "RFALA", "Rfala": "RFALA", "refala": "RFALA", "REFALA": "RFALA",
    
    # TAMDA NPOUMERCID
    "TAMDA NPOUMERCID": "TAMDA NPOUMERCID", "Tamda Npoumercid": "TAMDA NPOUMERCID",
    
    # TANANT
    "TANANT": "TANANT", "Tanant": "TANANT", "tanant": "TANANT",
    
    # TIFNI
    "TIFNI": "TIFNI", "Tifni": "TIFNI", "tifni": "TIFNI",
    
    # TISKI
    "TISKI": "TISKI", "tiski": "TISKI", "TISQUI": "TISKI", "tisqui": "TISKI",
    
    # AFOURER
    "AFOURER": "AFOURER", "Afourer": "AFOURER", "afourer": "AFOURER",
}

# Coordonnées GPS pour les 20 centres
GPS_20_CENTRES = {
    "AIT ATTAB": (31.9833, -6.3500),
    "AIT MHAMED": (31.9500, -6.5000),
    "AZILAL": (31.9667, -6.5667),
    "BENI AYAT": (32.2000, -6.4167),
    "BENI HASAN": (32.2000, -6.5000),
    "BZOU": (32.1000, -6.5500),
    "DEMNATE": (31.8500, -7.0167),
    "DR BENI AYAT": (32.1800, -6.4200),
    "FOUM JEMAA": (32.1167, -6.4167),
    "IMDAHEN": (32.0833, -6.4500),
    "IMLIL": (31.7593, -7.0099),
    "OUAOUIZEGHT": (32.1667, -6.4000),
    "OUAOULA": (32.0500, -6.4500),
    "OUZOUD": (32.0167, -6.7167),
    "RFALA": (32.2500, -6.2500),
    "TAMDA NPOUMERCID": (32.0000, -6.5500),
    "TANANT": (31.7833, -6.9167),
    "TIFNI": (31.9000, -6.5000),
    "TISKI": (31.8500, -6.5000),
    "AFOURER": (32.2000, -6.4167),
}

def standardiser_centre(nom):
    if pd.isna(nom):
        return nom
    nom_str = str(nom).strip()
    return MAPPING_STANDARD.get(nom_str, nom_str)

if os.path.exists("Donnees_fusionnees.xlsx"):
    # Lire les données
    df_centres = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Centres")
    df_interventions = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Interventions")
    
    print(f"📊 Centres avant nettoyage: {len(df_centres)}")
    
    # Standardiser les noms
    df_centres['Centre'] = df_centres['Centre'].apply(standardiser_centre)
    
    # Garder uniquement les centres standards (20)
    df_centres = df_centres[df_centres['Centre'].isin(CENTRES_STANDARDS_20)]
    
    # Grouper pour fusionner les doublons
    df_centres = df_centres.groupby('Centre', as_index=False).agg({
        'Cout_total_Dhs': 'sum',
        'Nb_interventions': 'sum',
        'Nb_correctives': 'sum',
        'Taux_correctif': 'mean',
        'Score_risque': 'mean',
        'Priorite': lambda x: x.mode()[0] if len(x) > 0 else 'Bon état'
    })
    
    # Ajouter les coordonnées GPS
    df_centres['Latitude'] = df_centres['Centre'].apply(lambda x: GPS_20_CENTRES.get(x, (32.0, -6.5))[0])
    df_centres['Longitude'] = df_centres['Centre'].apply(lambda x: GPS_20_CENTRES.get(x, (32.0, -6.5))[1])
    
    # Ajouter les centres manquants (ceux avec 0 interventions)
    centres_presents = set(df_centres['Centre'].tolist())
    centres_manquants = [c for c in CENTRES_STANDARDS_20 if c not in centres_presents]
    
    if centres_manquants:
        print(f"   ➕ Centres à ajouter (0 intervention): {centres_manquants}")
        for centre in centres_manquants:
            nouveau_centre = pd.DataFrame([{
                'Centre': centre,
                'Cout_total_Dhs': 0,
                'Nb_interventions': 0,
                'Nb_correctives': 0,
                'Taux_correctif': 0,
                'Score_risque': 5,
                'Priorite': 'Bon état',
                'Latitude': GPS_20_CENTRES.get(centre, (32.0, -6.5))[0],
                'Longitude': GPS_20_CENTRES.get(centre, (32.0, -6.5))[1]
            }])
            df_centres = pd.concat([df_centres, nouveau_centre], ignore_index=True)
    
    # Trier
    df_centres = df_centres.sort_values('Centre').reset_index(drop=True)
    
    # Sauvegarder
    with pd.ExcelWriter("Donnees_fusionnees.xlsx") as writer:
        df_centres.to_excel(writer, sheet_name="Centres", index=False)
        df_interventions.to_excel(writer, sheet_name="Interventions", index=False)
    
    print(f"\n✅ Centres après nettoyage: {len(df_centres)}")
    print("\n📋 LISTE FINALE (20 CENTRES):")
    for c in df_centres['Centre']:
        nb_int = df_centres[df_centres['Centre'] == c]['Nb_interventions'].values[0]
        print(f"   - {c}: {int(nb_int)} interventions")
else:
    print("❌ Fichier Donnees_fusionnees.xlsx non trouvé")