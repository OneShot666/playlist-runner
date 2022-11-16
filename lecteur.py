import pygame
from mutagen.mp3 import MP3
from random import randint, choice
from time import sleep, strftime, gmtime
from copy import deepcopy
from os import getcwd, listdir

""" Documentation
creator : One Shot
name : Playlist Runner
year of creation : 2020
purpose : Python file make to play musics
arguments : (4)
    - sound_gap : Default value = 0.01. The gap of the sound : 1% each time volume sound button is press.
    - randomly : Default value = True. Make the random mode for playlist lecture : Playlist Runner will choose a music 
      to play randomly.
    - mute : Default value = False. Mute the volume (set it to 0%) if activated.
    - theme : Default value = False. Change the theme of the Playlist Runner : black by default, can be white.
requirements : libraries 'pygame', 'mutagen', 'random', 'time' (optional), 'copy' and 'os'.
"""


# ! Ajouter use playlist (sélectionner artiste + confirmer choix + vérifier music jouée)
class Lecteur:
    def __init__(self, name_music=None, sound_gap=0.01, randomly=True, mute=False, theme=False):
        pygame.init()                                                          # ! Améliorer fond transparent (HP)
        pygame.mixer.init()
        self.running = True
        self.musicOn = True
        self.theme0n = theme
        self.endlessOn = not randomly
        self.randomOn = randomly
        self.muteOn = mute
        self.name = "Playlist Runner"
        self.button_fond = ""
        self.button_play = ""
        self.button_pause = ""
        self.button_suivant = ""                                               # Pour changer musiques
        self.button_precedent = ""
        self.button_after = ""                                                 # Pour changer position
        self.button_before = ""
        self.button_restart = ""
        self.button_random = ""
        self.button_endless = ""
        self.button_sound_loud = ""
        self.button_sound_middle = ""
        self.button_sound_low = ""
        self.button_sound_mute = ""
        self.artists = []
        self.current_artist = ""
        self.path = getcwd()                                                   # Obtient la position du fichier actuel
        self.path_music = "D:\\"
        self.Exceptions = ["icon"]
        self.Images = [_ for _ in listdir(f"{self.path}/Images") if not _.startswith("anti-") and _.endswith(".jpg")
                       and _[:-4] not in self.Exceptions]
        self.Images.sort()
        self.Anti_Images = [_ for _ in listdir(f"{self.path}/Images") if _.startswith("anti-") and _.endswith(".jpg")
                            and _[:-4] not in self.Exceptions]
        self.Anti_Images.sort()
        self.Fonts = [_ for _ in listdir(f"{self.path}\Polices") if _.endswith(".ttf")]  # Cherche fichiers polices
        self.police = choice(self.Fonts)                                       # Choisi une police (au hasard)
        self.title_font = pygame.font.Font(f"Polices/{self.police}", 25)       # Charge les polices
        self.default_font = pygame.font.Font(f"Polices/{self.police}", 20)
        self.artist_font = pygame.font.Font(f"Polices/{self.police}", 15)
        self.Song_list = [_ for _ in listdir(f"{self.path_music}\Musiques") if _.endswith(".mp3")]  # Cherche fichiers mp3
        # Choisi une musique (au hasard)
        self.place = self.set_place(name_music)                                # Cherche la music demandée
        self.song_name = self.path_music + f"Musiques/{self.Song_list[self.place]}"  # Acquière nom complet musique
        self.Historique = [self.place]                                         # Use pour précédent avec randomOn
        self.pressed = pygame.key.get_pressed()                                # Touche(s) enfoncée(s)
        self.repeat = -1 if self.endlessOn else 0                              # Gère l'endless mode
        self.sound = 0 if self.muteOn else 0.5                                 # Gère volume son (en % / 100)
        self.old_sound = 0 if self.muteOn else 0.5                             # Save ancien son (pour f° mute)
        self.sound_gap = sound_gap                                             # Décalage son (set_volume)
        self.timelapse = 10                                                    # Décalage temps (set_position_in_music)
        self.current_time = 0                                                  # Affiche position dans la music (en sec)
        self.deplacement = 0                                                   # Gère déplacement dans la music
        self.color = (240, 240, 240)                                           # Gère thème + clr police
        self.transparence = 255
        pygame.display.set_caption(self.name)                                  # Nom du lecteur
        self.icon = pygame.image.load("Images/icon.jpg")
        self.icon.set_colorkey((255, 255, 255))                                # Enlève le fond blanc
        self.icon = pygame.transform.scale(self.icon, (32, 32))
        pygame.display.set_icon(self.icon)                                     # Icon du lecteur
        self.horloge = pygame.time.Clock()                                     # Gère le number de fps
        self.height = 500
        self.width = 300
        self.size = [self.height, self.width]
        self.screen = pygame.display.set_mode(self.size)                       # Affiche fenêtre avec taille image de fond
        self.Run()

    def Run(self):                      # Lettres uses : flèches, C, A, H, I, J, K, L, M, O, Q, T
        print(f"Lancement de la musique n°{self.place} / {len(self.Song_list)}")
        self.set_theme()
        self.play_song()

        while self.running:
            self.update()
            self.horloge.tick(20)
            self.pressed = pygame.key.get_pressed()

            if self.pressed[pygame.K_c]:
                self.show_commandes()

            if self.pressed[pygame.K_UP]:
                self.set_volume(+ self.sound_gap)
            elif self.pressed[pygame.K_DOWN]:
                self.set_volume(- self.sound_gap)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close_lector()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.pause()

                    if event.key == pygame.K_RETURN:
                        self.next_song(1)

                    if event.key == pygame.K_LEFT:
                        self.set_position(- self.timelapse)
                    elif event.key == pygame.K_RIGHT:
                        self.set_position(+ self.timelapse)

                    if event.key == pygame.K_0:
                        self.set_position(pourcentage=0)
                    elif event.key == pygame.K_1:
                        self.set_position(pourcentage=0.1)
                    elif event.key == pygame.K_2:
                        self.set_position(pourcentage=0.2)
                    elif event.key == pygame.K_3:
                        self.set_position(pourcentage=0.3)
                    elif event.key == pygame.K_4:
                        self.set_position(pourcentage=0.4)
                    elif event.key == pygame.K_5:
                        self.set_position(pourcentage=0.5)
                    elif event.key == pygame.K_6:
                        self.set_position(pourcentage=0.6)
                    elif event.key == pygame.K_7:
                        self.set_position(pourcentage=0.7)
                    elif event.key == pygame.K_8:
                        self.set_position(pourcentage=0.8)
                    elif event.key == pygame.K_9:
                        self.set_position(pourcentage=0.9)

                    if event.key == pygame.K_a:
                        self.show_artists()

                    if event.key == pygame.K_h:
                        self.rewind()

                    if event.key == pygame.K_i:
                        self.random()

                    if event.key == pygame.K_j:
                        self.next_song(-1)
                    elif event.key == pygame.K_l:
                        self.next_song(1)

                    if event.key == pygame.K_k:
                        self.pause()

                    if event.key == pygame.K_m:
                        self.mute()

                    if event.key == pygame.K_o:
                        self.endless_mode()

                    if event.key == pygame.K_q:
                        self.close_lector()

                    if event.key == pygame.K_t:
                        self.set_theme()

    def set_place(self, name_music=None):                                       # Check if music ask exist
        if name_music:
            Musics = []
            for i, _ in enumerate(self.Song_list):
                if name_music.lower() in self.Song_list[i].lower():
                    Musics.append(i)

            if len(Musics) == 0:
                print(f"Aucune chanson trouvée avec '{name_music}' en titre ou auteur !")
                place = randint(0, len(self.Song_list) - 1) if self.randomOn else 0
            elif len(Musics) == 1:
                place = Musics[0]
                print(f"Chanson trouvée : '{self.Song_list[place][:-4]}'")
            else:
                place = -1
                print(f"Multiples chansons trouvées : ({len(Musics)})")
                for zik in Musics:
                    print(f"{zik} - '{self.Song_list[zik][:-4]}'")
                while place not in Musics:
                    place = int(input("Quelle chanson voulez-vous écouter ? (donnez l'index) "))
        else:
            place = randint(0, len(self.Song_list) - 1) if self.randomOn else 0

        return place

    def set_theme(self):
        self.theme0n = not self.theme0n

        if self.theme0n:                                                       # Thème sombre (par défaut)
            anti = False
            color = (0, 0, 0)
            self.color = (240, 240, 240)
        else:                                                                  # Thème clair
            anti = True
            color = (255, 255, 255)
            self.color = (15, 15, 15)

        self.button_fond = pygame.image.load(f"Images/{self.modifier_button('fond', anti)}")
        self.button_fond = pygame.transform.scale(self.button_fond, (self.height, self.width))
        self.button_play = pygame.image.load(f"Images/{self.modifier_button('play', anti)}")
        self.button_play.set_colorkey(color)
        self.button_play = pygame.transform.scale(self.button_play, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_pause = pygame.image.load(f"Images/{self.modifier_button('pause', anti)}")
        self.button_pause.set_colorkey(color)
        self.button_pause = pygame.transform.scale(self.button_pause, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_suivant = pygame.image.load(f"Images/{self.modifier_button('suivant', anti)}")
        self.button_suivant.set_colorkey(color)
        self.button_suivant = pygame.transform.scale(self.button_suivant, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_precedent = pygame.image.load(f"Images/{self.modifier_button('precedent', anti)}")
        self.button_precedent.set_colorkey(color)
        self.button_precedent = pygame.transform.scale(self.button_precedent, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_after = pygame.image.load(f"Images/{self.modifier_button('after', anti)}")
        self.button_after.set_colorkey(color)
        self.button_after = pygame.transform.scale(self.button_after, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_before = pygame.image.load(f"Images/{self.modifier_button('before', anti)}")
        self.button_before.set_colorkey(color)
        self.button_before = pygame.transform.scale(self.button_before, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_restart = pygame.image.load(f"Images/{self.modifier_button('restart', anti)}")
        self.button_restart.set_colorkey(color)
        self.button_restart = pygame.transform.scale(self.button_restart, (self.size[1] * 0.2, self.size[1] * 0.2))
        self.button_random = pygame.image.load(f"Images/{self.modifier_button('random', anti)}")
        self.button_random.set_colorkey(color)
        self.button_random = pygame.transform.scale(self.button_random, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_endless = pygame.image.load(f"Images/{self.modifier_button('endless', anti)}")
        self.button_endless.set_colorkey(color)
        self.button_endless = pygame.transform.scale(self.button_endless, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_loud = pygame.image.load(f"Images/{self.modifier_button('sound_loud', anti)}")
        self.button_sound_loud.set_colorkey(color)
        self.button_sound_loud = pygame.transform.scale(self.button_sound_loud, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_middle = pygame.image.load(f"Images/{self.modifier_button('sound_middle', anti)}")
        self.button_sound_middle.set_colorkey(color)
        self.button_sound_middle = pygame.transform.scale(self.button_sound_middle, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_low = pygame.image.load(f"Images/{self.modifier_button('sound_low', anti)}")
        self.button_sound_low.set_colorkey(color)
        self.button_sound_low = pygame.transform.scale(self.button_sound_low, (self.size[1] * 0.1, self.size[1] * 0.1))
        self.button_sound_mute = pygame.image.load(f"Images/{self.modifier_button('sound_mute', anti)}")
        self.button_sound_mute.set_colorkey(color)
        self.button_sound_mute = pygame.transform.scale(self.button_sound_mute, (self.size[1] * 0.1, self.size[1] * 0.1))

    def play_song(self):
        self.current_time = 0
        self.deplacement = 0
        self.song_name = self.path_music + f"Musiques/{self.Song_list[self.place]}"
        pygame.mixer.music.load(self.song_name)                                # Ecrase le dernier fichier chargé !
        pygame.mixer.music.play(self.repeat)                                   # Play endlessly : -1 ; Play x1 : 0

        if not self.musicOn:
            self.pause()

    def update(self):
        self.screen.blit(self.button_fond, (0, 0))
        pygame.mixer.music.set_volume(self.sound)

        self.current_time = pygame.mixer.music.get_pos() / 1000 + self.deplacement  # Temps music joué (en sec)
        song_mutagen = MP3(self.song_name)                                     # Load le format
        song_lenght = song_mutagen.info.length                                 # Récupère la durée (en sec)
        if self.current_time < 0:
            self.current_time = 0
        elif self.current_time > song_lenght:
            self.current_time = song_lenght

        if song_lenght >= 3600:
            current_time_format = strftime('%H:%M:%S', gmtime(self.current_time))
            song_lenght_format = strftime('%H:%M:%S', gmtime(song_lenght))
        else:
            current_time_format = strftime('%M:%S', gmtime(self.current_time))
            song_lenght_format = strftime('%M:%S', gmtime(song_lenght))

        current_song_time = self.default_font.render(f"{current_time_format}", True, self.color)
        current_song_time_size = current_song_time.get_size()
        self.screen.blit(current_song_time, (self.size[0] * 0.1 - current_song_time_size[0] * 0.5,
                                             self.size[1] * 0.9))              # Position dans la music
        pygame.draw.rect(self.screen, self.color, [self.size[0] * 0.2, self.size[1] * 0.9,
                                                   self.size[0] * 0.6, self.size[1] * 0.05],
                         border_radius=int(self.size[1] * 0.05))               # Barre du temps total
        pygame.draw.rect(self.screen, (128, 128, 128), [self.size[0] * 0.2, self.size[1] * 0.9,
                                                        self.current_time / song_lenght * self.size[0] * 0.6,
                                                        self.size[1] * 0.05],
                         border_radius=int(self.size[1] * 0.05))               # Barre du temps actuel (devant)
        current_song_lenght = self.default_font.render(f"{song_lenght_format}", True, self.color)
        current_song_lenght_size = current_song_lenght.get_size()
        self.screen.blit(current_song_lenght, (self.size[0] * 0.9 - current_song_lenght_size[0] * 0.5,
                                               self.size[1] * 0.9))            # Longueur de la music

        if self.current_time >= song_lenght:                                   # Si music finie, lance la suivante
            pygame.time.delay(1000)
            self.next_song(1)

        play_size = self.button_play.get_size()                                # Différents boutons affichés
        self.screen.blit(self.button_suivant, (self.size[0] * 0.7 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_after, (self.size[0] * 0.6 - play_size[0] * 0.5, self.size[1] * 0.7))
        if self.musicOn:
            self.screen.blit(self.button_play, (self.size[0] * 0.5 - play_size[0] * 0.5, self.size[1] * 0.7))
        else:
            self.screen.blit(self.button_pause, (self.size[0] * 0.5 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_before, (self.size[0] * 0.4 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_precedent, (self.size[0] * 0.3 - play_size[0] * 0.5, self.size[1] * 0.7))
        self.screen.blit(self.button_restart, (self.size[0] * 0.2 - play_size[0] * 0.5, self.size[1] * 0.7))

        if self.randomOn:                                                      # Gère random et endless
            self.screen.blit(self.button_random, (self.size[0] * 0.05, self.size[1] * 0.05))

        if self.endlessOn:
            self.screen.blit(self.button_endless, (self.size[0] * 0.15, self.size[1] * 0.05))

        max = self.size[1] * 0.7 - self.sound * self.size[1] * 0.4             # Affiche son
        if self.muteOn or self.sound == 0:
            sujet = self.button_sound_mute
        elif self.sound >= 0.66:
            sujet = self.button_sound_loud
        elif 0.66 > self.sound > 0.33:
            sujet = self.button_sound_middle
        else:
            sujet = self.button_sound_low
        size = sujet.get_size()
        self.screen.blit(sujet, (self.size[0] * 0.82, max - size[1] * 0.5))
        current_sound = self.default_font.render(f"{int(self.sound * 100)}", True, self.color)
        current_sound_size = current_sound.get_size()
        self.screen.blit(current_sound, (self.size[0] * 0.90, max - current_sound_size[1] * 0.5))

        commande = self.default_font.render(f"C : Commandes", True, self.color)
        commande_size = commande.get_size()
        self.screen.blit(commande, (int(self.size[0] * 0.5 - commande_size[0] * 0.5), int(self.size[1] * 0.0)))

        for i in range(len(self.song_name)):
            if self.song_name[i] == "-":
                music = self.song_name[12:i - 1]                               # 12 : 'D:\Musiques/' , -1 : ' '
                artist = self.song_name[i + 2:len(self.song_name) - 4]         # +2 : '- '       , -4 : '.mp3'
                break
        else:
            music = self.song_name[12: len(self.song_name) - 4]
            artist = ""

        music = self.title_font.render(f"{music}", True, self.color)           # Nom de la musique
        music_size = music.get_size()
        self.screen.blit(music, (int(self.size[0] * 0.5 - music_size[0] * 0.5), int(self.size[1] * 0.35)))
        artist = self.title_font.render(f"{artist}", True, self.color)         # Nom du groupe/auteur
        artist_size = artist.get_size()
        self.screen.blit(artist, (int(self.size[0] * 0.5 - artist_size[0] * 0.5), int(self.size[1] * 0.5)))

        if not pygame.mixer.music.get_busy() and self.musicOn:                 # Si music s'arrête, mais pas en pause...
            self.next_song(1)                                                  # ...lance music suivante

        pygame.display.flip()

    def write_message(self, contenu, position_x=0.5, position_y=0.1, duree=3):
        self.transparence = 0
        max = duree * 100

        while self.transparence < max:
            message = self.default_font.render(f"{contenu}", True, self.color)
            message.set_alpha(self.transparence)
            message_size = message.get_size()
            self.screen.blit(message, (int(self.size[0] * position_x - message_size[0] * 0.5), int(self.size[1] * position_y)))
            self.transparence += 1

            pygame.display.flip()
            # self.update()                                                    # ! Problème avec Lecture (redondances)
            # sleep(0.01)                                                      # ! Jolie animation mais lent

        del message

    def show_commandes(self):                                                   # Affiche commandes (use commandes() ?)
        max = self.size[1] * 0.7 - self.sound * self.size[1] * 0.4              # Gère messages autour de son

        artist = self.default_font.render(f"A : Artistes", True, self.color)
        artist_size = artist.get_size()
        self.screen.blit(artist, (int(self.size[0] * 0.5 - artist_size[0] * 0.5), int(self.size[1] * 0.2)))
        debut = self.default_font.render(f"H", True, self.color)
        debut_size = debut.get_size()
        self.screen.blit(debut, (int(self.size[0] * 0.2 - debut_size[0] * 0.5), int(self.size[1] * 0.65)))
        aleatoire = self.default_font.render(f"I", True, self.color)
        self.screen.blit(aleatoire, (int(self.size[0] * 0.07), int(self.size[1] * 0.0)))
        precedent_text = self.default_font.render(f"J", True, self.color)
        precedent_size = precedent_text.get_size()
        self.screen.blit(precedent_text, (int(self.size[0] * 0.3 - precedent_size[0] * 0.5), int(self.size[1] * 0.65)))
        avant = self.default_font.render(f"<-", True, self.color)
        avant_size = avant.get_size()
        self.screen.blit(avant, (int(self.size[0] * 0.4 - avant_size[0] * 0.5), int(self.size[1] * 0.65)))
        pause_text = self.default_font.render(f"K", True, self.color)
        pause_size = pause_text.get_size()
        self.screen.blit(pause_text, (int(self.size[0] * 0.5 - pause_size[0] * 0.5), int(self.size[1] * 0.65)))
        apres = self.default_font.render(f"->", True, self.color)
        apres_size = apres.get_size()
        self.screen.blit(apres, (int(self.size[0] * 0.6 - apres_size[0] * 0.5), int(self.size[1] * 0.65)))
        suivant_text = self.default_font.render(f"L", True, self.color)
        suivant_size = suivant_text.get_size()
        self.screen.blit(suivant_text, (int(self.size[0] * 0.7 - suivant_size[0] * 0.5), int(self.size[1] * 0.65)))
        muet = self.default_font.render(f"M", True, self.color)
        muet_size = muet.get_size()
        self.screen.blit(muet, (int(self.size[0] - muet_size[0] * 1.1), int(max - muet_size[1] * 0.5)))
        infini = self.default_font.render(f"O", True, self.color)
        self.screen.blit(infini, (int(self.size[0] * 0.17), int(self.size[1] * 0.0)))
        monter = self.default_font.render(f"Haut", True, self.color)
        monter_size = monter.get_size()
        self.screen.blit(monter, (int(self.size[0] * 0.9 - monter_size[0] * 0.5), int(max - monter_size[1] * 1.6)))
        baisser = self.default_font.render(f"Bas", True, self.color)
        baisser_size = baisser.get_size()
        self.screen.blit(baisser, (int(self.size[0] * 0.9 - baisser_size[0] * 0.5), int(max + baisser_size[1] * 0.6)))
        theme = self.default_font.render(f"T : Thème", True, self.color)
        theme_size = theme.get_size()
        self.screen.blit(theme, (int(self.size[0] * 0.5 - theme_size[0] * 0.5), int(self.size[1] * 0.1)))
        quitter = self.default_font.render(f"Q", True, self.color)
        quitter_size = quitter.get_size()
        self.screen.blit(quitter, (int(self.size[0] * 0.97 - quitter_size[0]), int(self.size[1] * 0.0)))
        pygame.display.flip()
        sleep(1)

    def modifier_button(self, nom_image, anti=False):
        if not nom_image.endswith(".jpg"):
            nom_image += ".jpg"

        if anti:
            nom_image = "anti-" + nom_image
            if nom_image in self.Anti_Images:
                return str(nom_image)
        else:
            if nom_image in self.Images:
                return str(nom_image)

        return self.__class__.__name__

    def get_artists(self):
        self.artists = []

        for song in self.Song_list:
            artist = {"artist": "", "musics": []}
            for i in range(len(song)):
                if song[i] == "-":
                    music = song[: i - 1]
                    artist["artist"] = song[i + 2: - 4]
                    break
            else:
                music = song[: - 4]

            artist["musics"].append(music)

            for group in self.artists:
                if artist["artist"] in group["artist"]:
                    group["musics"].append(music)
                    break
            else:
                self.artists.append(artist)

        self.artists.sort(key=lambda x: x["artist"])

    def show_artists(self):
        if not self.artists:                                                   # Si liste artistes non définie
            self.get_artists()

        position = 0

        while position < len(self.artists) - 1:                                # Affiche élément de liste par 10
            titre = self.artist_font.render(f"Artistes : ({len(self.artists)})", True, self.color)
            titre_size = titre.get_size()
            self.screen.blit(titre, (int(self.size[0] * 0.2 - titre_size[0] * 0.5), int(self.size[1] * 0.2)))

            for i in range(10):
                try:
                    element = self.artist_font.render(
                        f"{self.artists[position]['artist']} (x{len(self.artists[position]['musics'])})",
                        True, self.color)
                    element_size = element.get_size()
                    self.screen.blit(element, (int(self.size[0] * 0.2 - element_size[0] * 0.5),
                                               int(self.size[1] * 0.25 + element_size[1] * 0.75 * i)))
                except IndexError:
                    break

                position += 1
                pygame.display.update()
                sleep(0.2)
                del element, element_size

            sleep(3)
            self.update()

        del titre, titre_size

    def get_song_list(self):
        for i in self.Song_list:
            print(i)
            sleep(0.1)

    def endless_mode(self):
        self.endlessOn = not self.endlessOn

        if self.endlessOn:
            self.write_message("Mode infini activé")
            self.repeat = - 1
            # pygame.mixer.music.queue(self.song_name)                         # Load music actuelle ?
            if self.randomOn:
                self.random()
        else:
            self.write_message("Mode infini désactivé")
            self.repeat = 0

    def set_volume(self, gap: float):
        if self.muteOn:
            self.mute()

        self.sound += gap
        self.sound *= 100
        self.sound = round(self.sound)
        self.sound /= 100

        if self.sound < 0:
            self.sound = 0
        elif self.sound > 1:
            self.sound = 1

        self.old_sound = self.sound

    def set_position(self, timelapse=0, pourcentage=None):
        song_mutagen = MP3(self.song_name)
        duree_total = song_mutagen.info.length                                 # Durée (en sec)

        if pourcentage is not None:
            self.deplacement = duree_total * pourcentage
        else:
            self.deplacement = deepcopy(self.current_time) + timelapse
        self.current_time = self.deplacement                                   # Temps music joué (en sec)

        if self.current_time < 0:
            self.current_time = 0
        elif self.current_time > duree_total:
            self.current_time = duree_total
        pygame.mixer.music.play(self.repeat, self.current_time)                # play(start : en secs)

        if not self.musicOn:                                                   # Enlève la pause après déplacement
            self.pause()

    def next_song(self, direction=0):
        if self.endlessOn:
            pass
        elif self.randomOn:                                                     # Si le mode Random est activé
            if direction < 0:
                self.write_message("Précédent")
                place = -1 if len(self.Historique) < 2 else -2
                self.place = self.Historique[place]
            elif direction > 0:
                self.write_message("Suivant")
                self.place = randint(0, len(self.Song_list) - 1)
                while self.place in self.Historique:        # Empêche le lecteur de jouer une musique déjà jouée
                    self.place = randint(0, len(self.Song_list) - 1)
                self.Historique.append(self.place)
        else:
            if direction < 0:
                self.write_message("Précédent")
                self.place -= 1
                if self.place < 0:
                    self.place = len(self.Song_list) - 1
                self.Historique.append(self.place)
            elif direction > 0:
                self.write_message("Suivant")
                self.place += 1
                if self.place > len(self.Song_list) - 1:
                    self.place = 0
                self.Historique.append(self.place)
        print(f"Historique : {self.Historique}")

        self.play_song()

    def pause(self):
        self.musicOn = not self.musicOn

        if self.musicOn:                                                       # Reprend la musique où elle s'est arrêtée
            self.write_message("Lecture")
            pygame.mixer.music.unpause()
        else:                                                                  # Met sur pause la musique actuelle
            self.write_message("Pause")
            pygame.mixer.music.pause()

    def mute(self):
        self.muteOn = not self.muteOn

        if self.muteOn:
            self.write_message("Mode muet activé")
            self.sound = 0
        else:
            self.write_message("Mode muet désactivé")
            self.sound = self.old_sound

    def random(self):
        self.randomOn = not self.randomOn

        if self.randomOn:
            self.write_message("Mode aléatoire activée")
            if self.endlessOn:
                self.endless_mode()
        else:
            self.write_message("Mode aléatoire désactivée")

    def rewind(self):                                                           # Remet musics au début (sans interrompres)
        self.write_message("Relecture au début")
        self.play_song()

    def close_lector(self):                                                     # Ferme le lecteur de musique
        self.write_message("Fermeture de Playlist runner")
        self.running = False


if __name__ == "__main__":
    lecteur = Lecteur()

"""           Format          """
# ogg : compressé
# wav : qualité
# mp3 : lu par music (pas par mixer)
