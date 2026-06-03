# etape_ajouter_centres_manquants.py
"""
Ajouter les centres manquants dans Donnees_fusionnees.xlsx
"""

import pandas as pd
import os

# Les centres à ajouter (ceux li ma3ndhomx données f Excel)
NOUVEAUX_CENTRES = [
    {"Centre": "BENI HASAN", "Cout_total_Dhs": 0, "Nb_interventions": 0, 
     "Nb_correctives": 0, "Taux_correctif": 0, "Score_risque": 5, 
     "Priorite": "Bon état", "Latitude": 32.2000, "Longitude": -6.5000},
    
    {"Centre": "IMLIL", "Cout_total_Dhs": 0, "Nb_interventions": 0, 
     "Nb_correctives": 0, "Taux_correctif": 0, "Score_risque": 5, 
     "Priorite": "Bon état", "Latitude": 31.7593, "Longitude": -7.0099},
    
    {"Centre": "TAMDA NPOUMERCID", "Cout_total_Dhs": 0, "Nb_interventions": 0, 
     "Nb_correctives": 0, "Taux_correctif": 0, "Score_risque": 5, 
     "Priorite": "Bon état", "Latitude": 32.0000, "Longitude": -6.5500},
    
    {"Centre": "DR BENI AYAT", "Cout_total_Dhs": 0, "Nb_interventions": 0, 
     "Nb_correctives": 0, "Taux_correctif": 0, "Score_risque": 5, 
     "Priorite": "Bon état", "Latitude": 32.1800, "Longitude": -6.4200},
    
    {"Centre": "AFOURER", "Cout_total_Dhs": 0, "Nb_interventions": 0, 
     "Nb_correctives": 0, "Taux_correctif": 0, "Score_risque": 5, 
     "Priorite": "Bon état", "Latitude": 32.2000, "Longitude": -6.4167},
]

# Lire le fichier existant
if os.path.exists("Donnees_fusionnees.xlsx"):
    df_centres = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Centres")
    df_interventions = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Interventions")
    
    print(f"📊 Centres avant: {len(df_centres)}")
    print("   Liste actuelle:", sorted(df_centres['Centre'].tolist()))
    
    # Vérifier lesquels sont déjà présents
    centres_existants = set(df_centres['Centre'].tolist())
    centres_a_ajouter = []
    
    for centre in NOUVEAUX_CENTRES:
        if centre["Centre"] not in centres_existants:
            centres_a_ajouter.append(centre)
            print(f"   ➕ À ajouter: {centre['Centre']}")
        else:
            print(f"   ⏭️ Déjà présent: {centre['Centre']}")
    
    # Ajouter les nouveaux centres
    if centres_a_ajouter:
        df_nouveaux = pd.DataFrame(centres_a_ajouter)
        df_centres = pd.concat([df_centres, df_nouveaux], ignore_index=True)
        df_centres = df_centres.sort_values('Centre').reset_index(drop=True)
        
        # Sauvegarder
        with pd.ExcelWriter("Donnees_fusionnees.xlsx") as writer:
            df_centres.to_excel(writer, sheet_name="Centres", index=False)
            df_interventions.to_excel(writer, sheet_name="Interventions", index=False)
        
        print(f"\n✅ {len(centres_a_ajouter)} centres ajoutés")
        print(f"📊 Centres après: {len(df_centres)}")
        print("\n📋 LISTE FINALE DES CENTRES:")
        for c in sorted(df_centres['Centre']):
            print(f"   - {c}")
    else:
        print("\n⚠️ Aucun centre à ajouter (tous déjà présents)")
else:
    print("❌ Fichier Donnees_fusionnees.xlsx non trouvé")