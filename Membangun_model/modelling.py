import pandas as pd
import mlflow
import mlflow.sklearn
import joblib # <-- 1. Tambah ini buat jalur barbar
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
# import dagshub 

# 2. Masukin Username dan Nama Repo DagsHub lu di sini
# dagshub.init(repo_owner='indra-4', repo_name='EKSPERIMEN_SML_Rama', mlflow=True)

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Heart_Disease_Model")
mlflow.sklearn.autolog()

def train_model():
    print("Memuat dataset bersih...")
    df = pd.read_csv('heart_preprocessing/heart_clean.csv')
    
    X = df.drop('target', axis=1)
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Mulai melatih model KNN dengan MLflow ke DagsHub...")
    with mlflow.start_run():
        model = KNeighborsClassifier(n_neighbors=5)
        model.fit(X_train, y_train)
        
        # Simpan model beserta format standar MLflow ke folder lokal
        import os, shutil
        if os.path.exists("model_folder"):
            shutil.rmtree("model_folder")
        mlflow.sklearn.save_model(model, "model_folder")
        
        # Upload folder tersebut ke UI Artifacts dengan nama 'model'
        mlflow.log_artifacts("model_folder", "model")
        
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Pelatihan Selesai! Akurasi Model: {acc:.2f}")

if __name__ == "__main__":
    train_model()