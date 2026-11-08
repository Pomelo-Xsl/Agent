# day5-03Python基础-循环与核心数据结构

## 学习目标

今天结束后，你能够：
- 使用 for 和 while 循环处理重复任务
- 掌握 break 和 continue 控制循环流程
- 使用列表存储和管理批量数据
- 使用字典表示键值对关系
- 理解元组和集合的应用场景
- 用列表推导式简洁地创建列表
- 构建多轮对话消息管理系统

---

## 循环

循环让程序能够重复执行相同的代码块，是处理批量数据的基础。

### for 循环

for 循环用于遍历序列（字符串、列表[]、字典等）中的每个元素。场景: 明确循环次数

**基本语法：**

```python
for 变量 in 序列:
    # 循环体代码
    # 每次循环，变量会依次取序列中的一个值
```

**遍历字符串**

字符串也是序列，可以遍历其中的每个字符。

```python
text = "Python"
for char in text:
    print(char)
    print(char, end="")     # 不换行打印. end = "" 自定义
```

输出：

```
P
y
t
h
o
n
```

**遍历列表**

```python
models = ["gpt-3.5-turbo", "gpt-4", "claude-3"]
for model in models:
    print(f"模型: {model}")
```

输出：

```
模型: gpt-3.5-turbo
模型: gpt-4
模型: claude-3
```

**使用 `range()` 生成数字序列**

`range()` 是 Python 的内置函数，用于生成连续的整数序列。当需要循环指定次数时使用。

```python
# range(n) 生成从 0 到 n-1 的整数
for i in range(5):
    print(i)
```

输出：

```
0
1
2
3
4
```

`range()` 的三种用法：

```python
range(5)        # 生成 0, 1, 2, 3, 4
range(2, 5)     # 生成 2, 3, 4（起始值2，结束值5，不包含5）
range(0, 10, 2) # 生成 0, 2, 4, 6, 8（起始0，结束10，步长2）

# 示例：打印 1 到 10
for i in range(1, 11):
    print(i, end=" ")  # end=" " 让输出用空格分隔而不是换行
# 输出：1 2 3 4 5 6 7 8 9 10
```

**`enumerate()` 同时获取索引和值**

`enumerate()` 是 Python 的内置函数，在遍历序列时同时返回元素的索引（位置）和值。当需要知道"这是第几个元素"时使用。

```python
messages = ["你好", "天气不错", "再见"]
for index, msg in enumerate(messages):
    print(f"{index}: {msg}")
```

输出：

```
0: 你好
1: 天气不错
2: 再见
```

`enumerate()` 可以指定起始索引（默认从 0 开始）：

```python
messages = ["你好", "天气不错", "再见"]
for index, msg in enumerate(messages, 1):  # 从 1 开始计数
    print(f"{index}. {msg}")
```

输出：

```
1. 你好
2. 天气不错
3. 再见
```

**`zip()` 并行遍历多个序列**

`zip()` 是 Python 的内置函数，可以同时遍历多个序列，将它们对应位置的元素配对在一起。

```python
names = ["GPT-4", "Claude", "Gemini"]
prices = [0.03, 0.015, 0.002]

for name, price in zip(names, prices):
    print(f"{name}: ${price}/1K tokens")
```

输出：

```
GPT-4: $0.03/1K tokens
Claude: $0.015/1K tokens
Gemini: $0.002/1K tokens
```

`zip()` 会以最短序列的长度为准：

```python
list1 = [1, 2, 3]
list2 = ['a', 'b']
for x, y in zip(list1, list2):
    print(x, y)
# 输出：
# 1 a
# 2 b
# （3 没有配对，被忽略）
```

### while 循环

`while` 循环在条件为真时持续执行，适合不确定循环次数的场景。  使用无线循环的时候, 也优先使用while循环.

```python
count = 0
while count < 3:
    print(f"第 {count + 1} 次循环")
    count += 1
```

输出：

```
第 1 次循环
第 2 次循环
第 3 次循环
```

**注意死循环**

```python
# 错误：忘记更新条件，导致死循环
count = 0
while count < 3:
    print("循环中")
    # 忘记 count += 1
```

这会无限循环，需要按 Ctrl+C 终止。

### break 和 continue

**break：跳出整个循环**

```python
for i in range(10):
    if i == 5:
        break
    print(i)
```

输出：

```
0
1
2
3
4
```

**continue：跳过本次循环，继续下一次**

```python
for i in range(5):
    if i == 2:
        continue
    print(i)
```

输出：

```
0
1
3
4
```

### AI 场景示例

```python
# 模拟多轮对话
max_rounds = 3
round_count = 0

while round_count < max_rounds:
    user_input = input(f"[第{round_count + 1}轮] 用户: ")
    
    # lower() 是字符串方法，将字符串转为小写，方便不区分大小写的比较
    if user_input.lower() == "exit":
        print("退出对话")
        break
    
    # strip() 是字符串方法，去除首尾空格
    if user_input.strip() == "":
        print("输入为空，请重新输入")
        continue
    
    # 模拟 AI 回复
    print(f"AI: 收到您的消息「{user_input}」")
    round_count += 1

print(f"对话结束，共 {round_count} 轮")
```

### 课堂练习(作业)

**批量 token 计算器**

编写程序，输入多段文本（输入 "done" 结束），计算每段文本的预估 token 数（字符数 ÷ 4）。 

