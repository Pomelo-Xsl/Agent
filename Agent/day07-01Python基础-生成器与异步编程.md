# day7-01Python基础-生成器与异步编程

## 学习目标

- 掌握环境变量的应用

- 理解迭代器和生成器的概念

- 使用 yield 创建生成器函数

- 实现流式输出（类似 ChatGPT）

- 理解同步和异步的区别

- 使用 async/await 编写异步代码

- 使用 asyncio 进行并发编程

- 完成一个完整的 AI 对话系统项目(作业)

  重点:  环境变量, 开发当中使用. 

  ​           迭代器和生成器.  底层的一个关键字 yield 

  ​           异步实现方式: 协程, async, await 使用.  asyncio  并发编程.

  

---

## 环境变量

环境变量用于存储敏感信息（如 API Key），避免硬编码。 



### 使用 os.getenv

```python
import os

# 读取环境变量
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("API Key 未设置")
else:
    print(f"API Key: {api_key[:10]}...")  # 只显示前10位
    
  一个项目当中以后需要配置很多个环境变量, 直接配置在系统环境变量当中, 麻烦.  而且不同的项目使用的环境变量的值不一样, 每次切换麻烦.
```

### 使用 python-dotenv

python-dotenv 从 `.env` 文件加载环境变量。

**安装：**

```bash
pip install python-dotenv
```

**创建 .env 文件：**

```
OPENAI_API_KEY=sk-xxxxxxxxxxxx
MODEL=gpt-4
TEMPERATURE=0.7
```

**加载环境变量：**

```python
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

# 读取环境变量
api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("MODEL", "gpt-3.5-turbo")  # 提供默认值
temperature = float(os.getenv("TEMPERATURE", "0.7"))

print(f"模型: {model}")
print(f"温度: {temperature}")
```

只用步骤的总结: 

```text
从环境变量当中获取变量的值, 一定会使用[重要]
1: 导入python-dotenv 第三方库. pip install python-dotenv
2: 导入到当前文件当中: from dotenv import load_dotenv 
3: 使用load_dotenv() 加载.env这个文件. 
4: 使用os.getenv(key, defaultValue) 获取对应的值,如果key不存在,可以使用默认值
```

### AI 场景示例

```python
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field # 提供@dataclass 功能. 并且还提供了严格的字段校验.

# 加载环境变量
load_dotenv()

class AppConfig(BaseModel):
    """应用配置"""
    api_key: str = Field(default="gpt-4.5") # 这是给api_key提供了一个默认值:  类定义的时候这个值就确定了.
    # default_factor 使用了一个默认工厂. 实例化对象的时候,  才会调用 os.getenv() 获得值, 给api_key赋值.
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", "")) 
   
    model: str = Field(default_factory=lambda: os.getenv("MODEL", "gpt-3.5-turbo"))
    temperature: float = Field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "2000")))
    
    # 自定义校验器
    def validate(self) -> bool:
        """验证配置"""
        if not self.api_key:
            print("错误: API Key 未设置")
            return False
        if not (0 <= self.temperature <= 2):
            print("错误: 温度参数无效")
            return False
        return True

# 使用
config = AppConfig()
if config.validate():
    print("配置加载成功")
    print(f"模型: {config.model}")
else:
    print("配置验证失败")
    
解释: 
default_factory=lambda: xxx和直接写default=区别：
default在类定义阶段就计算默认值；
default_factory在实例化对象的时候动态执行函数取值，非常适合读取环境变量这种动态数据。
```

## 迭代器与生成器

### 迭代器（Iterator）

遍历和迭代的概念:  

遍历:   获取到列表当中的每一个元素. for , while , list[index] 

迭代:  next()  每次调用同一个方法, 但是获取到不同的值, 这个概念迭代. 



迭代器是 Python 中遍历可迭代对象的核心机制，是可以记住遍历位置的对象，大幅提升内存效率，尤其适用于大数据量场景。 



###  核心概念区分 

| 概念                                                         | 定义                                     | 判定方式                    |
| ------------------------------------------------------------ | ---------------------------------------- | --------------------------- |
| 可迭代对象（Iterable）, 起始就是可以使用迭代器获取元素, 使用for循环遍历得到每一个元素. | 支持被`iter()`函数调用生成迭代器的对象   | `isinstance(obj, Iterable)` |
| 迭代器（Iterator）                                           | 实现`__iter__()`和`__next__()`方法的对象 | `isinstance(obj, Iterator)` |

