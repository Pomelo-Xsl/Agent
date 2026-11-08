# day6-01Python基础-文件操作、异常处理、Http请求与日志

## 学习目标：

- 使用 open() 读写文本文件
- 处理文件路径（相对路径、绝对路径）
- 使用 with 语句自动管理文件资源(推荐)
- 捕获和处理异常（try-except）
- 记录程序日志（logging 模块）
- 读写 JSON 文件存储数据      
- 处理 CSV 文件
- 构建对话记录保存系统
- 使用requests库发送http请求

---

## 文件操作

文件操作是 Python 编程中数据持久化的核心手段，通过文件操作可将内存中的数据写入磁盘长期存储，或读取磁盘文件中的数据进行处理。

### 为什么需要文件操作

程序运行时的数据存储在内存中，程序关闭后数据就消失了。文件操作让数据可以：

- 永久保存
- 跨程序共享
- 批量处理

## 文件的基本概念

文件是存储在磁盘上的有序数据集合，可包含文本、图像、音频、视频、程序代码等多种类型数据。文件系统通过**文件名**（含名称和扩展名，如`test.txt`、`image.png`）和**文件路径**定位文件，确保程序能准确找到目标文件。

在编程中，数据默认存储在内存（程序结束后丢失），将数据写入磁盘文件的过程称为**持久化**，是长期保存数据的关键方式。

### 文件的分类

根据存储格式，文件主要分为两类：

1. **纯文本文件**：有统一字符编码（如 ASCII、UTF-8、GBK、ISO-8859-1），本质是存储在磁盘上的长字符串，可直接用文本编辑器打开阅读（如`.txt`、`.py`、`.md`文件）。
2. **二进制文件**：无统一字符编码，由 0 和 1 直接组成，存储原始数据（如`.jpg`、`.mp4`、`.zip`文件），需特定程序解析才能识别。

### 文件读取

文件操作是数据持久化的基础。AI 应用中需要读取 prompt 模板、知识库文档、配置文件等。

### 基本文件读取

**open() 函数**

```python
# 打开文件
file = open("example.txt", "r", encoding="utf-8")
# r: 读取模式
# encoding: 指定编码，中文文件必须指定 utf-8

# 读取内容
content = file.read()
print(content)

# 关闭文件（重要！）
file.close()
```

**文件读取模式：**

文件打开模式决定了文件的操作权限，常见模式组合如下：

| 模式 | 说明                                                         | 适用场景                                 |
| ---- | ------------------------------------------------------------ | ---------------------------------------- |
| r    | 文本模式 + 只读，文件不存在则报错(read)                      | 读取文本文件（如配置文件、日志）         |
| w    | 文本模式 + 写入，覆盖原有内容，文件不存在则创建(write)       | 重新写入文件（如生成报告、清空日志）     |
| a    | 文本模式 + 追加，在文件末尾添加内容，文件不存在则创建. (append) | 累加数据（如日志追加、记录操作记录）     |
| x    | 文本模式 + 创建写入，文件已存在则报错                        | 确保文件唯一（如创建新的用户配置文件）   |
| rb   | 二进制模式 + 只读(read+ binary)                              | 读取二进制文件（如图片、视频）           |
| wb   | 二进制模式 + 写入(write binary)                              | 写入二进制文件（如保存图片、生成压缩包） |
| a+   | 文本模式 + 读写 + 追加                                       | 边读边追加（如修改文件并保留历史内容）   |
| r+   | 文本模式 + 读写，光标在文件开头                              | 读取并修改文件（需注意光标位置）         |

### with 语句（推荐）

with 语句会自动关闭文件，即使发生错误也能正确关闭。

```python
with open("example.txt", "r", encoding="utf-8") as file:
    content = file.read()
    print(content)
# 离开 with 块后，文件自动关闭
```

### 读取方法

**read() - 读取全部内容**

```python
with open("prompt.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
```

**readline() - 逐行读取**

```python
with open("prompt.txt", "r", encoding="utf-8") as f:
    line1 = f.readline()  # 读取第一行
    line2 = f.readline()  # 读取第二行
    print(line1)
    print(line2)
```

