import pygame
import sys
import os


class GameUI:
    def __init__(self, width=800, height=600):
        """初始化游戏界面"""
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Black Mage Simulator")

        # 颜色定义
        self.COLOR_BG = (30, 30, 40)
        self.COLOR_HP_BG = (50, 50, 60)
        self.COLOR_HP = (50, 255, 50)  # 绿色
        self.COLOR_MP_BG = (50, 50, 60)
        self.COLOR_MP = (50, 150, 255)  # 蓝色
        self.COLOR_TEXT = (255, 255, 255)
        self.COLOR_STATUS_ICE = (100, 200, 255)
        self.COLOR_STATUS_FIRE = (255, 100, 50)
        self.COLOR_STATUS_NEUTRAL = (200, 200, 200)

        # 字体 - 使用系统中文字体
        chinese_font = self._get_chinese_font()
        self.font_large = pygame.font.Font(chinese_font, 48)
        self.font_medium = pygame.font.Font(chinese_font, 36)
        self.font_small = pygame.font.Font(chinese_font, 28)

        # 血量和蓝量条的位置和大小
        self.hp_bar_rect = pygame.Rect(50, 50, 700, 50)
        self.mp_bar_rect = pygame.Rect(50, 120, 700, 50)

        # 状态显示区域
        self.status_rect = pygame.Rect(50, 200, 700, 100)

        # 技能信息显示区域
        self.skill_info_rect = pygame.Rect(50, 320, 700, 250)

        self.clock = pygame.time.Clock()
        self.running = True

    def _get_chinese_font(self):
        """获取系统中文字体路径"""
        # macOS 常见中文字体路径
        macos_fonts = [
            "/System/Library/Fonts/PingFang.ttc",  # PingFang SC
            "/System/Library/Fonts/STHeiti Light.ttc",  # 华文黑体
            "/System/Library/Fonts/Hiragino Sans GB.ttc",  # 冬青黑体
            "/Library/Fonts/Arial Unicode.ttf",
        ]

        # Windows 常见中文字体路径
        windows_fonts = [
            "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
        ]

        # Linux 常见中文字体路径
        linux_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        ]

        # 合并所有字体路径
        all_fonts = macos_fonts + windows_fonts + linux_fonts

        # 查找第一个存在的字体
        for font_path in all_fonts:
            if os.path.exists(font_path):
                return font_path

        # 如果没有找到，尝试使用系统默认字体
        try:
            # pygame.font.get_fonts() 获取系统可用字体
            available_fonts = pygame.font.get_fonts()
            # 查找中文字体
            chinese_font_names = ['pingfang', 'pingfangsc', 'notosans', 'notosanscjk',
                                 'microsoftyahei', 'simhei', 'simsun', 'heiti', 'hiragino']
            for font_name in chinese_font_names:
                if font_name in available_fonts:
                    return pygame.font.match_font(font_name)
        except:
            pass

        # 如果都失败了，返回 None 使用默认字体
        return None

    def draw_bar(self, rect, current, maximum, color_fill, color_bg):
        """绘制一个进度条"""
        # 背景
        pygame.draw.rect(self.screen, color_bg, rect)
        # 边框
        pygame.draw.rect(self.screen, self.COLOR_TEXT, rect, 2)

        # 填充
        if maximum > 0:
            fill_width = int((current / maximum) * rect.width)
            fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
            pygame.draw.rect(self.screen, color_fill, fill_rect)

        # 文字显示数值
        text = self.font_medium.render(f"{current}/{maximum}", True, self.COLOR_TEXT)
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

    def draw_status(self, status, ice_needle, enochian_time, polyglot):
        """绘制状态信息"""
        pygame.draw.rect(self.screen, (40, 40, 50), self.status_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, self.status_rect, 2)

        # 确定状态文本和颜色
        if status > 0:
            status_text = f"火 {status} 档"
            status_color = self.COLOR_STATUS_FIRE
        elif status < 0:
            status_text = f"冰 {abs(status)} 档"
            status_color = self.COLOR_STATUS_ICE
        else:
            status_text = "无元素状态"
            status_color = self.COLOR_STATUS_NEUTRAL

        # 渲染状态文本
        text = self.font_large.render(status_text, True, status_color)
        text_rect = text.get_rect(center=(self.status_rect.centerx, self.status_rect.y + 30))
        self.screen.blit(text, text_rect)

        # 第二行：冰针和通晓
        info_line2 = f"冰针: {ice_needle}  |  通晓: {polyglot}"
        info2_text = self.font_small.render(info_line2, True, self.COLOR_TEXT)
        info2_rect = info2_text.get_rect(center=(self.status_rect.centerx, self.status_rect.y + 65))
        self.screen.blit(info2_text, info2_rect)

        # 第三行：天语剩余时间
        enochian_line = f"天语剩余: {enochian_time:.1f}s" if enochian_time > 0 else "天语: 未激活"
        enochian_text = self.font_small.render(enochian_line, True, self.COLOR_TEXT)
        enochian_rect = enochian_text.get_rect(center=(self.status_rect.centerx, self.status_rect.y + 90))
        self.screen.blit(enochian_text, enochian_rect)

    def draw_skill_info(self, skill_name, message="", current_input=""):
        """绘制技能信息"""
        pygame.draw.rect(self.screen, (40, 40, 50), self.skill_info_rect)
        pygame.draw.rect(self.screen, self.COLOR_TEXT, self.skill_info_rect, 2)

        y_offset = 30

        # 显示当前输入
        if current_input:
            input_text = self.font_large.render(f"当前输入: {current_input}", True, (255, 255, 100))
            input_rect = input_text.get_rect(center=(self.skill_info_rect.centerx, self.skill_info_rect.y + y_offset))
            self.screen.blit(input_text, input_rect)
            y_offset += 60

        # 显示施放的技能
        if skill_name:
            skill_text = self.font_medium.render(f"施放技能: {skill_name}", True, (100, 255, 100))
            skill_rect = skill_text.get_rect(center=(self.skill_info_rect.centerx, self.skill_info_rect.y + y_offset))
            self.screen.blit(skill_text, skill_rect)
            y_offset += 50

        if message:
            # 处理多行消息
            lines = message.split('\n')
            for line in lines:
                if line.strip():
                    msg_text = self.font_small.render(line, True, self.COLOR_TEXT)
                    msg_rect = msg_text.get_rect(center=(self.skill_info_rect.centerx, self.skill_info_rect.y + y_offset))
                    self.screen.blit(msg_text, msg_rect)
                    y_offset += 35

    def update(self, hp, max_hp, mp, max_mp, status, ice_needle, enochian_time, polyglot, skill_name="", message="", current_input=""):
        """更新并绘制整个界面"""
        # 不在这里处理事件，让 input_keyboard 统一处理
        # 清空屏幕
        self.screen.fill(self.COLOR_BG)

        # 绘制血量条
        hp_label = self.font_small.render("HP", True, self.COLOR_TEXT)
        self.screen.blit(hp_label, (10, 60))
        self.draw_bar(self.hp_bar_rect, hp, max_hp, self.COLOR_HP, self.COLOR_HP_BG)

        # 绘制蓝量条
        mp_label = self.font_small.render("MP", True, self.COLOR_TEXT)
        self.screen.blit(mp_label, (10, 130))
        self.draw_bar(self.mp_bar_rect, mp, max_mp, self.COLOR_MP, self.COLOR_MP_BG)

        # 绘制状态信息
        self.draw_status(status, ice_needle, enochian_time, polyglot)

        # 绘制技能信息
        self.draw_skill_info(skill_name, message, current_input)

        # 提示信息
        hint = self.font_small.render("按键施放技能 | ESC 退出", True, (150, 150, 150))
        self.screen.blit(hint, (50, 570))

        # 更新显示
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS

        return True

    def close(self):
        """关闭界面"""
        pygame.quit()


if __name__ == "__main__":
    # 测试UI
    ui = GameUI()
    hp = 60000
    mp = 10000
    status = 0
    ice_needle = 0

    while ui.running:
        if not ui.update(hp, 60000, mp, 10000, status, ice_needle, "测试技能", "这是一个测试消息"):
            break

    ui.close()
