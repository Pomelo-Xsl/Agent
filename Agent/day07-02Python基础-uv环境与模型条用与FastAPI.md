# day7-02Python基础-uv环境与模型条用与FastAPI

## 课程内容总览

- 使用 `uv` 创建并复现 Python 项目环境。
- 使用 `.env` 安全配置阿里云百炼 API Key。
- 用 OpenAI 兼容 SDK 完成单轮、多轮和流式大模型调用。
- 理解 `model`、`messages`、`stream`、`temperature`、`max_completion_tokens` 的作用。
- 用 FastAPI 编写、启动、测试并拆分 Web API。

---

## Python AI 项目实战：使用 uv 和阿里云百炼调用大模型

### 为什么 AI 适合用 Python

学习 AI 应用开发，很多项目都会从 Python 开始。原因不是 Python 语法最特别，而是它在 AI 领域的生态比较成熟。

可以从三个角度理解：

| 原因               | 说明                                                         |
| ------------------ | ------------------------------------------------------------ |
| 大模型平台支持多   | 百炼、OpenAI、Claude、Gemini、DeepSeek 等平台通常都提供 Python SDK 或 Python 调用示例 |
| AI 开发生态完整    | 数据处理、向量数据库、RAG、Agent、模型评测等方向都有大量 Python 工具 |
| 适合做 AI 项目原型 | 可以先用 Python 跑通模型调用、知识库问答、工具调用等核心流程，再接入 Web 或后台系统 |

---

### uv 是什么

`uv` 是一个 Python 项目和依赖管理工具。 虚拟环境 + 包资源管理 + 项目管理 (命令的形式管理项目) 

先用大白话理解：

> 做 Python 项目时，经常要安装很多第三方库。不同项目需要的库不一样，如果都装在同一个地方，很容易互相影响。uv 就是帮我们把“项目环境”和“项目依赖”管理清楚的工具。

比如：

- 这个 AI 项目需要 `openai`
- 另一个数据分析项目需要 `pandas`
- 还有一个老项目可能需要旧版本的库 

如果不管理环境，后面很容易出现：

- 明明昨天能跑，今天装了别的库就报错
- 同一个库，不同项目需要不同版本
- 换一台电脑后，不知道应该安装哪些依赖

Python 里常见的环境和依赖管理方式有这些：

| 工具/方式          | 通俗理解                                                     | 常见用途                                 |
| ------------------ | ------------------------------------------------------------ | ---------------------------------------- |
| `pip`              | pip是包资源管理工具,只要安装了python解释器,自带pip. 不需要额外安装.Python 最基础的安装工具 | 安装第三方库，比如 `pip install openai`  |
| `venv`             | Python 自带的虚拟环境工具                                    | 给每个项目单独建一个环境,不能进行包管理. |
| `requirements.txt` | 可以通过命令, 将项目依赖清单导出到一个requirements.txt 文件. | 记录项目需要安装哪些库                   |
| `conda`            | conda 是一个集成环境,数据分析,机器学习当中,  (深度学习属于机器学习的一个分支) | 常用于 Anaconda、数据分析、深度学习环境  |
| `uv`               | 新一代 Python 项目和依赖管理工具. pycharm 2025 版本之后才支持. | 创建项目、管理环境、安装依赖、运行代码   |

如果学过 Java，可以把 `uv` 粗略类比成 Python 项目里的 Maven。

| Java 项目 | Python + uv 项目 | 类比理解 |
| --- | --- | --- |
| `pom.xml` | `pyproject.toml` | 记录项目配置和依赖 |
| Maven 下载依赖 | `uv add` 安装依赖 | 把项目需要的库加进来 |
| Maven 管理项目构建(命令 ) | uv 管理项目环境和运行(uv 命令) | 让项目更容易被别人复现 |
| `mvn test` / `mvn package` | `uv run` 运行命令 | 在项目环境里执行代码或工具 |

区别是：Maven 主要服务 Java 项目的构建和依赖管理；==uv 主要服务 Python 项目的虚拟环境、依赖安装和命令运行==。

这节课选择 `uv`，是因为它把很多步骤合在了一起：

| 过去可能要分开做   | 使用 uv 后             |
| ---------- | ------------------- |
| 创建虚拟环境     | `uv` 自动处理           |
| 安装依赖       | `uv add`            |
| 记录依赖       | 写入 `pyproject.toml` |
| 在项目环境里运行代码 | `uv run`            |

#### 安装 uv

在使用 `uv init`、`uv add`、`uv run` 之前，电脑上必须先安装 `uv`。

不同系统安装方式不一样。

##### macOS 安装方式

macOS 可以打开终端，执行：

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

如果电脑上安装了 Homebrew，也可以使用：

```bash
brew install uv
```

安装完成后，重新打开一个终端窗口，执行：

```bash
uv --version
```

如果能看到类似下面的输出，说明安装成功：

```text
uv 版本号
```

##### Windows 安装方式

Windows 可以打开 PowerShell，执行：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

安装完成后，关闭当前 PowerShell 窗口，重新打开一个新的 PowerShell，执行：

```powershell
uv --version
```

如果能看到版本号，说明安装成功。

##### 如果提示找不到 uv

如果安装完成后执行：

```bash
uv --version
```

提示：

```text
command not found: uv
```

或者：

```text
'uv' 不是内部或外部命令
```

通常不是安装失败，而是系统还没有识别到 `uv` 命令。

可以先尝试：

- 关闭终端，重新打开。
- 关闭 PyCharm，重新打开。
- Windows 重新打开 PowerShell。
- 如果还不行，重启电脑。

这类问题通常和环境变量 `PATH` 有关。

`PATH` 可以简单理解成：

```text
系统查找命令的位置列表
```

当我们输入：

```bash
uv
```

系统会去 `PATH` 记录的目录里找有没有 `uv` 这个程序。