token概念 : 

今天天气很好. 我们不适合学习.   

token 和 字不是一一对应的.  有单独的token解析器进行解析. 进行token解析, 解析完成后获取token_id. 就是每个token的唯一标识. 

参考答案：

```python
print("=== 批量 Token 计算器 ===")
texts = []

while True:
    text = input("请输入文本（输入done结束）: ")
    if text.lower() == "done":
        break
    texts.append(text)

print("\n计算结果:")
for i, text in enumerate(texts, 1):  # enumerate(texts, 1) 让索引从1开始，而不是0
    token_count = len(text) // 4
    print(f"{i}. {text[:20]}... - {token_count} tokens")
    # text[:20] 是字符串切片，取前20个字符，用于显示文本预览
```

---

## 列表（List）

列表是 Python 中最常用的数据结构，列表是**可变、有序**的元素集合，支持增删改查全操作，使用 `[]` 定义，元素间用逗号分隔，可存储不同类型数据。 列表的元素个数发生了变化,还是原来的对象. 

### 列表创建

```python
# 空列表
messages = []

# 初始化列表
models = ["gpt-3.5-turbo", "gpt-4", "claude-3"]

# 不同类型的元素（不推荐，但语法允许）
mixed = [1, "hello", True, 3.14]

#列表推导式创建.
# 列表推导式（高效创建）
square_list = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

### 列表索引和切片

```python
models = ["gpt-3.5-turbo", "gpt-4", "claude-3", "gemini-pro"]

print(models[0])      # gpt-3.5-turbo（第一个）
print(models[-1])     # gemini-pro（最后一个）
print(models[1:3])    # ['gpt-4', 'claude-3']（切片）
print(models[:2])     # ['gpt-3.5-turbo', 'gpt-4']（前两个）
print(models[2:])     # ['claude-3', 'gemini-pro']（从第3个到末尾）
```

### 列表常用方法

```python
messages = []

# 添加元素
messages.append("你好")           # 在末尾添加
messages.append("天气不错")
print(messages)  # ['你好', '天气不错']

# 插入元素
messages.insert(1, "早上好")      # 在索引1处插入
print(messages)  # ['你好', '早上好', '天气不错']

# 扩展列表
more_messages = ["再见", "晚安"]
messages.extend(more_messages)
print(messages)  # ['你好', '早上好', '天气不错', '再见', '晚安']

# 删除元素
messages.remove("早上好")         # 删除指定值
print(messages)  # ['你好', '天气不错', '再见', '晚安']

last = messages.pop()            # 删除并返回最后一个元素
print(last)      # 晚安
print(messages)  # ['你好', '天气不错', '再见']

# 获取长度
print(len(messages))  # 3
# len() 是内置函数，返回序列（列表、字符串、字典等）的长度（元素个数）

# 获取指定元素的第一个索引位置
idx = numbers.index(target)  
print(f"索引号: {idx}, 值: {numbers[idx]}")

# 检查元素是否存在
print("你好" in messages)  # True
print("早安" in messages)  # False
# in 运算符检查元素是否在列表中，返回 True 或 False

# 排序. 字符串排序的时候, 使用的是unicode
numbers = [3, 1, 4, 1, 5]
numbers.sort()  # sort() 会直接修改原列表，按从小到大排序
print(numbers)  # [1, 1, 3, 4, 5]

# 反转
numbers.reverse()  # reverse() 会直接修改原列表，颠倒元素顺序
print(numbers)  # [5, 4, 3, 1, 1]
```

常用方法总结: 

### 

| 函数                         | 说明                                                |
| ---------------------------- | --------------------------------------------------- |
| list.insert(index,x)         | 在指定位置插入 x                                    |
| list.append(x)               | 在列表末尾追加 x                                    |
| list1.extend(list2)          | 在列表 1 的末尾追加列表 2 的数据                    |
| del list[index]              | 删除指定位置的数据或切片                            |
| list.remove(x)               | 删除第一次出现的 x                                  |
| list.pop([index])            | 删除指定位置的数据，默认为末尾数据                  |
| list.clear()                 | 清空列表中元素                                      |
| list[index] = x              | 修改指定位置的数据                                  |
| list1[start:end] = list2     | 修改列表切片的数据                                  |
| sorted(list[,reverse=True])  | 返回排序后的新列表，可选降序                        |
| list.sort([reverse=True])    | 对列表就地排序，可选降序                            |
| list.reverse()               | 反转列表中的元素                                    |
| list.index(x[,start,[,end]]) | 返回 x 在列表中首次出现的位置，可指定起始和结束范围 |
| list.count(x)                | 返回 x 的数量                                       |
| len(list)                    | 返回列表元素个数                                    |
| max(list)                    | 返回列表中最大值                                    |
| min(list)                    | 返回列表中最小值                                    |
| sum(list)                    | 返回列表中所有元素和                                |
| list.copy()                  | 拷贝列表                                            |
| list(x)                      | 将序列转换为列表                                    |

### 列表推导式

列表推导式是创建列表的简洁方式，它将一个可迭代对象（如列表、元组、集合、字符串等）的元素通过某种运算或条件筛选后生成一个新的列表.可以用一行代码完成"遍历→处理→生成新列表"的操作。

**基本语法：**

```python
[表达式 for 变量 in 序列]
```

**基础示例**

```python
# 传统方式：创建平方数列表
squares = []
for i in range(5):
    squares.append(i ** 2)
