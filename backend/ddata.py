from roboflow import Roboflow
import os
import yaml

def download_dataset():
    print("--- DOĞRU VERİ SETİ (OBJECT DETECTION) İNDİRİLİYOR ---")
    
    # Senin API Anahtarın
    api_key = "9quuU5UR3jPsguykgZbE" 
    rf = Roboflow(api_key=api_key)
    
    # Link: https://universe.roboflow.com/food-extra/food-detection-project-h6tss
    # Workspace: food-extra
    # Project: food-detection-project-h6tss
    
    print("Projeye bağlanılıyor (food-detection-project-h6tss)...")
    
    try:
       
        project = rf.workspace("food-extra").project("food-detection-project-h6tss")
        
        print("İndirme başlıyor")
        
        dataset = project.version(1).download("yolov8")
        
        print(f"\n İNDİRME TAMAMLANDI! Konum: {dataset.location}")
        
       
        print("\n siniflar okunuyor")
        yaml_path = os.path.join(dataset.location, "data.yaml")
        
        with open(yaml_path, 'r') as file:
            data = yaml.safe_load(file)
            siniflar = data['names']
            
            print("\n--- Siniflar ---")
            for i, yemek in enumerate(siniflar):
                print(f"{i}: {yemek}")
            print("------------------------------------------")
            

    except Exception as e:
        print(f"\n HATA! İndirme başarısız oldu.")
       

if __name__ == "__main__":
    download_dataset()