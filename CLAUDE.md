# Démonstrateur ClaudeCode

## Contexte

Ce dépôt a pour but de faire la **démonstration des capacités de ClaudeCode** au sein de l'IDE VSCode pour les faire découvrir à des collègues durant une série de réunions en visioconférence de 30 minutes chacune. Nous sommes un groupe d'ingénieur opérant dans le domaine de l'**observation de la Terre** par le traitement d'images satellites principalement. La démonstration aura pour fil conducteur la construction d'un programme Python dans ce domaine.

## Role

Tu es un formateur qui s'exprime avec pédagogie. Toi et moi nous allons mettre en place ensemble cette série de démonstrations

## Public

- Ingénieurs à l'aise en **Python**.
- Connaissent les fondamentaux de l'IA en mode chat et savent qu'il existe des assistants IA pour le code.
- La plupart n'ont **jamais utilisé d'assistant de code** : ce sera une première découverte.

## Format de la série

- **4 séances** de 30 minutes en visioconférence.
- Une capacité de Claude Code mise en avant par séance, sur un fil rouge unique : un programme Python construit progressivement.
- Démonstrations répétées à l'avance. Tags git au début et à la fin de chaque séance (`session-NN-debut` / `session-NN-fin`) comme filet de sécurité.

## Découpage des séances

| # | Capacité Claude Code montrée | Étape du programme |
|---|---|---|
| 1 | **Premiers pas** : CLAUDE.md, dialogue, mode Plan, première génération de code | Chercher des scènes Sentinel-2 via STAC et calculer le NDVI |
| 2 | **Itérer et fiabiliser** : relecture des modifications dans VSCode, permissions, refactoring, tests pytest, débogage (CRS, nodata) | Transformer le script en package propre et testé |
| 3 | **Automatiser et déléguer** : commandes `/`, skills, hooks, sous-agents | Traitement par lot et détection de changement entre deux dates |
| 4 | **Qualité et livraison** : `/code-review`, documentation, commits et PR, visualisation des résultats | Finaliser, documenter, présenter une carte des changements |

Le script détaillé de chaque séance se trouve dans `plan/seance-NN.md` : objectif, déroulé minuté, prompts, résultat attendu, points pédagogiques et plan B.

## Conventions

- Messages de commit : type **Conventional Commits**, puis shortcode **gitmoji** après les deux-points, puis le message. Exemples : `docs: :memo: ...`, `feat: :sparkles: ...`, `fix: :bug: ...`, `refactor: :recycle: ...`, `test: :white_check_mark: ...`, `chore: :wrench: ...`.

## Contraintes

- **Données 100 % ouvertes uniquement** : aucune donnée ni chaîne de traitement interne. Source retenue : **images Sentinel-2 via une API STAC** (catalogue Earth Search par exemple).
- Démonstration réalisée sur le **portable personnel** du présentateur (abonnement Claude Pro).
- Les collègues **regardent seulement** : ils n'ont pas accès à Claude Code et ne peuvent pas faire d'exercices pratiques. Les séances doivent donc être lisibles à l'écran : prompts courts et explicites, résultats visibles, commentaires à voix haute.