print(squares)  # [0, 1, 4, 9, 16]

# 列表推导式：一行搞定
squares = [i ** 2 for i in range(5)]
print(squares)  # [0, 1, 4, 9, 16]
```

**带条件过滤**

语法：`[表达式 for 变量 in 序列 if 条件]`

```python
# 只保留偶数
evens = [i for i in range(10) if i % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]

# 转换大小写
words = ["Hello", "WORLD", "Python"]
lower_words = [w.lower() for w in words]
print(lower_words)  # ['hello', 'world', 'python']
```

### AI 场景示例

```python
# 消息列表管理
messages = []

# 添加系统消息.
消息一共有三种. system 给模型设定一个角色..    user: 用户发出的消息.  assistant: 模型给你回复的问题. 
messages.append({
    "role": "system",
    "content": "你是一个 Python 编程助手"
})

# 添加用户消息
messages.append({
    "role": "user",
    "content": "如何读取文件？"
})

# 添加助手消息
messages.append({
    "role": "assistant",
    "content": "可以使用 open() 函数..."
})

# 打印所有消息
for msg in messages:
    print(f"[{msg['role']}] {msg['content']}")
```

输出：

```
[system] 你是一个 Python 编程助手
[user] 如何读取文件？
[assistant] 可以使用 open() 函数...
```

### 课堂练习

**模型名称筛选器**

给定一个模型名称列表，编写程序筛选出所有包含 "gpt" 的模型名称（不区分大小写）。

```python
models = [
    "gpt-3.5-turbo",
    "claude-3-opus",
    "gpt-4",
    "gemini-pro",
    "GPT-4-turbo",
    "llama-2"
]
```

参考答案：

```python
models = [
    "gpt-3.5-turbo",
    "claude-3-opus",
    "gpt-4",
    "gemini-pro",
    "GPT-4-turbo",
    "llama-2"
]

# 方式1：循环
gpt_models = []
for model in models:
    if "gpt" in model.lower():  # lower() 转为小写，实现不区分大小写
        gpt_models.append(model)

# 方式2：列表推导式（推荐）
gpt_models = [model for model in models if "gpt" in model.lower()]

print(f"GPT 模型数: {len(gpt_models)}")
for model in gpt_models:
    print(f"- {model}")
```

输出：

```
GPT 模型数: 3
- gpt-3.5-turbo
- gpt-4
- GPT-4-turbo
```

---

## 字典（Dictionary）

字典是**可变、无序**的键值对（key-value）集合，使用 `{key:value}` 定义，key 唯一且不可变（字符串、数字、元组），value 可任意类型，查询效率极高。  等价于Java当中的HashMap

字典用于存储键值对，是 AI 开发中最重要的数据结构之一，与 JSON 数据高度对应。{"":""}

### 字典创建

```python
# 空字典
config = {}

# 初始化字典
model_config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
}

# 字典的键必须是不可变类型（字符串、数字、元组）
# 值可以是任何类型
```

### 字典访问与修改

可通过 [] 访问字典中的元素。key 不存在时会报错。

也可以通过 get () 获取字典中的元素。key 不存在时会返回 None，也可以指定默认值 .安全访问.

```python
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
}

# 访问值, key不存在, 报错.
print(config["model"])        # gpt-4
print(config["temperature"])  # 0.7

# 修改值
config["temperature"] = 0.8
print(config["temperature"])  # 0.8

# 添加新键值对
config["stream"] = True
print(config)
# {'model': 'gpt-4', 'temperature': 0.8, 'max_tokens': 2000, 'stream': True}

# 删除键值对
del config["stream"]
```

**安全访问：`get()` 方法**

```python
config = {"model": "gpt-4"}

# 直接访问不存在的键会报错
# print(config["temperature"])  # KeyError

# 使用 get() 安全访问
print(config.get("temperature"))         # None
print(config.get("temperature", 0.7))    # 0.7（默认值）
```

### 字典常用方法

```python
config = {
    "model": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2000
}

# 获取所有键
print(config.keys())    # dict_keys(['model', 'temperature', 'max_tokens'])
# keys() 返回字典中所有的键

# 获取所有值
print(config.values())  # dict_values(['gpt-4', 0.7, 2000])
# values() 返回字典中所有的值

# 获取所有键值对
print(config.items())   # dict_items([('model', 'gpt-4'), ('temperature', 0.7), ...])
# items() 返回字典中所有的键值对，每个键值对是一个元组 (key, value)

# 遍历字典的键
for key in config:
    print(f"{key}: {config[key]}")

# 遍历键值对（推荐方式）
for key, value in config.items():
    print(f"{key}: {value}")
# 使用 items() 可以同时获取键和值，更方便

# 更新字典
new_config = {"stream": True, "temperature": 0.8}
config.update(new_config)  # update() 将另一个字典的内容合并进来
print(config)
# 如果键已存在，会覆盖原值；如果不存在，会添加新键值对

# 检查键是否存在
print("model" in config)      # True
print("api_key" in config)    # False
# in 检查字典中是否存在某个键
```

### 字典嵌套

字典可以嵌套，用于表示复杂的结构化数据。

```python
message = {
    "role": "user",
    "content": "如何使用 Python？",
    "metadata": {
        "timestamp": "2024-01-01 10:00:00",
        "user_id": "user123"
    }
}

