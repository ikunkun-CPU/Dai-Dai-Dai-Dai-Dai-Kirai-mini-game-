# -*- coding: utf-8 -*-
import asyncio
import pygame as pg
import random
import sys
import os

def resource_path(relative_path):
    """ 获取资源的绝对路径，兼容 PyInstaller 打包 """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时解压目录
        return os.path.join(sys._MEIPASS, relative_path)
    # 源码运行时的当前目录
    return os.path.join(os.path.abspath("."), relative_path)

class img(pg.sprite.Sprite):
    def __init__(self,lu:str,tou:bool=False,p:int=1):
        super().__init__()
        self.tu_name = lu
        self.p = p
        #是透明图片就透明处理，不是那算了
        if tou:
            self.image = pg.image.load(resource_path("images/"+lu)).convert_alpha()
        else:
            self.image = pg.image.load(resource_path("images/"+lu)).convert()
        #保存原图片，用于旋转计算而不丢失图片精度
        self.yuan_img = self.image
        self.du = 0
        self.suo_x = 1
        self.suo_y = 1

        self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=True)
        self.baiimg_yuan = self.baiimg
        #获取图片方形碰撞箱
        self.rect = self.image.get_rect()

        self.vel_y = 0
        self.vel_x = 0
        self.tiao_bool = False
        self.tiao_an = 0
        self.tiao_zhu = False
        self.shuai = False
        self.gun = False
        self.vel_gun = 1
        self.gun_NOchu = True
        self.hp = 10

        self.qing = 0

        self.shou_ou = False
        self.shou_time = 0
        self.shou_jian = 10
        self.pian_x = 0
        self.pian_y = 0
        self.shou_tu = False
        self.shou_tu_ji = 0

        self.bai_xian = False
        self.bai_time = 0
        self.bai_tou = 255
        self.bai_new = False

        self.move_kong = True
        self.huo = True
        self.huo_NOchu = True
        self.NOting = True

        self.shang = False
        self.shanghai = 0

    def baitou(self,toudu):
        self.baiimg.set_alpha(toudu)

    #绘制
    def draw(self,win):
        if self.NOting:
            if self.du != 0:
                win.blit(self.image,((self.rect.centerx-self.image.get_width()/2)+self.pian_x,self.rect.centery-self.image.get_height()/2+self.pian_y))
            else:
                win.blit(self.image,(self.rect.x+self.pian_x,self.rect.y+self.pian_y))

            if self.bai_xian:
                if self.bai_time > 0:
                    self.bai_new = True
                    self.bai_time -= 1
                    if self.bai_tou-20 < 0:
                        self.baiimg.set_alpha(0)
                        self.bai_tou = 0
                        self.bai_time = 0
                    else:
                        self.baiimg.set_alpha(self.bai_tou-20)
                        self.bai_tou-=15
                    if self.du != 0:
                        win.blit(self.baiimg,((self.rect.centerx-self.image.get_width()/2)+self.pian_x,self.rect.centery-self.image.get_height()/2+self.pian_y))
                    else:
                        win.blit(self.baiimg,(self.rect.x+self.pian_x,self.rect.y+self.pian_y))
                else:
                    self.bai_xian = False
            else:
                if self.bai_new:
                    self.bai_tou = 255
                    self.baiimg.set_alpha(2555)
                    self.bai_new = False

    def qie(self,lu,tou):
        self.tu_name = lu
        lin_cen = self.rect.center
        if tou:
            self.image = pg.image.load(resource_path("images/"+lu)).convert_alpha()
        else:
            self.image = pg.image.load(resource_path("images/"+lu)).convert()
        self.yuan_img = self.image
        self.rect = self.image.get_rect()
        self.rect.center = lin_cen

        self.baiimg_yuan = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=tou)

        if self.suo_y != 0 or self.suo_x != 0:
            self.suo(self.suo_x,self.suo_y)
        if self.du != 0:
            lin = self.du
            self.zhuan(self.du,True)
            self.du = lin

        self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=tou)

    #缩放函数
    def suo(self,xANDy:int,y:int=0):
        #临时保存缩放前物品中心坐标
        lin = self.rect.center
        self.suo_x = xANDy
        if y == 0:
            self.image = pg.transform.scale_by(self.image,xANDy)
            self.suo_y = xANDy
        else:
            self.image = pg.transform.scale(self.image,(self.rect.width*xANDy,self.rect.height*y))
            self.suo_y = y
        #缩放后重新获取碰撞箱并移动回原来位置
        self.rect = self.image.get_rect()
        self.rect.center = lin
        self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=True)

    #旋转函数
    def zhuan(self,du,she=False):
        if she:
            if du > 360 or du < -360:
                self.du = du % 360
            if self.du == 0:
                self.image = self.yuan_img
            else:
                self.image = pg.transform.rotate(self.yuan_img,self.du)
        else:
            self.du += du
            self.du %= 360
            self.image = pg.transform.rotate(self.yuan_img,self.du)
        if self.suo_x != 1 or self.suo_y != 1:
            self.image = pg.transform.scale(self.image,(self.image.get_width()*self.suo_x,self.image.get_height()*self.suo_y))

        self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=True)

    def geng(self,peng):
        if self.NOting:
            self.rect.x += self.vel_x
            if self.vel_x > 0:
                self.vel_x -= 0.5
                if self.vel_x < 0:
                    self.vel_x = 0
                if self.rect.x+self.rect.width > 1000 and not self.huo:
                    self.rect.x = 1000 - self.rect.width
                    self.vel_x = 0
            elif self.vel_x < 0:
                self.vel_x += 0.5
                if self.vel_x > 0:
                    self.vel_x = 0
                if self.rect.x < 0 and not self.huo:
                    self.rect.x = 0
                    self.vel_x = 0
                
            self.vel_y += 0.5
            self.rect.y += self.vel_y
            if self.huo:
                if (self.rect.y+self.rect.height) > 600:
                    self.rect.y = 600 - self.rect.height
                    self.vel_y = 0
                    self.tiao_an = 0                

                    if self.gun:
                        if self.gun_NOchu:
                            self.shou_time = max(self.shou_time,90)
                            self.bai_time = 20
                            self.bai_xian = True
                            self.qing = -360
                            self.gun_NOchu = False
                            self.vel_gun = 7
                        elif self.qing == 0:
                            self.gun = False
                            self.vel_gun = 2
                            if self.p == 1:
                                self.qie("teto1.png",True)
                            else:
                                self.qie("miku1.png",True)
                    else:
                        self.tiao_bool = True
                        if self.du > 0:
                            if self.du > 180:
                                self.qing = 360 - self.du
                            else:
                                self.qing = self.du * -1
                        else:
                            if self.du < -180:
                                self.qing = -360 - self.du
                            else:
                                self.qing = self.du * -1
                        if self.tu_name[-5] == "2":
                            if self.p == 1:
                                self.qie("teto1.png",True)
                            else:
                                self.qie("miku1.png",True)
                else:
                    self.tiao_bool = False
                    if self.vel_y > 0 and self.shuai:
                        self.qing -= 25
                        self.shuai = False
                        if self.p == 1:
                            self.qie("teto2.png",True)
                        else:
                            self.qie("miku2.png",True)
                        if random.randint(1,5) == 1:
                            self.gun = True
                            self.gun_NOchu = True
                            self.bai_xian = True
                    if self.rect.y < -200 and not self.gun:
                        self.shuai = True
                        self.gun = True
                        self.gun_NOchu = True

            if self.rect.x < -500:
                self.vel_x = 28
                self.vel_y *= -1.2
            elif self.rect.x+self.rect.width > 1500:
                self.vel_x = -28
                self.vel_y *= -1.2

            if self.qing > 0:
                self.zhuan(self.vel_gun)
                self.qing -= self.vel_gun
                if self.qing < 0:
                    self.zhuan(self.qing)
                    self.qing = 0
            elif self.qing < 0:
                self.zhuan(self.vel_gun*-1)
                self.qing += self.vel_gun
                if self.qing > 0:
                    self.zhuan(self.qing)
                    self.qing = 0

            if self.shou_time > 0:
                if self.shou_jian >= 3:
                    if self.shou_tu_ji >= 20:
                        self.shou_tu_ji = 0
                        self.shou_tu = True
                        self.image = pg.image.load(resource_path("images/"+self.tu_name))
                        self.image = pg.transform.scale_by(self.image,(self.suo_x,self.suo_y))
                        self.image = pg.transform.rotate(self.image,self.du)
                        self.image = pg.transform.scale_by(self.image,random.uniform(0.9,1.1))
                        self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=True)
                    self.shou_jian = 0
                    self.pian_x = 0
                    self.pian_y = 0
                    self.pian_x += random.randint(-15,15)
                    self.pian_y += random.randint(-15,15)
                else:
                    self.shou_tu_ji += 1
                    self.shou_jian += 1
                self.shou_time -= 1
            else:
                if self.shou_tu:
                    self.shou_tu = False
                    self.image = pg.image.load(resource_path("images/"+self.tu_name))
                    self.image = pg.transform.scale_by(self.image,(self.suo_x,self.suo_y))
                    self.image = pg.transform.rotate(self.image,self.du)
                    self.baiimg = pg.transform.solid_overlay(self.image,"#FFFFFF",keep_alpha=True)
                self.pian_x = 0
                self.pian_y = 0
                self.shou_tu_ji = 0

            if self.rect.x > 600:
                self.NOting = True

            if self.huo:
                for it in peng:
                    if self != it and it.huo:
                        peng_jie = self.collidejing(it.rect)
                        if peng_jie != None:
                            if it.shang:
                                self.hp -= it.shanghai
                                self.shou_time = max(self.shou_time,60)
                                self.bai()

                        if peng_jie == "up":
                            self.vel_y = -15
                            self.vel_y += it.vel_y
                            self.shou_time = max(self.shou_time,60)
                            self.bai()
                            if self.rect.centerx > it.rect.centerx:
                                lin_fang = "right"
                                self.vel_x += 15
                                self.qing -= 5
                            else:
                                lin_fang = "left"
                                self.vel_x -= 15
                                self.qing += 5
                            if random.randint(1,5) == 1:
                                self.shuai = True
                                self.gun = True
                                self.gun_NOchu = True
                                if self.p == 1:
                                    self.qie("teto2.png",True)
                                else:
                                    self.qie("miku2.png",True)
                                if lin_fang == "right":
                                    self.vel_x += 15
                                else:
                                    self.vel_x -= 15
                            self.rect.y = it.rect.y - self.rect.height

                        elif peng_jie == "down":
                            print(f"vel: {self.vel_y}",end='')
                            self.vel_y = 0
                            self.rect.y = it.rect.y + it.rect.height
                            self.tiao_zhu = False
                            print(f"  vel: {self.vel_y}")

    def collidejing(self,it):
        if self.rect.colliderect(it):
            peng = self.rect.clip(it)
            if peng.width < peng.height:
                if peng.centerx > it.centerx:
                    return "right"
                else:
                    return "left"
            else:
                if peng.centery > it.centery:
                    return "down"
                else:
                    return "up"

    def move(self,key):
        if self.move_kong:
            if self.p == 1:
                if self.vel_x > -15 and self.vel_x < 15:
                    if key[pg.K_a]:
                        if self.tiao_bool:
                            self.vel_x -= 1
                        else:
                            self.vel_x -= 0.7
                    if key[pg.K_d]:
                        if self.tiao_bool:
                            self.vel_x += 1
                        else:
                            self.vel_x += 0.7

                if key[pg.K_w] or key[pg.K_DOLLAR]:
                    if self.tiao_an == 0 and self.tiao_bool:
                        self.vel_y -= 10
                        self.tiao_zhu = True
                        self.qing += 5
                    if self.tiao_zhu and self.tiao_an == 3:
                        self.vel_y -= 5
                    elif self.tiao_zhu and self.tiao_an == 5:
                        self.vel_y -= 5
                    elif self.tiao_zhu and self.tiao_an == 10:
                        self.vel_y -= 5
                        if random.randint(1,3) == 1:
                            self.shuai = True
                    self.tiao_an += 1
                else:
                    self.tiao_zhu = False
                    self.tiao_an = 0
            else:
                if self.vel_x > -15 and self.vel_x < 15:
                    if key[pg.K_LEFT]:
                        if self.tiao_bool:
                            self.vel_x -= 1
                        else:
                            self.vel_x -= 0.7
                    if key[pg.K_RIGHT]:
                        if self.tiao_bool:
                            self.vel_x += 1
                        else:
                            self.vel_x += 0.7

                if key[pg.K_UP]:
                    if self.tiao_an == 0 and self.tiao_bool:
                        self.vel_y -= 10
                        self.tiao_zhu = True
                        self.qing += 5
                    if self.tiao_zhu and self.tiao_an == 3:
                        self.vel_y -= 5
                    elif self.tiao_zhu and self.tiao_an == 5:
                        self.vel_y -= 5
                    elif self.tiao_zhu and self.tiao_an == 10:
                        self.vel_y -= 5
                        if random.randint(1,3) == 1:
                            self.shuai = True
                    self.tiao_an += 1
                else:
                    self.tiao_zhu = False
                    self.tiao_an = 0

    def die(self):
        self.move_kong = False
        self.huo = False
        self.hp = 0
        if self.huo_NOchu:
            self.qing = 0
            self.bai()
            self.shou_time = 0
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.x + self.rect.width > 1000:
                self.rect.x = 1000 - self.rect.width
            self.huo_NOchu = False
            self.vel_y = -20
            if random.randint(1,2) == 1:
                self.vel_x = -20
            else:
                self.vel_x = 20
            if self.p == 1:
                self.qie("teto2.png",True)
            else:
                self.qie("miku2.png",True)

    def bai(self):
        if self.bai_xian:
            self.baitou(255)
            self.bai_tou = 255
        self.bai_xian = True
        self.bai_time = 20

    def beizhuang(self,it,peng_jie):
        self.vel_x += it.vel_x
        it.vel_x *= -1
        if peng_jie == "left":
            self.rect.x = it.rect.x - self.rect.width
        else:
            self.rect.x = it.rect.x + it.rect.width
            if random.randint(1,3) != 1:
                self.gun = True
                self.gun_NOchu = True
                self.vel_x += 10
                if self.p == 1:
                    self.qie("teto2.png",True)
                else:
                    self.qie("miku2.png",True)
                self.shou_time = max(self.shou_time,60)
                self.bai()
                self.hp -= 1

