from ultralytics import YOLO
import os
import warnings

MODEL_NAME = "best.pt" 

def load_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path_abs = os.path.join(script_dir, MODEL_NAME)

    try:
        if not os.path.exists(model_path_abs):
            raise FileNotFoundError
        
        # PyTorch 2.6+ uyumluluk için uyarıları sustur
        warnings.filterwarnings('ignore', category=FutureWarning)
        
        model = YOLO(model_path_abs) 
        print("Model basariyla yuklendi (best.pt)")
        print("Sinif sayisi:", model.model.yaml['nc'])
        return model
        
    except FileNotFoundError:
        print(f"HATA: Model dosyasi '{MODEL_NAME}' bulunamadi.")
        return None
    except Exception as e:
        print(f"Yukleme sirasinda bir hata olustu: {e}")
        print("NOT: Model dosyası eski PyTorch sürümü ile oluşturulmuş olabilir.")
        print("Çözüm: Model yeniden eğitilmeli veya ultralytics güncellenmelidir.")
        return None

if __name__ == "__main__":
    load_model()