print(message["role"])                    # user
print(message["metadata"]["user_id"])     # user123
```

### 字典常用方法总结: 

### 

| 函数                           | 说明                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| del dict[key]                  | 根据 key 删除键值对                                          |
| dict.pop(key[,default])        | .获取 key 所对应的 value，同时删除该键值对，可设置默认值     |
| dict.popitem()                 | 取出字典中的最后插入的键值对，字典为空则报错                 |
| dict.clear()                   | 清空字典                                                     |
| dict1.update(dict2)            | 将 dict2 中的键值对更新到 dict1 中                           |
| dict.get(key[,default])        | 获取字典中 key 对应 value，可设置默认值                      |
| dict.setdefault(key[,default]) | 获取字典中 key 对应 value，可设置默认值。若 key 不存在于字典中，将会添加 key 并将 value 设为默认值 |
| dict.keys()                    | 获取字典所有的 key，返回一个视图对象。字典改变，视图也会跟着变化 |
| dict.values()                  | 获取字典所有的 value，返回一个视图对象                       |
| dict.items()                   | 获取字典所有的 (key,value)，返回一个视图对象                 |
| dict.copy()                    | 拷贝字典, 涉及到神copy 和浅copy讲解                          |
| dict.fromkeys(seq[,default])   | 以序列 seq 中元素做字典的 key 创建一个新字典，可设置 value 的默认值 |

### AI 场景示例

```python
# 工具配置 , 大模型当中的工具.  

tools = [
    {
        "name": "get_weather",
        "description": "获取指定城市的天气",
        "parameters": {
            "city": {"type": "string", "required": True}
        }
    },
    {
        "name": "calculator",
        "description": "执行数学计算",
        "parameters": {
            "expression": {"type": "string", "required": True}
        }
    }
]

# 遍历工具
for tool in tools:
    print(f"工具: {tool['name']}")
    print(f"描述: {tool['description']}")
    print(f"参数: {tool['parameters']}")
    print("---")
```

输出：

```
工具: get_weather
描述: 获取指定城市的天气
参数: {'city': {'type': 'string', 'required': True}}
---
工具: calculator
描述: 执行数学计算
参数: {'expression': {'type': 'string', 'required': True}}
---
```

### 课堂练习

**配置合并器**

编写程序，将用户配置和默认配置合并，用户配置优先级更高。

```python
default_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": False
}

user_config = {
    "model": "gpt-4",
    "temperature": 0.9
}

```

参考答案：

```python
default_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": False
}

user_config = {
    "model": "gpt-4",
    "temperature": 0.9
}

# 合并配置
final_config = default_config.copy()  # copy() 创建字典的副本，避免修改原字典
final_config.update(user_config)

print("最终配置:")
for key, value in final_config.items():
    print(f"  {key}: {value}")
```

输出：

```
最终配置:
  model: gpt-4
  temperature: 0.9
  max_tokens: 1000
  stream: False
```

---

## 元组（Tuple）

元组是**不可变、有序**的元素集合，使用 `()` 定义（单个元素需加逗号），特性与列表类似，但无法修改元素，安全性更高。

元组是不可变的序列，一旦创建就不能修改。

### 元组创建

```python
# 空元组
empty = ()
empty2 = tuple() #创建一个空元组. 

# 包含元素的元组
point = (10, 20)
rgb = (255, 128, 0)

# 单元素元组（注意逗号）
single = (5,)    # 正确
not_tuple = (5)  # 这是整数，不是元组

# 元组推导式（需转换为元组）
tuple_gen = (x for x in range(3)) # <genexpr> at 0x00000151867F6800>
tuple2 = tuple(tuple_gen)  # (0,1,2)
```

### 元组操作

```python
point = (10, 20, 30)

# 索引访问
print(point[0])   # 10
print(point[-1])  # 30

# 切片
print(point[1:])  # (20, 30)

# 不能修改
# point[0] = 15  # TypeError: 'tuple' object does not support item assignment

# 元组解包
x, y, z = point
print(f"x={x}, y={y}, z={z}")  # x=10, y=20, z=30

# 遍历
for value in point:
    print(value)
```

### 元素的不可变

元组的不可变指的是元组所指向的内存中的内容不可变，但可以重新赋值。重新赋值后, 会产生一个全新的元组

```python
tuple1 = (100, 200, 300)
print(id(tuple1), tuple1)
tuple1 = tuple1 + (1, 2, 3)
print(id(tuple1), tuple1)
```



### 元组的应用场景

**函数多返回值**

```python
def get_model_info():
    name = "gpt-4"
    price = 0.03
    max_tokens = 8192
    return name, price, max_tokens  # 返回元组

model, price, tokens = get_model_info()
result = get_model_info()
print(f"模型: {model}, 价格: ${price}, 最大tokens: {tokens}")
print(type(result))
```

**作为字典的键**

```python
# key不允许改变, 列表不能作为字典的键，元组可以
coordinates = {
    (0, 0): "原点",
    (1, 0): "右侧",
    (0, 1): "上方"
}

