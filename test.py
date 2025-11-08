import json
import time
import pygame
from ui import GameUI

with open("./skills.json", "r", encoding="utf-8") as f:
    skill_data = json.load(f)


class BlackMage:
    def __init__(self, ui=None):
        self.healthy = 60000
        self.max_healthy = 60000
        self.magic = 10000
        self.max_magic = 10000
        self.skills = skill_data
        # gcd间隙插入的能力技数量，最多两个
        self.capability_count_gcdgap = 0
        # -3~3 冰3档～火3档
        self.status = 0
        self.status_list = [0]
        self.ice_needle = 0
        self.paradox = "6"
        # 天语剩余时间（秒）
        self.enochian_remain_time = 0
        self.start_enochian_time = None
        # UI界面
        self.ui = ui
        # 通晓档数，最多2档
        self.polyglot = 0
        # 通晓累计时间（秒）
        self.polyglot_accumulate_time = 0
        self.polyglot_accumulate_start_time = None
        # 上次输入的技能名
        self.last_input_skill = ""
    
    def calcu_enochian_remain_time(self):
        """计算天语剩余时间"""
        if self.start_enochian_time is None:
            return

        elapsed = time.time() - self.start_enochian_time
        self.enochian_remain_time = max(0, 15 - elapsed)

        # 天语时间过期，重置状态
        if self.enochian_remain_time <= 0:
            self.status = 0
            self.enochian_remain_time = 0
            self.start_enochian_time = None

    def calcu_polyglot_accumulate_time(self):
        """计算通晓累计时间"""
        if not self.polyglot_accumulate_start_time:
            return

        elapsed = time.time() - self.polyglot_accumulate_start_time
        self.polyglot_accumulate_time = elapsed

        # 累计到30秒，增加通晓档数并重置计时
        if self.polyglot_accumulate_time >= 30:
            if self.polyglot < 2:  # 最多2档
                self.polyglot += 1
            # 重置累计时间
            self.polyglot_accumulate_time = 0
            self.polyglot_accumulate_start_time = time.time()

    def input_keyboard(self):
        """监听一次按键，返回按键信息（使用pygame事件）"""
        waiting = True
        key_pressed = None

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'ESC'

                if event.type == pygame.KEYDOWN:
                    # 处理ESC键
                    if event.key == pygame.K_ESCAPE:
                        return 'ESC'

                    # 处理F1键
                    elif event.key == pygame.K_F1:
                        return 'f1'

                    # 处理普通字符键
                    elif event.unicode:
                        return event.unicode

            # 更新UI以保持窗口响应
            if self.ui:
                self.ui.clock.tick(60)

        return key_pressed

    def exam_magic(self, skill_id):
        # 当前是无状态
        if self.status == 0:
            consum_magic = skill_data[skill_id]["consumption"]
        # 当前是火状态
        elif self.status > 0:
            if skill_id in ["11"]:
                consum_magic = self.magic
            # 上个状态是冰状态
            elif self.status_list[-1] < 0:
                consum_magic = 0
            elif skill_id in ["6", "7", "8", "9", "10"]:
                if self.status_list[-1] > 0:
                    # 有冰针
                    if self.ice_needle > 0:
                        consum_magic = skill_data[skill_id]["consumption"]
                        self.ice_needle -= 1
                    else:
                        consum_magic = skill_data[skill_id]["consumption"] * 2
                    
                # 上个状态是无状态
                else:
                    consum_magic = skill_data[skill_id]["consumption"]
            else:
                consum_magic = skill_data[skill_id]["consumption"]
        # 当前是冰状态
        elif self.status < 0:
            # 用冰系魔法
            if skill_id in ["1", "2", "3", "4", "5"]:
                # 上个状态是无状态
                if self.status_list[-1] == 0:
                    consum_magic = skill_data[skill_id]["consumption"]
                
                else:
                    # 按冰的档数决定恢复的蓝量
                    consum_magic = -3200 - 1600 * (-self.status - 1)
                # 冰针
                if skill_id == "4":
                    self.ice_needle = 3
            # 使用其他魔法
            else:
                consum_magic = skill_data[skill_id]["consumption"]
        # 如果蓝量不够
        if self.magic - consum_magic < 0:
                return False
        # 减蓝量
        if consum_magic >= 0:
            self.magic = self.magic - consum_magic if self.magic - consum_magic >= 0 else 0
            
        # 加蓝量
        else:
            self.magic = self.magic - consum_magic if self.magic - consum_magic <= 10000 else 10000
        return True
        
    def exam_status(self, skill_id, skill_name):

        if self.status == 0:
            if "6" == skill_id:
                self.status += 1
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
                # 启动通晓累计计时
                if not self.polyglot_accumulate_start_time:
                    self.polyglot_accumulate_start_time = time.time()
            elif skill_id in ["7", "8"]:
                self.status = 3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
                # 启动通晓累计计时
                if not self.polyglot_accumulate_start_time:
                    self.polyglot_accumulate_start_time = time.time()
            elif "1" == skill_id:
                self.status = -1
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
                # 启动通晓累计计时
                if not self.polyglot_accumulate_start_time:
                    self.polyglot_accumulate_start_time = time.time()
            elif skill_id in ["2", "3"]:
                self.status = -3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
                # 启动通晓累计计时
                if not self.polyglot_accumulate_start_time:
                    self.polyglot_accumulate_start_time = time.time()

        elif self.status > 0:
            if skill_name == "绝望":
                self.status = 3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
            elif skill_id in ["6", "10"]:
                self.status = 3 if self.status + 1 >=3 else self.status + 1
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
            elif skill_id in ["7", "8"]:
                self.status = 3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
            elif "1" == skill_id:
                self.status = 0
                # 天语结束，重置通晓累计时间
                self.polyglot_accumulate_time = 0
                self.polyglot_accumulate_start_time = None
            elif skill_id in ["2", "3"]:
                self.status = -3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()


        elif self.status < 0:
            if "6" == skill_id:
                self.status = 0
                # 天语结束，重置通晓累计时间
                self.polyglot_accumulate_time = 0
                self.polyglot_accumulate_start_time = None
            elif skill_id in ["7", "8"]:
                self.status = 3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
            elif skill_id in ["1", "5"]:
                self.status = -3 if self.status -1 <=3 else self.status - 1
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()
            elif skill_id in ["2", "3"]:
                self.status = -3
                self.enochian_remain_time = 15
                self.start_enochian_time = time.time()

        # 判断是否有通晓打异言
        if skill_id == "16":
            if self.polyglot > 0:
                self.polyglot -= 1
            else:
                print(f"当前通晓为0，无法使用{skill_name}")



    def exam_paradox(self):
        if self.paradox != "6":
            return 
        
        if  self.status == 3 and len(self.status_list) > 1 and self.status_list[-1] == -3 and self.ice_needle == 3:
            self.paradox = "10"
            return
        elif self.status == -3 and len(self.status_list) > 1 and self.status_list[-1] == 3:
            self.paradox = "5"
            return
        else:
            self.paradox = "6"
            return
    # 计时天语
    async def exam_enochian():
        pass
    # 计时通晓
    async def exam_polyglot(self):
        pass
    def run_skill(self):
        # 计算天语剩余时间
        self.calcu_enochian_remain_time()
        # 计算通晓累计时间
        self.calcu_polyglot_accumulate_time()

        # 更新UI（技能施放前），显示上次输入的技能
        if self.ui:
            if not self.ui.update(self.healthy, self.max_healthy, self.magic, self.max_magic,
                                  self.status, self.ice_needle, self.enochian_remain_time,
                                  self.polyglot, self.polyglot_accumulate_time, "", "等待输入...", current_input=self.last_input_skill):
                return False

        user_input = self.input_keyboard()

        # 如果按下ESC，返回False表示退出
        if user_input == 'ESC':
            return False

        skill_id = [id for id, skill in self.skills.items() if skill["keyboard"] == user_input]
        if len(skill_id) > 1:
            skill_id = self.paradox
        elif len(skill_id) == 0:
            # 如果没有匹配的技能
            if self.ui:
                self.ui.update(self.healthy, self.max_healthy, self.magic, self.max_magic,
                              self.status, self.ice_needle, self.enochian_remain_time,
                              self.polyglot, self.polyglot_accumulate_time, "", f"无效按键: {user_input}", current_input=self.last_input_skill)
            else:
                print("无效按键")
            return True
        else:
            skill_id = skill_id[0]

        skill_name = skill_data[skill_id]["name"]

        # 保存当前输入的技能名
        self.last_input_skill = skill_name

        self.exam_status(skill_id, skill_name)
        if len(self.status_list) == 0 and skill_id in ["1", "2", "3", "6", "7", "8"]:
            self.enochian_remain_time = 15
            self.start_enochian_time = time.time()
            self.calcu_enochian_remain_time()


        message = f"状态: {self.status} 档, 冰针: {self.ice_needle}"

        if self.exam_magic(skill_id):
            casting_msg = f"{message}\n剩余蓝量: {self.magic}"
            if self.ui:
                self.ui.update(self.healthy, self.max_healthy, self.magic, self.max_magic,
                              self.status, self.ice_needle, self.enochian_remain_time,
                              self.polyglot, self.polyglot_accumulate_time, skill_name, casting_msg, current_input=self.last_input_skill)
            else:
                print(f"status: {self.status}, ice needle: {self.ice_needle}")
                print(f"casting... {skill_name}")
                print(f"remain magic: {self.magic}")
        else:
            error_msg = f"{message}\n蓝量不足！"
            if self.ui:
                self.ui.update(self.healthy, self.max_healthy, self.magic, self.max_magic,
                              self.status, self.ice_needle, self.enochian_remain_time,
                              self.polyglot, self.polyglot_accumulate_time, skill_name, error_msg, current_input=self.last_input_skill)
            else:
                print("remain magic not enough")

        if not self.ui:
            print(f"{'-'*30}")

        self.exam_paradox()
        self.status_list.append(self.status)
        self.status_list = self.status_list[-5:]

        return True
        
if __name__ == "__main__":
    # 创建UI界面
    ui = GameUI()

    # 创建BlackMage实例并传入UI
    b = BlackMage(ui=ui)

    # 主循环
    while ui.running:
        if not b.run_skill():
            break

    # 关闭UI
    ui.close()