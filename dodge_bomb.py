import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-30),
    pg.K_DOWN:(0,+30),
    pg.K_LEFT:(-30,0),
    pg.K_RIGHT:(+30,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    yoko,tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def create_bomb() -> tuple[pg.Surface, pg.Rect, int, int]:
    """
    新しい爆弾のSurface, Rect, 速度vx, vyを生成して返す。
    """
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = random.choice([-20, 20]), random.choice([-20, 20])
    return bb_img, bb_rct, vx, vy





def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
   

    bombs = [create_bomb()]

    clock = pg.time.Clock()
    font = pg.font.Font(None, 80)
    tmr = 0

    overlay = pg.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    kk2_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if tmr % 50 == 0:
            bombs.append(create_bomb()) 
        
        for bb_img, bb_rct, vx, vy in bombs:
            if kk_rct.colliderect(bb_rct):
                screen.blit(overlay, (0, 0))
                game_over_text = font.render("Game Over", True, (255, 255, 255))
                screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2 - 40))
                
                kk2_rct = kk2_img.get_rect()
                kk2_rct.center = 350,300
                screen.blit(kk2_img, kk2_rct)
                kk2_rct = kk2_img.get_rect()
                kk2_rct.center = 700,300
                screen.blit(kk2_img, kk2_rct)

                pg.display.update()
                time.sleep(5)
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        for i, (bb_img, bb_rct, vx, vy) in enumerate(bombs):
            bb_rct.move_ip(vx,vy)
          

            if bb_rct.left < 0 or bb_rct.right > WIDTH:
                vx *= -1
            if bb_rct.top < 0 or bb_rct.bottom > HEIGHT:
                vy *= -1
            bombs[i] = (bb_img, bb_rct, vx, vy)
            screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
