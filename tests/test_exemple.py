import io
import sys

import pytest

from webinaire import exemple


def test_get_hello_returns_hello_message_directly():
    """Vérifie que la fonction get_hello() retourne le message attendu."""
    # 1. Setup du test

    # 2. Exécution de la fonction à tester et récupération du résultat
    resultat = exemple.get_hello()

    # 3. Vérification que le résultat obtenu est conforme aux attentes
    assert resultat == exemple.HELLO_MESSAGE


def test_display_hello_prints_hello_message_on_stdout(capsys):
    """Vérifie que la fonction display_hello() affiche le message attendu
    sur le flux de sortie standard, soit sys.stdout."""
    # 1. Setup du test

    # 2. Exécution de la fonction à tester
    exemple.display_hello()

    # Ici, il n'y a pas de résultat, car display_hello ne retourne rien. Au
    # lieu de cela, cette fonction affiche un message sur le flux de sortie
    # standard. PyTest nous fournit l'outils pour capturer les messages
    # affichés sur sys.stdout (le flux de sortie standard) et sys.stderr
    # (le flux d'erreur standard)
    capture = capsys.readouterr()

    # 3. Vérification que le résultat obtenu est conforme aux attentes
    assert capture.out.strip() == exemple.HELLO_MESSAGE


def test_send_hello_sends_hello_message_using_custom_monkeypatch(
    capsys, my_monkeypatch
):
    """Vérifie que send_hello envoie l'email 'hello, world'.

    Dans ce test on utilise une fixture my_monkeypatch qui reproduit le
    comportement de la fixture monkeypatch. Cette approche est purement
    éducative et vise à démystifier la magie noir derrière monkeypatch.

    """
    # 1. setup
    def fake_send_email(subject, message, recipients):
        print(message, file=sys.stderr)  # ce message sera capturé par capsys

    my_monkeypatch.setattr(exemple, 'send_email', fake_send_email)

    # 2. Exécution de la fonction
    exemple.send_hello()

    # 3. vérifier que le résultat est conforme

    # resultat = capturer ce qui a été écrit sur stdout
    capture = capsys.readouterr()
    # vérifier que resultat est bien 'hello, world'
    assert capture.err.strip() == exemple.HELLO_MESSAGE


def test_send_hello_sends_hello_message_using_standard_monkeypatch(
    capsys, monkeypatch
):
    """Vérifie que send_hello envoie l'email 'hello, world'.

    Ce test est un duplicat du test précédent, mais il utilise la fixture
    standard monkeypatch pour remplacer la fonction send_email() par un
    faux.

    """
    # 1. setup
    def fake_send_email(subject, message, recipients):
        print(message, file=sys.stderr)  # ce message sera capturé par capsys

    monkeypatch.setattr(exemple, 'send_email', fake_send_email)

    # 2. Exécution de la fonction
    exemple.send_hello()

    # 3. vérifier que le résultat est conforme
    # resultat = capturer ce qui a été écrit sur stdout
    capture = capsys.readouterr()
    # vérifier que resultat est bien 'hello, world'
    assert capture.err.strip() == exemple.HELLO_MESSAGE


def test_send_hello_sends_hello_message_without_monkeypatch(capsys):
    """Vérifie que send_hello envoie l'email 'hello, world'.

    Ce test est un duplicat du test précédent, mais il utilise pas de fixure
    pour remplacer la fonction send_email() par un faux. Le travail est
    fait à la main.

    """
    # 1. setup
    def fake_send_email(subject, message, recipients):
        print(message, file=sys.stderr)  # ce message sera capturé par capsys

    # On remplate la fonction send_email par un faux
    send_email_backup = exemple.send_email
    exemple.send_email = fake_send_email

    # 2. Exécution de la fonction
    exemple.send_hello()

    # 3. vérifier que le résultat est conforme
    # resultat = capturer ce qui a été écrit sur stdout
    capture = capsys.readouterr()
    # vérifier que resultat est bien 'hello, world'
    assert capture.err.strip() == exemple.HELLO_MESSAGE

    # On remet la vraie fonction send_email à sa place pour ne pas influencer
    # les tests suivants
    exemple.send_email = send_email_backup


def test_read_labyrinth_returns_empty_list_if_file_does_not_exist():
    """Vérifie que read_labyrinth() retourne une liste vide lorsque
    le chemin reçu en argument ne correspond à aucun fichier existant."""

    # 1. setup du test

    # 2. exécuter la fonction à tester et récupérer son résultat
    resultat = exemple.read_labyrinth('doesnotexist.txt')

    # 3. vérifier que le résultat est celui attendu
    assert resultat == []


