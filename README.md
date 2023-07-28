# 语音助手项目

这是一个基于 Python 的语音助手项目，它使用了腾讯云的 ASR 服务，OpenAI 的 GPT-3 API，以及 Porcupine 唤醒词引擎。

## 结构

这个项目的结构如下：

```
voice_assistant/
│
├── docs/
│   └── README.md   # 项目文档
│
├── hardware/
│   ├── __init__.py
│   └── microphone.py   # 包含 AudioRecorder 和 WakeWordDetector 类
│
├── helpers/
│   ├── __init__.py
│   └── helper.py   # 包含一些实用函数
│
├── services/
│   ├── __init__.py
│   ├── gpt3.py   # 包含 GPT 类，用于与 GPT-3 API 进行交互
│   └── tencent.py   # 包含 TencentASR 类，用于与腾讯云 ASR 服务进行交互
│
├── tests/
│   ├── test_main.py
│   ├── test_gpt3.py
│   ├── test_microphone.py
│   └── test_tencent.py   # 测试脚本
│
├── config.py   # 包含所有的配置常量
├── main.py   # 主程序
└── README.md
└── requirements.txt
```

## 使用方法

1. 安装所有必需的依赖项。
   `pip3 install -r requirements.txt`
2. 在 "config.py" 文件中填写您的 API 密钥。【包括：腾讯ASR、porcupine、OpenAI】
3. 运行 "main.py" 文件以启动语音助手。
   `python main.py`

## 注意事项

请自备梯子以访问OpenAI API。
