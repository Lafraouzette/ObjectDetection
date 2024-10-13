import streamlit as st
from home import app as home_app
from authentificator import app as auth_app
from about import app as about_app
from home import app as home_app


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        st.sidebar.title('Navigation')
        app_names = [app["title"] for app in self.apps]
        selected_app = st.sidebar.radio("Go to", app_names)

        for app in self.apps:
            if app["title"] == selected_app:
                app["function"]()

# Instantiate the MultiApp class
multi_app = MultiApp()

# Add apps to the multi_app instance
multi_app.add_app("Authentification", auth_app)
multi_app.add_app("About", about_app)
multi_app.add_app("home", home_app)

multi_app.run()
