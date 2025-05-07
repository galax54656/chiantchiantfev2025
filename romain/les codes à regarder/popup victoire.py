"""
            #popup de victoire
        elif running == 2:
            minutes1 = int(win_time // 60)
            secondes1 = int(win_time % 60)
            timer_text = f"time= {minutes1:02}:{secondes1:02}"  # {}=variable 02=format 2 caractères
            timer1 = pygame.font.Font(None, 50).render(timer_text, True, WHITE)
            timer_rect = timer1.get_rect(center=(640, 275))

            tablvictoire.update(screen)
            homebtnn.update(screen)
            backarrowbtn.update(screen)
            screen.blit(timer1, timer_rect)
            screen.blit(gagner1, gagner_rect)
            nom_text.update3(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                    if box_saisie.collidepoint(event.pos):
                        active = True
                    color = color_active if active else color_inactive

                    if homebtnn.checkForInput(pygame.mouse.get_pos()):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        date = datetime.today().strftime("%Y-%m-%d")
                        # creation enregistrement
                        jeu = {"joueur": nom,
                               "level": level,
                               "date": date,
                               "resolutionTime": timer_text

                               }
                        # charger données dans fichier
                        with open('results.json', mode='a') as my_file:
                            json.dump(jeu, my_file)
                            my_file.write('\n')
                        main_menu()

                    if backarrowbtn.checkForInput(pygame.mouse.get_pos()):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        date = datetime.today().strftime("%Y-%m-%d")  # formate date anné-mois-jour
                        # creation enregistrement
                        jeu = {"joueur": nom,
                               "level": level,
                               "date": date,
                               "resolutionTime": timer_text
                               }
                        # charger données dans fichier
                        with open('results.json', mode='a') as my_file:
                            json.dump(jeu, my_file)
                            my_file.write('\n')
                        menu_niveaux()


                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            active = False
                        elif event.key == pygame.K_BACKSPACE:
                            nom = nom[:-1]
                        else:
                            nom += event.unicode

            color = color_active if active else color_inactive
            font = pygame.font.Font(None, 74)
            txt_surface = font.render(nom, True, (255, 255, 255))
            width = max(200, txt_surface.get_width() + 10)
            box_saisie.w = width
            screen.blit(txt_surface, (box_saisie.x + 5, box_saisie.y + 5))
            pygame.draw.rect(screen, color, box_saisie, 2)



        gagné = 0


        # print (gagné)
        if gagné == 5:
            time.sleep(1)
            win_time = temps_écoulé
            jeu_cour = False
            if bien_joué == 0:
                win_sound.play(loops=0)
                bien_joué = 1
                running = 2



        screen.blit(timer, (1138, 660))
        clock.tick(60)
        pygame.display.update()
"""