如果安装了但是 `PATH` 没刷新，就会出现“找不到命令”的提示。

##### 验证 uv 是否可以正常使用

课堂上统一用下面命令检查：

```bash
uv --version
```

只要能看到版本号，就可以继续后面的项目创建。

课堂上先记住三个命令：

```bash
uv init 项目名
uv add 依赖名   
uv run python Python文件 [少用, 直接使用集成工具图形化界面]
```

---

### 创建第一个 Python AI 项目

如果使用 PyCharm，可以按下面的方式创建项目。

#### 使用 PyCharm 创建项目

现在新版 PyCharm 已经可以直接用 `uv` 创建 Python 项目。

打开 PyCharm 后：

1. 打开 PyCharm
2. 选择 `New Project`
3. 左侧选择 `Pure Python`
4. `Location` 选择项目位置，项目名填写 `YanQue-AI`
5. `Interpreter type` 选择 `uv`
6. `Python version` 先保持 `Default`
7. `Path to uv` 显示绿色对勾，说明 PyCharm 已经找到 uv
8. 点击 `Create`

创建完成后，PyCharm 会在项目目录下创建 `.venv` 虚拟环境。

可以把它理解成：

- PyCharm 负责创建项目
- `uv` 负责创建和管理 Python 环境
- 后面安装依赖、运行程序，都可以继续在 PyCharm 下面的 `Terminal` 里完成

如果不用 PyCharm，也可以用命令创建同样的项目：

```bash
uv init YanQue-AI
```

然后再用 PyCharm 打开这个 `YanQue-AI` 文件夹。

#### 项目目录长什么样

用 PyCharm 直接选择 `uv` 创建项目后，项目里一般会看到这些内容：


```text
YanQue-AI/
├── .venv/
├── pyproject.toml
└── main.py
```

其中：

| 文件 | 作用 |
| --- | --- |
| `.venv/` | 当前项目自己的 Python 虚拟环境，依赖包会安装到这里 |
| `pyproject.toml` | 项目配置和依赖 |
| `main.py` | 默认入口代码，刚开始可以先不写业务逻辑 |

这里先知道两个文件：

- `main.py`：项目默认入口，后面真正做完整项目时再用
- `pyproject.toml`：记录项目依赖和项目配置

`.venv` 一般不用手动修改，知道它是项目环境就可以。

#### 在 PyCharm 里运行项目

如果 `main.py` 里有默认示例代码，可以在 PyCharm 终端里执行：

```bash
uv run python main.py
```

如果能正常输出内容，说明项目环境已经能跑起来。

后面所有 `uv add`、`uv run` 命令，都可以直接在 PyCharm 下方的 `Terminal` 里执行。

---

### 安装项目依赖

使用 OpenAI 兼容方式调用百炼模型。

阿里云百炼支持 OpenAI 兼容接口，也就是说：我们可以使用 Python 的 `openai` SDK 调用百炼模型。

安装依赖：

```bash
uv add openai python-dotenv
```

这两个依赖分别负责：

| 依赖 | 作用 |
| --- | --- |
| `openai` | 用 OpenAI 兼容方式调用百炼接口 |
| `python-dotenv` | 从 `.env` 文件读取环境变量 |

安装完成后，`pyproject.toml` 里会出现这些依赖。

**我们在公司里面 如果是克隆的项目 通常不会有 `.venv` 这个文件夹 项目中的文件打开也通常都会报错 因为缺少环境配置和本地依赖**
**如果你看到有 `pyproject.toml` 这个文件 我们就可以通过 uv 来对当前项目进行依赖的下载和环境的配置 使用的命令是 `uv sync`**

---

### 准备阿里云百炼 API Key

阿里云:  综合的平台,云服务器,计算引擎, 云存储, 域名,....  

火山引擎: 综合的平台,云服务器,计算引擎, 云存储, 域名,....   使用方式基本一样.  

阿里百炼:  模型平台,  千问系列, deepseek, gpt, genina,  OpenAI规则. 

火山方舟: 模型平台,  千问系列, deepseek, gpt, genina,  OpenAI规则. 





打开百炼控制台：

