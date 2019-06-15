# Djangauto

Djangauto est une application d'administration de consessionnaire de voiture.

Il faut être connecté pour faire n'immporte quel action sur le site.<br/>
L'administrateur peut register d'autres utilisateurs à partir du bouton register sur la page /model_list.

### /model_list

Sur cette page est listé tous les models de voiture répertoriés. Cliquer sur un modèle renvoie vers /car_list.<br/>
Un Bouton *Add a model* revoie vers la page /add_model.<br/>
On peut supprimer un modèle. Cela supprimera toutes les voitures de ce modèle ainsi que les images stockées sur cloudinary.<br/>
On peut modifier un modèle. Si le prix est changé, toutes les voitures neuves de ce modèle voit leur prix changé. Si le modèle, la marque ou l'année de production est changé, de nouvelles images seront générées.<br/>

### /add_model

Ajouter un modèle de voitures insert une nouvelle marque en base si elle est inexistante.<br/>
**FEATURE ORIGINALE :** Les images du modèle sont générées automatiquement à partir de google image. Celles-ci sont stockées sur cloudinary.

### /car_list

Ici on voit la liste des voitures du modèle sélectionné.<br/>
Les voitures neuves sont concaténées sur un item unique.<br/>
On peut ajouter ou supprimer une voiture neuve avec les raccourci *+* et *-*.<br/>
Une voiture d'occasion peut être supprimer et son prix peut être modifié.<br/>
On peut ajouter une voiture via le bouton *Add a car*.<br/>

### /add_car

On peut ajouter plusieurs voitures en même temps via le champs *number*.