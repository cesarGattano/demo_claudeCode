# Séance 1 — Premiers pas avec Claude Code

**Durée** : 30 min · **Public** : ingénieurs Python, première découverte d'un assistant de code

## Objectif

À la fin de la séance, les collègues ont compris que Claude Code n'est **pas un chat** : c'est un **agent** qui lit le projet, propose un plan, écrit des fichiers et exécute des commandes, toujours sous le contrôle du développeur.

**Fil rouge** : à partir d'un dépôt vide, obtenir un script qui cherche la scène Sentinel-2 la moins nuageuse sur une zone et affiche une carte NDVI.

**Message à retenir** : « Je décris l'intention, Claude propose, je valide. »

## Déroulé minuté

| Temps | Étape | Capacité montrée |
|---|---|---|
| 0:00 – 0:03 | Introduction | Chat ou agent : quelle différence ? |
| 0:03 – 0:06 | Étape 1 : le contexte du projet | CLAUDE.md, lecture du dépôt |
| 0:06 – 0:12 | Étape 2 : planifier | Mode Plan |
| 0:12 – 0:19 | Étape 3 : exécuter le plan | Écriture de fichiers, commandes, permissions |
| 0:19 – 0:23 | Étape 4 : voir le résultat et itérer | Boucle courte de modification |
| 0:23 – 0:30 | Questions et teaser de la séance 2 | — |

---

## Introduction (3 min)

À dire, sans écran de code :

- En mode chat, on copie-colle du code dans une fenêtre, puis on recopie la réponse dans l'éditeur.
- Claude Code travaille **directement dans le projet** : il lit les fichiers, les modifie et lance des commandes dans le terminal.
- Chaque action sensible (écrire un fichier, lancer une commande) **demande une autorisation**. On garde la main.
- Aujourd'hui : partir d'un dépôt vide et obtenir une carte NDVI à partir de vraies données Sentinel-2.

## Étape 1 — Le contexte du projet (3 min)

Montrer à l'écran le dépôt presque vide, puis ouvrir `CLAUDE.md`.

**Prompt :**

```
Que sais-tu de ce projet et de ce qu'on va faire ensemble ?
```

**Résultat attendu** : Claude résume le contexte (observation de la Terre, démonstrations, données ouvertes) sans qu'on l'ait réexpliqué.

**Point pédagogique** : `CLAUDE.md` est la **mémoire du projet**. On y écrit une fois les conventions, le contexte et les contraintes, et Claude les relit à chaque session. C'est l'équivalent d'un document d'accueil pour un nouveau collègue.

## Étape 2 — Planifier avant de coder (6 min)

Passer en **mode Plan** (sélecteur de mode dans le panneau Claude, ou `Shift+Tab`).

**Prompt :**

```
Je veux un script Python qui :
- cherche, via le catalogue STAC Earth Search, la scène Sentinel-2 L2A
  la moins nuageuse sur la Beauce (bbox 1.40, 48.30, 1.50, 48.36) en juillet 2025 ;
- lit uniquement les bandes rouge et proche infrarouge sur cette emprise ;
- calcule le NDVI et l'enregistre en image PNG avec une légende.
Propose-moi un plan.
```

**Résultat attendu** : un plan en quelques étapes. Il doit couvrir les bibliothèques (`pystac-client`, `rasterio`, `numpy`, `matplotlib`), la recherche STAC, la lecture fenêtrée des COG, le calcul du NDVI et l'export de l'image.

**Commenter à voix haute :**
- Claude n'a encore **rien modifié**. Le mode Plan sert à se mettre d'accord avant d'agir.
- Lire le plan de façon critique. Si Claude ne parle pas de la reprojection de l'emprise (la bbox est en WGS84, les images en UTM), le faire remarquer. C'est un bon exemple de relecture métier.

**Prompt d'ajustement** (optionnel, pour montrer qu'on peut modifier le plan) :

```
Mets les paramètres (bbox, dates, couverture nuageuse max) en haut du script
pour pouvoir les changer facilement.
```

Puis **valider le plan**.