- 可迭代对象

  - 可迭代对象（Iterable）指能被 **for** 循环遍历的对象，通常为实现了 **iter()** 方法，或实现了 **getitem()** 并支持从 **0** 开始的整数索引的对象

  - 使用 **isinstance(obj, collections.abc.Iterable)** 进行类型判定

    ```python
    from collections.abc import Iterable
    
    # 列表：list，内置可变序列类型，支持迭代
    print(isinstance([], Iterable))  # True
    
    # 元组：tuple，内置不可变序列类型，支持迭代
    print(isinstance((), Iterable))  # True
    
    # 集合：set，内置可变集合类型，支持迭代
    print(isinstance(set(), Iterable))  # True
    
    # 字典：dict，内置映射类型；默认迭代的是“键”
    print(isinstance({}, Iterable))  # True
    
    # 字符串：str，内置序列类型，按字符迭代
    print(isinstance("100", Iterable))  # True
    
    # 整数：int，内置数值类型，非可迭代对象
    print(isinstance(100, Iterable))  # False
    
    
    for element in [1, 2, 3]:
        print(element)
    for element in (1, 2, 3):
        print(element)
    for key in {"one": 1, "two": 2}:
        print(key)
    for char in "123":
        print(char)
    
    # 迭代文件对象. 
    for line in open("test.txt"):
        print(line, end="")
    ```
  
  - 内置可迭代类型总览
  
    | 分类           | 代表类型                                                     | 说明                                                    |
    | -------------- | ------------------------------------------------------------ | ------------------------------------------------------- |
    | 容器类         | <font color='red'>list、tuple、str、set、dict、</font>       | 常见内置容器，均可在 for 中遍历；dict 默认迭代键        |
    | 序列与字节     | **==range==、bytes、bytearray、memoryview**                  | 序列或字节视图，支持索引/切片（memoryview 为内存视图）  |
    | 文件对象       | **io.TextIOBase/io.BufferedIOBase**（文本/二进制文件）       | ==文件对象本身可逐行/逐块迭==代                         |
    | 迭代器与生成器 | **==iterator、generator==、generator expression**            | 迭代器遵循迭代协议；生成器是特殊的迭代器                |
    | 高阶返回迭代器 | **==enumerate、zip、map(function,Iterable)==、filter、reversed** | 内置函数/类型，返回迭代器用于惰性组合、过滤、映射、反转 |
    | 字典视图       | **dict_keys、dict_values、dict_items**                       | 视图对象，惰性反映字典变化，可迭代                      |



###  迭代器及其与可迭代对象关系

1. 可迭代对象通过`iter()`函数生成迭代器
2. 迭代器通过`next()`函数获取下一个元素，耗尽时抛出`StopIteration`异常
3. 迭代器本身也是可迭代对象（`__iter__()`返回自身）

```python
from collections.abc import Iterable, Iterator

# 验证可迭代对象
lst = [1, 2, 3]
print("列表是否可迭代:", isinstance(lst, Iterable))  # 输出：True
print("列表是否迭代器:", isinstance(lst, Iterator))  # 输出：False

# 生成迭代器
lst_iter = iter(lst)
print("迭代器是否可迭代:", isinstance(lst_iter, Iterable))  # 输出：True
print("迭代器是否迭代器:", isinstance(lst_iter, Iterator))  # 输出：True

# 遍历迭代器
print(next(lst_iter))  # 输出：1
print(next(lst_iter))  # 输出：2
print(next(lst_iter))  # 输出：3
# print(next(lst_iter))  # 抛出 StopIteration 异常

print("===================================================")
# 创建迭代器对象后使用while循环遍历
while True:
    try: 
       print(next(lst_iter))
    except StopIteration as e:
       print("遍历结束")

print("===================================================")
# 创建迭代器对象后使用for循环遍历
it = iter(lst) 
for i in it:
  print(i)
```

###  自定义迭代器(了解) 

通过实现`__iter__()`和`__next__()`方法，创建自定义迭代器

```python
# 定义一个数字容器类，给与一个数值，如10，那么返回该数字容器的迭代器，迭代器可以遍历从1-10对应的数字


# 需求: 给定一个num值, 打印1.2 ...num .
class NumberCount:

    # 初始化方法,num是用户输入的最大值.
    def __init__(self,num):
        self.num = num

    # 定义一个方法,这个方法要获取一个迭代器, 类比: 实现 list.__iter__() -> 迭代器.
    def __iter__(self):

        # 创建一个迭代器, NumberCountIterator
        class NumberCountIterator:
            # 初始化方法, 迭代器的初始值. 迭代器需要复制一份外部的数据，对数据进行记录与迭代操作
            def __init__(self,num):
                self.num = num
                self.current_num = 1

            #  迭代器的方法, __next__ () 每调用一次, 都会返回一个值.
            def __next__(self):
                if self.current_num <= self.num:
                    # current_num当前方法的局部变量.
                    current_num = self.current_num
                    self.current_num += 1
                    return current_num
                else: #没有迭代的元素, 就抛出异常信息.
                    raise StopIteration

             # __iter__ ()迭代器自己的方法, 每次调用都会返回迭代器本身
            def __iter__(self):
                return self

        # 方法的返回值, 返回迭代器实例对象.
        return NumberCountIterator(self.num)

#测试:
# 获取实例对象
number_count = NumberCount(9)
# 获取迭代器对象.
number_count_iter = number_count.__iter__()
#
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# print(number_count_iter.__next__())
# 获取到迭代器本身.
print(number_count_iter.__iter__())


#使用for循环.
for i in number_count:
    print(i)


```

