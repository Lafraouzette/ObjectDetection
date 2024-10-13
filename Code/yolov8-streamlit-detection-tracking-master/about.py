import streamlit as st

def app():
    st.title('à-propos')

    st.markdown("""
    Bienvenue dans cette application de détection d'objets avec YOLOv8. 
    ### Cette application a été développée dans le cadre d'un projet de fin d'année pour démontrer la puissance de YOLOv8 dans la detection des objets.
    ### Fonctionnalités :
    - **Authentification** : Utilisez l'authentification par email et mot de passe pour accéder à l'application.
    - **Détection d'Objets** : Utilisez le modèle YOLOv8 pour détecter des objets dans des images ou des vidéos.
    
    ### Réalisateur : 
    - **Fait par** : LAFRAOUZI Mouhssine
                
    ### REFERENCES :
    - https://docs.streamlit.io/get-started/tutorials/create-an-app
    - https://www.datacamp.com/blog/yolo-object-detection-explained
    - https://rs-punia.medium.com/building-a-real-time-object-detection-and-tracking-app-with-yolov8-and-streamlit-part-2-d1a273592e7e
                


    Pour plus d'informations, vous pouvez me contacter.[Adresse Email](mailto:lafraouzimouhssine@email.com).
    """)


  
if __name__ == '__main__':
    app()