[阿里云百炼 API 页面](https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.528f133cecRmYk&tab=api#/api/?type=model&url=3016807)

获取APIKey: https://bailian.console.aliyun.com/cn-beijing?spm=a2c4g.11186623.0.0.25055ec6Vww3jl&tab=model#/api-key
获取业务空间ID: https://bailian.console.aliyun.com/cn-beijing?spm=a2c4g.11186623.0.0.21e85e8esELU1k&tab=globalset#/efm/business_management?agentName=&pageNo=1&z_type_=%7B%22pageNo%22%3A%22num%22%7D



在控制台里需要关注三个信息：

| 信息 | 用途 |
| --- | --- |
| API Key | 程序调用模型时的身份凭证 |
| Base URL | 接口地址 |
| Model | 要调用的模型名称 |

不要把 API Key 写死在代码里。

推荐新建一个 `.env` 文件：

```bash
touch .env
```

在 `.env` 里写入：

```env
BAILIAN_API_KEY=你的百炼API_KEY
BAILIAN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
BAILIAN_MODEL=qwen-plus
```

说明：

- `BAILIAN_API_KEY`：换成你自己的百炼 API Key
- `BAILIAN_BASE_URL`：OpenAI 兼容接口地址
- `BAILIAN_MODEL`：可以先用 `qwen-plus`

---

### 第一个模型调用测试

这一步先写一个简单的测试文件，确认百炼接口能正常调用。

在项目里新建一个 `test` 目录，再新建一个 `bailian_api_test.py` 文件：

```text
YanQue-AI/
└── test/
    └── bailian_api_test.py
```

把 `test/bailian_api_test.py` 写成下面这样：

```python
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("BAILIAN_API_KEY")
base_url = os.getenv("BAILIAN_BASE_URL")
model = os.getenv("BAILIAN_MODEL", "qwen-plus")


if not api_key:
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "你是一个耐心的 AI 课程助教。"},
        {"role": "user", "content": "用一句话解释什么是大模型。"},
    ],
)


answer = response.choices[0].message.content
print("AI 回复：")
print(answer)
```

运行：

```bash
uv run python test/bailian_api_test.py
```

如果配置正确，终端会输出模型回答。

---

### 这段代码做了什么

先不要急着背代码。

可以把这段程序理解成 5 步：

| 步骤 | 代码做的事 |
| --- | --- |
| 1 | 从 `.env` 读取 API Key、接口地址和模型名 |
| 2 | 创建一个 OpenAI 兼容客户端 |
| 3 | 准备 system 和 user 消息 |
| 4 | 调用百炼大模型接口 |
| 5 | 取出模型回复并打印 |

这里最重要的是 `messages`。

```python
messages=[
    {"role": "system", "content": "你是一个耐心的 AI 课程助教。"},
    {"role": "user", "content": "用一句话解释什么是大模型。"},
]
```

可以先这样理解：

| role        | 含义            |
| ----------- | ------------- |
| `system`    | 给模型设定身份、规则和边界 |
| `user`      | 用户提出的问题       |
| `assistant` | 模型之前的回答       |

后面做多轮对话时，会把历史消息继续放进 `messages`。

---

### 大模型接口常见参数

刚才的代码里，我们已经调用了一次百炼大模型接口。

调用代码大概是这样：

```python
response = client.chat.completions.create(
    model=model,
    messages=messages,
)
```

这行代码看起来很短，但真实项目里经常会配置一些参数。

这一节先讲最常用的几个：

```text
model
messages
stream
temperature
max_completion_tokens
```

这些参数不是百炼独有的概念。

百炼提供了 OpenAI 兼容的调用方式，所以很多大模型平台在调用体验上都比较相似。

#### model：指定使用哪个模型

`model` 表示本次请求要调用哪个大模型。 名称一定是平台提供的. 不是自己瞎写.
https://bailian.console.aliyun.com/cn-beijing/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.528f133cecRmYk&tab=model#/model-market

通俗理解：

```text
model = 选择这次让哪个模型来回答 ,
```

比如：

```python
model = "qwen-plus"
```

表示这次调用百炼平台里的 `qwen-plus` 模型。

不同模型能力、速度、价格可能不一样。

可以先这样理解：

| 模型差异 | 通俗理解 |
| --- | --- |
| 能力不同 | 有的模型更擅长推理，有的更擅长写作，有的更擅长代码 |
| 速度不同 | 大模型通常更强，但可能更慢 |
| 成本不同 | 能力越强、上下文越长，调用成本通常越高 |
| 场景不同 | 聊天、代码、长文档、Embedding 可能会用不同模型 |

示例代码：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "用一句话解释什么是 AI。"},
    ],
)

print(response.choices[0].message.content)
```

课堂提醒：

```text
ChatGPT、通义千问、DeepSeek 官网是 AI 产品；
qwen-plus、GPT、DeepSeek-V3 这类才是具体模型或模型系列。
```

#### messages：告诉模型本次对话内容

`messages` 是大模型对话接口里最重要的参数之一。

它表示本次要交给模型的消息列表。

通俗理解：



```text
messages = 把“系统要求 + 用户问题 + 历史对话”一起交给模型
```

`messages` 里常见的角色有三个： 

| role        | 作用                                        | 类比                     |
| ----------- | ------------------------------------------- | ------------------------ |
| `system`    | 设定模型身份、规则、边界                    | 老师提前给助教的工作要求 |
| `user`      | 用户输入的问题或需求                        | 学生提出的问题           |
| `assistant` | 模型之前回答过的内容                        | 助教前面已经说过的话     |
| tool (工具) | 调用第三方工具响应的结果信息, 携带给大模型. |                          |

##### system 示例

`system` 通常用来规定模型怎么回答。

示例代码：

```python
messages = [
    {
        "role": "system",
        "content": "你是一个 Java + AI 课程助教，回答要通俗，适合零基础学生。",
    },
    {
        "role": "user",
        "content": "什么是大模型？",
    },
]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
)

print(response.choices[0].message.content)
```

##### user 示例

`user` 表示用户当前提出的问题。

示例代码：

```python
messages = [
    {
        "role": "user",
        "content": "帮我用 3 句话解释什么是 Prompt。",
    },
]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
)

print(response.choices[0].message.content)
```

##### assistant 示例

`assistant` 表示模型之前已经回答过的内容。

它通常用于多轮对话。

例如第一轮：

```text
用户：我正在学习 Java + AI 课程。
AI：好的，我可以作为你的课程助教。
```

第二轮用户问：

```text
那我第一天应该重点掌握什么？
```

如果我们想让模型知道前面聊过什么，就要把历史消息也放进 `messages`。

示例代码：

```python
messages = [
    {
        "role": "system",
        "content": "你是一个 Java + AI 课程助教。",
    },
    {
        "role": "user",
        "content": "我正在学习 Java + AI 课程。",
    },
    {
        "role": "assistant",
        "content": "好的，我可以作为你的课程助教。",
    },
    {
        "role": "user",
        "content": "那我第一天应该重点掌握什么？",
    },
]

response = client.chat.completions.create(
    model="qwen-plus",
    messages=messages,
)

print(response.choices[0].message.content)
```

课堂提醒：

```text
大模型不会自动知道上一轮聊了什么。
多轮对话的关键，是把历史消息继续放进 messages。
```

#### stream：是否开启流式输出

`stream` 表示是否让模型边生成边返回。

通俗理解：

```text
stream=False：等模型全部生成完，一次性返回
stream=True：模型生成一点，就返回一点. chuck 片段. 
```

如果不开启流式输出，用户可能要等完整回答生成完才能看到结果。

示例代码：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "请用 200 字介绍 RAG。"},
    ],
    stream=False,
)

print(response.choices[0].message.content)
```

