import streamlit as st
from code_editor import code_editor


def SQL_Code_Editor(default_String: str):
    """
    Runs streamlit_code_editor and reruns the value.
    All default values where set on function itself.
    @param default_String: default string to show on running.
    @return: returns the edited string.
    """
    # Button configuration for Execute button.
    editor_button_configuration = [
        {
            "name":"Execute",
            "feather":"Play",
            "primary":False,
            "hasText":True,
            "showWithIcon":True,
            "commands":["submit"],
            "style":{"bottom":"0.44rem", "right":"0.4rem"}},
        {
            "name":"Copy",
            "feather":"Copy",
            "hasText":True,
            "alwaysOn":True,
            "commands":["copyAll",
                        ["infoMessage",
                         {
                             "text":"Copied to clipboard!",
                             "timeout":2500,
                             "classToggle":"show"
                         }
                         ]
                        ],
            "style":{
                "top":"-0.25rem",
                "right":"0.4rem"
            }}
    ]

    # Auto complete list for Ace Editor.
    Auto_completes = [
        {"caption":"channels", "value":"channels", "meta":"youtube_dh.channels", "name":"Table", "score":400},
        {"caption":"playlists", "value":"playlists", "meta":"youtube_db.playlists", "name":"Table", "score":400},
        {"caption":"comments", "value":"comments", "meta":"youtube_db.comments", "name":"Table", "score":400},
        {"caption":"videos", "value":"videos", "meta":"youtube_db.videos", "name":"Table", "score":400},
        {"caption":"youtube_dh", "value":"youtube_dh", "meta":"youtube_dh", "name":"Database", "score":400},
    ]

    response_dict = code_editor(default_String,
                                lang="sql",
                                height=[19, 10],
                                key="sql_editor",
                                buttons=editor_button_configuration,
                                shortcuts="vscode",
                                completions=Auto_completes,
                                theme="dark",
                                options={"wrap":True})

    if len(response_dict['id']) != 0 and (response_dict['type'] == "selection" or response_dict['type'] == "submit"):
        edited_text = response_dict['text']
        # st.write(edited_text)
        st.code(edited_text, language='sql')


if __name__ == '__main__':
    sample_python_code = '''-- Example SQL Query
    SELECT * FROM your_table
    WHERE condition = 'value';  --no change '''

    st.subheader("SQL Query code Editor: (MySQL)")
    st.write(" write only one query only. I made code to display only one table at a time.")

    SQL_Code_Editor(sample_python_code)