print(coordinates[(0, 0)])  # 原点
```

### 元组 vs 列表

| 特性 | 列表 | 元组 |
|------|------|------|
| 可变性 | 可变, 内容变化, 还是原来列表 | 不可变,一旦发生了改变, 一定会产生一个新的元组 |
| 语法 | `[1, 2, 3]` | `(1, 2, 3)` 注意: (5,) |
| 性能 | 稍慢 | 稍快. |
| 应用 | 同类数据集合 | 固定结构数据 |

---

## 集合（Set）

集合是**可变、无序、无重复**的元素集合，使用 `{}` 或 `set()` 定义，适用于去重、快速数据判断等集合运算场景,因为没有索引，所以不能使用索引或切片访问。 

注意: set集合的应用场景.   当集合要进行判断, 运算, 优先考虑set . 

### 集合创建

```python
# 使用 {} 创建非空集合
tags = {"Python", "AI", "GPT"}

# 使用 set() 从列表创建集合（自动去重）
numbers = set([1, 2, 2, 3, 3, 3])
print(numbers)  # {1, 2, 3}

# 空集合必须用 set()
empty = set()  # 正确：创建空集合
# empty = {}   # 错误：这是空字典，不是空集合
# 因为 {} 优先表示字典，所以空集合要用 set()

# 集合推导式
even_set = {x for x in range(10) if x % 2 == 0}  # {0,2,4,6,8}
```

### 集合操作

```python
tags = {"Python", "AI"}

# 添加元素
tags.add("GPT")
print(tags)  # {'Python', 'AI', 'GPT'}

# 删除元素
tags.remove("AI")
print(tags)  # {'Python', 'GPT'}

# 检查是否存在
print("Python" in tags)  # True
#删除一个元素, 如果元素不存在, 不会报错.
set1.discard(1)
print(set1)
# 长度
print(len(tags))  # 2
```

### 集合运算

```python
redis 当中 set,  set数据存储数据之后 计算运算 , 交集,并集,差集,  canal

skills_a = {"Python", "AI", "SQL"}
skills_b = {"Python", "Java", "AI"}

# 交集（共同拥有）
print(skills_a & skills_b)  # {'Python', 'AI'}
print(skills_a.intersection(skills_b))  # 等价写法

# 并集（合并）
print(skills_a | skills_b)  # {'Python', 'AI', 'SQL', 'Java'}
print(skills_a.union(skills_b))  # 等价写法

# 差集（A有但B没有）
print(skills_a - skills_b)  # {'SQL'}
print(skills_a.difference(skills_b))  # 等价写法

# 对称差集（A或B独有）
print(skills_a ^ skills_b)  # {'SQL', 'Java'}
```

集合常用函数总结; 

### 

| 函数                                   | 说明                                                         |              |
| -------------------------------------- | ------------------------------------------------------------ | ------------ |
| set.add(x)                             | 添加元素                                                     |              |
| set.update(x)                          | 添加元素，x 可以为列表、元组、字符串、字典等可迭代对象       |              |
| set.union(x)                           | 添加元素后返回一个新的集合，x 可以为列表、元组、字符串、字典等可迭代对象 |              |
| set.remove(x)                          | 从集合中移除 x，x 不存在则报错                               |              |
| set.discard(x)                         | 从集合中移除 x，x 不存在也不报错                             |              |
| set.pop()                              | 随机取出集合中的一个元素，如果集合为空则报错                 |              |
| set.clear()                            | 清空集合                                                     |              |
| set.difference(x1,...)                 | 求 set1 和 x1 的差集，返回一个新的集合                       |              |
| set.difference_update(x1,...)          | 求 set1 和 x1 的差集                                         |              |
| set.intersection(x1,...)               | 求 set1 和 x1 的交集，返回一个新的集合                       |              |
| set.intersection_update(x1,...)        | 求 set1 和 x1 的交集                                         |              |
| set1 & set2                            | 两集合求交集                                                 |              |
| set1                                   | set2                                                         | 两集合求并集 |
| set1 - set2                            | 两集合求差集                                                 |              |
| set1.isdisjoint(set2)                  | 判断两集合是否没有交集                                       |              |
| set1.issubset(set2)                    | 判断 set1 是否为 set2 的子集                                 |              |
| set1.issuperset(set2)                  | 判断 set2 是否为 set1 的子集                                 |              |
| set1.symmetric_difference(set2)        | 求两集合中不重复的元素，返回一个新的集合                     |              |
| set1.symmetric_difference_update(set2) | 求两集合中不重复的元素                                       |              |
| set.copy()                             | 拷贝集合                                                     |              |
| len(set)                               | 返回集合元素个数                                             |              |
| max(set)                               | 求集合中元素的最大值                                         |              |
| min(set)                               | 求集合中元素的最小值                                         |              |
| sum(set)                               | 求集合中元素的加和                                           |              |

### AI 场景示例

```python
# 文档去重
docs = [
    "Python入门.txt",
    "AI基础.txt",
    "Python入门.txt",  # 重复
    "API文档.txt",
    "AI基础.txt"       # 重复
]

# 去重
unique_docs = set(docs)
print(f"原始: {len(docs)} 个文档")
print(f"去重后: {len(unique_docs)} 个文档")
print(unique_docs)
```

输出：

```
原始: 5 个文档
去重后: 3 个文档
{'AI基础.txt', 'Python入门.txt', 'API文档.txt'}
```

### 课堂练习

**关键词统计**

给定多个用户问题，统计所有出现过的关键词（去重）。

参考答案：

```python
questions = [
    "Python 如何 读取 文件",
    "如何 使用 Python 处理 JSON",
    "Python 异常 处理",
    "文件 读取 错误 怎么办"
]