**readlines() - 读取所有行到列表**

```python
with open("prompts.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()  # 返回列表，每个元素是一行
    for line in lines:
        print(line.strip())  # strip() 去除行尾换行符
```

**遍历文件对象**

```python
with open("prompts.txt", "r", encoding="utf-8") as f:
    for line in f:  # 直接遍历文件对象
        print(line.strip())
```

### AI 场景示例

```python
# 读取 prompt 模板
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

print("=== 系统 Prompt ===")
print(system_prompt)

# 读取多个 prompt 模板
prompts = {}
template_files = ["coder.txt", "translator.txt", "helper.txt"]

for filename in template_files:
    role = filename.replace(".txt", "") coder translator helper
    with open(f"prompts/{filename}", "r", encoding="utf-8") as f:
        prompts[role] = f.read()
      

print(prompts["coder"])
```

### 课堂练习

**读取知识库文档**

创建一个 `knowledge.txt` 文件，内容如下：
```
Python 是一门编程语言
适合 AI 开发
语法简洁易学
```

读取并打印每一行。

参考答案：

```python
with open("knowledge.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())
```

输出：

```
Python 是一门编程语言
适合 AI 开发
语法简洁易学
```

---

## 文件写入

### 写入模式

**"w" - 覆盖写入**(不同的操作系统换行符不统一. \r\n  , \n)

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!\n")
    f.write("这是第二行\n")
```

注意：`"w"` 模式会覆盖原文件内容！

**"a" - 追加写入**

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("新日志记录\n")
```

### 写入方法

**write() - 写入字符串**

```python
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")
```

**writelines() - 写入列表**

```python
lines = ["第一行\n", "第二行\n", "第三行\n"]
with open("output.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)
```

### AI 场景示例

```python
# 保存对话记录
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮你？"}
]

with open("chat_history.txt", "w", encoding="utf-8") as f:
    for msg in messages:
        line = f"[{msg['role']}] {msg['content']}\n"
        f.write(line)

print("对话记录已保存")
```

输出文件内容：
```
[user] 你好
[assistant] 你好！有什么可以帮你？
```

### 课堂练习

**生成 Prompt 文件**

根据用户输入生成 prompt 并保存到文件。

参考答案：

```python
role = input("请输入角色: ")
task = input("请输入任务: ")

prompt = f"""你是一个{role}。

任务：{task}

请按照要求完成任务。
"""

with open("generated_prompt.txt", "w", encoding="utf-8") as f:
    f.write(prompt)

print("Prompt 已保存到 generated_prompt.txt")
```

---

## 文件路径

### 相对路径 vs 绝对路径

**相对路径：** 相对于当前工作目录

```python
# 当前目录下的文件
"data.txt"

# 当前目录下的子目录
"data/chat.txt"

# 上级目录
"../config.txt"

#相对路径, 一定要注意是相对谁. 
os.getcwd() 能够获取当前工作路径
```

**绝对路径：** 从根目录开始的完整路径

```python
# Windows
"C:/Users/username/project/data.txt"

# macOS/Linux
"/Users/username/project/data.txt"
```

### os.path 模块

os.path 提供了跨平台的路径操作函数。

```python
 换行符: \r\n  \n 
 文件分隔符:  \   / 
 环境变量分隔符: window ;    mac/linux 
import os

# 拼接路径（自动处理斜杠）
path = os.path.join("data", "prompts", "system.txt")
print(path)  # Windows: data\prompts\system.txt
             # macOS: data/prompts/system.txt

    
    
# 检查文件是否存在
if os.path.exists("data.txt"):
    print("文件存在")
else:
    print("文件不存在")

# 检查是否是文件
print(os.path.isfile("data.txt"))

# 检查是否是目录
print(os.path.isdir("data"))

# 获取文件名
filename = os.path.basename("/path/to/file.txt")
print(filename)  # file.txt

# 获取目录名
dirname = os.path.dirname("/path/to/file.txt")
print(dirname)  # /path/to

# 获取当前工作目录
cwd = os.getcwd()
print(cwd)

# 创建目录
# 1: 可以创建多级目录
# 2: 如果目录存在, 再次创建会失败,抛出异常信息: FileExistsError 
# 3: exist_ok = True 表示目录存在时,不报错
os.makedirs("data/logs", exist_ok=True)  # exist_ok=True 表示目录存在时不报错
```