## Étape 3 — Exécuter le plan (7 min)

Claude enchaîne les actions. **Laisser les demandes d'autorisation s'afficher** et les commenter, c'est le cœur de la démonstration :

1. **Installation des dépendances** (`pip install ...`) : Claude demande l'autorisation de lancer une commande. Lire la commande à voix haute avant d'accepter.
2. **Création du fichier** (par exemple `ndvi.py`) : montrer le diff proposé dans VSCode avant d'accepter.
3. **Exécution du script** : Claude lance le script, lit la sortie et corrige seul en cas d'erreur.

**Points pédagogiques :**
- Le développeur reste **décisionnaire** : rien n'est écrit ni exécuté sans son accord (dans le mode par défaut).
- Si une erreur survient, Claude lit le message, comprend et corrige. C'est la boucle agentique. **Une erreur ici est une bonne nouvelle pour la démo** : la commenter plutôt que s'en excuser.

## Étape 4 — Voir le résultat et itérer (4 min)

Ouvrir le PNG généré dans VSCode et le commenter : parcelles agricoles, contraste entre cultures et sols nus.

**Prompt d'itération :**

```
Ajoute à côté du NDVI la vue en couleurs naturelles de la même zone
pour comparer.
```

**Résultat attendu** : une figure avec deux panneaux, couleurs naturelles et NDVI.

**Point pédagogique** : une fois la base en place, chaque évolution se demande en une phrase. On reste au niveau de l'**intention métier**, pas de la syntaxe matplotlib.

Pour conclure la démo :

```
Commite ce travail avec un message clair.
```

## Questions et teaser (7 min)

Questions qui reviennent souvent, à préparer :
- **Le code est-il fiable ?** Pas automatiquement. On relit comme une contribution d'un collègue. La séance 2 sera consacrée aux tests et à la fiabilisation.
- **Où partent mes données ?** Le code et les fichiers lus par Claude sont envoyés à l'API d'Anthropic. D'où notre contrainte : données 100 % ouvertes pour cette démo.
- **Combien ça coûte ?** Démo réalisée avec un abonnement Claude Pro personnel.

**Teaser de la séance 2** : « Ce script fonctionne, mais est-ce qu'on lui fait confiance ? La prochaine fois, on le transforme en package testé, et on chasse les bugs classiques : CRS, nodata, nuages. »

---

## Préparation (avant la séance)

### Matériel et environnement

- [ ] Environnement virtuel Python créé et activé dans le dépôt (`python -m venv .venv`), **sans** les dépendances (Claude les installe en direct).
- [ ] Vérifier que `.venv/` est bien dans `.gitignore`.
- [ ] Connexion réseau testée vers `https://earth-search.aws.element84.com/v1`.
- [ ] VSCode : police agrandie (`Ctrl+=` deux ou trois fois), notifications coupées, onglets inutiles fermés.
- [ ] Panneau Claude Code ouvert, **nouvelle conversation** (pas d'historique de la répétition).
- [ ] Mode de permission par défaut (pour que les demandes d'autorisation soient visibles).

### Répétition et filet de sécurité

1. Partir de l'état initial et le marquer : `git tag session-01-debut`.
2. Faire une répétition complète sur une branche : `git switch -c repetition-01`.
3. Si le résultat est bon, le marquer : `git tag session-01-fin`. Garder une capture du PNG obtenu.
4. Revenir à l'état initial : `git switch dev`.

## Plan B

| Problème | Réaction |
|---|---|
| Le catalogue STAC est lent ou ne répond pas | Montrer la capture du PNG obtenu en répétition et expliquer le code de `session-01-fin` (`git switch --detach session-01-fin`). |
| Aucune scène trouvée | Élargir à juin–août 2025 ou monter le seuil de nuages. C'est aussi un bon exemple d'itération. |
| Claude part dans une mauvaise direction | Refuser l'action, reformuler le prompt. Montrer qu'on garde la main **fait partie de la démo**. |
| Plus de temps | Sauter l'étape 4 et finir sur le commit de `session-01-fin`. |