开启流式输出：

```python
stream = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "请用 200 字介绍 RAG。"},
    ],
    stream=True,
)

for chunk in stream:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)
```

课堂提醒：

```text
stream=True 不会让模型变聪明。
它主要改善用户体验，让用户更快看到回答正在生成。
```

后面做学生端 AI 问答时，页面上“逐字输出”的效果，就和流式输出有关。

#### temperature：控制回答的随机性

`temperature` 用来控制模型回答的随机性。

通俗理解：

```text
temperature 越低：回答越稳定、越保守
temperature 越高：回答越发散、越有创造性
```

比如：

| temperature | 常见效果    | 适合场景             |
| ----------- | ------- | ---------------- |
| `0` 或接近 `0` | 更稳定、更确定 | 代码生成、SQL 生成、规则问答 |
| `0.7` 左右    | 稍微有变化   | 普通聊天、文案、解释概念     |
| `1` 或更高     | 更发散     | 创意写作、头脑风暴        |

示例代码：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "给 Java + AI 课程起 5 个标题。"},
    ],
    temperature=0.2,
)

print(response.choices[0].message.content)
```

如果想要更有创意，可以调高一点：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "给 Java + AI 课程起 5 个有吸引力的标题。"},
    ],
    temperature=0.9,
)

print(response.choices[0].message.content)
```

课堂提醒：

```text
业务系统里如果要求稳定，temperature 不要太高。
```

比如生成 SQL、判断订单状态、回答制度规则时，通常更希望稳定，不希望模型自由发挥太多。

#### max_completion_tokens：限制模型最多生成多少 Token

`max_completion_tokens` 用来限制模型本次最多生成多少 Token。

通俗理解：

```text
max_completion_tokens = 给模型回答设置一个最长输出长度
```

注意它限制的是“模型输出”，不是用户输入。

比如：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "详细解释什么是 Agent。"},
    ],
    max_completion_tokens=100,
)

print(response.choices[0].message.content)
```

如果设置太小，模型可能还没说完就被截断。 

比如让模型“详细解释 Agent”，但只给 30 个 Token：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "user", "content": "详细解释什么是 Agent。"},
    ],
    max_completion_tokens=30,
)

print(response.choices[0].message.content)
```

可能会出现回答不完整的情况。

课堂提醒：

```text
max_completion_tokens 太小：回答可能被截断
max_completion_tokens 太大：可能增加等待时间和 token 成本
```

所以在真实项目里，一般会根据业务场景设置合理上限。

#### 参数放在一起的完整示例

最后把这些参数组合起来看一遍：

```python
response = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {
            "role": "system",
            "content": "你是一个 Java + AI 课程助教，回答要通俗、结构清楚。",
        },
        {
            "role": "user",
            "content": "用通俗的话解释什么是 RAG，并举一个教育系统里的例子。",
        },
    ],
    temperature=0.3,
    max_completion_tokens=300,
    stream=False,
)

print(response.choices[0].message.content)
```

这段代码可以翻译成：

```text
使用 qwen-plus 模型
按照 system 的要求扮演课程助教
回答 user 提出的问题
回答尽量稳定一点
最多生成 300 个 Token
等完整回答生成完以后一次性返回
```

---

### 加入多轮对话

第一个测试程序只能问一次。

现在可以再建一个测试文件：

```text
test/chat_loop_test.py
```

这个文件用来测试“多轮对话”。

把 `test/chat_loop_test.py` 写成下面这样：

```python
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("BAILIAN_API_KEY")
base_url = os.getenv("BAILIAN_BASE_URL")
model = os.getenv("BAILIAN_MODEL", "qwen-plus")


if not api_key:
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


messages = [
    {
        "role": "system",
        "content": "你是一个 AI 课程助教，回答要清楚、简洁，适合零基础学生。",
    }
]


print("AI 助手已启动，输入 exit / quit / 退出 都可以结束。")


while True:
    user_input = input("\n用户:")

    if user_input.strip().lower() in {"exit", "quit", "退出"}:
        print("已退出。")
        break

    messages.append({"role": "user", "content": user_input})
 
    #调用模型, 发送消息. 
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    # 模型的第一次响应的结果: 
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})

    print("\nAI：")
    print(answer)
```

运行：

```bash
uv run python test/chat_loop_test.py
```

可以连续输入：

```text
什么是大模型？
那它和普通程序有什么区别？
能不能举一个客服系统的例子？
```

这个版本已经具备最基础的多轮对话能力。

---

### 加入流式输出

真实 AI 产品里，模型通常不是等全部生成完再显示，而是一边生成一边显示。

把多轮对话里的调用部分改成：

```python
import os  
  
from dotenv import load_dotenv  
from openai import OpenAI  
  
  
load_dotenv()  
  
  
api_key = os.getenv("BAILIAN_API_KEY")  
base_url = os.getenv("BAILIAN_BASE_URL")  
model = os.getenv("BAILIAN_MODEL", "qwen-plus")  
  
  
if not api_key:  
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")  
  
  
client = OpenAI(  
    api_key=api_key,  
    base_url=base_url,  
)  
  
  
messages = [  
    {  
        "role": "system",  
        "content": "你是一个 AI 课程助教，回答要清楚、简洁，适合零基础学生。",  
    }  
]  
  
  
print("AI 助手已启动，输入 exit / quit / 退出 都可以结束。")  
  
  
while True:  
    user_input = input("\n你：")  
  
    if user_input.strip().lower() in {"exit", "quit", "退出"}:  
        print("已退出。")  
        break  
  
    messages.append({"role": "user", "content": user_input})  
  
    # 模型的响应信息. 
    response = client.chat.completions.create(  
        model=model,  
        messages=messages,  
        stream=True,  
    )  
  
    # [chunk,chunk2, chunk3]  chunk 片段 ---> 落库. 保存. 
    answer_parts = []  
  
    print("\nAI：", end="")  
    for chunk in response:  
        delta = chunk.choices[0].delta.content  
        if delta:  
            print(delta, end="")  
            answer_parts.append(delta)  
   # [chunk,chunk2, chunk3] answer 是一个完成的答案. 
    answer = "".join(answer_parts)  
    messages.append({"role": "assistant", "content": answer})  # 实际项目当中, 一定要落库. 
```

