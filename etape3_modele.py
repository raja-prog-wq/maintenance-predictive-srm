# etape3_modele.py - CORRIGÉ
"""
ÉTAPE 3: MODÈLES COMPLETS
"""

import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    mean_absolute_error, mean_squared_error, r2_score
)
from sklearn.preprocessing import StandardScaler
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🤖 ÉTAPE 3: MODÈLES CLASSIFICATION + RÉGRESSION")
print("="*60)

# ============================================================================
# CHARGEMENT DES DONNÉES
# ============================================================================
print("\n📂 1. Chargement des données...")

if os.path.exists("Donnees_fusionnees.xlsx"):
    df = pd.read_excel("Donnees_fusionnees.xlsx", sheet_name="Centres")
else:
    print("   ❌ Fichier Donnees_fusionnees.xlsx non trouvé")
    exit()

print(f"   ✅ {len(df)} centres chargés")
print(f"   📋 Colonnes disponibles: {list(df.columns)}")

# ============================================================================
# PRÉPARATION DES FEATURES
# ============================================================================
print("\n🔧 2. Préparation des features...")

# Features pertinentes
features = ['Nb_interventions', 'Taux_correctif']

# Ajouter coût moyen par intervention
if 'Cout_total_Dhs' in df.columns and 'Nb_interventions' in df.columns:
    df['Cout_moyen_par_int'] = df['Cout_total_Dhs'] / (df['Nb_interventions'] + 1)
    features.append('Cout_moyen_par_int')
    print("   ✅ Feature ajoutée: Cout_moyen_par_int")

print(f"\n   📋 Features utilisées: {features}")

X = df[features].copy().fillna(0)

# Normalisation
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(f"   ✅ Normalisation effectuée sur {X_scaled.shape[1]} features")

# ============================================================================
# CIBLE
# ============================================================================
if 'Score_risque' not in df.columns:
    print("   ❌ Colonne 'Score_risque' non trouvée")
    exit()

y_reg = df['Score_risque'].values

def get_classe(score):
    if score >= 70:
        return 2  # Critique
    elif score >= 40:
        return 1  # Surveillance
    else:
        return 0  # Bon état

y_class = np.array([get_classe(s) for s in y_reg])
class_names = ['Bon état', 'Surveillance', 'Critique']

# CORRIGÉ: utiliser np.median au lieu de .median()
print(f"\n   🎯 Statistiques du score de risque:")
print(f"      - Min: {y_reg.min():.1f}")
print(f"      - Max: {y_reg.max():.1f}")
print(f"      - Moyenne: {y_reg.mean():.1f}")
print(f"      - Médiane: {np.median(y_reg):.1f}")

# ============================================================================
# DIVISION DES DONNÉES
# ============================================================================
print("\n📊 3. Division des données...")

# Pour la classification (avec stratification)
X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X_scaled, y_class, test_size=0.3, random_state=42, stratify=y_class
)

# Pour la régression
X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_scaled, y_reg, test_size=0.3, random_state=42
)

print(f"   ✅ Train: {len(X_train_c)} échantillons")
print(f"   ✅ Test: {len(X_test_c)} échantillons")

# ============================================================================
# MODÈLE 1: CLASSIFICATION
# ============================================================================
print("\n" + "="*40)
print("📊 MODÈLE 1: CLASSIFICATION")
print("="*40)

print(f"\n   🎯 Distribution des classes (train):")
print(f"      - Bon état (0): {(y_train_c == 0).sum()}")
print(f"      - Surveillance (1): {(y_train_c == 1).sum()}")
print(f"      - Critique (2): {(y_train_c == 2).sum()}")

# Entraînement
model_class = RandomForestClassifier(
    n_estimators=50,
    max_depth=3,
    min_samples_split=3,
    random_state=42,
    class_weight='balanced'
)
model_class.fit(X_train_c, y_train_c)

# Évaluation
y_pred_c = model_class.predict(X_test_c)
accuracy = accuracy_score(y_test_c, y_pred_c)

print(f"\n   📈 Performance sur test:")
print(f"   - Accuracy: {accuracy*100:.2f}%")

print(f"\n   📋 Rapport de classification:")
print(classification_report(y_test_c, y_pred_c, target_names=class_names))

# Matrice de confusion
cm = confusion_matrix(y_test_c, y_pred_c)
print(f"\n   📊 Matrice de confusion:")
print(f"                 Prédit")
print(f"              Bon   Surv  Crit")
print(f"   Réel Bon    [{cm[0][0]:2d}    {cm[0][1]:2d}    {cm[0][2]:2d}]")
print(f"        Surv   [{cm[1][0]:2d}    {cm[1][1]:2d}    {cm[1][2]:2d}]")
print(f"        Crit   [{cm[2][0]:2d}    {cm[2][1]:2d}    {cm[2][2]:2d}]")

# Validation croisée
cv_scores = cross_val_score(model_class, X_scaled, y_class, cv=min(5, len(X)), scoring='accuracy')
print(f"\n   🔄 Validation croisée (CV={min(5, len(X))}):")
print(f"   - Accuracy moyenne: {cv_scores.mean()*100:.2f}% (+/- {cv_scores.std()*100:.2f}%)")

# ============================================================================
# MODÈLE 2: RÉGRESSION
# ============================================================================
print("\n" + "="*40)
print("📈 MODÈLE 2: RÉGRESSION")
print("="*40)

