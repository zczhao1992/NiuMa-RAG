import streamlit as st


def hide_specific_pages(keywords):
    css = []

    for keyword in keywords:
        css.append(f'''
        [data-testid="stSidebarNav"] li a[href*="{keyword}"] {{
            display: none !important;
            visibility: hidden !important;
        }}
        ''')

    st.markdown(
        f'''
        <style>
            {"".join(css)}
        </style>
        ''',
        unsafe_allow_html=True
    )


def hide_main_page():
    st.markdown('''
        <style>
            [data-testid="stSidebarNav"] li a[href$="/"]:not([href*="page="]),
            [data-testid="stSidebarNav"] li a[href*="app"] {
                display: none !important;
                visibility: hidden !important; 
            }   
        </style>
        ''',
                unsafe_allow_html=True
                )


def hide_pages():
    # hide_main_page()
    hide_specific_pages(
        ["chunks", "file_upload", "namespace_add", "namespace_update"])
