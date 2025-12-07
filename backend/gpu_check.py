import torch
import os

def check_gpu():
    print("--- GPU  ---")
    
    
    is_available = torch.cuda.is_available()
    
    print(f"CUDA Erişilebilir mi?: {is_available}")
    
    if is_available:
        print(f"Ekran Kartı Sayısı: {torch.cuda.device_count()}")
        print(f"Ekran Kartı Modeli: {torch.cuda.get_device_name(0)}")
        print("NVIDIA Ekran kartın var ve kullanima hazır.")
    else:
        print(" Şu an GPU kullanilamiyor.")
        
    print("-" * 30)
    
    print(f"Isletim Sistemi: {os.name}")

if __name__ == "__main__":
    check_gpu()