def test_read_labyrinth_returns_list_with_path_coordinates(tmp_path):
    """Vérifie que read_labyrinth() retourne une liste contenant autant de
    coordonnées qu'il y a de chemins dans le fichier de description du
    labyrinthe."""

    # 1. Setup du test
    MAZE_DESCRIPTION = (
        '#####',
        '    #',
        '### #',
        '### #',
        '### #',
    )
    PATH_COORDINATES = {(1, 0), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3)}

    description_file = tmp_path / 'maze.txt'
    description_file.write_text('\n'.join(MAZE_DESCRIPTION))

    # 2. Exécution de la fonction à tester avec les arguments choisis
    #    pour le présent scénario et récupération du résultat de la fonction
    resultat = exemple.read_labyrinth(str(description_file))

    # 3. Vérification le résultat de la fonction est conforme aux attentes
    assert isinstance(resultat, list)
    assert len(resultat) == 7
    assert PATH_COORDINATES == set(resultat)


def test_read_labyrinth_returns_empty_list_if_description_file_is_empty(
    tmp_path,
):
    """Vérifie que read_labyrinth() retourne une liste vide si le fichier de
    description du labyrinthe existe mais qu'il est vide."""

    # 1. Setup du test
    description_file = tmp_path / 'maze.txt'
    description_file.write_text('')

    # 2. Exécution de la fonction à tester et récupération son résultat
    resultat = exemple.read_labyrinth(str(description_file))

    # 3. Vérification que le résultat est conforme aux attentes
    assert resultat == []


def test_read_labyrinth_returns_empty_list_if_maze_contains_only_walls(
    tmp_path,
):
    """Vérifie que read_labyrinth() retourne une liste vide si le fichier de
    description du labyrinthe existe mais qu'il est vide."""

    # 1. Setup du test
    MAZE_DESCRIPTION = (
        '######',
        '######',
        '######',
        '######',
        '######',
    )

    description_file = tmp_path / 'maze.txt'
    description_file.write_text('\n'.join(MAZE_DESCRIPTION))

    # 2. Exécution de la fonction à tester et récupération du résultat
    resultat = exemple.read_labyrinth(str(description_file))

    # 3. Vérification que le résultat est conforme aux attentes
    assert resultat == []


def test_read_labyrinth_with_exception_raises_if_file_does_not_exist():
    """Vérifie que la fonction lève une exception de type FileNotFoundError
    si le chemin passé en argument ne correspond à aucun fichier existant."""

    # 1. Setup du test

    # 2. exécuter la fonction à tester et récupérer son résultat + vérification
    #    qu'une exception de type FileNotFoundError a été levée.

    # Le test échoue si l'exception désirée n'est pas levée par la fonction
    with pytest.raises(FileNotFoundError):
        resultat = exemple.read_labyrinth_with_exception('doesnotexist.txt')


# Tests de fonctions interagissant avec un utilisateur: mock de input


def test_input_number_returns_user_number_successfully(monkeypatch):
    """Vérifie que la fonction input_number() retourne l'entier désiré si
    l'utilisateur saisit un nombre valide."""

    # 1. Setup du test: simulation d'une saisie utilisateur avec monkeypatch
    USER_NUMBER = 10
    saisie_utilisateur = io.StringIO(str(USER_NUMBER) + '\n')
    monkeypatch.setattr('sys.stdin', saisie_utilisateur)

    # 2. Exécution de la fonction à tester et collecte du résultat
    resultat = exemple.input_number(">>> ")

    # 3. Valider que le résultat est conforme aux attentes
    assert resultat == USER_NUMBER


def test_input_number_returns_user_number_with_error_message(
    monkeypatch, capsys
):
    """Vérifie que la fonction input_number() retourne l'entier désiré au
    essai après un premier nombre invalide saisit par l'utilisateur."""

    # 1. Setup du test: simulation d'une saisie utilisateur
    USER_NUMBER = 10
    ERR_MESSAGE = "Erreur de saisie"
    saisie_utilisateur = io.StringIO(f'pas un nombre\n{USER_NUMBER}\n')
    monkeypatch.setattr('sys.stdin', saisie_utilisateur)

    # 2. Exécution de la fonction à tester et collecte du résultat
    resultat = exemple.input_number(">>> ", err_msg=ERR_MESSAGE)

    # Capture du contenu affiché sur la sortie standard
    capture = capsys.readouterr()

    # 3. Valider que le résultat est conforme aux attentes
    assert resultat == USER_NUMBER
    assert ERR_MESSAGE in capture.out