### pathlib 模块（python3.4+ 提供)

pathlib 是更现代的路径操作方式，面向对象。

```python
# pathlib 是包  Path是类
from pathlib import Path

# 创建路径对象
path = Path("data/prompts/system.txt")

# 检查是否存在
if path.exists():
    print("文件存在")

# 读取文件
content = path.read_text(encoding="utf-8")

# 写入文件(原内容会被覆盖),不能实现追加写
path.write_text("新内容", encoding="utf-8")

# 获取父目录
parent = path.parent
print(parent)  # data/prompts

# 获取文件名
print(path.name)  # system.txt

# 获取后缀
print(path.suffix)  # .txt

# 遍历目录
# iterdir()  遍历当前目录下所有直接子项(一级), 文件+文件夹,不会递归进入子文件夹.
# 
data_dir = Path("data")
for file in data_dir.iterdir():
    print(file)

# 遍历目录中文件, 带通配符筛选的目录遍历，支持匹配规则，返回生成器。   
# *.txt  当前目录下 所有 .txt 文件
# **/*/txt 是遍历当前目录以及所有子目录的.txt文件
for file in data_dir.glob("*.txt"):  # 所有 .txt 文件
    print(file)
```

### AI 场景示例

```python
from pathlib import Path

# 组织项目文件结构
project_dir = Path("my_ai_project")
data_dir = project_dir / "data"
logs_dir = project_dir / "logs"

# 创建目录 parents=False 默认是False,不支持创建多级目录. 两个属性一起使用. 
data_dir.mkdir(parents=True, exist_ok=True)
logs_dir.mkdir(parents=True, exist_ok=True)

# 保存对话记录
chat_file = data_dir / "chat_20240611.txt"
with open(chat_file, "w", encoding="utf-8") as f:
    f.write("对话记录...\n")

print(f"对话记录已保存到: {chat_file}")
```

---

## JSON 文件处理

JSON 是 AI 开发中最常用的数据格式，用于存储配置、消息、API 响应等。

### 为什么使用 JSON(目前系统进行数据传输的主流方式.)

- 人类可读
- 跨语言通用.  
- 支持复杂数据结构（嵌套字典、列表） 
- AI API 的标准格式

### JSON 基础操作

**写入 JSON 文件**

```python
import json

# Python 数据结构
data = {
    "model": "gpt-4",
    "temperature": 0.7,
    "messages": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！"}
    ]
}

# 保存到文件
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False: 保存中文而不是 \uXXXX
    # indent=2: 格式化输出，方便阅读

print("已保存到 config.json")
```

生成的 config.json：
```json
{
  "model": "gpt-4",
  "temperature": 0.7,
  "messages": [
    {
      "role": "user",
      "content": "你好"
    },
    {
      "role": "assistant",
      "content": "你好！"
    }
  ]
}
```

**读取 JSON 文件**

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)  # 解析 JSON 为 Python 对象

print(data["model"])  # gpt-4
print(data["messages"][0]["content"])  # 你好
```

### AI 场景示例

```python
import json
from datetime import datetime

# 保存对话记录（带时间戳）
def save_chat_history(messages, filename="chat_history.json"):
    """保存对话记录到 JSON 文件"""
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "messages": messages
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, ensure_ascii=False, indent=2)
    
    print(f"对话记录已保存: {filename}")

# 加载对话记录
def load_chat_history(filename="chat_history.json"):
    """从 JSON 文件加载对话记录"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["messages"]
    except FileNotFoundError:
        print("文件不存在，返回空列表")
        return []

# 使用
messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]

save_chat_history(messages)
loaded = load_chat_history()
print(f"加载了 {len(loaded)} 条消息")
```

### 课堂练习(作业)

**配置文件管理**

创建一个配置管理系统，保存和读取 AI 模型配置。

参考答案：

```python
import json

def save_config(config, filename="config.json"):
    """保存配置"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_config(filename="config.json"):
    """加载配置"""
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# 测试
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000,
    "system_prompt": "你是一个Python助手"
}

