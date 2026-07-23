# -*- coding: utf-8 -*-
"""
Makine Öğrenmesi Dönem Projesi
Ad Soyad : Hatice İKKAN
Öğrenci No: Y255012009
"""

import os
import glob
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

# 0) AYARLAR 
# Dünya Bankası dosyası
WORLD_BANK_FILE = os.path.join("Data", "dunyabankasi.csv")

# Kaggle World Happiness Report yıllık csv'leri
HAPPINESS_FILES_GLOB = os.path.join("Data", "[0-9][0-9][0-9][0-9].csv")

# Çıktı birleştirilmiş veri seti
OUTPUT_MERGED_CSV = "proje_veri_seti.csv"

# Çıktı klasörü (grafikler vs.)
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Kullanılacak yıllar
YEAR_START = 2015
YEAR_END = 2022

# Sınıflandırma hedefi için sınırlar (Life expectancy)
LIFE_BINS = [0, 70, 78, 100]
LIFE_LABELS = ["Düşük", "Orta", "Yüksek"]

# 1) YARDIMCI FONKSİYONLAR

def _to_numeric_fix(series: pd.Series) -> pd.Series:
    """Virgül/nokta sorunlarını düzeltip numeric'e çevirir."""
    if series.dtype == "object":
        series = series.astype(str).str.replace(",", ".", regex=False)
    return pd.to_numeric(series, errors="coerce")


def _print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

# 2) VERİ BİRLEŞTİRME

