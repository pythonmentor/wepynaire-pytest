import pathlib

HELLO_MESSAGE = 'hello, world'


def send_email(subject, message, recipients):
    pass


def send_hello():
    """Envoie le message un message de salutation par email.

    Cette fonction ne retourne aucune information mais réalise sa tâche à
    l'aide d'un effet de bord: l'envoi d'un email.

    """
    send_email(
        subject='Salutations',
        message=HELLO_MESSAGE,
        recipients=['moi@moi.com'],
    )


def display_hello():
    """Affiche un message de salutation sur le flux de sortie standard.

    Cette fonction ne retourne aucune information mais réalise sa tâche à
    l'aide d'un effet de bord en affichant le message sur le flux de sortie
    standard (par défaut le terminal).

    """
    print(HELLO_MESSAGE)


def get_hello():
    """Retourne un message de salutation.

    Cette fonction retourne directement le message de salution. C'est la
    situation la plus simple à tester, car nous obtenons directement le
    résultat de la fonction en sortie. On dit de ce type de fonction qui ne
    font pas d'effet de bord qu'elles sont pures.

    """
    return HELLO_MESSAGE


def read_labyrinth(file):
    """Lit la structure du labyrinthe depuis un fichier et returne une
    liste des coordonnées des passages sous forme (ligne, colonne)."""
    positions = []

    # Handles non existing files
    file = pathlib.Path(file).resolve()
    if not file.exists():
        return positions

    with open(file) as mazefile:
        for y, line in enumerate(mazefile):
            for x, col in enumerate(line):
                if col == " ":
                    positions.append((y, x))
    return positions


def read_labyrinth_with_exception(file):
    """Lit la structure du labyrinthe depuis un fichier et returne une
    liste des coordonnées des passages sous forme (ligne, colonne).

    Cette fonction lève une exception de type FileNotFoundError si le chemin
    passé en argument ne correspond à aucun fichier existant."""
    positions = []

    # Handles non existing files
    file = pathlib.Path(file).resolve()
    if not file.exists():
        raise FileNotFoundError(
            f'Maze description file {file} does not exist.'
        )

    with open(file) as mazefile:
        for y, line in enumerate(mazefile):
            for x, col in enumerate(line):
                if col == " ":
                    positions.append((y, x))
    return positions


def input_number(
    prompt,
    min_=None,
    max_=None,
    allowed=None,
    err_msg=None,
):
    """Demande à l'utilisateur de saisir un avec des contraintes de minimum,
    maximum ou de valeurs autorisée.

    Args:
        prompt: message à afficher à l'utilisateur pour lui demander le nombre.
        min_: valeur minimale acceptée. None signifie pas de minimum.
        max_: valeur maximale acceptée. None signifie pas de maximum.
        allowed: séquence de valeurs autorisées. None signifie que toutes les
            valeurs sont autorisée.
        err_msg: message à afficher à l'utilisateur en cas d'erreur de saisie.

    Return:
        Retourne l'entier saisit par l'utilisateur."""
    validators = [
        # Min validitor
        lambda value: True if min_ is None or value >= min_ else False,
        # Max validator
        lambda value: True if max_ is None or value <= max_ else False,
        # In allowed values validator
        lambda value: True if allowed is None or value in allowed else False,
    ]

    while True:
        number = input(prompt).strip()
        if number.isdecimal():
            number = int(number)
            if all(validator(number) for validator in validators):
                return number

        if err_msg is not None:
            print(err_msg)