流式输出的体验更接近 ChatGPT、通义、豆包这类产品。

---

### 课堂练习：调用大模型实现猜数字游戏

前面我们已经完成了：

```text
单轮问答
  ↓
多轮对话
  ↓
流式输出
```

接下来做一个小练习：

```text
调用大模型实现一个猜数字游戏
```

游戏规则：

```text
AI 先固定一个 1 到 100 之间的数字
用户每次输入一个数字
AI 根据用户输入提示“大了”或“小了”
同时告诉用户下一次应该在什么范围内继续猜
重复这个过程
直到用户猜对数字
```

这里要注意一个工程细节：

```text
为了让课堂 Demo 更稳定，秘密数字由 Python 程序随机生成一次。
当前可猜范围也由 Python 程序维护。
大模型负责扮演游戏主持人，根据程序给出的结果生成提示语。
```

也就是说：

```text
Python 程序负责固定答案、更新范围、控制退出
大模型负责把判断结果包装成自然语言提示
```

这样既能体现大模型参与游戏，又能避免模型每轮自己改答案。

新建文件：

```text
test/guess_number_game.py
```

代码如下：

```python
import os
import random

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


api_key = os.getenv("BAILIAN_API_KEY")
base_url = os.getenv("BAILIAN_BASE_URL")
model = os.getenv("BAILIAN_MODEL", "qwen-plus")


if not api_key:
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


secret_number = random.randint(1, 100)
low = 1
high = 100


messages = [
    {
        "role": "system",
        "content": """
你是一个猜数字游戏主持人。

游戏规则：
1. 用户每次会输入一个 1 到 100 之间的数字。
2. 程序会告诉你用户本次猜测结果，以及下一次应该猜的范围。
3. 你只负责根据程序给出的结果生成提示语。
4. 在用户猜对之前，绝对不要自己编造或透露秘密数字。
5. 回复要简短、自然，像一个游戏主持人。
""",
    }
]


print("猜数字游戏开始。")
print("我已经想好了一个 1 到 100 之间的数字。")
print("请输入你的猜测，输入 exit / quit / 退出 可以结束游戏。")
print(f"当前可猜范围：{low} 到 {high}")


while True:
    user_input = input("\n你猜：").strip()

    if user_input.lower() in {"exit", "quit", "退出"}:
        print("游戏结束。")
        break

    if not user_input.isdigit():
        print("请输入一个数字。")
        continue

    guess = int(user_input)

    if guess < low or guess > high:
        print(f"请输入 {low} 到 {high} 之间的数字。")
        continue

    if guess < secret_number:
        low = guess + 1
        result = "猜小了"
        range_text = f"{low} 到 {high}"
        is_correct = False
    elif guess > secret_number:
        high = guess - 1
        result = "猜大了"
        range_text = f"{low} 到 {high}"
        is_correct = False
    else:
        result = "猜对了"
        range_text = "游戏结束"
        is_correct = True

    messages.append(
        {
            "role": "user",
            "content": f"""
用户本次猜测数字：{guess}
判断结果：{result}
下一次可猜范围：{range_text}

请根据上面的结果回复用户。
如果没有猜对，必须明确告诉用户下一次可猜范围。
如果猜对了，要恭喜用户并结束游戏。
""",
        }
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
        max_completion_tokens=80,
    )

    answer = response.choices[0].message.content
    messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    print("\nAI：")
    print(answer)

    if is_correct:
        break
```

运行：

```bash
uv run python test/guess_number_game.py
```

运行效果大概是：

```text
猜数字游戏开始。
我已经想好了一个 1 到 100 之间的数字。
请输入你的猜测，输入 exit / quit / 退出 可以结束游戏。

你猜：50

AI：
猜小了，请再大一点。下一次可以在 51 到 100 之间猜。

你猜：75

AI：
猜大了，请再小一点。下一次可以在 51 到 74 之间猜。

你猜：63

AI：
恭喜你，猜对了！
```

这个练习里用到了前面学过的几个点：

| 内容 | 在游戏里的作用 |
| --- | --- |
| `system` | 告诉模型扮演猜数字游戏主持人，并告诉它秘密数字和规则 |
| `user` | 用户每次输入的猜测 |
| `assistant` | 模型每轮给出的提示 |
| `messages` | 保存整个游戏过程，让模型知道前面猜过什么 |
| `temperature=0.2` | 让模型回答更稳定，不要太发散 |
| `max_completion_tokens=80` | 限制提示语不要太长 |
| `low` / `high` | 由 Python 程序维护当前可猜范围 |

课堂思考：

```text
为什么秘密数字和当前范围都不建议完全交给大模型维护？
```

参考答案：

```text
因为如果每轮都让模型自由生成，它可能前后不一致。
第一轮心里想的是 63，第二轮可能又变成 72。
或者第一轮提示范围是 51 到 100，第二轮又说成 40 到 100。
真实项目里，关键状态最好由程序保存，大模型负责理解和生成。
```

这个练习也能帮助大家理解：

> **==AI 应用开发不是把所有事情都交给模型，而是让程序控制关键逻辑，让模型负责适合它的自然语言交互。==**

---

### FastAPI 是什么

前面我们已经能在 Python 文件里调用大模型了。

