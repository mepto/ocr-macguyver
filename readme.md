# Jeu: MacGuyver's escape

## Specifications

- Il n'y a qu'un seul niveau. La structure (départ, emplacement des murs, arrivée), devra être enregistrée dans un fichier pour la modifier facilement au besoin.
- MacGyver sera contrôlé par les touches directionnelles du clavier.
- Les objets seront répartis aléatoirement dans le labyrinthe et changeront d’emplacement si l'utilisateur ferme le jeu et le relance.
- La fenêtre du jeu sera un carré pouvant afficher 15 sprites sur la longueur.
- MacGyver devra donc se déplacer de case en case, avec 15 cases sur la longueur de la fenêtre !
- Il récupèrera un objet simplement en se déplaçant dessus.
- Le programme s'arrête uniquement si MacGyver a bien récupéré tous les objets et trouvé la sortie du labyrinthe. S'il n'a pas tous les objets et qu'il se présente devant le garde, il meurt (la vie est cruelle pour les héros).
- Le programme sera standalone, c'est-à-dire qu'il pourra être exécuté sur n'importe quel ordinateur.

## Libs and tools
os
random
pygame


## Elements

### class Board

        width
        height
        add_background(filepath)
        add_humans()
        add_items()
        add_scoreboard()


### class Human

        position_xy(error_if_none)
        image(error_if_none)
        is_alive=True
        victory_phrase="Yay"
        failure_phrase="Argh..."


### class Hero(Human)

        position_x
        position_y
        *is_alive
        image
        items=0
        create_


### class Villain(Human)

        position_x
        position_y
        is_evil=True
        is_static=True
        *is_alive
        image


### class Item

        position_x=randomize_position()
        position_y=randomize_position()
        image
        is_acquired=False


#### def randomize_position()
        set random position
        check_collision()

#### def check_collision()
        humans can't walk through walls
        only hero can grab items
        hero dies if collides with villains
        items can't be in walls
        Items can't appear on human positions

#### def add_background(filepath)
        check_file_exists
        read_file
        implement_instructions

#### def add_humans()
        new Hero(posx, posy)
        new Villain(posx, posy)

#### def add_items()
        new Item(seringe)
        new Item(tube)
        new Item(needle)
        
#### def add_score_board()
        hero.items
        moves

#### def move_human(who, key_pressed)
        if arrow_up or arrow_down:
            check_collistion()
            who.position_y += xx
            moves += 1
        elsif arrow_left or arrow_right:
            check_collistion()
            who.position_x += xx
            moves += 1
