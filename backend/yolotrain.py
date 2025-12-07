from ultralytics import YOLO
import os
import torch

def start_training():
    print("--- egitim basladi ---")
    print(f"Kullanilan cihaz: {torch.cuda.get_device_name(0)}")

    model = YOLO('yolov8n.pt') 
    dataset_folder = "Food-Detection-Project-1"
    current_dir = os.getcwd()
    data_path = os.path.join(current_dir, dataset_folder, "data.yaml")
    
    model.train(
        data=data_path,
        epochs=15,      
        imgsz=640,       
        batch=16,       
        project="runs/detect",
        name="yemek_modeli_gpu",
        device=0         
    )
    
    print("--- egitim bitti---")
    print("Sonuclarin yolu: runs/detect/yemek_modeli_gpu/weights/best.pt")

if __name__ == '__main__':
    start_training()