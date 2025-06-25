# 智护夜巡机器人

本项目是一个基于 Tkinter 的医疗巡航机器人对话系统，集成了语音识别、AI医疗对话、语音合成等功能，适用于医院夜间巡查、病患初步咨询等场景。

## 目录结构

```
.
├── main.py                  # 启动入口（UI模式）
├── requirements.txt         # 依赖包
├── ui/
│   └── medical_robot_tk.py  # 图形界面（Tkinter）
├── core/
│   ├── chat.py              # AI对话核心
│   ├── audio.py             # 录音与语音识别
│   └── tts.py               # 语音合成
├── configs/
│   ├── system_prompt.txt    # AI角色与行为设定
│   └── languages.json       # 语言配置
└── ...
```

## 功能简介

- **多语言支持**：支持普通话、粤语、英语的语音识别与合成。
- **语音识别**：基于 faster-whisper 实现高质量转写。
- **AI医疗对话**：调用大模型 API，结合自定义 prompt，提供专业医疗建议。
- **语音合成**：edge-tts 实现多语言语音播报。
- **图形界面**：Tkinter 实现美观易用的对话窗口，支持一键录音、语言切换、对话清除等。

## 安装依赖

建议使用 Python 3.8+，并提前安装好 PortAudio（macOS 可用 `brew install portaudio`）。

```bash
pip install -r requirements.txt
```

## 运行方式

```bash
python main.py
```

首次运行会自动弹出图形界面。

## 配置说明

- `configs/system_prompt.txt`：AI角色、能力、行为准则等设定，支持自定义修改。
- `configs/languages.json`：支持的语言及其参数。
- `core/chat.py`：如需更换大模型API，可修改此文件中的 `api_url` 和 `api_key`。

## 录音设备说明

- 默认使用系统的**默认输入设备**（通常为内置麦克风）。
- 如需指定设备，可在 `core/audio.py` 的 `AudioProcessor` 类中设置 `input_device_index`。
- 可用设备列表可通过如下代码获取：
  ```python
  import pyaudio
  p = pyaudio.PyAudio()
  for i in range(p.get_device_count()):
      info = p.get_device_info_by_index(i)
      print(f"设备ID: {i}, 名称: {info['name']}")
  ```

## 常见问题

- **录音失败 `[Errno -9981] Input overflowed`**  
  说明：系统处理不过来音频流。  
  解决：减小 `CHUNK`，关闭其他占用麦克风的程序，或在 `stream.read` 加 `exception_on_overflow=False`。

- **API调用失败**  
  检查 `configs/system_prompt.txt`、API Key 是否正确，或网络是否畅通。

## 联系方式

- 开发团队：Robotdream team
- 研发组织：香港科技大学（广州）
- 邮箱：jruan189@connect.hkust.edu.cn

---

如需英文版或更详细的开发文档，请告知！ 