# How going to work:
The program is a notepad which allows the user to create texts and generate text's notes.

## DataBase
- **there will 3 db layers**
    - *(NoSQL)*
        - A table for save system settings (GUI settings, auto save...)
        - A table to save tabs that have not been closed from the screen
            - link id
    - *(SQL)*
        - First table: a table to save the user texts
            - id, type (txt), title, content, date infos

        - Second table: a table to user annotations
            - id, type (note), reference, content, date infos

        - Third table: a table for links that will join the texts and annotations of the respective texts
            - link id (primary key),text id, annotation ids (one to many)

## Work layer
**A system manager**