save_config(config)
print("配置已保存")

loaded_config = load_config()
print(f"模型: {loaded_config['model']}")
print(f"温度: {loaded_config['temperature']}")
```

---

## 异常处理

程序运行时可能遇到各种错误：文件不存在、网络断开、数据格式错误等。异常处理让程序更健壮。

### 为什么需要异常处理

没有异常处理时，一个错误会导致程序崩溃：

```python
# 文件不存在，程序直接崩溃
with open("not_exists.txt", "r") as f:
    content = f.read()
# FileNotFoundError: [Errno 2] No such file or directory: 'not_exists.txt'
```

有异常处理时，可以优雅地处理错误：

```python
try:
    with open("not_exists.txt", "r") as f:
        content = f.read()
except FileNotFoundError:
    print("文件不存在，使用默认配置")
    content = "默认内容"
```

### try-except 基础

**基本语法：**

```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理特定错误
    print("不能除以零")
```

**捕获多种异常：**

```python
try:
    value = int("abc")
except ValueError:
    print("值错误")
except TypeError:
    print("类型错误")
```

**捕获所有异常：**

```python
try:
    # 危险操作
    risky_operation()
except Exception as e:
    print(f"发生错误: {e}")
```

### try-except-else-finally

完整的异常处理结构：

```python
try:
    # 可能出错的代码
    with open("data.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    # 处理文件不存在
    print("文件不存在")
    data = ""
except Exception as e:
    # 处理其他错误
    print(f"未知错误: {e}")
    data = ""
else:
    # 没有异常时执行
    print("文件读取成功")
finally:
    # 无论是否异常都执行（常用于清理资源）
    print("操作完成")
```

### AI 场景示例

```python
import json

def load_config_safe(filename="config.json"):
    """安全加载配置文件"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            config = json.load(f)
        print(f"配置加载成功: {filename}")
        return config
    except FileNotFoundError:
        print(f"配置文件不存在: {filename}，使用默认配置")
        return {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7
        }
    except json.JSONDecodeError as e:
        print(f"JSON 格式错误: {e}")
        return {}
    except Exception as e:
        print(f"未知错误: {e}")
        return {}

# 使用
config = load_config_safe("config.json")
print(f"模型: {config.get('model', '未设置')}")
```

### 课堂练习

**健壮的文件读取**

编写函数，安全地读取文件，如果失败返回默认值。

参考答案：

```python
def read_file_safe(filename, default=""):
    """安全读取文件"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"文件不存在: {filename}")
        return default
    except UnicodeDecodeError:
        print(f"编码错误: {filename}")
        return default
    except Exception as e:
        print(f"读取失败: {e}")
        return default

# 测试
content = read_file_safe("prompt.txt", "默认 Prompt")
print(content)
```

---

## 日志记录

`print()` 只能输出到控制台，日志可以保存到文件，方便追踪问题。

问题: 

(1)不便于日志追踪.

(2)不能控制日志的打印级别. 

### 为什么使用日志(一定会使用)

- 记录程序运行状态
- 调试问题
- 监控错误
- 审计操作

### logging 模块基础

**基本配置：**

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,  # 日志级别
    format='%(asctime)s - %(levelname)s - %(message)s',  # 日志格式
    filename='app.log',  # 输出到文件, 该文件不存在会自动创建. 不指定该属性,日志打印在控制台.
    encoding='utf-8'  # python 3.9 版本原生支持, 老版本不写会出现乱码问题. 
)

# 记录日志
logging.debug("调试信息")
logging.info("程序启动")
logging.warning("警告：配置缺失")
logging.error("错误：文件不存在")
logging.critical("严重错误：系统崩溃")
```

### 日志级别

从低到高：
- **DEBUG**：详细调试信息, 对应的数值是10
- **INFO**：一般信息,  20
- **WARNING**：警告, 30
- **ERROR**：错误,40
- **CRITICAL**：严重错误, 50

只有大于等于设定级别的日志才会被记录。

### 同时输出到控制台和文件

```python
import logging

# 创建 logger
print(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 文件处理器, 不指定encoding="utf-8" 默认输出到文件使用系统默认GBK
file_handler = logging.FileHandler('app.log', encoding='utf-8')  
file_handler.setLevel(logging.INFO)

# 控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 格式化
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# 添加处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 使用
logger.info("程序启动")
logger.warning("配置缺失")
logger.error("发生错误")
```

### AI 场景示例

```python
import logging
import json

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='ai_app.log',
    encoding='utf-8'
)

def call_ai_api(prompt):
    """调用 AI API（模拟）"""
    logging.info(f"调用 API，prompt 长度: {len(prompt)}")
    
    try:
        # 模拟 API 调用
        if len(prompt) == 0:
            raise ValueError("Prompt 不能为空")
        
        # 模拟响应
        response = "这是 AI 的回复"
        logging.info("API 调用成功")
        return response
        
    except ValueError as e:
        logging.error(f"参数错误: {e}")
        return None
    except Exception as e:
        logging.critical(f"API 调用失败: {e}")
        return None

# 使用
result = call_ai_api("你好")
if result:
    print(f"回复: {result}")
else:
    print("调用失败")
```

### 课堂练习(作业)

**带日志的文件操作**

为文件读写操作添加日志记录。

参考答案：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='file_operations.log',
    encoding='utf-8'
)

