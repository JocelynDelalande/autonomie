Conventions et workflow de développement
========================================

Workflow git
------------

- la branche *master* est la version « vivante » du logiciel
- les branches thématiques partent et reviennent sur *master*
- on fait des branches (ou tags ?) pour les versions déployées en prod
- On essaye de mentionner le ticket en début de message de commit::

    Fix #1234 Restreint l'accès foo bar

    suite du commit

  ::

     #1234 Blabala

     suite du commit message


.. note:: GitHub repère les identifiants de ticket et lie les commits au ticket
          concerné. En présence du mot clef ``Fix`` Il ferme le ticket quand le
          commit est fusionné dans *master*.

Tickets
-------

- Essayer d'avoir un ticket pour chaque bug, même petit (pour meilleur
  reporting)


Les Pull Requests (PR)
----------------------

- on fait ses branches sur le même remote (``CroissanceCommune``) (afin que
  travis puisse tester les PR)
- on essaye d'aller vers des PR thématiques (à l'opposé des
  branches par personne)
- review / test / merge des PR par un autre dév (et pas forcément
  Gaston) ;  au besoin on peut appeler un 2e avis si jugé nécessaire
- on nomme les branches en mentionant l'auteur (initiales) et (si applicable) le
  n° de ticket. ::

    git checkout -b 'jd-1234-better-login-page'

Vérifications à faire par l'auteur :

- L'auteur rebase sa PR sur *master*
- L'auteur teste les migrations entre la dernière release et sa PR, et ajoute
  les revision de merge alembic au besoin
- L'auteur vérifie, en cas de modification des modèles, que
  ``autonomie/scripts/anonymize.py`` anonymise correctement les champs
  ajoutés/modifiés.

.. warning:: Mettre ``WIP:`` dans le titre d'une PR signifie qu'elle **ne doit
             pas être fusionnée** pour l'instant, et qu'elle n'est pas prête pour
             review.

Les releases
------------

- TODO : Tag ? Branche ? reste à définir
- À chaque release on produit un dump SQL anonymisé de référence

Le code
-------

- docstrings et noms de variables en anglais
- commentaire ``#`` en français



Améliorations process diverses
-------------------------------

- On utilise plus les cartouches en début de chaque fichier, mais un
  CONTRIBUTORS à la racine du dépôt
- tester automatiquement (travis) la migration depuis ce dump de référence.
- CONTRIBUTORS.md + retirer les cartouches de contributeurs
