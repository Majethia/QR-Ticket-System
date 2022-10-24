import pygame
import sys
import sqlite3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri', 25)

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


SCREEN.fill(WHITE)
textsurface = font.render(f"Loading Google Forms...", False, BLACK)
SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 50))

pygame.display.update()
connection = sqlite3.connect('db.sqlite3')
cur = connection.cursor()


def check_transactions():
    query = "SELECT * FROM TedXDypit WHERE Approved='R'"
    cur.execute(query)
    applications = cur.fetchall()
    max = len(applications)
    current = 0
    run = True
    if max == 0:
        run = False
    while run:
        query = "SELECT * FROM TedXDypit WHERE Approved='R'"
        cur.execute(query)
        try:
            current_application = cur.fetchall()[0]
        except:
            run = False
            sys.exit()

        image = pygame.image.load(f"downloads/{current_application[6]}.png")
        image = pygame.transform.scale(image, (400, 800))
        SCREEN.fill(WHITE)
        SCREEN.blit(image, (0, 0))
        textsurface = font.render(f"Name - {current_application[1]}", False, BLACK)
        SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 50))
        textsurface = font.render(f"Ph Number - {current_application[2]}", False, BLACK)
        SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 100))
        textsurface = font.render(f"Email - {current_application[3]}", False, BLACK)
        SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 150))
        textsurface = font.render(f"Press Enter to approve", False, BLACK)
        SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 200))
        textsurface = font.render(f"Press Space to Skip", False, BLACK)
        SCREEN.blit(textsurface,(WINDOW_WIDTH/2 + 27, 250))
        pygame.display.update()
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                query = f"UPDATE TedXDypit SET Approved='Y' WHERE Id={applications[current][0]}"
                cur.execute(query)
                connection.commit()
                current += 1

            elif event.key == pygame.K_SPACE:
                query = f"UPDATE TedXDypit SET Approved='N' WHERE Id={applications[current][0]}"
                cur.execute(query)
                connection.commit()
                current += 1

check_transactions()