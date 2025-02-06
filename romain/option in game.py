"""
        #Option ingame
        elif running == 1:

            temps_écoulé_pause = time.time() - moment_appuie
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:  # si appuie sur la souris
                    if quit_button.rect.collidepoint(
                            pygame.mouse.get_pos()):  # lance le menu options si appuie sur options
                        running = 0
                        temps_perdu += temps_écoulé_pause
                    elif home_bouton.checkForInput(event.pos):
                        piece_place = []
                        boxes = []
                        all_l_objects = []
                        board = []

                        main_menu()
                music_button.on_off_music(pygame.mouse.get_pos(), event)
                music_plus_button.change_volume(pygame.mouse.get_pos(), event)
                music_moins_button.change_volume(pygame.mouse.get_pos(), event)
            # Clear the screen
            screen.blit(option_jeu_back, (40, 40))

            menu_mouse_pos = pygame.mouse.get_pos()

            # Create and render the button
            quit_button.update2(screen)
            sound_text.update3(screen)
            volume_text.update3(screen)
            music_button.update2(screen)
            music_plus_button.update2(screen)
            music_moins_button.update2(screen)
            restart_button.changeColor(pygame.mouse.get_pos())
            home_bouton.update(screen)
            home_bouton.changeColor(pygame.mouse.get_pos())
            pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, 300, 60), width=5, border_radius=20)
            volume_bar_width = int(300 * volume)  # Calculate the width of the volume bar based on the volume level
            if volume_bar_width == 300:
                pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, volume_bar_width, 60), border_radius=20)
            else:
                pygame.draw.rect(screen, WHITE, (480 + 84, 440 - 135, volume_bar_width, 60), border_top_left_radius=20,
                                 border_bottom_left_radius=20)
"""