但真实项目里，AI 能力通常不会只在命令行里运行，而是会做成一个接口，让网页、后台系统、小程序或其他服务来调用。

这时候就可以用 `FastAPI`。 

`FastAPI` 是一个 Python Web 框架，可以用来快速开发接口。

可以先这样理解：

| 内容         | 作用                            |
| ---------- | ----------------------------- |
| Python 函数  | 写具体业务逻辑                       |
| FastAPI 接口 | 把 Python 函数变成可以被外部访问的 HTTP 接口 |
| 浏览器或前端     | 通过接口调用后端能力                    |

比如：

- Python 代码负责调用百炼大模型
- FastAPI 负责提供 `/chat` 接口
- 前端页面或其他系统向 `/chat` 发送问题
- 后端调用大模型后，把回答返回给前端

FastAPI 里常见两个对象：

| 对象            | 作用                |
| ------------- | ----------------- |
| `FastAPI()`   | 创建整个 Web 应用       |
| `APIRouter()` | 创建一组接口，方便把接口按模块管理 |

可以先这样理解：

- `app = FastAPI()`：整个后端服务
- `router = APIRouter()`：某一组接口
- `app.include_router(router)`：把这组接口挂到整个服务上

---

### 安装 FastAPI

继续在 PyCharm 终端里安装依赖：

```bash
uv add fastapi uvicorn
```

这两个依赖分别负责：

| 依赖        | 作用              |
| --------- | --------------- |
| `fastapi` | 用来编写 Web 接口     |
| `uvicorn` | 用来启动 FastAPI 服务 |

安装完成后，`pyproject.toml` 里会出现 `fastapi` 和 `uvicorn`。 

注意: 如果安装不成功, 网络问题, 考虑梯子问题. 

---

### 写一个最简单的 FastAPI 接口

单文件方式适合学习，因为所有代码都在一个文件里，更容易看清楚：

在项目根目录新建一个 `app.py` 文件：

```text
YanQue-AI/
├── .env
├── app.py
├── pyproject.toml
└── test/
    └── bailian_api_test.py
```

#### 一个完整的单文件示例

在 `app.py` 里写入下面代码。

	这份代码既包含普通接口，也包含一个调用大模型的 `/chat` 接口。

```python
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()


api_key = os.getenv("BAILIAN_API_KEY")
base_url = os.getenv("BAILIAN_BASE_URL")
model = os.getenv("BAILIAN_MODEL", "qwen-plus")


if not api_key:
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")


client = OpenAI(api_key=api_key, base_url=base_url)


app = FastAPI()


class ChatRequest(BaseModel):
    question: str


class CourseUpdateRequest(BaseModel):
    title: str
    description: str = ""


@app.get("/")
def index():
    return {"message": "YanQue AI 服务已启动"}


@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    include_detail: bool = False,
    x_user_id=Header(default=None),
):
    description = "这是课程详情" if include_detail else None

    return {
        "course_id": course_id,
        "title": "Java + AI 应用开发",
        "description": description,
        "operator": x_user_id,
    }


@app.post("/chat")
def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个耐心的 AI 课程助教。"},
            {"role": "user", "content": request.question},
        ],
    )

    answer = response.choices[0].message.content
    return {"answer": answer}


@app.put("/courses/{course_id}")
def update_course(
    request: CourseUpdateRequest,
    course_id: int,
    x_user_id=Header(default=None),
):
    return {
        "course_id": course_id,
        "title": request.title,
        "description": request.description,
        "operator": x_user_id,
    }


@app.delete("/courses/{course_id}")
def delete_course(
    course_id: int,
    x_user_id=Header(default=None),
):
    return {
        "success": True,
        "message": f"课程 {course_id} 已删除",
        "operator": x_user_id,
    }
```

#### GET、POST、PUT、DELETE 分别怎么理解

常见写法：

```python
@app.get("/路径")
def 函数名():
    ...

@app.post("/路径")
def 函数名():
    ...

@app.put("/路径")
def 函数名():
    ...

@app.delete("/路径")
def 函数名():
    ...
```

可以先这样理解：

| 请求类型     | 常见用途        | 本节示例                          |
| -------- | ----------- | ----------------------------- |
| `GET`    | 查询数据        | `GET /courses/{course_id}`    |
| `POST`   | 新增数据或提交复杂请求 | `POST /chat`                  |
| `PUT`    | 修改已有数据      | `PUT /courses/{course_id}`    |
| `DELETE` | 删除数据        | `DELETE /courses/{course_id}` |

#### 请求参数怎么接收

HTTP 请求里常见参数可以分成几类。

##### 路径参数

路径参数写在 URL 路径中。

比如：

```text
GET /courses/1001
```

这里的 `1001` 就是课程 ID。

FastAPI 代码：

```python
@app.get("/courses/{course_id}")
def get_course(course_id: int):
    return {"course_id": course_id}
```

这里的 `: int` 可以让 FastAPI 把路径里的 `1001` 转成整数。

如果不写类型，也能接收到参数，但默认更像普通字符串。

但是必须要记住：

```text
路径参数写在路由里：/courses/{course_id}
函数参数名要和 {course_id} 对上
```

##### 查询参数

查询参数写在 URL 问号后面。

比如：

```text
GET /courses/1001?include_detail=true
```

这里的 `include_detail=true` 就是查询参数。

FastAPI 代码：

```python
@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    include_detail: bool = False,
):
    return {
        "course_id": course_id,
        "include_detail": include_detail,
    }
```

这里没有使用 `Query(...)`，也可以正常接收查询参数。

`Query(...)` 主要用于补充说明、默认值校验、最小值最大值限制等高级用法。

##### 请求头

请求头通常用来传递身份、Token、客户端信息等。

比如：

```text
X-User-Id: 10086
```

FastAPI 代码：

