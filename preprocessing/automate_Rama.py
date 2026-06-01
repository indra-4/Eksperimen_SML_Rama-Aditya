import pandas as pd
import os

def run_preprocessing():
    print("Memulai proses preprocessing...")
    
    # Menentukan path file
    raw_data_path = '../heart_raw/heart.csv'
    clean_data_path = 'heart_preprocessing/heart_clean.csv'
    
    # 1. Memuat Dataset
    df = pd.read_csv(raw_data_path)
    
    # 2. Menghapus data duplikat (Sesuai dengan eksperimen)
    initial_duplicates = df.duplicated().sum()
    df = df.drop_duplicates()
    final_duplicates = df.duplicated().sum()
    
    # 3. Menyimpan data yang sudah bersih
    # Pastikan folder target ada
    os.makedirs('heart_preprocessing', exist_ok=True)
    df.to_csv(clean_data_path, index=False)
    
    print(f"Preprocessing selesai!")
    print(f"Data duplikat dihapus: {initial_duplicates - final_duplicates} baris.")
    print(f"Data bersih disimpan di: {clean_data_path}")

if __name__ == "__main__":
    run_preprocessing()