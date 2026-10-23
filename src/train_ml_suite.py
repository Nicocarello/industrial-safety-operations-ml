"""
=============================================================================
TECHNOSTAMP INDUSTRIES - ADVANCED MACHINE LEARNING SUITE
=============================================================================
Author: Decision Science & Machine Learning Showcase
Focus: Industrial Workforce Analytics, Safety Prediction & Flight Risk Modeling
Models Implemented:
  1. Workplace Safety Risk Classifier (Accident Early Warning Engine)
  2. Employee Flight Risk / Voluntary Churn Predictor (Retention ML)
  3. Operational Scrap Risk Predictor (Predictive Quality & Waste Prevention)
=============================================================================
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, OneHotEncoder
from sklearn.metrics import (
    roc_auc_score, average_precision_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report, roc_curve, precision_recall_curve
)
from lightgbm import LGBMClassifier, LGBMRegressor

def build_ml_suite():
    print("="*75)
    print("INICIANDO SUITE DE MACHINE LEARNING APLICADO - TECHNOSTAMP INDUSTRIES")
    print("="*75)

    os.makedirs('assets/models', exist_ok=True)
    os.makedirs('assets/figures', exist_ok=True)

    # 1. Cargar datasets
    df_emp = pd.read_csv('data/empleados_mensual.csv', encoding='latin-1')
    df_eve = pd.read_csv('data/eventos_rrhh.csv', encoding='latin-1')
    df_cap = pd.read_csv('data/capacitaciones.csv', encoding='latin-1')

    # Limpieza estándar
    df_cap['categoria_training'] = df_cap['categoria_training'].replace({'Técnica': 'Técnico'})
    df_emp['fecha_snapshot'] = pd.to_datetime(df_emp['mes_snapshot'])
    df_emp = df_emp.sort_values(['empleado_id', 'fecha_snapshot']).reset_index(drop=True)

    # Reconstruir manager_id
    mgr_map = (
        df_emp.dropna(subset=['manager_id', 'manager_nombre'])
        .drop_duplicates('manager_nombre')
        .set_index('manager_nombre')['manager_id']
        .to_dict()
    )
    df_emp['manager_id'] = df_emp['manager_id'].fillna(df_emp['manager_nombre'].map(mgr_map)).fillna(0)

    # =========================================================================
    # FEATURE ENGINEERING GLOBAL
    # =========================================================================
    print("\n[FASE 1] Ingeniería de Atributos Temporales y de Negocio...")
    
    # 1.1 Features de capacitaciones
    seg_cap = df_cap[(df_cap['categoria_training'] == 'Seguridad') & (df_cap['completado'] == True)]
    seg_hours = seg_cap.groupby('empleado_id')['duracion_horas'].sum().rename('total_hrs_seguridad')
    tec_cap = df_cap[(df_cap['categoria_training'] == 'Técnico') & (df_cap['completado'] == True)]
    tec_hours = tec_cap.groupby('empleado_id')['duracion_horas'].sum().rename('total_hrs_tecnicas')
    
    df_emp = df_emp.merge(seg_hours, on='empleado_id', how='left')
    df_emp = df_emp.merge(tec_hours, on='empleado_id', how='left')
    df_emp['total_hrs_seguridad'] = df_emp['total_hrs_seguridad'].fillna(0)
    df_emp['total_hrs_tecnicas'] = df_emp['total_hrs_tecnicas'].fillna(0)

    # 1.2 Rolling features por empleado
    df_emp['he_roll_3m'] = df_emp.groupby('empleado_id')['horas_extra'].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df_emp['he_roll_6m'] = df_emp.groupby('empleado_id')['horas_extra'].transform(lambda x: x.rolling(6, min_periods=1).mean())
    df_emp['ausencias_roll_3m'] = df_emp.groupby('empleado_id')['dias_ausente'].transform(lambda x: x.rolling(3, min_periods=1).sum())
    
    # Ratios de fatiga y sobrecarga
    df_emp['ratio_sobrecarga'] = df_emp['horas_extra'] / (df_emp['horas_trabajadas'] + 1e-4)
    df_emp['indice_fatiga_sin_seguridad'] = df_emp['horas_extra'] / (df_emp['total_hrs_seguridad'] + 1.0)
    df_emp['umbral_he_critico_20h'] = (df_emp['horas_extra'] > 20).astype(int)

    # 1.3 Efecto Manager: Tasa histórica de rotación del supervisor
    mgr_stats = df_emp.groupby('manager_nombre').agg(
        mgr_total=('empleado_id', 'count'),
        mgr_salidas=('activo', lambda x: (~x).sum())
    )
    mgr_stats['mgr_turnover_rate'] = (mgr_stats['mgr_salidas'] / mgr_stats['mgr_total']).fillna(0)
    df_emp = df_emp.merge(mgr_stats['mgr_turnover_rate'], on='manager_nombre', how='left')
    df_emp['mgr_turnover_rate'] = df_emp['mgr_turnover_rate'].fillna(0)

    # 1.4 Benchmark salarial por nivel jerárquico
    sal_mean = df_emp.groupby(['nivel_jerarquico', 'categoria_collar'])['salario_base_mensual'].transform('mean')
    df_emp['ratio_salario_vs_promedio'] = df_emp['salario_base_mensual'] / (sal_mean + 1e-4)

    results_summary = {}

    # =========================================================================
    # MODELO 1: SAFETY RISK CLASSIFIER (Accident Early Warning Engine)
    # =========================================================================
    print("\n" + "="*70)
    print("MODELO 1: SAFETY RISK CLASSIFIER (Predicción de Accidentes en Planta)")
    print("="*70)

    blue_df = df_emp[df_emp['categoria_collar'] == 'Blue'].copy()
    blue_df['target_accidente'] = (blue_df['incidentes_seguridad_count'] > 0).astype(int)

    num_safety = [
        'edad', 'antiguedad_meses', 'rating_performance', 'horas_extra',
        'he_roll_3m', 'he_roll_6m', 'ausencias_roll_3m', 'ratio_sobrecarga',
        'indice_fatiga_sin_seguridad', 'total_hrs_seguridad', 'umbral_he_critico_20h',
        'duracion_turno_horas'
    ]
    cat_safety = ['area', 'subarea', 'turno_trabajo', 'genero']

    X_s = blue_df[num_safety + cat_safety]
    y_s = blue_df['target_accidente']

    X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(
        X_s, y_s, test_size=0.20, stratify=y_s, random_state=42
    )

    prep_s = ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('scl', RobustScaler())]), num_safety),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))]), cat_safety)
    ])

    clf_safety = Pipeline([
        ('prep', prep_s),
        ('model', LGBMClassifier(
            class_weight='balanced',
            max_depth=4,
            num_leaves=15,
            learning_rate=0.03,
            n_estimators=180,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbose=-1
        ))
    ])

    clf_safety.fit(X_train_s, y_train_s)
    probs_s = clf_safety.predict_proba(X_test_s)[:, 1]
    auc_s = roc_auc_score(y_test_s, probs_s)
    prauc_s = average_precision_score(y_test_s, probs_s)

    # Top 20% Lift
    top20_cut_s = np.percentile(probs_s, 80)
    top20_recall_s = y_test_s[probs_s >= top20_cut_s].sum() / y_test_s.sum() * 100

    print(f"  * ROC-AUC: {auc_s:.4f} | PR-AUC: {prauc_s:.4f}")
    print(f"  * Recall en Top 20% de Mayor Riesgo: {top20_recall_s:.1f}% de todos los accidentes")

    # Extraer Feature Importances
    feat_names_s = num_safety + list(clf_safety.named_steps['prep'].named_transformers_['cat'].named_steps['ohe'].get_feature_names_out(cat_safety))
    importances_s = clf_safety.named_steps['model'].feature_importances_
    feat_imp_s = sorted(zip(feat_names_s, importances_s), key=lambda x: x[1], reverse=True)[:6]
    print("  * Top 6 Drivers de Riesgo de Accidente:")
    for fn, imp in feat_imp_s:
        print(f"    - {fn}: {imp}")

    joblib.dump(clf_safety, 'assets/models/model_safety_risk_lgbm.pkl')

    results_summary['safety_model'] = {
        "name": "Workplace Safety Early Warning Classifier",
        "algorithm": "LightGBM Classifier (Balanced)",
        "target": "incidentes_seguridad_count > 0",
        "roc_auc": round(float(auc_s), 4),
        "pr_auc": round(float(prauc_s), 4),
        "top20_recall_pct": round(float(top20_recall_s), 1),
        "top_features": [f[0] for f in feat_imp_s]
    }

    # =========================================================================
    # MODELO 2: VOLUNTARY FLIGHT RISK (Predicción de Renuncia Voluntaria)
    # =========================================================================
    print("\n" + "="*70)
    print("MODELO 2: FLIGHT RISK CLASSIFIER (Predicción de Renuncia Voluntaria)")
    print("="*70)

    # Creamos target: renunciará en los próximos 1 o 2 meses
    # Marcamos a los empleados que renunciaron voluntariamente en su último snapshot
    df_emp['target_renuncia_proxima'] = 0
    # Obtenemos empleados con renuncia voluntaria
    renunciantes = df_emp[df_emp['motivo_salida'] == 'Renuncia voluntaria']['empleado_id'].unique()

    for emp_id in renunciantes:
        emp_records = df_emp[df_emp['empleado_id'] == emp_id].sort_values('fecha_snapshot')
        if len(emp_records) >= 1:
            # Los últimos 2 meses antes de la salida reciben target 1
            idx_renuncia = emp_records.index[-2:]
            df_emp.loc[idx_renuncia, 'target_renuncia_proxima'] = 1

    # Entrenar sobre empleados activos o durante su vida activa
    active_pool = df_emp[df_emp['activo'] == True].copy()
    
    num_churn = [
        'edad', 'antiguedad_meses', 'rating_performance', 'horas_extra',
        'he_roll_3m', 'ausencias_roll_3m', 'ratio_sobrecarga',
        'ratio_salario_vs_promedio', 'mgr_turnover_rate', 'salario_base_mensual'
    ]
    cat_churn = ['area', 'nivel_jerarquico', 'genero', 'turno_trabajo']

    X_c = active_pool[num_churn + cat_churn]
    y_c = active_pool['target_renuncia_proxima']

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X_c, y_c, test_size=0.20, stratify=y_c, random_state=42
    )

    prep_c = ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('scl', RobustScaler())]), num_churn),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))]), cat_churn)
    ])

    clf_churn = Pipeline([
        ('prep', prep_c),
        ('model', LGBMClassifier(
            class_weight='balanced',
            max_depth=4,
            num_leaves=15,
            learning_rate=0.03,
            n_estimators=160,
            subsample=0.8,
            random_state=42,
            verbose=-1
        ))
    ])

    clf_churn.fit(X_train_c, y_train_c)
    probs_c = clf_churn.predict_proba(X_test_c)[:, 1]
    auc_c = roc_auc_score(y_test_c, probs_c)
    prauc_c = average_precision_score(y_test_c, probs_c)

    top20_cut_c = np.percentile(probs_c, 80)
    top20_recall_c = y_test_c[probs_c >= top20_cut_c].sum() / y_test_c.sum() * 100

    print(f"  * ROC-AUC: {auc_c:.4f} | PR-AUC: {prauc_c:.4f}")
    print(f"  * Recall en Top 20% de Mayor Riesgo de Fuga: {top20_recall_c:.1f}% de renuncias capturadas")

    feat_names_c = num_churn + list(clf_churn.named_steps['prep'].named_transformers_['cat'].named_steps['ohe'].get_feature_names_out(cat_churn))
    importances_c = clf_churn.named_steps['model'].feature_importances_
    feat_imp_c = sorted(zip(feat_names_c, importances_c), key=lambda x: x[1], reverse=True)[:6]
    print("  * Top 6 Drivers de Fuga de Talento:")
    for fn, imp in feat_imp_c:
        print(f"    - {fn}: {imp}")

    joblib.dump(clf_churn, 'assets/models/model_flight_risk_lgbm.pkl')

    results_summary['flight_risk_model'] = {
        "name": "Voluntary Churn / Flight Risk Predictor",
        "algorithm": "LightGBM Classifier (Balanced)",
        "target": "Renuncia voluntaria en ventana de 60 días",
        "roc_auc": round(float(auc_c), 4),
        "pr_auc": round(float(prauc_c), 4),
        "top20_recall_pct": round(float(top20_recall_c), 1),
        "top_features": [f[0] for f in feat_imp_c]
    }

    # =========================================================================
    # MODELO 3: HIGH SCRAP PREDICTOR (Predicción de Desperdicio y Calidad)
    # =========================================================================
    print("\n" + "="*70)
    print("MODELO 3: PREDICTIVE QUALITY (Alerta Temprana de Scrap Excesivo > 3%)")
    print("="*70)

    scrap_df = df_emp.dropna(subset=['tasa_scrap_porcentaje']).copy()
    scrap_df['target_alto_scrap'] = (scrap_df['tasa_scrap_porcentaje'] > 3.0).astype(int)

    num_scrap = [
        'antiguedad_meses', 'horas_extra', 'he_roll_3m', 'ratio_sobrecarga',
        'unidades_producidas', 'eficiencia_vs_target', 'total_hrs_tecnicas',
        'duracion_turno_horas'
    ]
    cat_scrap = ['turno_trabajo', 'area', 'subarea']

    X_q = scrap_df[num_scrap + cat_scrap]
    y_q = scrap_df['target_alto_scrap']

    X_train_q, X_test_q, y_train_q, y_test_q = train_test_split(
        X_q, y_q, test_size=0.20, stratify=y_q, random_state=42
    )

    prep_q = ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('scl', RobustScaler())]), num_scrap),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False))]), cat_scrap)
    ])

    clf_scrap = Pipeline([
        ('prep', prep_q),
        ('model', LGBMClassifier(
            class_weight='balanced',
            max_depth=4,
            num_leaves=15,
            learning_rate=0.04,
            n_estimators=150,
            random_state=42,
            verbose=-1
        ))
    ])

    clf_scrap.fit(X_train_q, y_train_q)
    probs_q = clf_scrap.predict_proba(X_test_q)[:, 1]
    auc_q = roc_auc_score(y_test_q, probs_q)
    prauc_q = average_precision_score(y_test_q, probs_q)

    top20_cut_q = np.percentile(probs_q, 80)
    top20_recall_q = y_test_q[probs_q >= top20_cut_q].sum() / y_test_q.sum() * 100

    print(f"  * ROC-AUC: {auc_q:.4f} | PR-AUC: {prauc_q:.4f}")
    print(f"  * Recall en Top 20% de Mayor Riesgo de Scrap: {top20_recall_q:.1f}%")

    feat_names_q = num_scrap + list(clf_scrap.named_steps['prep'].named_transformers_['cat'].named_steps['ohe'].get_feature_names_out(cat_scrap))
    importances_q = clf_scrap.named_steps['model'].feature_importances_
    feat_imp_q = sorted(zip(feat_names_q, importances_q), key=lambda x: x[1], reverse=True)[:6]
    print("  * Top 6 Drivers de Alto Scrap:")
    for fn, imp in feat_imp_q:
        print(f"    - {fn}: {imp}")

    joblib.dump(clf_scrap, 'assets/models/model_high_scrap_lgbm.pkl')

    results_summary['scrap_model'] = {
        "name": "Operational Scrap Risk Predictor (>3.0%)",
        "algorithm": "LightGBM Classifier (Balanced)",
        "target": "tasa_scrap_porcentaje > 3.0%",
        "roc_auc": round(float(auc_q), 4),
        "pr_auc": round(float(prauc_q), 4),
        "top20_recall_pct": round(float(top20_recall_q), 1),
        "top_features": [f[0] for f in feat_imp_q]
    }

    # Guardar resumen de modelos
    with open('assets/ml_models_summary.json', 'w', encoding='utf-8') as f:
        json.dump(results_summary, f, indent=4)

    print("\n" + "="*70)
    print("SUITE DE MACHINE LEARNING ENTRENADA Y GUARDADA CON ÉXITO")
    print("Modelos serializados en assets/models/:")
    print("  1. model_safety_risk_lgbm.pkl")
    print("  2. model_flight_risk_lgbm.pkl")
    print("  3. model_high_scrap_lgbm.pkl")
    print("Métricas consolidadas en assets/ml_models_summary.json")
    print("="*70)

if __name__ == '__main__':
    build_ml_suite()
