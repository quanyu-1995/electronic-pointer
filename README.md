# electronic-pointer

一个轻量级的电子教鞭工具，适用于教学演示、会议讲解等场景。

## 功能特性

- **绘图工具**
  - 画笔 (B) - 自由绘制
  - 橡皮擦 (E) - 擦除内容
  - 线条 (L) - 绘制直线
  - 矩形 (R) - 绘制矩形
  - 圆形 (C) - 绘制圆形
  - 文本 (T) - 添加文字

- **放大镜** (M) - 局部放大显示，支持调整放大倍数和窗口大小

- **截图功能** - 一键截取当前屏幕

- **历史记录** - 支持撤销 (Ctrl+Z) 和重做 (Ctrl+Y)

- **窗口穿透** - 按 F9 切换穿透模式，不影响对底层窗口的操作

- **透明置顶** - 透明背景，始终置顶，不遮挡演示内容

## 快捷键

| 功能 | 快捷键 |
|------|--------|
| 画笔 | B |
| 橡皮擦 | E |
| 线条 | L |
| 矩形 | R |
| 圆形 | C |
| 文本 | T |
| 放大镜 | M |
| 撤销 | Ctrl+Z |
| 重做 | Ctrl+Y |
| 清除 | Delete |
| 保存 | Ctrl+S |
| 退出 | Escape |
| 穿透模式 | F9 |

## 环境要求

- Python 3.8+
- Windows 操作系统

## 安装

1. 克隆仓库

```bash
git clone https://github.com/yourusername/electronic-pointer.git
cd electronic-pointer
```

2. 创建虚拟环境（推荐）

```bash
python -m venv venv
venv\Scripts\activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python src/main.py
```

## 打包

运行打包脚本生成可执行文件：

```bash
python build.py
```

打包完成后，可执行文件位于 `dist/电子教鞭工具.exe`。

## 项目结构

```
electronic-pointer/
├── src/
│   ├── config/          # 配置模块
│   ├── drawing/         # 绘图画布
│   ├── managers/        # 管理器（历史、样式）
│   ├── tools/           # 工具实现
│   ├── ui/              # 用户界面
│   ├── utils/           # 工具函数
│   └── main.py          # 程序入口
├── tests/               # 测试文件
├── requirements.txt     # 依赖列表
└── build.py            # 打包脚本
```

## 依赖

- PyQt6 >= 6.7.0
- Pillow >= 10.1.0
- pywin32 >= 307

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。