### 迭代器的优势与应用场景

1. 内存高效：无需一次性加载所有数据，按需生成（如处理 100 万条数据时仅占用少量内存） next()
2. 支持无限序列：如无限斐波那契数列（通过迭代器可一直生成，不会内存溢出） 1 1 2  3 5 8 13 ....
3. 统一遍历接口：无论何种可迭代对象，都可通过`for`循环统一遍历

### 生成器（Generator）

生成器是一种特殊的迭代器，用 yield 关键字创建。

**基本语法：**

```python
 1. 生成器表达式（简洁版）

语法：`(表达式 for 变量 in 可迭代对象 if 条件)`（类似列表推导式，将`[]`改为`()`）

# 生成1-10的平方（生成器表达式）
square_gen = (x*x for x in range(1, 11))
print(type(square_gen))  # 输出：<class 'generator'>

# 遍历生成器
for num in square_gen:
    print(num, end=" ")  # 输出：1 4 9 16 25 36 49 64 81 100
  

2. 生成器表达式（函数版）
def count_up_to(max_count):
    """生成器函数"""
    count = 1
    while count <= max_count:
        yield count  # 暂停并返回值
        count += 1

# 使用
for num in count_up_to(5):
    print(num)  # 1 2 3 4 5
```

**yield vs return：**

- return：结束函数，返回值. 一次性将所有值全部返回. 
- yield：暂停函数，返回值,一次性返回一个值，当这个值被取走之后,继续执行,继续返回.

**生成器表达式：**

```python
# 列表推导式（一次性生成所有元素）
squares = [x**2 for x in range(1000000)]  # 占用大量内存

# 生成器表达式（按需生成）
squares = (x**2 for x in range(1000000))  # 几乎不占内存

# 使用
for square in squares:
    if square > 100:
        break
    print(square)
    
列表推导式 [] 是一次性把全部数据算出来，装进列表存在内存里；
生成器表达式 () 不会提前计算任何数字，遍历一个算一个，极致节省内存。

2. 第一行
squares = [x**2 for x in range(1000000)]
执行逻辑
循环 0~999999 每一个数字
立刻计算 x²
把100 万个计算结果全部保存到一个列表中
变量squares直接持有完整大列表
特点
✅ 优点：可以随意索引取值squares[100]、切片、重复遍历、修改元素
❌ 致命缺点：内存爆炸
100 万个整数全部常驻内存，如果是千万级、亿级数据，直接造成内存占用飙升、程序卡顿甚至 OOM 内存溢出。
2. 第二行：生成器表达式 (x**2 for x in range(1000000))
执行逻辑
代码运行时完全不做平方计算、不存储任何结果
只保存一套公式：「遍历 x，返回 x 平方」
只有你用for循环迭代、next()取值的时候，才临时算出一个值，用完直接丢弃，不留存
特点
✅ 优点：对象本身极小，内存占用可以忽略，超大序列必备
❌ 缺点：
不能下标取值：squares[50]直接报错
只能遍历一次，迭代完生成器就空了，无法二次使用
不能修改、切片

3. 两段代码直观对比演示
# 列表：全部预加载
lst = [x**2 for x in range(5)]
print(lst)  # [0, 1, 4, 9, 16]，直接拿到全部数据
print(lst[2]) # 可以直接取第三个值 4

# 生成器：惰性计算
gen = (x**2 for x in range(5))
print(gen) # <generator object ...>，看不到具体数值
# 必须循环取值
for num in gen:
    print(num)
# 再次循环生成器，没有任何输出（已经耗尽）
for num in gen:
    print(num)
    
4. 底层核心概念：惰性求值 VS 积极求值
列表推导式：积极求值（饿汉）
上来把所有结果全部算好存起来，用空间换速度。
适合：数据量小、需要多次读取、随机访问。
生成器表达式：惰性求值（懒汉）
什么时候要，什么时候算，不囤货。
适合：超大文件读取、海量数据遍历、流式数据、爬虫分页拉取，控制内存。

5. 总结
生成器可以强制转列表：list(gen)，一次性把所有数据载入内存
函数里带yield的就是生成器函数，和()生成器表达式原理一模一样
range()本身也是惰性序列，所以案例里range(1000000)本身不占内存，拖累内存的只有[]列表
```

### 为什么使用生成器

**内存效率：**

```python
# 不好：一次性加载所有行
def read_file_bad(filename):
    with open(filename, 'r') as f:
        return f.readlines()  # 整个文件加载到内存. 

# 好：按需读取
def read_file_good(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()

# 处理大文件
for line in read_file_good("large_file.txt"):
    process(line)  # 一次只处理一行
```