keywords = set()
for question in questions:
    words = question.split()
    for word in words:
        keywords.add(word)

print(f"关键词总数: {len(keywords)}")
print(sorted(keywords))  # sorted() 返回排序后的列表，不修改原集合
```

输出：

```
关键词总数: 11
['JSON', 'Python', 'processing', '如何', '处理', '异常', '文件', '怎么办', '读取', '错误', '使用']
```

---

## 序列通用操作

序列是有序的元素集合，支持通过索引访问、切片等统一操作，核心包含列表（List）、元组（Tuple）、字符串（String）三种类型。 





### 序列的操作总结

- **索引**：通过 `sequence[index]` 访问元素，正向索引从 0 开始，反向索引从 - 1 开始。
- **切片**：通过 `sequence[start:end:step]` 截取部分元素，start 默认 0、end 默认序列长度、step 默认 1。
- **拼接**：使用 `+` 合并两个同类型序列，如 `[1,2] + [3,4]`。
- **重复**：使用 `*` 重复序列元素，如 `[1,2] * 3` 得到 `[1,2,1,2,1,2]`。
- **成员判断**：使用 `in`/`not in` 检查元素是否在序列中。
- **长度 / 最值**：通过 `len()`/`max()`/`min()` 获取序列长度、最大值、最小值。

### 索引切片  不演示

### 拼接和重复

```python
# 拼接
list1 = [1, 2]
list2 = [3, 4]
print(list1 + list2)  # [1, 2, 3, 4]

# 重复
print([0] * 5)  # [0, 0, 0, 0, 0]
print("=" * 20) # ====================
```

### 成员判断

```python
messages = ["你好", "天气不错", "再见"]

print("你好" in messages)    # True
print("晚安" in messages)    # False
print("晚安" not in messages) # True
```

### 长度、最大值、最小值

Python 提供了一些内置函数，可以对序列进行统计操作。

```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6]

print(len(numbers))  # 8 - 返回元素个数
print(max(numbers))  # 9 - 返回最大值
print(min(numbers))  # 1 - 返回最小值
print(sum(numbers))  # 31 - 返回所有元素的总和（仅限数字）
```

### 列表、元组、集合的选择原则

| 场景 | 推荐类型 |
|------|---------|
| 需要修改（增删改） | 列表 |
| 不需要修改，性能优先 | 元组 |
| 需要去重 | set集合 |
| 需要顺序 | 列表或元组 |
| 需要键值对 | 字典 |

---

## 浅拷贝与深拷贝

在处理列表和字典时，理解拷贝机制很重要，尤其是处理嵌套结构（列表套字典、字典套列表）时。

### 为什么需要拷贝

```python
# 直接赋值：不是拷贝，只是引用
messages = [{"role": "user", "content": "你好"}]
messages2 = messages  # 只是创建了一个新的引用

messages2.append({"role": "assistant", "content": "你好！"})
print(len(messages))   # 2（原列表也被修改了！）
print(len(messages2))  # 2
```

直接赋值不会创建新对象，两个变量指向同一个列表。

### 浅拷贝（Shallow Copy）

浅拷贝创建新的外层对象，但内层对象仍然共享。

**三种方式：**

```python
# 方式1：切片
list1 = [1, 2, 3]
list2 = list1[:]

# 方式2：copy()方法
list3 = list1.copy()

# 方式3：copy模块
import copy
list4 = copy.copy(list1)
```

**简单数据结构的浅拷贝：**

```python
# 简单列表（元素是不可变类型）
models = ["gpt-3.5", "gpt-4", "claude"]
models_copy = models.copy()

models_copy.append("gemini")
print(models)       # ['gpt-3.5', 'gpt-4', 'claude']（不受影响）
print(models_copy)  # ['gpt-3.5', 'gpt-4', 'claude', 'gemini']
```

**嵌套结构的浅拷贝问题：**

```python
# 嵌套列表（列表中包含字典）
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]

# 浅拷贝
messages_copy = messages.copy()

# 修改外层：互不影响
messages_copy.append({"role": "user", "content": "再见"})
print(len(messages))       # 2（不受影响）
print(len(messages_copy))  # 3

# 修改内层：会相互影响！
messages_copy[0]["content"] = "Hello"
print(messages[0]["content"])       # Hello（被影响了！）
print(messages_copy[0]["content"])  # Hello
```

### 深拷贝（Deep Copy）

深拷贝会递归复制所有层级的对象，完全独立。

```python
import copy

messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]

# 深拷贝
messages_deep = copy.deepcopy(messages)

# 修改内层：互不影响
messages_deep[0]["content"] = "Hello"
print(messages[0]["content"])       # 你好（不受影响）
print(messages_deep[0]["content"])  # Hello
```

### AI 场景示例

```python
import copy

# 原始配置
default_config = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "params": {
        "max_tokens": 2000,
        "top_p": 1.0
    }
}

# 浅拷贝：修改嵌套字典会影响原配置
config1 = default_config.copy()
config1["params"]["max_tokens"] = 1000
print(default_config["params"]["max_tokens"])  # 1000（被影响）

