import datetime
import pygame
import datedata

# Pygame の初期化
pygame.init()

# 画面のサイズ
display_info = pygame.display.Info()
screen_width = int(display_info.current_w * 1.0)
screen_height = int(display_info.current_h * 0.97)

# 画面の作成
screen = pygame.display.set_mode((screen_width, screen_height))

# フォントの設定
font = pygame.font.Font("/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf", 60)

weekday_code = {
    0 : '(月)',
    1 : '(火)',
    2 : '(水)',
    3 : '(木)',
    4 : '(金)',
    5 : '(土)',
    6 : '(日)',
}

# テキストの表示
def draw_text(font, screen, x=0, y=0, display_txt='', rgb = (0,0,0)):
    text = font.render(display_txt, True, rgb)
    screen.blit(text,(x, y))
    return None

if __name__ == '__main__':

    # ゲームループ
    while True:
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 背景の描画
        screen.fill((255, 255, 255))

        # 現在時刻の取得
        current_time = datetime.datetime.now()

        # 更新時刻のフォーマット
        current_time_str = f"更新時刻 : {current_time.strftime('%Y/%m/%d %H:%M')}"

        # テキストの描画
        text = font.render(current_time_str, True, (0, 0, 0))
        screen.blit(text, (10, 10))
        
        # データ取得
        ddl = datedata.make_datedata_list()
        for dd in ddl:
            print(
                # dd.target_date,
                # dd.temp_max,
                # dd.temp_min,
                # dd.weather_code,
                dd.events
            )

        # 予定の描画
        
        x = 100
        y = 100
        y_range = 50
        y_idx = 0
        
        for i,dd in enumerate(ddl):
            
            for j in range(5):
                if j == 0:
                    display_txt = '--------------------------------'
                elif j == 1:
                    
                    display_txt = str(dd.target_date.strftime('%Y/%m/%d')) + ' : ' + weekday_code[dd.target_date.weekday()]
                elif j == 2:
                    display_txt = f'最高気温 : {str(dd.temp_max)}'
                elif j == 3:
                    display_txt = f'最低気温 : {str(dd.temp_min)}'
                elif j == 4:
                    display_txt = f'天気コード : {str(dd.weather_code)}'
                draw_text(
                    font, 
                    screen, 
                    x = x, 
                    y = y + y_range * y_idx, 
                    display_txt = display_txt, 
                    rgb = (0,0,0)
                )
                y_idx += 1
            
            event_str_list = [event['start_at'].strftime('%H:%M') + ' - ' + event['end_at'].strftime('%H:%M') + ' : ' + event['title'] for event in dd.events]
            
            for j,event_str in enumerate(event_str_list):
                event_str = event_str.replace('\u3000',' ')
                text = font.render(event_str, True, (0, 0, 0))
                screen.blit(text,(x, y + y_range * y_idx))
                y_idx += 1
                

        # 画面の更新
        pygame.display.update()

        # 1分待機
        pygame.time.wait(60000)