### AI 场景示例

```python
def token_stream(text, chunk_size=10):
    """模拟流式输出"""
    words = text.split()
    for i in range(0, len(words), chunk_size):
        # 分隔符字符串.join(可迭代对象)
        chunk = " ".join(words[i:i+chunk_size])
        yield chunk

# 使用
text = "这是 一段 很长的 文本 内容，模拟 AI 的流式 输出 效果"
for chunk in token_stream(text, chunk_size=3):
    print(chunk)
    # 模拟延迟
    import time
    time.sleep(0.5)
```

输出（每0.5秒输出一部分）：
```
这是 一段 很长的
文本 内容，模拟 AI
的流式 输出 效果
```

### 课堂练习

**文本分块生成器**

实现一个生成器，将长文本按指定字符数分块。

参考答案：chunk 片段. 

```python
def chunk_text(text, chunk_size=100):
    """将文本分块"""
    for i in range(0, len(text), chunk_size):
        yield text[i:i+chunk_size]

# 测试
long_text = "Python " * 50
for i, chunk in enumerate(chunk_text(long_text, 20), 1):
    print(f"块 {i}: {chunk}")
```

---

## 流式输出

流式输出是 AI 应用的常见需求，让用户看到内容逐步生成。

### 模拟流式输出

```python
import time

def stream_response(text, delay=0.05):
    """模拟流式输出"""
    for char in text:
        yield char   # 函数变成生成器，不会一次性把所有字符全部返回，一次只吐出 1 个字符，暂停函数执行；外部循环取一个值，函数才往下走一步。
        time.sleep(delay)  # 出字符后休眠指定时间，制造打字卡顿感

# 使用
response = "这是 AI 的回复内容"
print("AI: ", end="", flush=True)
for char in stream_response(response):
    print(char, end="", flush=True)  #end=""：正常 print 结尾会自动换行，end=""让打印结束不换行、光标停在当前行末尾 	
print()  # 换行,打印完成后将光标放在下一行


贴合LLM真实流式场景 
线上大模型接口就是流式 Chunk 分段返回，和这个逻辑一致：
后端不断yield文本片段，前端持续接收拼接渲染，就是你看到的 AI 打字效果
```

### AI 场景示例

```python
class StreamingChat:
    """流式对话类"""
    
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
    
    def chat(self, message):
        """发送消息并流式返回"""
        # 模拟 API 调用
        response = f"收到您的消息：{message}。这是一段流式输出的回复内容。"
        
        for word in response.split():
            yield word + " "
    
     # 将流式输出所有的chunk , 追加在[]当中, 方便一次性落库.实现会话长久记忆 /     
    def chat_with_collect(self, message):
        """流式输出并收集完整响应"""
        full_response = []
        
        for chunk in self.chat(message):
            full_response.append(chunk)
            yield chunk
        
        # 可以在这里保存完整响应
        complete = "".join(full_response)
        return complete

# 使用
chat = StreamingChat()
print("用户: 你好")
print("AI: ", end="", flush=True)

for chunk in chat.chat("你好"):
    print(chunk, end="", flush=True)
    time.sleep(0.05)
print()
```

---

## 异步编程基础

### 同步 vs 异步

**同步（Synchronous）：**

- 一件事做完再做下一件
- 等待 I/O 时阻塞

**异步（Asynchronous）：**

- 多件事并发进行
- 等待 I/O 时可以做其他事

**示例对比：**

```python
import time

# 同步：总共需要 6 秒
def sync_task():
    print("任务1开始")
    time.sleep(2)
    print("任务1完成")
    
    print("任务2开始")
    time.sleep(2)
    print("任务2完成")
    
    print("任务3开始")
    time.sleep(2)
    print("任务3完成")

# 异步：总共需要 2 秒（三个任务并发）
import asyncio

# 带async def的函数，调用后是协程对象，必须通过await或者gather触发执行。
async def async_task(name, delay):
    print(f"{name}开始")
    await asyncio.sleep(delay) # 只能在async函数 内部使用，交出 CPU 使用权，在 IO 等待期间执行其他任务。
    print(f"{name}完成")

async def async_main():
    # 用于多协程并发，适合一次性批量发起多个异步任务，等待全部完成。
    await asyncio.gather(
        async_task("任务1", 2),
        async_task("任务2", 2),
        async_task("任务3", 2)
    )

# 运行
asyncio.run(async_main())


```

### 概念: 

​    python当中,协程是实现异步的主要手段

​    **协程**:协程（Coroutine），是一种线程内部的任务调度机制(事件循环)，它通过事件循环，在用户态中实现任务的挂起与恢复执行，从而在遇到 IO 操作时，不让 CPU 等待，而是继续执行其它需要 CPU 的任务。

   协程的本质就是：在一个线程里，趁着某些任务在等 IO，把 CPU 交给其它任务去用。