async def main():

    pg.init()

    def draw(win):
        bei.draw(win)
        bei2.draw(win)
        player1.draw(win)
        player2.draw(win)

        hp1.draw(win)
        if player1.hp < 10:
            if player1.hp == 9:
                pg.draw.rect(win,"#000000",(276,hp1.rect.y,25,34.2))
            elif player1.hp == 8:
                pg.draw.rect(win,"#000000",(252,hp1.rect.y,49,34.2))
            elif player1.hp == 7:
                pg.draw.rect(win,"#000000",(228,hp1.rect.y,73,34.2))
            elif player1.hp == 6:
                pg.draw.rect(win,"#000000",(204,hp1.rect.y,97,34.2))
            elif player1.hp == 5:
                pg.draw.rect(win,"#000000",(180,hp1.rect.y,121,34.2))
            elif player1.hp == 4:
                pg.draw.rect(win,"#000000",(156,hp1.rect.y,145,34.2))
            elif player1.hp == 3:
                pg.draw.rect(win,"#000000",(133,hp1.rect.y,170,34.2))
            elif player1.hp == 2:
                pg.draw.rect(win,"#000000",(109,hp1.rect.y,192,34.2))
            elif player1.hp == 1:
                pg.draw.rect(win,"#000000",(85,hp1.rect.y,216,34.2))
            else:
                pg.draw.rect(win,"#000000",(60,hp1.rect.y,241,34.2))
        win.blit(p1_text,(5,26))

        hp2.draw(win)
        if player2.hp < 10:
            if player2.hp == 9:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,32,34.1))
            elif player2.hp == 8:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,56,34.1))
            elif player2.hp == 7:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,80,34.1))
            elif player2.hp == 6:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,104,34.1))
            elif player2.hp == 5:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,128,34.1))
            elif player2.hp == 4:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,152,34.1))
            elif player2.hp == 3:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,176,34.1))
            elif player2.hp == 2:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,200,34.1))
            elif player2.hp == 1:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,224,34.1))
            else:
                pg.draw.rect(win,"#000000",(693,hp2.rect.y,248,34.1))
        win.blit(p2_text,(951,26))
            

    def geng(peng):
        bei.rect.x -= 10
        if bei.rect.x + bei.rect.width <= 0:
            bei.rect.x = bei2.rect.x + bei2.rect.width -20

        bei2.rect.x -= 10
        if bei2.rect.x + bei2.rect.width <= 0:
            bei2.rect.x = bei.rect.x + bei.rect.width

        player1.geng(peng)
        player2.geng(peng)
        if player1.huo and player2.huo:
            peng_jie = player1.collidejing(player2.rect)
            if peng_jie == "left" or peng_jie == "right":
                if abs(player1.vel_x) > abs(player2.vel_x):
                    if peng_jie == "left":
                        player2.beizhuang(player1,"right")
                    else:
                        player2.beizhuang(player1,"left")
                else:
                    player1.beizhuang(player2,peng_jie)

        if player1.hp <= 0:
            player1.die()
        if player2.hp <= 0:
            player2.die()
                
    main_img = pg.image.load(resource_path("images/xiao.ico"))

    win = pg.display.set_mode((1000,600))
    peng = []

    pg.display.set_caption("mini game v0.1.0-beta.1")
    pg.display.set_icon(main_img)

    font = pg.font.Font(resource_path("fonts/k12x8.ttf"),30)

    bei = img("bei.png")
    bei.suo(0.6)
    bei.rect.x,bei.rect.y = 0,0

    bei2 = img("bei.png")
    bei2.suo(0.6)
    bei2.rect.x = bei.rect.width
    bei2.rect.y = 0

    hp1 = img("p1hp.png")
    hp1.suo(0.6)
    hp1.rect.x = 50
    hp1.rect.y = 25
    p1_text = font.render("1P",True,"#E00516")

    hp2 = img("p2hp.png")
    hp2.suo(0.6019,0.6182)
    hp2.rect.x = 693
    hp2.rect.y = 25
    p2_text = font.render("2P",True,"#9a17fd")

    player1 = img("teto1.png",True)
    player1.suo(0.15)
    player1.rect.x,player1.rect.y = 0,200
    peng.append(player1)

    player2 = img("miku1.png",True,2)
    player2.suo(0.14)
    player2.rect.x,player2.rect.y = 200,200
    peng.append(player2)

    clock = pg.time.Clock()
    jie = True
    while jie:
        win.fill("#000000")
        clock.tick(60)
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                jie = False

            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_g:
                    player2.hp = 10
                if ev.key == pg.K_f:
                    player2.hp -= 1

        ke = pg.key.get_pressed()
        player1.move(ke)
        player2.move(ke)

        geng(peng)

        draw(win)



        pg.display.update()
        await asyncio.sleep(0)

    pg.quit() 

asyncio.run(main())