#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import *
from flask import send_file
from werkzeug import secure_filename
import os
from a import *

PEOPLE_FOLDER = os.path.join('static')
app = Flask(__name__)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

#DOSSIER_UPS = 

def extension_ok(nomfic):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    return '.' in nomfic and nomfic.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg', 'gif', 'bmp')

@app.route('/up/', methods=['GET', 'POST'])
def upload():
    global nom,full_filename
    
    if request.method == 'POST':
         # on vérifie que le mot de passe est bon
        f = request.files['fic']
        if f: # on vérifie qu'un fichier a bien été envoyé
            if extension_ok(f.filename): # on vérifie que son extension est valide
                nom = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'],nom))
                flash(u'Image envoyée ! Voici <a href="{lien}">son lien</a>.'.format(lien=url_for('upped', nom=nom)), 'suc')
                full_filename = os.path.join(app.config['UPLOAD_FOLDER'],nom)
                return render_template('up_up.html',img=nom)
            else:
                flash(u'Ce fichier ne porte pas une extension autorisée !', 'error')
        else:
                flash(u'Vous avez oublié le fichier !', 'error')
        
        
    else:
        return render_template('up_up.html')

@app.route('/escalier', methods=['POST'])
def escalier():
    global nom,full_filename
    if request.method == 'POST':
        niveau = int(request.form['gris'])
        img = open(full_filename)
        img_gris = fonctionEscalier(img, niveau)
        name = "img_gris.png"
        img_gris.save(os.path.join(app.config['UPLOAD_FOLDER'],name))

        return render_template('up_up.html',img=nom,img_gris=name,niveau=niveau)

@app.route('/up/view/')
def liste_upped():
    images = [img for img in os.listdir(app.config['UPLOAD_FOLDER']) if extension_ok(img)] # la liste des images dans le dossier
    return render_template('up_liste.html', images=images)

@app.route('/up/view/<nom>')
def upped(nom):
    nom = secure_filename(nom)
    if os.path.isfile(app.config['UPLOAD_FOLDER']+nom): # si le fichier existe
        return send_file(app.config['UPLOAD_FOLDER']+nom, as_attachment=True) # on l'envoie
    else:
        flash(u'Fichier {nom} inexistant.'.format(nom=nom), 'error')
        return redirect(url_for('liste_upped')) # sinon on redirige vers la liste des images, avec un message d'erreur

if __name__ == '__main__':
    app.run(debug=True)
