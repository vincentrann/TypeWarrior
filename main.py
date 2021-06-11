import pygame
from pygame.locals import *
import sys
import time
import random
from operator import itemgetter
import pickle
scoreboard = []
class Game:
    def __init__(self):
        pygame.init()
        self.start = False
        self.stop = False
        self.w = 750
        self.h = 500
        self.user_input = ''
        self.final_input = ''
        self.sentence = ''
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.accuracy = 0
        self.rank = ''
        self.results = ''
        self.click = False
        self.player_name = 'cool'

        self.scoreboard = []

        self.rank_img = pygame.image.load('Season_2019_-_Bronze_2.png')
        self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))

        self.input_box = pygame.Rect(50,250,650,50)
        self.exit_box = pygame.Rect(206,413,119,70)
        self.retry_box = pygame.Rect(389,411,122,73)
        self.back_box = pygame.Rect(0,0,90,40)

        self.menu_bg = pygame.image.load('typewarrior.JPG')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (750,500))

        self.score_bg = pygame.image.load('scoreboard.JPG')
        self.score_bg = pygame.transform.scale(self.score_bg, (750, 500))

        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Type Warrior')

    def getSentence(self):
        o = open('AllTexts.txt').read()
        quotes = o.split('\n')
        quote = random.choice(quotes)
        return quote

    def displayText(self, screen, message, y, font_size, colour=(250,250,250)):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, 1, colour)
        text_pos = text.get_rect(center= (self.w/2, y))
        screen.blit(text, text_pos)
        if self.start:
            pygame.draw.rect(self.screen, (0, 0, 128), self.input_box, 2)
        else:
            pygame.draw.rect(self.screen, (255,255,255), self.input_box, 2)
        pygame.display.update()

    def displayScore(self,screen, message, x, y, font_size, colour=(250,250,250)):
        font = pygame.font.SysFont('comicsansms', font_size)
        text = font.render(message, False, colour)
        text_pos = text.get_rect(center=(x, y))
        screen.blit(text, text_pos)
        pygame.display.update()

    def displayQuote(self, screen, quote, pos, font_size, colour=(225,225,225)):
        font = pygame.font.Font(None, font_size)
        words = [word.split(' ') for word in quote.splitlines()]
        space = font.size(' ')[0]
        mw, mh = screen.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = font.render(word, 10, colour)
                ww, wh = word_surface.get_size()
                if x + ww >= mw:
                    x = pos[0]
                    y += wh
                screen.blit(word_surface, (x,y))
                x += ww + space
            x = pos[0]
            y += wh

    def displayResults(self):
        if not self.stop:
            # time
            self.total_time = time.time() - self.start_time

            # accuracy
            count = 0
            for i, c in enumerate(self.sentence):
                try:
                    if self.final_input[i] == c:
                        count += 1
                except:
                    pass
            self.accuracy = count/len(self.sentence)*100

            # wpm
            self.wpm =  len(self.final_input)*60/(5*self.total_time)
            self.end = True

            # rank
            if self.wpm <=24:
                self.rank = 'Bronze'
                self.rank_img = pygame.image.load('Season_2019_-_Bronze_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))
            elif self.wpm <= 30:
                self.rank = 'Silver'
                self.rank_img = pygame.image.load('Season_2019_-_Silver_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))
            elif self.wpm <= 41:
                self.rank = 'Gold'
                self.rank_img = pygame.image.load('Season_2019_-_Gold_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))
            elif self.wpm <= 54:
                self.rank = 'Platinum'
                self.rank_img = pygame.image.load('Season_2019_-_Platinum_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))
            elif self.wpm <= 79:
                self.rank = 'Diamond'
                self.rank_img = pygame.image.load('Season_2019_-_Diamond_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))
            elif self.wpm >= 80:
                self.rank = 'Warrior'
                self.rank_img = pygame.image.load('Season_2019_-_Challenger_2.png')
                self.rank_img = pygame.transform.scale(self.rank_img, (100, 100))

            self.results = 'Time: ' + str(round(self.total_time)) + " secs Accuracy: " + str(round(self.accuracy)) + '% Wpm: ' + str(round(self.wpm)) + ' Rank: '  + self.rank

            # buttons
            self.exit_img = pygame.image.load('exit button.png')
            self.exit_img = pygame.transform.scale(self.exit_img, (150,150))

            self.retry_img = pygame.image.load('retry button.png')
            self.retry_img = pygame.transform.scale(self.retry_img, (150,109))

            pygame.display.update

    def mainGame(self):
        running = True

        self.resetGame()
        self.sentence = self.getSentence()
        words = [word.split(' ') for word in self.sentence.splitlines()]
        space_count = 0

        while running:
            self.screen.fill((0,0,0))
            # user input

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.start = True
                        self.start_time = time.time()
                    if self.retry_box.collidepoint(event.pos):
                        scoreboard.append([self.player_name, round(self.wpm), self.results])
                        with open('pickled_scoreboard.pickle', 'wb') as f:
                            pickle.dump(scoreboard, f)
                        self.resetGame()
                        self.sentence = self.getSentence()
                        words = [word.split(' ') for word in self.sentence.splitlines()]
                        space_count = 0
                    if self.exit_box.collidepoint(event.pos):
                        running = False
                        scoreboard.append([self.player_name, round(self.wpm), self.results])
                        with open('pickled_scoreboard.pickle', 'wb') as f:
                            pickle.dump(scoreboard, f)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        if self.stop:
                            scoreboard.append([self.player_name, round(self.wpm), self.results])
                            with open('pickled_scoreboard.pickle',  'wb') as f:
                                pickle.dump(scoreboard, f)
                        running = False
                    elif self.start and not self.stop:
                        if event.key == pygame.K_SPACE:
                            self.user_input = ''
                            space_count += 1
                            self.final_input += event.unicode
                        elif event.key == pygame.K_BACKSPACE:
                            self.user_input = self.user_input[:-1]
                            self.final_input = self.final_input[:-1]
                        else:
                            self.user_input += event.unicode
                            self.final_input += event.unicode

            self.displayQuote(self.screen, self.sentence, (0, 0), 30)

            if space_count == len(words[0]):
                self.displayResults()
                self.screen.blit(self.rank_img, (616, 295))
                self.screen.blit(self.exit_img, (self.w/4, self.h-140))
                self.screen.blit(self.retry_img, (self.w/2, self.h-110))
                self.displayText(self.screen, self.results, 350, 28)
                self.stop = True

            self.displayText(self.screen, self.user_input, 274, 26)

            pygame.display.update()
            self.clock.tick(60)

    def score(self):
        running = True
        self.screen.blit(self.score_bg, (0, 0))

        self.back_arrow = pygame.image.load('back arrow.png')
        self.back_arrow = pygame.transform.scale(self.back_arrow, (90,40))
        self.screen.blit(self.back_arrow, (0,0))

        while running:
            y = 50
            y2 = 68
            num = 1
            with open('pickled_scoreboard.pickle', 'rb') as f:
                new_scoreboard = pickle.load(f)

            for i in range(9):
                self.score_box = pygame.Rect(0, 42, 750, y)
                pygame.draw.rect(self.screen, (225, 225, 225), self.score_box, 2)
                self.displayScore(self.screen, str(num), 20, y2, 26)
                y += 50
                y2 += 49
                num += 1

            if len(new_scoreboard) > 1:
                new_scoreboard = sorted(scoreboard, key=itemgetter(1), reverse=True)
                if len(new_scoreboard) > 9:
                    del new_scoreboard[8:]

            if len(new_scoreboard) > 0:
                y2 = 68
                for score in new_scoreboard:
                    self.displayScore(self.screen, score[0]+': '+score[2], self.w/2, y2, 20)
                    y2 += 49

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_box.collidepoint(event.pos):
                        running = False

                pygame.display.update()
                self.clock.tick(60)

    def menu(self):
        while True:
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(258, 196, 239, 109)
            button_2 = pygame.Rect(248, 349, 254, 114)
            if button_1.collidepoint((mx, my)):
                if self.click:
                    self.mainGame()
                    self.click = False
            if button_2.collidepoint((mx,my)):
                if self.click:
                    self.score()
                    self.click = False
            pygame.draw.rect(self.screen, (255, 255, 255), button_1)
            pygame.draw.rect(self.screen, (255, 255, 255), button_2)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click = True
                if event.type == MOUSEBUTTONUP:
                    self.click = False

            self.screen.blit(self.menu_bg,(0,0))

            pygame.display.update()
            self.clock.tick(60)

    def resetGame(self):
        self.start = False
        self.stop = False
        self.final_input = ''
        self.sentence = ''
        self.start_time = 0
        self.total_time = 0
        self.wpm = 0
        self.accuracy = 0
        self.rank = ''
        self.results = ''


Game().menu()