**关键点1️⃣：协程不是线程，也不是进程**

进程,线程, process: cpu可以识别线程.   

- 协程不是操作系统提供的，并且 CPU 看不见协程。

- 操作系统不知道协程的存在。

- 协程是程序员在用户态，用代码“设计出来”的任务切换机制。 

  

**关键点2️⃣：协程发生在一个线程内部**

- 协程不是线程之间的切换。
- 而是线程内部多个任务之间的切换。
- 本质是一个线程里，写了很多任务，由事件循环统一调度。

**关键点3️⃣：协程的核心能力：挂起与恢复**

- 当任务 遇到 IO 操作 时：任务会被挂起。
- 当 IO 操作完成后：任务会被恢复执行。

**关键点4️⃣：协程依赖一个关键角色：事件循环**

- 事件循环负责：调度任务、判断是否该挂起、决定何时恢复执行，事件循环是协程系统的“大脑”

**关键点5️⃣：协程的目标是尽量减少线程切换**

- 在单线程场景下，最大化 CPU 利用率，特别适合 IO 密集型任务

  

### 协程函数 vs 协程对象   

   协程函数(coroutine function): 使用async关键字修饰的函数,就是协程函数. 

   协程对象(coroutine object): 调用协程函数,就会得到协程对象.

   注意: 调用协程函数, 并不会执行协程函数中的代码. 

### 定义一个协程函数

协程的实现有多种方式, 只讲解当前python最新版本推荐的

```python
# 定义一个协程函数
async def work():
    print("work开始...")
    print("work执行中...")
    print("work执行结束")
    return "工作结果"

# 调用协程函数,会得到一个协程对象.
coroutine_object = work()
print(coroutine_object)
```

### 协程函数执行

```python
"""
   asyncio.run方法做了3件事情. 
   (1)创建了一个事件循环
   (2)将接收到的协程对象,包装成一个任务(task) ,交给事件循环 
   (3)启动事件循环
   
   注意: asyncio.run() 会阻塞当前线程,直到任务执行完毕,并返回该任务return的最终结果. 
"""
import asyncio
print(asyncio.run(coroutine_object))
```

### await关键字

```python

"""
  await关键字的作用:  
   (1) 挂起: 遇到await关键字, 会暂停当前协程的执行.  
   
   (2) 等待: 遇到await关键字,事件循环会立即安排. await后面的对象去执行,并等待该对象执行完成. 并且可以拿到执行结果. 
       关键点: 在执行await后面的对象时, 会遇到两种情况.  
       情况一: 如果在执行该对象的代码时, 遇到了 await IO 操作, (需要等待外部资源返回结果的操作)
              案例: 网络请求,文件读写
              那CPU的执行权就会交给事件循环. 
              事件循环会去调度循环中的其他任务(如果有的话)
              
       情况二: 如果该对象中的代码,不包含任何 await IO操作.
              案例: print打印, 数学计算, 逻辑计算等. 
              此时事件循环拿不到CPU 控制权, 无法调度循环中的其他任务,不会发生任务切换.
  (3) 恢复:  当await 后的对象执行完毕,事件循环会恢复之前被挂起的协程,该协程会从当时挂起的位置继续执行,并且拿到返回值. 
  
  注意: 
  await后面只能写可等待的对象. 不能直接写 await 888等. 常见的可等待对象: a:协程对象 c:Task任务对象   b:Future对象(忽略)
"""

#定义一个协程函数
async def work():
    print("work开始...")
    print("work执行中...")
    #await asyncio.sleep(10)
    print("work执行结束")
    return "工作结果"

async def main():
    print("main开始执行")
    res = await work()
    print(res)
    print("main结束执行")
    return "main返回值结果"

#调用协程函数.
print(asyncio.run(main()))

```

### 定义多个同步任务

```python
import asyncio
import time

# 定义一个协程函数
async def work(n, delay):
    print(f'work{n}开始')
    print(f'work{n}执行中......')
    # 模拟一个IO等待
    await asyncio.sleep(delay)
    print(f'work{n}结束')
    return f'work{n}的返回值'

async def main():
    print('main开始')
    start = time.time()

    # 调用三次work函数，分别得到三个协程对象
    coroutine1 = work(1, 2)
    coroutine2 = work(2, 2)
    coroutine3 = work(3, 2)

    # 此处会等待coroutine1执行完成
    res1 = await coroutine1
    print(res1)

    # 等待上面的coroutine1完成后，再等待coroutine2完成
    res2 = await coroutine2
    print(res2)

    # 等待上面的coroutine2完成后，再等待coroutine3完成
    res3 = await coroutine3
    print(res3)

    print('main结束', time.time() - start)
    return '我是main的返回值'

# 将协程对象交给事件循环
result = asyncio.run(main())
print(result)

```

### 定义多个任务异步执行