# 深拷贝：完全独立
config2 = copy.deepcopy(default_config)
config2["model"] = "gpt-4"
config2["params"]["max_tokens"] = 4000
print(default_config["model"])                 # gpt-3.5-turbo（不受影响）
print(default_config["params"]["max_tokens"])  # 1000（不受影响）
```

### 实用建议

**什么时候用浅拷贝：**

- 列表只包含简单类型（数字、字符串）
- 不需要修改嵌套对象

**什么时候用深拷贝：**

- 列表或字典包含嵌套结构
- 需要完全独立的副本
- AI 开发中复制消息列表、配置对象

**记忆口诀：**
- 直接赋值 = 共享同一个对象
- 浅拷贝 = 新容器，旧内容
- 深拷贝 = 全新对象

### 课堂练习(作业)

**消息列表的安全复制**

有一个消息列表，需要创建多个独立的会话副本。

```python
import copy

# 原始消息模板
template_messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
]

# 错误方式：直接赋值
session1 = template_messages
session1.append({"role": "assistant", "content": "你好！"})
print(len(template_messages))  # 3（模板被污染）

# 正确方式：深拷贝
template_messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"}
]

session2 = copy.deepcopy(template_messages)
session3 = copy.deepcopy(template_messages)

session2.append({"role": "assistant", "content": "你好！"})
session3.append({"role": "assistant", "content": "Hi!"})

print(len(template_messages))  # 2（模板不受影响）
print(len(session2))           # 3
print(len(session3))           # 3
```

---

## 今日总结

### 核心知识点回顾

**1. 循环**

- for 循环：遍历序列（字符串、列表、字典）

- while 循环：条件不确定时使用. 

  明确循环次数优先使用for,不明确循环次数, while. 无线循环,使用while

- range()：生成数字序列，支持起始、结束、步长. range(0,10,2)

- enumerate()：同时获取索引和值,

- zip()：并行遍历多个序列

  range(), enumerate(), zip() 都是属于python的内置函数. 内置函数可以直接使用.

- break：跳出循环

- continue：跳过本次循环

**2. 列表（list）**

- 有序、可变、可重复
- 常用方法：append()、insert()、extend()、remove()、pop()、sort()
- 索引和切片：[0]、[-1]、[1:3] 重点,序列有两套索引. 
- 列表推导式：`[expr for item in iterable if condition]`

**3. 字典（dict）**

- 键值对存储，键必须不可变. []不能充当key. 元组可以.
- 常用方法：get()、keys()、values()、items()、update()
- 字典嵌套：表示复杂数据结构
- 与 JSON 数据高度对应. json模块,字典和json转换操作.

**4. 元组（tuple）**

- 有序、不可变
- 用于固定结构数据、函数多返回值
- 可作为字典的键

**5. 集合（set）**

- 无序、不重复
- 用于去重
- 集合运算：交集(&)、并集(|)、差集(-)

**6. 序列通用操作** 

- 索引
- 切片
- 拼接：+
- 重复：*
- 成员判断：in、not in
- 长度、最大、最小：len()、max()、min()、sum()

### 数据结构选择指南

| 需求 | 推荐 | 原因 |
|------|------|------|
| 需要修改（增删改） | 列表 | 可变 |
| 不需要修改 | 元组 | 不可变，性能更好 |
| 需要去重 | 集合 | 自动去重 |
| 需要键值对 | 字典 | key-value 映射 |
| 需要保持顺序 | 列表或元组 | 有序 |
| AI 消息列表 | 列表 + 字典 | `[{"role": "...", "content": "..."}]` |
| 工具配置 | 字典 | JSON 对应 |
| 文档去重 | 集合 | 自动去重 |

### AI 开发中的应用

**消息管理**
```python
messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！"}
]
```

**工具配置**

```python
tools = {
    "calculator": {"desc": "计算器", "params": ["expression"]},
    "weather": {"desc": "天气", "params": ["city"]}
}
```

**批量处理**

```python
# 批量处理文档
for doc in documents:
    chunks = split_text(doc)
    for chunk in chunks:
        process(chunk)
```

### 常见问题

**Q：列表和元组有什么区别？**
A：列表可变，元组不可变。列表用 []，元组用 ()。元组性能更好，适合不需要修改的数据。

**Q：什么时候用列表推导式？**
A：需要从一个列表创建另一个列表时。比传统循环更简洁，但不要过度复杂化。

**Q：字典的键可以是列表吗？**
A：不可以，键必须是不可变类型（字符串、数字、元组）。列表是可变的，不能作为键。

**Q：如何选择用字典还是列表？**
A：如果数据有明确的 key-value 关系，用字典。如果只是一组有序的值，用列表。

**Q：为什么 AI 开发中字典这么重要？**
A：因为 JSON 是 AI API 的标准数据格式，Python 字典与 JSON 高度对应，可以直接互转。 JSON模块讲解

**Q：集合什么时候用？**
A：主要用于去重和集合运算（交集、并集等）。比如去重文档名、关键词统计等。

注意: 这个知识点如何学会了?  



### 重点注意事项

1. **循环中的索引**：Python 索引从 0 开始，不是 1
2. **range() 的边界**：range(5) 生成 0-4，不包含 5
3. **字典访问**：访问不存在的键会报错，用 get() 更安全 
4. **列表是可变的**：修改列表会影响所有引用
5. **集合是无序的**：不能用索引访问，不保证顺序
6. **列表推导式不要过度复杂**：超过两层嵌套就用传统循环



## 当天作业

### 多轮对话消息管理器

编写一个命令行程序，实现以下功能：

- 用户可以输入多轮消息
- 每条消息保存为字典格式 `{"role": "user", "content": "..."}`
- 输入 "history" 查看所有历史消息
- 输入 "clear" 清空历史
- 输入 "exit" 退出程序

参考答案：

```python
print("=== 多轮对话消息管理器 ===")
print("命令: history(查看历史), clear(清空), exit(退出)\n")

