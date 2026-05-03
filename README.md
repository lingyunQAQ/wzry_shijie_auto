# 自动点击监控系统

> **作者：是凌云诶**  
> **抖音：是凌云诶**

极简的自动化监控脚本，检测到"点击前往"文字后自动点击。

## 功能特点

- 极速检测：0.1秒检测一次
- 瞬时点击：检测到后立即点击10次
- 自动退出：点击成功后自动退出
- 音频提醒：点击成功后播放提示音

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置检测区域

```bash
python config_gui.py
```

- 点击"选择区域"
- 拖动鼠标选择包含"点击前往"的区域
- 点击"应用配置"

### 3. 启动监控

```bash
python main.py
```

## 配置说明

编辑 `config.json`：

```json
{
    "detection_area": {
        "x": 560,
        "y": 240,
        "width": 800,
        "height": 600
    },
    "target_text": "点击前往",
    "loop_interval": 0.1,
    "click_count": 10,
    "click_interval": 0.01,
    "enable_sound": true,
    "fast_mode": true
}
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| detection_area | 检测区域坐标和大小 | - |
| target_text | 要检测的文字 | "点击前往" |
| loop_interval | 检测间隔（秒） | 0.1 |
| click_count | 点击次数 | 10 |
| click_interval | 点击间隔（秒） | 0.01 |
| enable_sound | 是否播放提示音 | true |
| fast_mode | 快速模式（减少输出） | true |

## 性能

- 检测间隔：0.1秒
- 点击速度：0.1秒（10次）
- 总响应时间：约0.2-0.3秒

## 项目结构

```
.
├── main.py              # 主程序
├── config_gui.py        # 配置工具
├── config.json          # 配置文件
├── requirements.txt     # 依赖清单
├── modules/             # 核心模块
│   ├── config.py        # 配置管理
│   ├── window.py        # 窗口操作
│   ├── ocr.py           # 文字识别
│   ├── clicker.py       # 点击操作
│   └── sound.py         # 音频播放
└── logs/                # 日志目录
```

## 常见问题

### Q: 识别不到文字

**解决**：
1. 确保Tesseract已正确安装
2. 缩小检测区域，只包含目标文字
3. 确保文字清晰可见

### Q: 点击位置不准

**解决**：
1. 调整 `click_offset` 参数
2. 重新选择检测区域

### Q: 速度太慢

**解决**：
1. 缩小检测区域（最重要）
2. 降低 `loop_interval` 到 0.05
3. 确保 `fast_mode` 为 true

## 注意事项

1. 检测区域越小越快
2. 建议区域大小：300x100 左右
3. 快速模式下输出较少，查看详情请看日志文件

---

**立即运行：`python main.py`**