def save_data(filename, data):
    """保存数据并记录日志"""
    try:
        logging.info(f"开始保存数据到: {filename}")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(data)
        logging.info(f"数据保存成功: {filename}")
        return True
    except Exception as e:
        logging.error(f"保存失败: {e}")
        return False

# 测试
success = save_data("output.txt", "测试数据")
print(f"保存{'成功' if success else '失败'}")
```

---

## CSV 文件处理

CSV文件: 文本文件.非常适合大量数据的存储和传输. python擅长处理csv文件.  数据分析岗位, 很重要

CSV 是常见的表格数据格式，常用于数据交换和批量处理。

### csv 模块

**读取 CSV：**

```python
import csv

# 读取 CSV 文件
with open("models.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    
    # 跳过表头
    header = next(reader)
    print(f"表头: {header}")
    
    # 读取数据
    for row in reader:
        print(row)
```

models.csv 内容：
```csv
model,price,max_tokens
gpt-3.5-turbo,0.002,4096
gpt-4,0.03,8192
claude-3,0.015,100000
```

**使1用 DictReader（推荐）：** 根据列名称访问数据,不依赖列的顺序.

```python
import csv

with open("models.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)  # 自动解析表头
    
    for row in reader:
        print(f"模型: {row['model']}, 价格: {row['price']}")
```

输出：
```
模型: gpt-3.5-turbo, 价格: 0.002
模型: gpt-4, 价格: 0.03
模型: claude-3, 价格: 0.015
```

总结: 

(1)字典构建有开销,性能稍微有损耗. 

(2)开头第一行必须是表头

(3) 读取到的值全部是字符串, 需要使用对应的数据类型进行转换. int()/float()

写入 CSV：**

```python
import csv

data = [
    ["model", "price", "max_tokens"],
    ["gpt-3.5-turbo", "0.002", "4096"],
    ["gpt-4", "0.03", "8192"]
]

with open("output.csv", "w", encoding="utf-8", newline='') as f:
    #创建了一个csv写入器
    writer = csv.writer(f)
    writer.writerows(data)

print("CSV 文件已保存")
```

**使用 DictWriter：**

```python
import csv

data = [
    {"model": "gpt-3.5-turbo", "price": 0.002, "max_tokens": 4096},
    {"model": "gpt-4", "price": 0.03, "max_tokens": 8192}
]

with open("output.csv", "w", encoding="utf-8", newline='') as f:
    fieldnames = ["model", "price", "max_tokens"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()  # 写入表头
    writer.writerows(data)  # 写入数据

print("CSV 文件已保存")
```

### AI 场景示例(作业)

```python
import csv
from datetime import datetime

def log_api_call(model, tokens, cost, filename="api_log.csv"):
    """记录 API 调用到 CSV"""
    # 检查文件是否存在
    import os
    file_exists = os.path.exists(filename)
    
    with open(filename, "a", encoding="utf-8", newline='') as f:
        fieldnames = ["timestamp", "model", "tokens", "cost"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # 如果文件不存在，写入表头
        if not file_exists:
            writer.writeheader()
        
        # 写入数据
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "tokens": tokens,
            "cost": cost
        })

# 使用
log_api_call("gpt-4", 1500, 0.045)
log_api_call("gpt-3.5-turbo", 800, 0.0016)
print("API 调用已记录")
```

---

## HTTP 请求与 API 调用

### requests 库

requests 是最常用的 HTTP 库。 是一个第三方库, 必须得安装使用. 

**安装：**

```bash
pip install requests
```

**基本用法：**

```python
import requests

# GET 请求  响应得数据是json: https://httpbin.org/get
response = requests.get("https://postman-echo.com/get")
print(response.status_code)  # 200
print(response.json())  # 解析 JSON


```

```python
# POST 请求
import requests

# POST JSON 请求
url = "https://postman-echo.com/post"
data = {"name": "Alice", "email": "alice@example.com"}

response = requests.post(url, json=data)

print("状态码：", response.status_code)
# 解析返回json
result = response.json()
print("返回数据：")
print(result)
# 获取我们上传的参数
print("提交的json数据 ==>", result["json"])

# 带请求头
headers = {"Authorization": "Bearer xxx"}
response = requests.get("https://api.example.com/protected", headers=headers)
```

注意: 

post(url,data,json, header,cookie...)

url: 访问的路径. 

data: 传递的是表单数据 原始字符串.  默认的请求头是 Content-Type: application/x-www-form-urlencoded 

username=lisi&password=123456

json: 传递JSON对象(字典/列表) 默认的请求头是 Content-Type : application/json(MIME) ,这个参数可用对接后端json,是最常用的. 

两个参数不要同时使用. 

### 异常处理

```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=5)
    response.raise_for_status()  # 状态码非 2xx 抛出异常
    data = response.json()
    print(data)
except requests.Timeout:
    print("请求超时")
except requests.HTTPError as e:
    print(f"HTTP 错误: {e}")
except requests.RequestException as e:
    print(f"请求失败: {e}")
```

### AI API 调用示例

```python
# 导入依赖库
import requests
import os

def ai_chat(messages, api_key, model="deepseek-v4-flash", temperature=0.7):
    """
    AI对话核心函数
    messages: 对话上下文列表，里面是字典
    api_key: 自己的OpenAI密钥
    model: 使用的大模型
    temperature: 创造性，数值越大回答越天马行空
    """
    # 接口基础地址
    base_url = "https://api.deepseek.com"
    chat_url = base_url + "/chat/completions"

    # 请求头：身份认证+数据格式
    headers = {
        "Authorization": "Bearer " + api_key,
        "Content-Type": "application/json"
    }

    # 请求体，传给接口的参数
    post_data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    try:
        # 发送POST请求，设置30秒超时防止卡死
        response = requests.post(chat_url, headers=headers, json=post_data, timeout=30)
        # 如果接口返回400/401/500这类错误状态码，直接抛出异常
        response.raise_for_status()
        # 将返回的json转为Python字典
        res_json = response.json()
        # 提取大模型回答内容
        answer = res_json["choices"][0]["message"]["content"]
        return answer

    except requests.exceptions.RequestException as net_err:
        print("网络请求异常：", net_err)
        return None
    except Exception as err:
        print("接口调用发生未知错误：", err)
        return None


# ==================== 主程序调用演示 ====================
if __name__ == "__main__":
    # 方式1：从系统环境变量读取密钥（推荐，防止密钥泄露）
    # openai_key = os.getenv("OPENAI_API_KEY")
    # 方式2：直接填写密钥（仅本地临时测试使用，禁止上传代码到网络）
    openai_key = "sk-1eb3ed686cbw4e0a9cd07e6e16f43c51"
    # 构造对话内容
    chat_history = [
        {"role": "user", "content": "用通俗易懂的语言解释什么是Python编程语言"}
    ]

    # 调用AI对话函数
    ai_result = ai_chat(chat_history, openai_key)

    # 打印AI返回结果
    if ai_result is not None:
        print("===== AI回答 =====")
        print(ai_result)
    else:
        print("AI问答调用失败，请检查密钥、网络或者接口地址")
```



## 今日总结

### 核心知识点回顾

**1. 文件操作**

- `open()` 打开文件，模式：r/w/a
- `with` 语句自动关闭文件
- 读取：read(), readline(), readlines()
- 写入：write(), writelines(list)

**2. 路径处理**

- 相对路径 vs 绝对路径
- os.path：跨平台路径操作
- pathlib：面向对象的路径操作（推荐）

**3. JSON 文件**

- json.dump()：保存到文件
- json.load()：从文件加载
- ensure_ascii=False：保存中文
- indent：格式化输出

**4. 异常处理**
- try-except：捕获异常
- try-except-else-finally：完整结构
- 捕获特定异常类型
- Exception：捕获所有异常

**5. 日志记录**

- logging 模块
- 日志级别：DEBUG < INFO < WARNING < ERROR < CRITICAL
- basicConfig：简单配置
- Handler：输出到文件和控制台

**6. CSV 文件**

- csv.reader / csv.writer

- csv.DictReader / csv.DictWriter（推荐）

- newline=''：写入时避免空行,不同操作系统换行问题.

  **7. HTTP 请求**

  - requests.get/post
  - headers：请求头
  - json：JSON 数据
  - response：检查状态码,获取response的响应内容.

  

### 常见问题

**Q：为什么要用 with 语句？**
A：自动关闭文件，即使发生异常也能正确关闭，避免资源泄漏。

**Q：相对路径和绝对路径该用哪个？**
A：项目内部文件用相对路径，便于移植；外部文件或配置用绝对路径。

**Q：JSON 和 CSV 该选哪个？**
A：复杂嵌套数据用 JSON；简单表格数据用 CSV；AI 消息和配置通常用 JSON。

**Q：什么时候应该捕获异常？**
A：可能失败的 I/O 操作（文件、网络）、用户输入、外部 API 调用。

**Q：日志和 print 有什么区别？**
A：print 只能输出到控制台；日志可以保存、分级、格式化，适合生产环境。

### 重点注意事项

1. **文件编码**：中文文件必须指定 `encoding="utf-8"`

2. **异常粒度**：捕获具体异常而不是所有 Exception
   ```python
   # 好
   try:
       f = open("file.txt")
   except FileNotFoundError:
       pass
   
   # 差
   try:
       f = open("file.txt")
   except Exception:  # 太宽泛
       pass
   ```

3. **资源清理**：使用 with 或 finally 确保资源释放

4. **JSON 中文**：`ensure_ascii=False` 避免中文变成 \uXXXX

5. **CSV 空行**：写入时使用 `newline=''` 避免空行

## 当天作业

### 对话记录管理系统

实现一个完整的对话记录管理系统，支持保存、加载、追加对话。

参考答案：

```python
import json
from datetime import datetime
from pathlib import Path

class ChatManager:
    """对话管理器"""
    
    def __init__(self, data_dir="chat_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_chat(self, messages, session_id=None):
        """保存对话"""
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = self.data_dir / f"chat_{session_id}.json"
        
        data = {
            "session_id": session_id,
            "timestamp": datetime.now().isoformat(),
            "messages": messages
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"对话已保存: {filename}")
        return session_id
    
    def load_chat(self, session_id):
        """加载对话"""
        filename = self.data_dir / f"chat_{session_id}.json"
        
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data["messages"]
        except FileNotFoundError:
            print(f"会话不存在: {session_id}")
            return []
        except json.JSONDecodeError:
            print(f"文件格式错误: {filename}")
            return []
    
    def list_sessions(self):
        """列出所有会话"""
        sessions = []
        for file in self.data_dir.glob("chat_*.json"):
            session_id = file.stem.replace("chat_", "")
            sessions.append(session_id)
        return sorted(sessions)

# 测试
manager = ChatManager()

# 保存对话
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]
session_id = manager.save_chat(messages)

# 加载对话
loaded_messages = manager.load_chat(session_id)
print(f"加载了 {len(loaded_messages)} 条消息")

# 列出所有会话
sessions = manager.list_sessions()
print(f"共有 {len(sessions)} 个会话")
```

### Prompt 模板管理器

创建一个 Prompt 模板管理系统，支持多个模板。

参考答案：

```python
import json
from pathlib import Path

class PromptManager:
    """Prompt 模板管理器"""
    
    def __init__(self, templates_file="prompt_templates.json"):
        self.templates_file = Path(templates_file)
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """加载模板"""
        try:
            with open(self.templates_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def _save_templates(self):
        """保存模板"""
        with open(self.templates_file, "w", encoding="utf-8") as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)
    
    def add_template(self, name, template):
        """添加模板"""
        self.templates[name] = template
        self._save_templates()
        print(f"模板已添加: {name}")
    
    def get_template(self, name):
        """获取模板"""
        return self.templates.get(name, "")
    
    def list_templates(self):
        """列出所有模板"""
        return list(self.templates.keys())
    
    def delete_template(self, name):
        """删除模板"""
        if name in self.templates:
            del self.templates[name]
            self._save_templates()
            print(f"模板已删除: {name}")
        else:
            print(f"模板不存在: {name}")

# 测试
manager = PromptManager()

# 添加模板
manager.add_template("coder", "你是一个专业的编程助手")
manager.add_template("translator", "你是一个专业的翻译助手")

# 列出模板
templates = manager.list_templates()
print(f"可用模板: {templates}")

# 使用模板
system_prompt = manager.get_template("coder")
print(f"系统 Prompt: {system_prompt}")
```

### API 调用统计

记录 API 调用并生成统计报告。

参考答案：

```python
import csv
import json
from datetime import datetime
from pathlib import Path

class APILogger:
    """API 调用日志记录器"""
    
    def __init__(self, log_file="api_calls.csv"):
        self.log_file = Path(log_file)
    
    def log_call(self, model, input_tokens, output_tokens, cost):
        """记录一次 API 调用"""
        file_exists = self.log_file.exists()
        
        with open(self.log_file, "a", encoding="utf-8", newline='') as f:
            fieldnames = ["timestamp", "model", "input_tokens", 
                         "output_tokens", "total_tokens", "cost"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
                "cost": cost
            })
    
    def get_statistics(self):
        """生成统计报告"""
        if not self.log_file.exists():
            return {"total_calls": 0, "total_cost": 0}
        
        total_calls = 0
        total_cost = 0.0
        total_tokens = 0
        model_stats = {}
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                total_calls += 1
                total_cost += float(row["cost"])
                total_tokens += int(row["total_tokens"])
                
                model = row["model"]
                if model not in model_stats:
                    model_stats[model] = {"calls": 0, "cost": 0.0}
                
                model_stats[model]["calls"] += 1
                model_stats[model]["cost"] += float(row["cost"])
        
        return {
            "total_calls": total_calls,
            "total_cost": total_cost,
            "total_tokens": total_tokens,
            "model_stats": model_stats
        }

# 测试
logger = APILogger()

# 记录调用
logger.log_call("gpt-4", 1000, 500, 0.045)
logger.log_call("gpt-3.5-turbo", 800, 400, 0.0024)
logger.log_call("gpt-4", 1200, 600, 0.054)

# 查看统计
stats = logger.get_statistics()
print(f"总调用次数: {stats['total_calls']}")
print(f"总费用: ${stats['total_cost']:.4f}")
print(f"总 Token 数: {stats['total_tokens']}")
print("\n各模型统计:")
for model, data in stats["model_stats"].items():
    print(f"  {model}: {data['calls']} 次, ${data['cost']:.4f}")
```

输出：

```
总调用次数: 3
总费用: $0.1014
总 Token 数: 4500

各模型统计:
  gpt-4: 2 次, $0.0990
  gpt-3.5-turbo: 1 次, $0.0024
```

------



