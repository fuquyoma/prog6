import cv2
import os
import glob
import numpy as np

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    height, width = frameOpencvDnn.shape[:2]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(height / 150)), 8)
    return frameOpencvDnn, faceBoxes

def resize_to_fit(image, max_width=800, max_height=600):
    """Масштабирует изображение, чтобы оно помещалось в указанные размеры"""
    height, width = image.shape[:2]
    
    # Рассчитываем коэффициент масштабирования
    scale = min(max_width/width, max_height/height, 1.0)  # Не увеличиваем изображение
    
    # Если масштабирование не требуется
    if scale == 1.0:
        return image, scale
    
    # Рассчитываем новые размеры
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    # Масштабируем изображение
    resized = cv2.resize(image, (new_width, new_height))
    return resized, scale

def find_images():
    """Поиск изображений в текущей директории"""
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(ext))
    return sorted(image_files)

def main():
    # Загрузка модели
    face_proto = "opencv_face_detector.pbtxt"
    face_model = "opencv_face_detector_uint8.pb"
    
    if not os.path.exists(face_proto) or not os.path.exists(face_model):
        print("Ошибка: Файлы моделей не найдены! Убедитесь что в директории есть:")
        print(f"- {face_proto}")
        print(f"- {face_model}")
        return
    
    face_net = cv2.dnn.readNet(face_model, face_proto)
    
    # Поиск изображений
    images = find_images()
    
    print("\nДоступные режимы:")
    print("1: Запуск камеры")
    print("2: Выбрать изображение из текущей директории")
    
    choice = input("Выберите режим (1/2): ")
    
    if choice == '1':
        # Режим камеры
        video = cv2.VideoCapture(0)
        if not video.isOpened():
            print("Ошибка: Камера недоступна")
            return
            
        print("\nРежим камеры активирован. Нажмите 'q' для выхода...")
        while True:
            has_frame, frame = video.read()
            if not has_frame:
                break
                
            result_img, face_boxes = highlightFace(face_net, frame)
            
            # Масштабируем для отображения
            display_img, _ = resize_to_fit(result_img)
            cv2.imshow("Face Detection - Camera", display_img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        video.release()
        
    elif choice == '2':
        # Режим файла
        if not images:
            print("\nВ текущей директории не найдено изображений!")
            print("Поддерживаемые форматы: JPG, JPEG, PNG, BMP, TIFF, WEBP")
            return
            
        print("\nНайдены изображения:")
        for i, img in enumerate(images, 1):
            print(f"{i}: {img}")
            
        try:
            selection = int(input("\nВведите номер изображения: "))
            if selection < 1 or selection > len(images):
                raise ValueError
        except ValueError:
            print("Некорректный выбор!")
            return
            
        file_path = images[selection-1]
        print(f"Обработка: {file_path}")
        
        frame = cv2.imread(file_path)
        if frame is None:
            print(f"Ошибка: Не удалось загрузить {file_path}")
            return
            
        result_img, face_boxes = highlightFace(face_net, frame)
        
        if face_boxes:
            print(f"Найдено лиц: {len(face_boxes)}")
        else:
            print("Лица не обнаружены")
            
        
        # Масштабируем для отображения
        display_img, scale = resize_to_fit(result_img)
        
        # Показываем результат
        window_name = f"Face Detection: {os.path.basename(file_path)}"
        cv2.imshow(window_name, display_img)
        
        print("Нажмите любую клавишу для закрытия окна...")
        cv2.waitKey(0)
        
    else:
        print("Некорректный выбор")
        
    cv2.destroyAllWindows()
    print("Программа завершена")

if __name__ == "__main__":
    main()