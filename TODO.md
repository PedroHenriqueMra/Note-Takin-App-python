# How it will to work:
The program is a notepad which allows the user to create texts and generate text's notes.

## DataBase
- **there will 3 db layers**
    - *(NoSQL)*
        - A table for save system settings (font size, other GUI settings...)
        - A table to save tabs that have not been closed from the screen
            - link id, last view, content edited unsaved, opened (this bool field will inform if the tab is open or closed and will be cleaned from the database)
    - *(SQL)*
        - First table: a table to save the user texts
            - id, type (txt), title, content, create date, edit date

        - Second table: a table to user annotations
            - id, type (note), reference (excerpt from quote), content, create date, edit date

        - Third table: a table for links that will join the texts and annotations of the respective texts
            - link id (PK),text id, annotation ids (one to many)