```python
@app.get("/courses/{course_id}")
def get_course(
    course_id: int,
    x_user_id=Header(default=None),
):
    return {
        "course_id": course_id,
        "operator": x_user_id,
    }
```

注意：

```text
Python 参数名 x_user_id
对应 HTTP 请求头 X-User-Id
```

FastAPI 会自动把下划线和横线做对应。

##### 请求体

请求体通常用来接收 JSON。

比如调用聊天接口时，请求体是：

```json
{
  "question": "用一句话解释什么是大模型"
}
```

FastAPI 通常用 Pydantic 模型接收请求体：

```python
class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
def chat(request: ChatRequest):
    return {"question": request.question}
```

这里的 `question: str` 建议保留。

因为 Pydantic 需要通过这个类型知道：

```text
请求体里应该有一个 question 字段
这个字段应该是字符串
```

#### 返回数据怎么定义

最简单的返回方式是直接返回字典：

```python
@app.get("/")
def index():
    return {"message": "YanQue AI 服务已启动"}
```

可以先采用更简单的写法：

```python
@app.post("/chat")
def chat(request: ChatRequest):
    return {"answer": "这里是 AI 回答"}
```

后面项目代码变复杂以后，可以再使用 `response_model`。

它的作用是让返回结构更清楚，并且自动生成更完整的接口文档。

#### 启动 FastAPI 服务

命令行启动：

```bash
uv run uvicorn app:app --reload
```

这里的 `app:app` 可以拆成两部分：

```text
app : app
```

- 前面的 `app`：表示 `app.py` 这个文件
- 后面的 `app`：表示文件里的 `app = FastAPI()` 这个对象

这里有一个常见误解：

```text
文件名不一定必须叫 app.py
对象名也不一定必须叫 app
```

比如文件叫：

```text
main.py
```

代码里写：

```python
api = FastAPI()
```

那么启动命令就是：

```bash
uv run uvicorn main:api --reload
```

也就是说：

```text
uvicorn 模块路径:FastAPI对象名
```

`--reload` Uvicorn 会监控我们的项目的文件,当我们修改了代码并且进行了保存, 它会字段进行加载应用而不需要进行重启服务, 相当于是一个热启动

#### 默认端口和修改端口

如果不指定端口，`uvicorn` 默认使用 `8000` 端口。

所以：

```bash
uv run uvicorn app:app --reload
```

启动后默认访问：

```text
http://127.0.0.1:8000
```

如果 8000 端口被占用，或者想换一个端口，可以加 `--port`：

```bash
uv run uvicorn app:app --reload --port 9000
```

启动后访问：

```text
http://127.0.0.1:9000
```

如果希望局域网其他电脑也能访问，可以指定 `host`：

```bash
uv run uvicorn app:app --reload --host 0.0.0.0 --port 9000
```

一般使用本机访问即可：

```text
http://127.0.0.1:8000
```

#### 在 PyCharm 中启动服务

除了在终端里输入命令，也可以在 PyCharm 中配置启动。

方式一：使用 PyCharm 终端。

在 PyCharm 底部打开 Terminal，执行：

```bash
uv run uvicorn app:app --reload
```

这是最简单、最推荐第一天使用的方式。

方式二：创建 Python 启动入口。

在 `app.py` 最下面加上：

```python
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
```

然后在 PyCharm 里右键运行 `app.py`。

这里的 `"app:app"` 仍然表示：

```text
app.py 文件里的 app 对象
```

如果文件名或对象名改了，这里也要同步修改。

---

### 多个 API 文件用 APIRouter 管理

前面是把所有接口都写在一个 `app.py` 里。

优点是简单。

缺点是项目稍微变大，文件会越来越乱。

比如后面我们可能会有：

- 健康检查接口
- AI 对话接口
- 会话管理接口
- 知识库接口
- 文件上传接口
- 流式输出接口

如果全部放在一个文件里，会很难维护。

所以项目稍微大一点时，通常会把代码放到 `src` 目录下，并使用 `APIRouter` 管理多个接口文件。

可以先这样理解：

```text
FastAPI() = 整个后端服务
APIRouter() = 某一组接口
include_router() = 把某一组接口挂到整个服务上
```

目录可以这样放：

```text
YanQue-AI/
├── .env
├── app.py
├── pyproject.toml
├── src/
│   └── yanque_ai/
│       ├── main.py
│       └── api/
│           ├── health_api.py
│           └── session_api.py           
└── test/
    └── bailian_api_test.py
```

可以先这样理解：

| 文件                                 | 作用                           |
| ---------------------------------- | ---------------------------- |
| `src/yanque_ai/main.py`            | FastAPI 主入口，统一加载所有 router    |
| `src/yanque_ai/api/health_api.py`  | 健康检查接口，比如 `/`                |
| `src/yanque_ai/api/chat_api.py`    | AI 对话接口，比如 `/api/v1/chat`    |
| `src/yanque_ai/api/session_api.py` | 会话管理接口，比如 `/api/v1/sessions` |

在 `src/yanque_ai/api/health_api.py` 里写入：

```python
from fastapi import APIRouter


router = APIRouter(tags=["health"])


@router.get("/")
def index():
    return {"message": "YanQue AI 服务已启动"}
```

在 `src/yanque_ai/api/chat_api.py` 里写入：

```python
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Header
from openai import OpenAI
from pydantic import BaseModel


load_dotenv()


api_key = os.getenv("BAILIAN_API_KEY")
base_url = os.getenv("BAILIAN_BASE_URL")
model = os.getenv("BAILIAN_MODEL", "qwen-plus")


if not api_key:
    raise RuntimeError("请先在 .env 文件中配置 BAILIAN_API_KEY")


client = OpenAI(api_key=api_key, base_url=base_url)


router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("")
def chat(
    request: ChatRequest,
    x_user_id=Header(default=None),
):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"你是一个耐心的 AI 课程助教。当前用户 ID：{x_user_id}",
            },
            {"role": "user", "content": request.question},
        ],
    )

    answer = response.choices[0].message.content
    return {"answer": answer}
```

