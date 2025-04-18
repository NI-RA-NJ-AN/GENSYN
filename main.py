# import streamlit as st
# from streamlit_option_menu import option_menu
# import sg4, synthetic02


# st.set_page_config(
#     page_title="GENSYN"
# )

# class Multiapp:
    
#     def __init__(self):
#         self.apps = []

#     def add_app(self, title, function):
#         self.apps.append({
#             "title": title,
#             "function": function
#         })

#     def run(self):
#         with st.sidebar:
#             app = option_menu(
#                 menu_title=None,
#                 options=['First Generation', 'Final Generation'],
#                 default_index=0,
#                 orientation="horizontal",
#             )

#         if app == 'First Generation':
#             sg4.app()
#         elif app == 'Final Generation':
#             synthetic02.app()


# app_instance = Multiapp()
# app_instance.run()



import streamlit as st
from streamlit_option_menu import option_menu
import sg4, synthetic02

st.set_page_config(page_title="GENSYN")

class Multiapp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        app = option_menu(
            menu_title=None,
            options=['Data Generation', 'Data Compilation'],
            icons=['robot', 'stack'],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal"
        )

        if app == 'Data Generation':
            sg4.app()
        elif app == 'Data Compilation':
            synthetic02.app()

app_instance = Multiapp()
app_instance.run()