messages = []

while True:
    user_input = input("用户: ")
    
    if user_input == "exit":
        print("退出程序")
        break
    
    if user_input == "history":
        if not messages:
            print("暂无历史消息")
        else:
            print(f"\n共 {len(messages)} 条消息:")
            for i, msg in enumerate(messages, 1):
                print(f"{i}. [{msg['role']}] {msg['content']}")
        print()
        continue
    
    if user_input == "clear":
        messages = []
        print("历史已清空\n")
        continue
    
    if user_input.strip() == "":
        print("输入为空，请重新输入\n")
        continue
    
    # 保存用户消息
    messages.append({
        "role": "user",
        "content": user_input
    })
    
    # 模拟 AI 回复
    ai_response = f"收到您的消息: {user_input}"
    messages.append({
        "role": "assistant",
        "content": ai_response
    })
    
    print(f"AI: {ai_response}\n")
```

### Prompt 模板管理器

创建一个 prompt 模板字典，根据用户选择的任务类型返回对应的模板。

要求：

- 至少包含 3 种任务类型（代码编写、文本分析、翻译）
- 每个模板是一个字典，包含 system_prompt 和 user_template
- 用户选择任务类型后，输入具体内容，生成完整 prompt

参考答案：

```python
templates = {
    "code": {
        "system_prompt": "你是一个专业的编程助手，擅长编写高质量代码。",
        "user_template": "请帮我编写: {task}"
    },
    "analyze": {
        "system_prompt": "你是一个文本分析专家，擅长理解和分析文本。",
        "user_template": "请分析以下内容: {task}"
    },
    "translate": {
        "system_prompt": "你是一个专业翻译，精通中英互译。",
        "user_template": "请翻译: {task}"
    }
}

print("=== Prompt 模板管理器 ===")
print("任务类型:")
for key, value in templates.items():
    print(f"  {key}: {value['system_prompt']}")

task_type = input("\n选择任务类型: ")

if task_type in templates:
    user_input = input("输入任务内容: ")
    
    template = templates[task_type]
    system = template["system_prompt"]
    user = template["user_template"].format(task=user_input)
    # format() 是字符串方法，用于替换字符串中的 {task} 占位符
    
    print("\n" + "="*60)
    print("[System]", system)
    print("[User]", user)
    print("="*60)
else:
    print("无效的任务类型")
```

### 工具配置去重

给定一个包含重复工具的列表，根据工具名称去重。

```python
tools = [
    {"name": "calculator", "desc": "计算器"},
    {"name": "weather", "desc": "天气查询"},
    {"name": "calculator", "desc": "计算器"},  # 重复
    {"name": "search", "desc": "搜索"},
    {"name": "weather", "desc": "天气查询"}   # 重复
]
```

参考答案：

```python
tools = [
    {"name": "calculator", "desc": "计算器"},
    {"name": "weather", "desc": "天气查询"},
    {"name": "calculator", "desc": "计算器"},
    {"name": "search", "desc": "搜索"},
    {"name": "weather", "desc": "天气查询"}
]

# 使用集合记录已见过的名称
seen_names = set()
unique_tools = []

for tool in tools:
    if tool["name"] not in seen_names:
        seen_names.add(tool["name"])
        unique_tools.append(tool)

print(f"原始工具数: {len(tools)}")
print(f"去重后: {len(unique_tools)}")
print("\n去重后的工具:")
for tool in unique_tools:
    print(f"  - {tool['name']}: {tool['desc']}")
```

输出：

```
原始工具数: 5
去重后: 3

去重后的工具:
  - calculator: 计算器
  - weather: 天气查询
  - search: 搜索
```

### 消息统计分析器

编写程序，分析消息列表，统计：

- 用户消息数量
- 助手消息数量
- 平均消息长度
- 最长的消息

```python
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮你的吗？"},
    {"role": "user", "content": "如何学习 Python"},
    {"role": "assistant", "content": "学习 Python 可以从基础语法开始..."},
    {"role": "user", "content": "谢谢"}
]
```

参考答案：

```python
messages = [
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮你的吗？"},
    {"role": "user", "content": "如何学习 Python"},
    {"role": "assistant", "content": "学习 Python 可以从基础语法开始..."},
    {"role": "user", "content": "谢谢"}
]

user_count = 0
assistant_count = 0
total_length = 0
longest_msg = ""

for msg in messages:
    content = msg["content"]
    
    if msg["role"] == "user":
        user_count += 1
    elif msg["role"] == "assistant":
        assistant_count += 1
    
    total_length += len(content)
    
    if len(content) > len(longest_msg):
        longest_msg = content

avg_length = total_length / len(messages) if messages else 0

print("=== 消息统计 ===")
print(f"用户消息: {user_count} 条")
print(f"助手消息: {assistant_count} 条")
print(f"平均长度: {avg_length:.1f} 字符")
print(f"最长消息: {longest_msg}")
```

输出：

```
=== 消息统计 ===
用户消息: 3 条
助手消息: 2 条
平均长度: 10.0 字符
最长消息: 学习 Python 可以从基础语法开始...
```

------

## 