因为这里写了：

```python
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
```

又写了：

```python
@router.post("")
```

所以最终接口地址是：

```text
POST /api/v1/chat
```

再新建 `src/yanque_ai/api/session_api.py`：

```python
from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


class SessionCreateRequest(BaseModel):
    title: str


@router.get("")
def list_sessions(
    page: int = 1,
    size: int = 10,
):
    return [
        {"session_id": 1, "title": "第一轮 AI 问答", "status": "ACTIVE"},
        {"session_id": 2, "title": "RAG 学习记录", "status": "ACTIVE"},
    ]


@router.post("")
def create_session(request: SessionCreateRequest):
    return {
        "session_id": 1001,
        "title": request.title,
        "status": "ACTIVE",
    }


@router.delete("/{session_id}")
def delete_session(session_id: int):
    return {
        "success": True,
        "message": f"会话 {session_id} 已删除",
    }
```

在 `src/yanque_ai/main.py` 里统一加载这些 router：

```python
from fastapi import FastAPI

from yanque_ai.api.chat_api import router as chat_router
from yanque_ai.api.health_api import router as health_router
from yanque_ai.api.session_api import router as session_router


app = FastAPI()


app.include_router(health_router)
app.include_router(chat_router)
app.include_router(session_router)
```

其中：

- `health_api.py` 负责健康检查相关接口
- `chat_api.py` 负责 AI 对话相关接口
- `session_api.py` 负责会话管理相关接口
- 每个 API 文件都有自己的 `router = APIRouter(...)`
- `main.py` 通过 `app.include_router(...)` 把多个 router 加到同一个 FastAPI 应用里

#### 一个模块中可以有多个 router 吗

可以。(不推荐)

比如一个 `admin_api.py` 里同时定义：

```python
from fastapi import APIRouter


course_router = APIRouter(prefix="/api/v1/admin/courses", tags=["admin-course"])
student_router = APIRouter(prefix="/api/v1/admin/students", tags=["admin-student"])


@course_router.get("")
def list_courses():
    return []


@student_router.get("")
def list_students():
    return []
```

然后在 `main.py` 中：

```python
from yanque_ai.api.admin_api import course_router, student_router


app.include_router(course_router)
app.include_router(student_router)
```

但是真实项目里更推荐：

```text
一个业务模块一个文件
一个文件里优先放一个主要 router
```

这样结构更清楚。

除非某个文件确实需要拆出多个完全不同的接口分组，否则不要一开始就把 router 设计得太复杂。

#### router 的常见参数

`APIRouter` 里可以写参数，用来统一管理这一组接口。

比如：

```python
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
```

常见参数可以先记住这些：

| 参数                | 作用                                      |
| ------------------- | ----------------------------------------- |
| `prefix`            | 给这一组接口统一加前缀(重要)              |
| `tags`              | 给接口文档分组，方便在 `/docs` 页面里查看 |
| `dependencies`      | 给这一组接口统一加依赖，比如统一鉴权      |
| `responses`         | 给这一组接口补充统一的响应说明            |
| `deprecated`        | 标记这一组接口是否已废弃                  |
| `include_in_schema` | 是否显示在自动生成的接口文档里            |

其中最常用的是 `prefix` 和 `tags`。

比如：

```python
router = APIRouter(prefix="/api/v1/chat", tags=["chat"])
```

再配合：

```python
@router.post("")
def chat(request: ChatRequest):
    ...
```

最终接口地址就是：

```text
/api/v1/chat
```

`tags=["chat"]` 不会影响接口地址，它只是让这个接口在 `http://127.0.0.1:8000/docs` 里归到 `chat` 分组下面。

#### 启动多文件项目

启动命令：

```bash
uv run uvicorn yanque_ai.main:app --reload
```

这里的 `yanque_ai.main:app` 可以拆成两部分：

```text
yanque_ai.main : app
```

- 前面的 `yanque_ai.main`：表示 `src/yanque_ai/main.py` 这个模块
- 后面的 `app`：表示文件里的 `app = FastAPI()` 这个对象

如果端口被占用，也可以修改端口：

```bash
uv run uvicorn yanque_ai.main:app --reload --port 9000
```

在 PyCharm 中启动也可以使用同样思路。

方式一：在 PyCharm Terminal 执行启动命令。

方式二：在 `src/yanque_ai/main.py` 里添加：

```python
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "yanque_ai.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
```

然后右键运行 `main.py`。

如果启动时报：

```text
ModuleNotFoundError: No module named 'yanque_ai'
```

说明 Python 没有找到 `src/yanque_ai` 这个包。

可以用下面方式解决：

```bash
PYTHONPATH=src uv run uvicorn yanque_ai.main:app --reload
```

在 PyCharm 中，也可以把 `src` 标记为 Sources Root。

简单理解：

```text
src 是源码目录
Python 要知道从 src 下面找 yanque_ai 包
```

---

### 访问 FastAPI 服务

无论使用方式一还是方式二，只要服务启动成功，终端都会看到类似这样的地址：

```text
http://127.0.0.1:8000
```

打开浏览器访问：

```text
http://127.0.0.1:8000
```

如果看到下面的内容，说明服务已经启动：

```json
{"message":"YanQue AI 服务已启动"}
```

FastAPI 还会自动生成接口文档。

打开：

```text
http://127.0.0.1:8000/docs
```

如果启动的是方式一，找到 `POST /chat`。

如果启动的是方式二，找到 `POST /api/v1/chat`。

点击 `Try it out`，输入：

```json
{
  "question": "用一句话解释什么是大模型"
}
```

点击 `Execute`，就可以看到大模型返回的回答。