def merge_verileri(
    world_bank_file: str = WORLD_BANK_FILE,
    output_csv: str = OUTPUT_MERGED_CSV,
    year_start: int = YEAR_START,
    year_end: int = YEAR_END
) -> pd.DataFrame:
    """
    Dünya Bankası Life Expectancy + Kaggle World Happiness Report (2015-2022) birleştirme.
    Çıktı: proje_veri_seti.csv
    """
    _print_section("1) VERİ BİRLEŞTİRME BAŞLIYOR")

    # --- 1. Dünya Bankası verisi ---
    print(f"📥 Dünya Bankası verisi okunuyor: {world_bank_file}")
    if not os.path.exists(world_bank_file):
        # Data klasöründe bulamazsa hata verecek
        raise FileNotFoundError(f"World Bank dosyası 'Data' klasöründe bulunamadı: {world_bank_file}")

    df_wb = pd.read_csv(world_bank_file, skiprows=4)

    cols_to_keep = ["Country Name"] + [str(y) for y in range(year_start, year_end + 1)]
    missing_cols = [c for c in cols_to_keep if c not in df_wb.columns]
    if missing_cols:
        raise ValueError(
            "Dünya Bankası dosyasında beklenen kolon(lar) yok: "
            + ", ".join(missing_cols)
        )

    df_wb = df_wb[cols_to_keep]
    df_wb_melted = df_wb.melt(
        id_vars=["Country Name"],
        var_name="Year",
        value_name="Yasam_Beklentisi"
    )
    df_wb_melted["Year"] = df_wb_melted["Year"].astype(int)
    df_wb_melted.rename(columns={"Country Name": "Country"}, inplace=True)

    # Ülke adı standardizasyonu (mantıksal eşleme)
    wb_mapping = {
        "Bahamas, The": "Bahamas",
        "Brunei Darussalam": "Brunei",
        "Cabo Verde": "Cape Verde",
        "Czechia": "Czech Republic",
        "Egypt, Arab Rep.": "Egypt",
        "Gambia, The": "Gambia",
        "Hong Kong SAR, China": "Hong Kong",
        "Iran, Islamic Rep.": "Iran",
        "Korea, Rep.": "South Korea",
        "Kyrgyz Republic": "Kyrgyzstan",
        "Lao PDR": "Laos",
        "Macao SAR, China": "Macau",
        "Micronesia, Fed. Sts.": "Micronesia",
        "North Macedonia": "Macedonia",
        "Russian Federation": "Russia",
        "Slovak Republic": "Slovakia",
        "Syrian Arab Republic": "Syria",
        "Turkiye": "Turkey",
        "Türkiye": "Turkey",
        "Congo, Dem. Rep.": "Congo (Kinshasa)",
        "Congo, Rep.": "Congo (Brazzaville)",
        "Cote d'Ivoire": "Ivory Coast",
        "Venezuela, RB": "Venezuela",
        "Viet Nam": "Vietnam",
        "Yemen, Rep.": "Yemen",
        "United States": "United States of America",
        "United States of America": "United States of America",
        "USA": "United States of America",
    }
    df_wb_melted["Country"] = df_wb_melted["Country"].replace(wb_mapping)
    print("✅ Dünya Bankası verisi hazır. Satır:", len(df_wb_melted))

    # --- 2. Mutluluk raporları (2015-2022) ---
    print("📥 World Happiness yıllık dosyaları okunuyor...")
    all_happiness_data = []
    for year in range(year_start, year_end + 1):
        filename = os.path.join("Data", f"{year}.csv")
        
        if not os.path.exists(filename):
            print(f"⚠️ Dosya yok, atlandı: {filename}")
            continue

        df = pd.read_csv(filename)

        # Farklı yıllarda ülke kolonu farklı isimlerde olabiliyor
        if "Country or region" in df.columns:
            df.rename(columns={"Country or region": "Country"}, inplace=True)
        elif "Country name" in df.columns:
            df.rename(columns={"Country name": "Country"}, inplace=True)

        # Kolon isimlerini yakalama
        score_col = [c for c in df.columns if "score" in c.lower() and "error" not in c.lower() and "rank" not in c.lower()]
        if score_col:
            df.rename(columns={score_col[0]: "Mutluluk_Skoru"}, inplace=True)

        gdp_col = [c for c in df.columns if "gdp" in c.lower()]
        if gdp_col:
            df.rename(columns={gdp_col[0]: "Kisi_Basi_GSYH"}, inplace=True)

        social_col = [c for c in df.columns if "social" in c.lower() or "family" in c.lower()]
        if social_col:
            df.rename(columns={social_col[0]: "Sosyal_Destek"}, inplace=True)

        free_col = [c for c in df.columns if "freedom" in c.lower()]
        if free_col:
            df.rename(columns={free_col[0]: "Ozgunluk"}, inplace=True)

        gen_col = [c for c in df.columns if "generosity" in c.lower()]
        if gen_col:
            df.rename(columns={gen_col[0]: "Comertlik"}, inplace=True)

        corr_col = [c for c in df.columns if "corruption" in c.lower() or "trust" in c.lower()]
        if corr_col:
            df.rename(columns={corr_col[0]: "Yolsuzluk_Algisi"}, inplace=True)

        rank_col = [c for c in df.columns if "rank" in c.lower()]
        if rank_col:
            df.rename(columns={rank_col[0]: "Mutluluk_Sirasi"}, inplace=True)

        # Mutluluk verisinde de isim düzeltmesi
        if "Country" in df.columns:
            df["Country"] = df["Country"].replace({
                "United States": "United States of America",
                "Taiwan Province of China": "Taiwan",
                "North Cyprus": "Cyprus",
            })

        wanted_cols = [
            "Country", "Mutluluk_Sirasi", "Mutluluk_Skoru", "Kisi_Basi_GSYH",
            "Sosyal_Destek", "Ozgunluk", "Comertlik", "Yolsuzluk_Algisi"
        ]
        existing_cols = [c for c in wanted_cols if c in df.columns]
        df = df[existing_cols].copy()
        df["Year"] = year
        all_happiness_data.append(df)

    if not all_happiness_data:
        raise FileNotFoundError("Hiç mutluluk dosyası bulunamadı. Data klasöründe 2015.csv ... 2022.csv dosyaları olmalı.")

    df_happiness = pd.concat(all_happiness_data, ignore_index=True)
    print("✅ Mutluluk verisi hazır. Satır:", len(df_happiness))

    # --- 3. Birleştirme (Inner Join) ---
    print("🔗 Country + Year üzerinden INNER JOIN yapılıyor...")
    final_df = pd.merge(df_happiness, df_wb_melted, on=["Country", "Year"], how="inner")

    # Eksik veri stratejisi:
    # Temel kolonlar yoksa satırı at; diğerlerini ortalama ile doldur.
    before = len(final_df)
    final_df.dropna(subset=["Yasam_Beklentisi", "Mutluluk_Skoru", "Kisi_Basi_GSYH"], inplace=True)
    after_drop = len(final_df)

    numeric_cols = final_df.select_dtypes(include=[np.number]).columns
    final_df[numeric_cols] = final_df[numeric_cols].fillna(final_df[numeric_cols].mean())

    print(f"🧹 Eksik veri: {before-after_drop} satır kritik kolonlar nedeniyle silindi.")
    print(f"📊 Birleşmiş veri: {len(final_df)} satır, {final_df.shape[1]} sütun")

    # Çıktı
    final_df.to_csv(output_csv, index=False)
    print(f"✅ DOSYA KAYDEDİLDİ: {output_csv}")

    return final_df

