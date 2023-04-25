import random
import sys

import pygame as pg


# 練習4: 矢印キーの辞書
delta = {
        pg.K_UP: (0, -1), 
        pg.K_DOWN: (0, +1), 
        pg.K_LEFT: (-1, 0), 
        pg.K_RIGHT: (+1, 0)
}


def check_bound(scr_rct: pg.Rect, obj_rct: pg.Rect) -> tuple[bool, bool]:
    """オブジェクトが画面内または画面外かを判定し、真理値のタプルを返す関数

    Args:
        scr_rct (Rect): 画面SurfaceのRect
        obj_rct (Rect): こうかとんまたは爆弾SurfaceのRect
    
    Returns:
        True: 画面内
        False: 画面外
    """
    
    yoko, tate = True, True
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = False
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((1600, 900))
    clock = pg.time.Clock()
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = (900, 400)
    
    # 練習1: 爆弾の作成
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    
    # 練習2: 爆弾をランダムに配置
    x, y = random.randint(0, 1600), random.randint(0, 900)
    
    # 練習3: 爆弾を移動
    vx, vy = +1, +1
    bb_rct = bb_img.get_rect()
    bb_rct.center = (x, y)
    
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return 0

        tmr += 1
        
        # 演習2: 爆弾の加速度の設定
        if tmr % 1000 == 0:
            vx *= 1.05
            vy *= 1.05
            print(vx, vy)
        
        # 練習4: 矢印キーでの移動
        key_lst = pg.key.get_pressed()
        for k, mv in delta.items():
            if key_lst[k]:
                kk_rct.move_ip(mv)
        
        # 練習5: こうかとんを画面内のみの移動にする
        if check_bound(screen.get_rect(), kk_rct) != (True, True):
            for k, mv in delta.items():
                if key_lst[k]:
                    kk_rct.move_ip(-mv[0], -mv[1])
        
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        
        # 練習5: 爆弾が画面外の場合速度の符号を反転
        yoko, tate = check_bound(screen.get_rect(), bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        # 練習3: 爆弾の表示
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        
        # 練習6: こうかとんと爆弾の衝突判定
        if kk_rct.colliderect(bb_rct):
            return

        pg.display.update()
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()