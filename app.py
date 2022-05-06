from database import Database
import datetime
from utils.verifierEntree import *
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import redirect


tp1 = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@tp1.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@tp1.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        titre = "Les articles récents:"
        articles = get_db().get_articles(5)

    else:
        titre = "Résultat de la recherche:"
        recherche = request.form["recherche"]
        recherche = recherche.strip()
        articles = get_db().get_articles_clef(recherche)

    return render_template("liste_articles.html",
                           titre=titre, articles=articles)


@tp1.route('/article/<string:identifiant>', methods=['GET'])
def get_article(identifiant):
    temp = get_db().get_article_by_id(identifiant)
    if temp is None:
        return render_template("erreur.html"), 404
    else:
        article = []
        article.append(temp)
        return render_template("liste_articles.html", articles=article)


@tp1.route('/admin', methods=['GET'])
def admin():
    titre = "Administrateur:"
    if request.method == 'GET':
        articles = get_db().get_articles()
        return render_template("admin.html", titre=titre, articles=articles)


@tp1.route('/modifier/<string:identifiant>', methods=['GET', 'POST'])
def modifier_article(identifiant):
    if request.method == 'GET':
        return render_template("modifier.html", identifiant=identifiant)
    else:
        nouveau_titre = request.form["titre"]
        nouveau_paragraphe = request.form["paragraphe"]
        if (format_texte(nouveau_paragraphe) and format_nom(nouveau_titre)):
            get_db().modifier_article(identifiant,
                                      nouveau_titre, nouveau_paragraphe)
            return redirect("/confirmation")

        chemin = "/modifier/"+identifiant
        return redirect(chemin, 304)


@tp1.route('/admin-nouveau', methods=['GET', 'POST'])
def new_article():
    if request.method == 'GET':
        return render_template("creation.html")
    else:
        titre = request.form["titre"]
        auteur = request.form["auteur"]
        date_publication = request.form["date"]
        paragraphe = request.form["paragraphe"]
        identifiant = request.form["identifiant"]
        identifiant = identifiant.strip().replace(" ", "")

        today = datetime.datetime.now().strftime('%Y-%m-%d')
        if not (format_nom(titre)
                and format_nom(auteur)
                and format_texte(paragraphe)
                and isurl(identifiant)
                and date_publication >= today):
            erreur = True
            return render_template("creation.html", titre=titre,
                                   auteur=auteur,
                                   date=date_publication,
                                   identifiant=identifiant,
                                   paragraphe=paragraphe,
                                   erreur=erreur)

        get_db().creer_article(titre, auteur,
                               date_publication, paragraphe, identifiant)
        return redirect("/confirmation")


@tp1.route("/confirmation", methods=["GET"])
def confirmation():
    return render_template("confirmation.html")