# 3) EDA + ÖN İŞLEME GÖRSELLERİ 

def eda_analiz(input_csv: str = OUTPUT_MERGED_CSV):
    """
    EDA: özet istatistik, korelasyon matrisi, histogramlar.
    """
    _print_section("2) EDA (Keşifsel Veri Analizi)")

    df = pd.read_csv(input_csv)

    numeric_cols = ["Mutluluk_Skoru", "Kisi_Basi_GSYH", "Sosyal_Destek",
                    "Ozgunluk", "Comertlik", "Yolsuzluk_Algisi", "Yasam_Beklentisi"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = _to_numeric_fix(df[col])

    df_numeric = df[[c for c in numeric_cols if c in df.columns]].copy()

    print("--- VERİ SETİ İSTATİSTİKLERİ (describe) ---")
    print(df_numeric.describe().T)

    # Korelasyon matrisi
    corr = df_numeric.corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    # Seaborn ile çizim
    sns.heatmap(corr, annot=True, fmt=".2f", linewidths=0.5)
    
    plt.title("Korelasyon Matrisi")
    out_path = os.path.join(OUTPUT_DIR, "grafik_korelasyon_matrisi.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.show()
    print(f"✅ Kaydedildi: {out_path}")

    # Histogram / dağılım grafikleri 
    _print_section("Histogramlar / Dağılımlar")

    for col in ["Yasam_Beklentisi", "Mutluluk_Skoru", "Kisi_Basi_GSYH"]:
        if col in df_numeric.columns:
            plt.figure(figsize=(8, 4))
            plt.hist(df_numeric[col].dropna(), bins=30)
            plt.title(f"Dağılım: {col}")
            plt.xlabel(col)
            plt.ylabel("Frekans")
            out_path = os.path.join(OUTPUT_DIR, f"hist_{col}.png")
            plt.tight_layout()
            plt.savefig(out_path, dpi=200)
            plt.show()
            print(f"✅ Kaydedildi: {out_path}")

    # Outlier (aykırı değer) analizi - IQR yöntemi
    _print_section("Outlier Analizi (IQR)")

    def iqr_outlier_summary(s: pd.Series):
        s = s.dropna()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        low = q1 - 1.5 * iqr
        high = q3 + 1.5 * iqr
        outlier_mask = (s < low) | (s > high)
        return {
            "q1": q1, "q3": q3, "iqr": iqr,
            "low": low, "high": high,
            "outlier_count": int(outlier_mask.sum()),
            "outlier_rate": float(outlier_mask.mean())
        }

    outlier_report = {}
    for col in df_numeric.columns:
        outlier_report[col] = iqr_outlier_summary(df_numeric[col])

        # boxplot ile görselleştirme
        plt.figure(figsize=(8, 2.8))
        plt.boxplot(df_numeric[col].dropna(), vert=False)
        plt.title(f"Boxplot (Outlier görseli): {col}")
        out_path = os.path.join(OUTPUT_DIR, f"box_{col}.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.show()
        print(f"✅ Kaydedildi: {out_path}")

    # Raporu csv olarak kaydet
    outlier_df = pd.DataFrame(outlier_report).T
    out_path = os.path.join(OUTPUT_DIR, "outlier_ozet_iqr.csv")
    outlier_df.to_csv(out_path, index=True)
    print(f"✅ Outlier özeti kaydedildi: {out_path}")

# 4) MODEL KARŞILAŞTIRMA

def model_karsilastirma(input_csv: str = OUTPUT_MERGED_CSV):
    """
    5 algoritma ile sınıflandırma: Accuracy, Weighted F1, 10-fold CV, grafikler,
    en iyi model için confusion matrix ve classification report.
    """
    _print_section("3) MODEL KARŞILAŞTIRMA (5 Algoritma)")

    from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report, confusion_matrix, f1_score, accuracy_score
    from sklearn.impute import SimpleImputer

    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.svm import SVC

    df = pd.read_csv(input_csv)

    numeric_cols = ["Mutluluk_Skoru", "Kisi_Basi_GSYH", "Sosyal_Destek",
                    "Ozgunluk", "Comertlik", "Yolsuzluk_Algisi", "Yasam_Beklentisi"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = _to_numeric_fix(df[col])

    # hedef sınıf
    df["Yasam_Sinifi"] = pd.cut(df["Yasam_Beklentisi"], bins=LIFE_BINS, labels=LIFE_LABELS)

    # X-y
    drop_cols = ["Country", "Yasam_Beklentisi", "Yasam_Sinifi"]
    if "Mutluluk_Sirasi" in df.columns:
        drop_cols.append("Mutluluk_Sirasi")
    if "Year" in df.columns:
        drop_cols.append("Year")

    X = df.drop(columns=drop_cols, errors="ignore")
    y = df["Yasam_Sinifi"]

    # eksik doldurma + ölçeklendirme
    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=2000),
        "Support Vector Machine (RBF)": SVC(kernel="rbf", probability=True),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "Gradient Boosting": GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42),
    }

    results = []
    best_model = None
    best_score = -1.0
    best_model_name = ""

    print(f"{'MODEL':<30} | {'ACC':<8} | {'F1(w)':<8} | {'CV(10)-ACC':<10}")
    print("-" * 70)

    kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        cv_scores = cross_val_score(model, X_scaled, y, cv=kfold, scoring="accuracy")
        cv_mean = cv_scores.mean()

        results.append({
            "Model": name,
            "Accuracy": acc,
            "F1_Weighted": f1,
            "CV_Acc_Mean": cv_mean
        })

        print(f"{name:<30} | {acc:<8.4f} | {f1:<8.4f} | {cv_mean:<10.4f}")

        if acc > best_score:
            best_score = acc
            best_model = model
            best_model_name = name

    results_df = pd.DataFrame(results)
    out_path = os.path.join(OUTPUT_DIR, "model_sonuclari.csv")
    results_df.to_csv(out_path, index=False)
    print(f"\n✅ Model sonuçları kaydedildi: {out_path}")

    # Grafik: model karşılaştırma
    plt.figure(figsize=(12, 5))

    # Seaborn barplot
    ax = sns.barplot(x="Model", y="Accuracy", data=results_df)
    # Bar üstüne 0.7009 gibi yaz
    for p in ax.patches:
        h = p.get_height()
        ax.annotate(f"{h:.4f}",
                    (p.get_x() + p.get_width() / 2., h),
                    ha="center", va="bottom",
                    fontsize=10,
                    xytext=(0, 3), textcoords="offset points")

    plt.xticks(rotation=15, ha="right")
    plt.title("Model Karşılaştırma (Accuracy)")
    plt.ylim(0, 1.1)
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_DIR, "grafik_model_karsilastirma.png")
    plt.savefig(out_path, dpi=200)
    plt.show()
    print(f"✅ Kaydedildi: {out_path}")


    print(f"\n🏆 En iyi model (test accuracy): {best_model_name} -> {best_score:.4f}")

    # Confusion matrix
    y_pred_best = best_model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred_best, labels=LIFE_LABELS)

    plt.figure(figsize=(7, 5))
    
    # Seaborn heatmap
    sns.heatmap(cm, annot=True, fmt="d", xticklabels=LIFE_LABELS, yticklabels=LIFE_LABELS)
    
    plt.title(f"Confusion Matrix ({best_model_name})")
    plt.xlabel("Tahmin")
    plt.ylabel("Gerçek")
    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "grafik_confusion_matrix.png")
    plt.savefig(out_path, dpi=200)
    plt.show()
    print(f"✅ Kaydedildi: {out_path}")

    print("\n📄 Classification Report:")
    print(classification_report(y_test, y_pred_best))

    # GridSearch (tuning)
    # Sadece en iyi aday model RandomForest veya SVC ise koşsun
    _print_section("GridSearch ile tuning")

    try:
        from sklearn.model_selection import GridSearchCV

        if "Random Forest" in best_model_name:
            param_grid = {
                "n_estimators": [100, 300],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 5]
            }
            base = RandomForestClassifier(random_state=42)
        elif "Support Vector Machine" in best_model_name:
            param_grid = {
                "C": [0.5, 1.0, 2.0],
                "gamma": ["scale", 0.1, 0.01],
                "kernel": ["rbf"]
            }
            base = SVC(probability=True)
        elif "Gradient Boosting" in best_model_name:
            param_grid = {
                "n_estimators": [100, 300],
                "learning_rate": [0.05, 0.1],
                "max_depth": [2, 3]
            }
            base = GradientBoostingClassifier(random_state=42)
        else:
            print("Bu en iyi model için tuning eklemedim (zaten basit/az parametreli).")
            return

        gs = GridSearchCV(
            estimator=base,
            param_grid=param_grid,
            scoring="accuracy",
            cv=kfold,
            n_jobs=-1
        )
        gs.fit(X_scaled, y)

        print("✅ GridSearch bitti.")
        print("En iyi parametreler:", gs.best_params_)
        print("CV best accuracy:", gs.best_score_)

        # Tuning sonuçlarını kaydet
        out_path = os.path.join(OUTPUT_DIR, "gridsearch_best.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"Best model: {type(base).__name__}\n")
            f.write(f"Best params: {gs.best_params_}\n")
            f.write(f"Best CV accuracy: {gs.best_score_}\n")
        print(f"✅ Kaydedildi: {out_path}")
       
    except Exception as e:
        print("⚠️ GridSearch bölümü çalıştırılamadı (paket/CPU vs.). Hata:", e)

# 5) ÖZELLİK ÖNEMİ 

def ozellik_onemi(input_csv: str = OUTPUT_MERGED_CSV):
    """
    Random Forest ile feature importance çıkarır ve grafiğini kaydeder.
    """
    _print_section("4) ÖZELLİK ÖNEMİ (Random Forest)")

    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer

    df = pd.read_csv(input_csv)

    numeric_cols = ["Mutluluk_Skoru", "Kisi_Basi_GSYH", "Sosyal_Destek",
                    "Ozgunluk", "Comertlik", "Yolsuzluk_Algisi", "Yasam_Beklentisi"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = _to_numeric_fix(df[col])

    df["Yasam_Sinifi"] = pd.cut(df["Yasam_Beklentisi"], bins=LIFE_BINS, labels=LIFE_LABELS)

    X = df.drop(columns=["Country", "Yasam_Beklentisi", "Yasam_Sinifi", "Year", "Mutluluk_Sirasi"], errors="ignore")
    y = df["Yasam_Sinifi"]

    imputer = SimpleImputer(strategy="mean")
    X_imputed = imputer.fit_transform(X)

    rf = RandomForestClassifier(n_estimators=200, random_state=42)
    rf.fit(X_imputed, y)

    fi = pd.DataFrame({
        "Faktör": X.columns,
        "Önem": rf.feature_importances_
    }).sort_values("Önem", ascending=False)

    print("\nEn önemli 10 özellik:")
    print(fi.head(10))

    plt.figure(figsize=(10, 6))

    # Seaborn barplot
    ax = sns.barplot(x="Önem", y="Faktör", data=fi.head(12))
    
    # Barların üzerine değer yaz
    for p in ax.patches:
        w = p.get_width()
        ax.annotate(f"{w:.4f}",
                    (w, p.get_y() + p.get_height() / 2),
                    va="center", ha="left",
                    fontsize=10,
                    xytext=(5, 0),
                    textcoords="offset points")
    
    plt.title("Özellik Önemi (Random Forest)")
    plt.xlabel("Önem (0-1)")
    plt.ylabel("Özellik")
    plt.tight_layout()
    
    out_path = os.path.join(OUTPUT_DIR, "grafik_ozellik_onemi.png")
    plt.savefig(out_path, dpi=200)
    plt.show()
    print(f"✅ Kaydedildi: {out_path}")

# 6) ANA ÇALIŞTIRMA

if __name__ == "__main__":
    
    RUN_MERGE = False
    RUN_EDA = False
    RUN_MODEL = False
    RUN_FEATURE_IMPORTANCE = True

    if RUN_MERGE:
        merge_verileri()

    if RUN_EDA:
        eda_analiz()

    if RUN_MODEL:
        model_karsilastirma()

    if RUN_FEATURE_IMPORTANCE:
        ozellik_onemi()