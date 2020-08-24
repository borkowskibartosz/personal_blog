Project końcowy: Blog osobisty

Django web app

Modele :
    + Category
        + name
    + Photo
        + description
        + uploaded_by - jeden do wielu z modelem User
        + image
    + UserProfile
        + user - jeden do jeden z User
        + avatar
    + Post
        + title
        + slug
        + author
        + edited_on
        + created_on
        + content
        + status
        + photos - wiele do wielu z Photo
        + categories - wiele do wielu z Category
    + Comment
        + rating
        + content
        + author - jeden do wielu
        + source_post - jeden do wielu
        + created_on

Widoki:
    + wszystkie kategorie (bez logowania)
    + wszystkie artykuły danego autora (bez logowania)
    + wszystkie artykuły danej kategorii (bez logowania)
    + widok profilu - wszystkie aktywności zalogowanego użytkownika
    + dodaj awatar (zalogowany/właściciel)
    + edytuj profil (zalogowany/właściciel)
    + dodaj artykuł (zalogowany)
    + usuń artykuł (zalogowany/właściciel)
    + edytuj artykuł (zalogowany/właściciel)
    + dodaj komentarz (zalogowany)
    + usuń komentarz (zalogowany/właściciel)
    + edytuj komentarz (zalogowany/właściciel)
    + dodaj zdjęcie (zalogowany)
    + usuń zdjęcie (zalogowany)
    + edytuj zdjęcie (zalogowany)   
    + dodaj profil
    - reset hasła 
    - kontakt
    + about

Dodatkowe rozwiązania:
    + stronicowanie
    + wyszukiwanie po zawartości artykułów i w tytule
    - kontrola dostępu (permissions)

Testy:
    - jeszcze muszę się doedukować

Wrzucić na Heroku:
    - do zrobienia

Dodatkowo jak starczy czasu:
    - ocena komentarza (+/-)


DONE
+ all categories view
+ author view
+ individual category view
+ categories in post detail
+ logins
+ Add comments
+ links for categories with popularity
+ Create comment
+ Edit comment
+ Delete comment
+ profile view
+ CRUD article
    + update forms
    + picture handling
+ delete picture view
+ search
+ about page
+ pagination
+ data komentarza
+ social login Github and Google
+ reset password
+ delete user if staf member
+ all users view to delete
+ contact page

TODO:

- tests
- admin pass
- admin path
- heroku
- add avatar from social

TODO: BUGS:
    - 

- post rating (?)