```python
使用asyncio.create_task()方法向事件循环中添加任务，从而实现多个任务异步执行,
import asyncio
import time


# 定义一个协程函数
async def work(n, delay):
    print(f'work{n}开始')
    print(f'work{n}执行中......')
    # 模拟一个IO等待
    await asyncio.sleep(delay)
    print(f'work{n}结束')
    return f'work{n}的返回值'

async def main():
    print('main开始')
    start = time.time()

    # asyncio.create_task 会把一个协程对象包装成一个可被事件循环调度的任务，并注册到事件循环中
    task1 = asyncio.create_task(work(1, 2))
    task2 = asyncio.create_task(work(2, 2))
    task3 = asyncio.create_task(work(3, 2))

    # 此处会等待task1执行完成
    res1 = await task1
    print(res1)

    # 等待上面的task1完成后，再等待task2完成
    res2 = await task2
    print(res2)

    # 等待上面的task2完成后，再等待task3完成
    res3 = await task3
    print(res3)

    print('main结束', time.time() - start)
    return '我是main的返回值'

# 将协程对象交给事件循环
result = asyncio.run(main())
print(result)
```

### 定义多个任务异步执行升级版本

```python
syncio.gather方法可以把多个协程对象丢给事件循环，并在全部执行完后，一次性拿到所有结果.

import asyncio
import time


# 定义一个协程函数
async def work(n, delay):
    print(f'work{n}开始')
    print(f'work{n}执行中......')
    # 模拟一个IO等待
    await asyncio.sleep(delay)
    print(f'work{n}结束')
    return f'work{n}的返回值'

async def main():
    print('main开始')
    start = time.time()

    # 把多个协程对象同时丢给事件循环，并在全部执行完后，一次性拿到所有结果。
    result = await asyncio.gather(work(1, 2), work(2, 2), work(3, 2))
    print(result)

    print('main结束', time.time() - start)
    return '我是main的返回值'

# 将协程对象交给事件循环
result = asyncio.run(main())
print(result)

```

### AI 场景示例(AI模型的底层代码实现的原理)

```python
import asyncio
#import aiohttp  # 异步 HTTP 库

class AsyncAIClient:
    """异步 AI 客户端"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
    
    async def chat(self, message, model="gpt-3.5-turbo"):
        """异步发送消息"""
        # 模拟 API 调用
        await asyncio.sleep(1)
        return f"回复: {message}"
    
    async def batch_chat(self, messages):
        """批量并发发送消息"""
        tasks = [self.chat(msg) for msg in messages]
        return await asyncio.gather(*tasks)

async def main():
    client = AsyncAIClient("sk-xxx")
    
    # 并发发送多个消息
    messages = ["你好", "天气如何", "再见"]
    responses = await client.batch_chat(messages)
    
    for msg, resp in zip(messages, responses):
        print(f"Q: {msg}")
        print(f"A: {resp}")
        print()

asyncio.run(main())
```

---

## 异步流式输出

结合生成器和异步，实现异步流式输出。

### 异步生成器

```python
import asyncio

# 定义一个协程函数. 
async def async_stream(text, delay=0.1):
    """异步流式输出"""
    for word in text.split():
        # 模拟了耗时操作. 
        await asyncio.sleep(delay)
        # 返回出去之后,for循环暂定.  数被取走之后, for循环继续执行. 
        yield word + " "

async def main():
    text = "这是 异步 流式 输出 的内容"
    print("输出: ", end="", flush=True)
    
    async for chunk in async_stream(text, 0.2):
        print(chunk, end="", flush=True)
    print()

asyncio.run(main())
```

### AI 异步流式响应(看懂)

```python
import asyncio

class AsyncStreamingChat:
    """异步流式对话"""
    
    async def chat_stream(self, message):
        """流式返回响应"""
        response = f"收到消息：{message}。这是流式回复。"
        
        for word in response.split():
            await asyncio.sleep(0.1)  # 模拟延迟
            yield word + " "
    
    async def parallel_chat(self, messages):
        """并发处理多个对话"""
        async def collect_stream(message):
            chunks = []
            async for chunk in self.chat_stream(message):
                chunks.append(chunk)
            return "".join(chunks)
        
        tasks = [collect_stream(msg) for msg in messages]
        return await asyncio.gather(*tasks)

# 使用
async def main():
    chat = AsyncStreamingChat()
    
    # 流式输出单个响应
    print("单个对话:")
    async for chunk in chat.chat_stream("你好"):
        print(chunk, end="", flush=True)
    print("\n")
    
    # 并发处理多个对话
    print("并发对话:")
    messages = ["早上好", "天气如何"]
    responses = await chat.parallel_chat(messages)
    for msg, resp in zip(messages, responses):
        print(f"Q: {msg}\nA: {resp}\n")

asyncio.run(main())
```

---

## 综合项目：AI 对话系统(选作)

综合前面学习的所有知识，构建一个完整的 AI 对话系统。

