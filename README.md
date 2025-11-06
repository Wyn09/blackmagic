# Black Mage Simulator

最终幻想XIV黑魔法师职业模拟器，带有图形界面显示血量和蓝量。

## 安装依赖

```bash
pip install pygame
```

## 运行方式

### 带UI界面运行（推荐）

```bash
python test.py
```

这将打开一个图形界面窗口，显示：
- 绿色血量条（HP）
- 蓝色蓝量条（MP）
- 当前元素状态（冰/火档位）
- 冰针数量
- 施放的技能信息

### 命令行模式运行

如果你想使用纯命令行模式（无图形界面），可以这样修改 `test.py`：

```python
if __name__ == "__main__":
    # 不创建UI，使用命令行模式
    b = BlackMage()
    for _ in range(20):
        if not b.run_skill():
            break
```

## 操作说明

- 按下键盘上的技能对应按键施放技能（参见 `skills.json`）
- 按 `ESC` 键退出程序
- 点击窗口关闭按钮也可以退出

## 技能按键映射

根据 `skills.json` 文件：

| 技能 | 按键 |
|------|------|
| 冰1 | 1 |
| 冰2 | ! |
| 冰3 | q |
| 冰4 | V |
| 冰悖论 | 2 |
| 火1 | 2 |
| 火2 | @ |
| 火3 | e |
| 火4 | A |
| 火悖论 | 2 |
| 绝望 | 4 |
| 醒梦 | 6 |
| 黑魔纹 | f1 |

注意：冰悖论、火1和火悖论共享按键 `2`，程序会根据当前状态自动选择正确的技能。

## UI界面说明

### 血量条（HP）
- 绿色填充矩形
- 显示当前血量/最大血量
- 当前固定为 60000/60000

### 蓝量条（MP）
- 蓝色填充矩形
- 显示当前蓝量/最大蓝量（0-10000）
- 会根据技能施放实时更新

### 状态显示
- **火状态**：显示"火 X 档"（橙红色）
- **冰状态**：显示"冰 X 档"（浅蓝色）
- **无元素状态**：显示"无元素状态"（灰色）
- 同时显示当前冰针数量（0-3）

### 技能信息
- 显示正在施放的技能名称
- 显示当前状态和剩余蓝量
- 如果蓝量不足会显示错误提示

## 代码集成说明

如果你想在自己的代码中使用UI界面：

```python
from ui import GameUI
from test import BlackMage

# 1. 创建UI实例
ui = GameUI(width=800, height=600)

# 2. 创建BlackMage实例并传入UI
mage = BlackMage(ui=ui)

# 3. 主游戏循环
while ui.running:
    if not mage.run_skill():
        break

# 4. 关闭UI
ui.close()
```

### 不使用UI的情况

如果不需要图形界面，只需在创建BlackMage时不传入ui参数：

```python
from test import BlackMage

# 创建BlackMage实例（无UI）
mage = BlackMage()

# 运行技能
for _ in range(20):
    if not mage.run_skill():
        break
```

## 文件说明

- `test.py`: 主程序文件，包含BlackMage类和主循环
- `ui.py`: UI界面模块，包含GameUI类
- `skills.json`: 技能数据配置文件
- `CLAUDE.md`: 项目架构说明文档

## 自定义UI

你可以通过修改 `ui.py` 中的颜色常量来自定义界面外观：

```python
self.COLOR_HP = (50, 255, 50)  # 血量条颜色
self.COLOR_MP = (50, 150, 255)  # 蓝量条颜色
self.COLOR_STATUS_ICE = (100, 200, 255)  # 冰状态颜色
self.COLOR_STATUS_FIRE = (255, 100, 50)  # 火状态颜色
```

你也可以调整窗口大小、条形位置和字体大小等参数。
