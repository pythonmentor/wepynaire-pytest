# WePyNaire: Apprenez à tester votre code python avec Pytest

Le code dans ce dépôt est un code retravaillé après le WePyNaire du 4 décembre
2021 sur l'apprentissage du framework de test pytest.

## Utilisation:

Pour utiliser le code de ce dépôt, il suffit de travailler avec pipenv et
d'installer les dépendances (pytest et pytest-mock) avec la commande 
`$ pipenv install`

Une fois les dépendances installées, les tests peuvent être exécutés à l'aide
de la commande `pipenv run pytest -vvv`

## Description des fonctions dans le module webinaire.exemple

Un certain nombre de fonctions simple ont été programmée pour illustrer 
différents principes de tests. Voici la description de chaque fonction.

### get_hello()

Cette fonction retourne directement le message de salution. C'est la
situation la plus simple à tester, car nous obtenons directement le
résultat de la fonction en sortie. On dit de ce type de fonction qui ne
font pas d'effet de bord qu'elles sont pures.

### display_hello()

Cette fonction ne retourne aucune information mais réalise sa tâche à
l'aide d'un effet de bord en affichant le message sur le flux de sortie
standard (par défaut le terminal).

### send_hello() et send_email(subject, message, recipients)

Cette fonction send_hello ne retourne aucune information mais réalise sa tâche à
l'aide d'un effet de bord: l'envoi d'un email à l'aide de la fonction send_email 
(qui n'a pas été implémentée ici).

### read_labyrinth(file)

Cette fonction lit la structure d'un labyrinthe à l'aide d'un fichier. L'objectif
est ici de montrer comment pytest permet de gérer une fonction qui attend un fichier.

### read_labyrinth_with_exception(file)

Cette fonction lit la structure d'un labyrinthe à l'aide d'un fichier et lève 
une exception de type FileNotFoundError si le chemin reçu en argument ne 
correspond à aucun fichier existant. L'objectif
est ici de montrer comment pytest permet de tester si une exception a été 
levée par la fonction testée.

### input_number(prompt, min_=None, max_=None, allowed=None,err_msg=None)

Cette fonction demande à l'utilisateur de saisir un avec des contraintes de minimum,
maximum ou de valeurs autorisée. L'interaction avec l'utilisateur est ici gérée 
par la fonction input() et l'objectif est de montrer comment il est possible de 
tester une fonction interactive avec pytest.