### 项目需求

**功能：**

1. 支持多轮对话
2. 消息历史管理
3. 流式输出
4. 配置管理
5. 日志记录
6. 数据持久化
7. 异常处理

**项目结构：**
```
ai_chat_system/
├── config.py          # 配置管理
├── models.py          # 数据模型
├── chat.py            # 对话逻辑
├── storage.py         # 数据存储
├── utils.py           # 工具函数
├── main.py            # 主程序
├── .env               # 环境变量
└── requirements.txt   # 依赖
```

### 数据模型（models.py）

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Message(BaseModel):
    """消息模型"""
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.now)
    
    def token_count(self) -> int:
        return len(self.content) // 4

class ChatConfig(BaseModel):
    """对话配置"""
    model: str = "gpt-3.5-turbo"
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: int = Field(2000, gt=0)
    stream: bool = True

class ChatSession(BaseModel):
    """对话会话"""
    session_id: str
    messages: List[Message] = []
    config: ChatConfig
    created_at: datetime = Field(default_factory=datetime.now)
    
    def add_message(self, role: str, content: str):
        msg = Message(role=role, content=content)
        self.messages.append(msg)
    
    def total_tokens(self) -> int:
        return sum(msg.token_count() for msg in self.messages)
```

### 配置管理（config.py）

```python
import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class AppConfig(BaseModel):
    """应用配置"""
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = os.getenv("MODEL", "gpt-3.5-turbo")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "2000"))
    
    data_dir: str = "data"
    log_file: str = "app.log"
    
    def validate(self) -> bool:
        if not self.api_key:
            print("错误: API Key 未设置")
            return False
        return True

config = AppConfig()
```

### 数据存储（storage.py）

```python
import json
from pathlib import Path
from typing import Optional
from models import ChatSession

