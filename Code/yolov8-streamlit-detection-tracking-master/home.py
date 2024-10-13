# Importations des bibliothèques nécessaires
from pathlib import Path
import PIL.Image
import streamlit as st
import numpy as np
import cv2
import settings
import helper
from authentificator import is_user_logged_in

# Définir les noms de classes (à adapter selon votre modèle)
CLASS_NAMES = [
    "Person", "Bicycle", "Car", "Motorcycle", "Airplane", "Bus", "Train", "Truck",
    "Boat", "Traffic Light", "Fire Hydrant", "Stop Sign", "Parking Meter", "Bench",
    "Bird", "Cat", "Dog", "Horse", "Sheep", "Cow", "Elephant", "Bear", "Zebra",
    "Giraffe", "Backpack", "Umbrella", "Handbag", "Tie", "Suitcase", "Frisbee",
    "Skis", "Snowboard", "Sports Ball", "Kite", "Baseball Bat", "Baseball Glove",
    "Skateboard", "Surfboard", "Tennis Racket", "Bottle", "Wine Glass", "Cup",
    "Fork", "Knife", "Spoon", "Bowl", "Banana", "Apple", "Sandwich", "Orange",
    "Broccoli", "Carrot", "Hot Dog", "Pizza", "Donut", "Cake", "Chair", "Couch",
    "Potted Plant", "Bed", "Dining Table", "Toilet", "TV", "Laptop", "Mouse",
    "Remote", "Keyboard", "Cell Phone", "Microwave", "Oven", "Toaster", "Sink",
    "Refrigerator", "Book", "Clock", "Vase", "Scissors", "Teddy Bear", "Hair Drier",
    "Toothbrush"
]

def plot_filtered_results(image, boxes):
    # Convertir l'image en format numpy array si nécessaire
    image_np = np.array(image)
    
    # Dessiner les boîtes filtrées sur l'image
    for box in boxes:
        xyxy = box.xyxy.tolist()[0]  # Convertir les coordonnées en liste
        x1, y1, x2, y2 = map(int, xyxy)  # Convertir les coordonnées en entiers
        confidence = box.conf.item()
        class_id = int(box.cls.item())
        class_name = CLASS_NAMES[class_id] if class_id < len(CLASS_NAMES) else "Unknown"
        cv2.rectangle(image_np, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image_np, f"{class_name}: {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image_np

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Détection des objets",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

def app():
    if not is_user_logged_in():
        st.write("Connectez-vous pour accéder à cette page.")
    else:
        st.title("Détection des objets avec YOLOv8")

        st.sidebar.header("Configuration du modèle ML")
        model_type = st.sidebar.radio("Sélectionner la tâche", ['Détection', 'Segmentation'])
        confidence = float(st.sidebar.slider("Sélectionner la confiance du modèle", 25, 100, 40)) / 100
        object_to_detect = st.sidebar.selectbox("Choisir l'objet à détecter", CLASS_NAMES)

        if model_type == 'Détection':
            model_path = Path(settings.DETECTION_MODEL)
        elif model_type == 'Segmentation':
            model_path = Path(settings.SEGMENTATION_MODEL)

        try:
            model = helper.load_model(model_path)
        except Exception as ex:
            st.error(f"Impossible de charger le modèle. Vérifiez le chemin spécifié : {model_path}")
            st.error(ex)
            return

        st.sidebar.header("Configuration Image/Vidéo")
        source_radio = st.sidebar.radio("Sélectionner la source", settings.SOURCES_LIST)

        source_img = None

        if source_radio == settings.IMAGE:
            source_img = st.sidebar.file_uploader("Choisir une image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

            col1, col2 = st.columns(2)

            with col1:
                try:
                    if source_img is None:
                        default_image_path = str(settings.DEFAULT_IMAGE)
                        default_image = PIL.Image.open(default_image_path)
                        st.image(default_image_path, caption="Image par défaut", use_column_width=True)
                    else:
                        uploaded_image = PIL.Image.open(source_img)
                        st.image(source_img, caption="Image téléchargée", use_column_width=True)
                except Exception as ex:
                    st.error("Erreur lors de l'ouverture de l'image.")
                    st.error(ex)

            with col2:
                if source_img is None:
                    default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
                    default_detected_image = PIL.Image.open(default_detected_image_path)
                    st.image(default_detected_image_path, caption='Image détectée', use_column_width=True)
                else:
                    if st.sidebar.button('Détecter les objets'):
                        res = model.predict(uploaded_image, conf=confidence)
                        try:
                            filtered_boxes = []
                            for box in res[0].boxes:
                                class_id = int(box.cls.item())  # Convertir en entier

                                if class_id < len(CLASS_NAMES):
                                    class_name = CLASS_NAMES[class_id]
                                    if class_name.lower() == object_to_detect.lower():
                                        filtered_boxes.append(box)
                                else:
                                    st.write(f"Classe {class_id} détectée mais non définie dans CLASS_NAMES.")

                            if not filtered_boxes:
                                st.write(f"Aucun {object_to_detect} détecté.")
                            else:
                                # Tracer les boîtes filtrées
                                result_img = PIL.Image.fromarray(plot_filtered_results(uploaded_image, filtered_boxes))
                                st.image(result_img, caption='Image détectée', use_column_width=True)
                                with st.expander("Résultats de la détection"):
                                    for box in filtered_boxes:
                                        st.write(f"Classe: {object_to_detect}, Confiance: {box.conf.item()}")
                        except Exception as ex:
                            st.write("Erreur lors de l'affichage des résultats de la détection.")
                            st.write(ex)

        elif source_radio == settings.VIDEO:
            helper.play_stored_video(confidence, model)

        elif source_radio == settings.WEBCAM:
            helper.play_webcam(confidence, model)

        elif source_radio == settings.RTSP:
            helper.play_rtsp_stream(confidence, model)

        elif source_radio == settings.YOUTUBE:
            helper.play_youtube_video(confidence, model)

        else:
            st.error("Veuillez sélectionner un type de source valide !")

if __name__ == "__main__":
    app()
