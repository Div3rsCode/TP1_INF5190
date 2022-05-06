import sqlite3


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/database.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def get_articles(self, nbArticles=0):
        cursor = self.get_connection().cursor()
        try:
            int(nbArticles)
        except NameError:
            print(NameError)
            return None
        else:
            requete = ""
            if nbArticles > 0:
                requete = "SELECT * FROM article WHERE date_publication" + \
                    " <= date() LIMIT " + \
                    str(nbArticles)
            else:
                requete = "SELECT titre, date_publication, " + \
                    "identifiant FROM article"
            cursor.execute(requete)
            articles = cursor.fetchall()
            return articles

    def get_articles_clef(self, mot_clef):
        articles = []
        pattern = "%"+mot_clef+"%"
        cursor = self.get_connection().cursor()
        cursor.execute(
            "SELECT titre, date_publication, "
            "identifiant FROM article WHERE titre"
            " LIKE (?) OR paragraphe LIKE (?)", (pattern, pattern))
        articles = cursor.fetchall()
        return articles

    def get_article_by_id(self, identifiant):
        requete = "SELECT * FROM article WHERE identifiant like '" + \
            identifiant+"'"
        cursor = self.get_connection().cursor()
        cursor.execute(requete)
        article = cursor.fetchone()
        return article

    def creer_article(self, titre, auteur, date_publication,
                      paragraphe, identifiant):
        connection = self.get_connection()
        connection.execute(
            "INSERT INTO article " "VALUES(?,?,?,?,?)",
            (identifiant, titre, auteur, date_publication, paragraphe))
        connection.commit()

    def modifier_article(self, identifiant, nouveau_titre, nouveau_paragraphe):
        connection = self.get_connection()
        requete = "UPDATE article SET "
        if len(nouveau_titre) > 0:
            requete += "titre = \"%s\"" % nouveau_titre
        if len(nouveau_paragraphe) > 0:
            if len(nouveau_titre) > 0:
                requete += ", paragraphe = \"%s\"" % nouveau_paragraphe
            else:
                requete += "paragraphe = \"%s\"" % nouveau_paragraphe
        requete += " WHERE identifiant = \"%s\"" % identifiant
        print(requete)
        connection.execute(requete)
        connection.commit()