class Storage:
    """数据存储"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def save_session(self, session: ChatSession):
        """保存会话"""
        filename = self.data_dir / f"{session.session_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(session.model_dump(), f, ensure_ascii=False, indent=2, default=str)
    
    def load_session(self, session_id: str) -> Optional[ChatSession]:
        """加载会话"""
        filename = self.data_dir / f"{session_id}.json"
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            return ChatSession(**data)
        except FileNotFoundError:
            return None
    
    def list_sessions(self) -> list:
        """列出所有会话"""
        return [f.stem for f in self.data_dir.glob("*.json")]
```

### 对话逻辑（chat.py）

```python
import time
from typing import Generator
from models import ChatSession, ChatConfig
from config import config

class ChatClient:
    """对话客户端"""
    
    def __init__(self, chat_config: ChatConfig):
        self.config = chat_config
    
    def send_message(self, session: ChatSession, message: str) -> str:
        """发送消息（同步）"""
        session.add_message("user", message)
        
        # 模拟 API 调用
        response = f"这是对 '{message}' 的回复"
        session.add_message("assistant", response)
        
        return response
    
    def send_message_stream(self, session: ChatSession, message: str) -> Generator[str, None, None]:
        """发送消息（流式）"""
        session.add_message("user", message)
        
        # 模拟流式响应
        response = f"这是对 '{message}' 的流式回复内容"
        full_response = []
        
        for word in response.split():
            chunk = word + " "
            full_response.append(chunk)
            yield chunk
            time.sleep(0.1)
        
        # 保存完整响应
        session.add_message("assistant", "".join(full_response).strip())
```

### 工具函数（utils.py）

```python
import logging
from datetime import datetime

def setup_logging(log_file: str = "app.log"):
    """配置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def generate_session_id() -> str:
    """生成会话ID"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
```

### 主程序（main.py）

```python
import logging
from models import ChatSession, ChatConfig
from chat import ChatClient
from storage import Storage
from utils import setup_logging, generate_session_id
from config import config

def main():
    """主程序"""
    # 配置日志
    setup_logging(config.log_file)
    
    # 验证配置
    if not config.validate():
        return
    
    # 初始化
    storage = Storage(config.data_dir)
    chat_config = ChatConfig(
        model=config.model,
        temperature=config.temperature,
        max_tokens=config.max_tokens
    )
    client = ChatClient(chat_config)
    
    # 创建会话
    session_id = generate_session_id()
    session = ChatSession(session_id=session_id, config=chat_config)
    session.add_message("system", "你是一个Python助手")
    
    logging.info(f"会话开始: {session_id}")
    print(f"=== AI 对话系统 ===")
    print(f"会话ID: {session_id}")
    print("输入 'exit' 退出，'save' 保存会话\n")
    
    # 对话循环
    try:
        while True:
            user_input = input("你: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                break
            
            if user_input.lower() == "save":
                storage.save_session(session)
                print("会话已保存\n")
                continue
            
            # 流式输出
            print("AI: ", end="", flush=True)
            for chunk in client.send_message_stream(session, user_input):
                print(chunk, end="", flush=True)
            print("\n")
            
            logging.info(f"用户: {user_input}")
            logging.info(f"Token 数: {session.total_tokens()}")
    
    except KeyboardInterrupt:
        print("\n\n对话中断")
    
    finally:
        # 保存会话
        storage.save_session(session)
        logging.info(f"会话结束，总 tokens: {session.total_tokens()}")
        print(f"\n会话已保存: {session_id}")
        print(f"总消息数: {len(session.messages)}")
        print(f"总 tokens: {session.total_tokens()}")

if __name__ == "__main__":
    main()
```

### requirements.txt

```
pydantic>=2.0.0
python-dotenv>=1.0.0
requests>=2.31.0
```

### 运行项目

```bash
# 安装依赖
pip install -r requirements.txt

# 创建 .env 文件
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# 运行
python main.py
```

---

## 项目扩展建议

### 1. 真实 API 集成

```python
import requests

class RealChatClient(ChatClient):
    """真实 API 客户端"""
    
    def send_message_stream(self, session: ChatSession, message: str):
        session.add_message("user", message)
        
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": [msg.model_dump() for msg in session.messages],
            "temperature": self.config.temperature,
            "stream": True
        }
        
        response = requests.post(url, headers=headers, json=data, stream=True)
        full_response = []
        
        for line in response.iter_lines():
            if line:
                # 解析 SSE 格式
                chunk = parse_sse(line)
                if chunk:
                    full_response.append(chunk)
                    yield chunk
        
        session.add_message("assistant", "".join(full_response))
```

### 2. 异步版本

```python
import asyncio
import aiohttp

class AsyncChatClient:
    """异步对话客户端"""
    
    async def send_message_stream(self, session: ChatSession, message: str):
        session.add_message("user", message)
        
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(url, headers=headers, json=data) as response:
                full_response = []
                
                async for line in response.content:
                    chunk = parse_sse(line)
                    if chunk:
                        full_response.append(chunk)
                        yield chunk
                
                session.add_message("assistant", "".join(full_response))
```

### 3. 多模型支持

```python
class MultiModelClient:
    """多模型客户端"""
    
    def __init__(self):
        self.clients = {
            "openai": OpenAIClient(),
            "claude": ClaudeClient(),
            "gemini": GeminiClient()
        }
    
    def send_message(self, provider: str, message: str):
        client = self.clients.get(provider)
        if not client:
            raise ValueError(f"不支持的模型: {provider}")
        return client.send_message(message)
```

---

## 今日总结

### 核心知识点回顾

**1. 迭代器**

   可迭代对象, 就是可以被for循环遍历的对象. iter() 获取迭代器. 

- `__iter__` 和 `__next__` 方法. 
- 实现自定义迭代器(了解)

**2. 生成器**

- yield 关键字, 返回并且暂定,数值取走之后,继续运行.
- 生成器表达式: 便捷方式,不涉及yield关键字.
- 内存效率高

**3. 流式输出**
- 逐步返回结果
- 提升用户体验

**4. 异步编程**

协程概念:  

协程函数: async 函数

协程对象: async 函数调用.

- async/await 语法
- asyncio 模块
- await 关键字. 一定好好理解. 代码的执行顺序分析出来. 挂起,等待,恢复.

**5. 异步生成器** 读懂代码.

- async def + yield , await 
- async for 循环

**6. 综合项目**
- 模块化设计
- 数据模型（Pydantic）
- 配置管理
- 数据持久化

### 常见问题

**Q：生成器和列表推导式的区别？**
A：列表推导式一次生成所有元素，生成器按需生成，节省内存。

**Q：什么时候用异步？**
A：I/O 密集型操作（网络请求、文件读写、数据库查询）。

**Q：async def 和 def 的区别？**
A：async def 定义异步函数，必须用 await 调用；def 定义同步函数。

**Q：如何选择同步还是异步？**
A：计算密集型用同步；I/O 密集型用异步；简单脚本用同步。

**Q：综合项目如何组织代码？**
A：按功能分模块（models, config, storage, chat, utils, main）。

### 重点注意事项

1. **生成器只能遍历一次**：
   ```python
   gen = (x for x in range(5))
   list(gen)  # [0, 1, 2, 3, 4]
   list(gen)  # [] 已耗尽
   ```

2. **异步函数必须在异步上下文调用**：
   ```python
   # 错误
   result = await async_func()  # 在同步函数中不能用 await
   
   # 正确
   async def main():
       result = await async_func()
   asyncio.run(main())
   ```

3. **不要混用同步和异步 I/O**：
   ```python
   # 错误：异步函数中用同步 I/O
   async def bad():
       time.sleep(1)  # 阻塞整个事件循环
   
   # 正确
   async def good():
       await asyncio.sleep(1)
   ```

4. **项目配置不要硬编码**：使用 .env 文件和环境变量

1. **数据模型用 Pydantic**：自动验证和类型检查