# Entraînement
model_reg = RandomForestRegressor(
    n_estimators=50,
    max_depth=3,
    min_samples_split=3,
    random_state=42
)
model_reg.fit(X_train_r, y_train_r)

# Évaluation
y_pred_r = model_reg.predict(X_test_r)
mae = mean_absolute_error(y_test_r, y_pred_r)
rmse = np.sqrt(mean_squared_error(y_test_r, y_pred_r))
r2 = r2_score(y_test_r, y_pred_r)

print(f"\n   📈 Performance sur test:")
print(f"   - MAE: {mae:.1f} points")
print(f"   - RMSE: {rmse:.1f} points")
print(f"   - R²: {r2:.3f}")

# Validation croisée
cv_scores_reg = cross_val_score(model_reg, X_scaled, y_reg, cv=min(5, len(X)), scoring='r2')
print(f"\n   🔄 Validation croisée (CV={min(5, len(X))}):")
print(f"   - R² moyen: {cv_scores_reg.mean():.3f} (+/- {cv_scores_reg.std():.3f})")

# ============================================================================
# IMPORTANCE DES FEATURES
# ============================================================================
print("\n📊 4. Importance des features:")

importance_class = pd.DataFrame({
    'Feature': features,
    'Classification': model_class.feature_importances_
}).sort_values('Classification', ascending=False)

importance_reg = pd.DataFrame({
    'Feature': features,
    'Régression': model_reg.feature_importances_
}).sort_values('Régression', ascending=False)

print("\n   📋 Classification:")
for _, row in importance_class.iterrows():
    print(f"      - {row['Feature']}: {row['Classification']:.3f}")

print("\n   📋 Régression:")
for _, row in importance_reg.iterrows():
    print(f"      - {row['Feature']}: {row['Régression']:.3f}")

# ============================================================================
# COMPARAISON DES PRÉDICTIONS
# ============================================================================
print("\n📈 5. Comparaison des prédictions (test set):")

# Récupérer les centres du test set
test_indices = X_test_r.index if hasattr(X_test_r, 'index') else range(len(y_test_r))
centres_test = df.iloc[test_indices]['Centre'].values if 'Centre' in df.columns else [f"Centre_{i}" for i in range(len(y_test_r))]

comparaison = pd.DataFrame({
    'Centre': centres_test[:len(y_test_r)],
    'Score_réel': y_test_r,
    'Score_prédit': y_pred_r,
    'Erreur': np.abs(y_test_r - y_pred_r),
    'Classe_réelle': [class_names[int(c)] for c in y_test_c],
    'Classe_prédite': [class_names[int(c)] for c in y_pred_c]
}).sort_values('Erreur', ascending=False)

print(comparaison.head(10).to_string(index=False))

# ============================================================================
# SAUVEGARDE
# ============================================================================
print("\n💾 6. Sauvegarde des modèles...")

joblib.dump(model_class, 'random_forest_classifier.pkl')
joblib.dump(model_reg, 'random_forest_regressor.pkl')
joblib.dump(scaler, 'scaler.pkl')

print("   ✅ random_forest_classifier.pkl")
print("   ✅ random_forest_regressor.pkl")
print("   ✅ scaler.pkl")

# ============================================================================
# TEST AVEC EXEMPLES
# ============================================================================
print("\n🧪 7. Test avec exemples:")

exemples = [
    {"nom": "🟢 Centre peu actif", "Nb_interventions": 2, "Taux_correctif": 20, "Cout_moyen_par_int": 500},
    {"nom": "🟠 Centre actif", "Nb_interventions": 6, "Taux_correctif": 60, "Cout_moyen_par_int": 1500},
    {"nom": "🔴 Centre très actif", "Nb_interventions": 12, "Taux_correctif": 90, "Cout_moyen_par_int": 3000},
]

print("\n   " + "-"*70)

for ex in exemples:
    ex_df = pd.DataFrame([{f: ex.get(f, 0) for f in features}])
    ex_scaled = scaler.transform(ex_df.fillna(0))
    
    score = model_reg.predict(ex_scaled)[0]
    classe_id = model_class.predict(ex_scaled)[0]
    classe = class_names[classe_id]
    
    if score >= 70:
        niveau = "🔴 CRITIQUE"
    elif score >= 40:
        niveau = "🟠 SURVEILLANCE"
    else:
        niveau = "🟢 BON ÉTAT"
    
    print(f"   {ex['nom']}:")
    print(f"      - Interventions: {ex['Nb_interventions']}, Taux correctif: {ex['Taux_correctif']}%")
    print(f"      - Score prédit: {score:.1f}% ({niveau})")
    print(f"      - Classe: {classe}")
    print()

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "="*60)
print("✅ ÉTAPE 3 TERMINÉE")
print("="*60)

print(f"\n📊 RÉSUMÉ DES PERFORMANCES:")
print(f"   " + "-"*45)
print(f"   📋 CLASSIFICATION:")
print(f"      - Accuracy: {accuracy*100:.2f}%")
print(f"      - Validation croisée: {cv_scores.mean()*100:.2f}%")
print(f"   " + "-"*45)
print(f"   📈 RÉGRESSION:")
print(f"      - R²: {r2:.3f}")
print(f"      - MAE: {mae:.1f} points")
print(f"      - Validation croisée R²: {cv_scores_reg.mean():.3f}")