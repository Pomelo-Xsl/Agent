# day6-00Python基础-函数与模块

## 学习目标

- 定义和调用函数，实现代码复用
- 理解参数传递（位置参数、关键字参数、默认参数）
- 使用返回值获取函数执行结果
- 理解变量作用域（局部、全局）
- 使用 lambda 表达式创建简单函数
- 导入和使用标准库模块
- 创建自定义模块并在多文件项目中使用
- 使用 pip 管理第三方包

---

## 函数

函数是把重复使用的代码封装起来，给它一个名字，需要时调用。

### 为什么需要函数

没有函数时，代码会重复：

```python
# 计算三次 token 费用
tokens1 = 1000
cost1 = (tokens1 / 1000) * 0.03
print(f"费用1: ${cost1:.4f}")

tokens2 = 1500
cost2 = (tokens2 / 1000) * 0.03
print(f"费用2: ${cost2:.4f}")

tokens3 = 2000
cost3 = (tokens3 / 1000) * 0.03
print(f"费用3: ${cost3:.4f}")
```

有了函数，代码简洁：

```python
def calculate_cost(tokens):
    """计算 token 费用"""
    return (tokens / 1000) * 0.03

print(f"费用1: ${calculate_cost(1000):.4f}")
print(f"费用2: ${calculate_cost(1500):.4f}")
print(f"费用3: ${calculate_cost(2000):.4f}")
```

输出：

```
费用1: $0.0300
费用2: $0.0450
费用3: $0.0600
```

### 函数定义

**基本语法：**

```python
def 函数名(参数1, 参数2):
    """函数说明文档（可选）"""
    # 函数体
    return 返回值
```

**示例：**

```python
def greet(name):
    """向用户打招呼"""
    message = f"你好，{name}！"
    return message

result = greet("小明")
print(result)  # 你好，小明！
```

**函数命名规范：**

- 使用小写字母和下划线
- 名字要表达函数的功能
- 动词开头：`get_user_info()`、`calculate_cost()`、`build_prompt()`

**函数说明文档（docstring）：**

三引号字符串，写在函数开头，说明函数的功能。

```python
def calculate_cost(tokens, price_per_1k=0.03):
    """
    计算 token 费用
    
    参数:
        tokens: token 数量
        price_per_1k: 每 1K tokens 的价格，默认 0.03
    
    返回:
        float: 总费用
    """
    return (tokens / 1000) * price_per_1k
```

### 参数传递

**位置参数**

按照顺序传递参数。

```python
def build_message(role, content):
    return {"role": role, "content": content}

msg = build_message("user", "你好")
print(msg)  # {'role': 'user', 'content': '你好'}
```

**关键字参数**

使用参数名传递，不依赖顺序。

```python
msg = build_message(content="你好", role="user")
print(msg)  # {'role': 'user', 'content': '你好'}
```

**默认参数**

参数可以有默认值，调用时可以不传。

```python
def call_api(model="gpt-3.5-turbo", temperature=0.7):
    """调用 AI 模型"""
    print(f"模型: {model}, 温度: {temperature}")

call_api()                              # 使用默认值
call_api("gpt-4")                       # 只改 model
call_api(temperature=0.9)               # 只改 temperature
call_api("gpt-4", 0.9)                  # 全部指定
```

输出：

```
模型: gpt-3.5-turbo, 温度: 0.7
模型: gpt-4, 温度: 0.7
模型: gpt-3.5-turbo, 温度: 0.9
模型: gpt-4, 温度: 0.9
```

**注意：默认参数必须放在位置参数后面**

```python
# 错误
def func(a=1, b):  # SyntaxError
    pass

# 正确
def func(b, a=1):
    pass
```

### 位置参数和关键字参数

1. `*args`：接收**不定长位置参数**，打包为**元组 (tuple)**，名字`args`可以自定义（如`*nums`），`*`是核心
2. `**kwargs`：接收**不定长关键字参数**，打包为**字典 (dict)**，名字`kwargs`可自定义，`**`是核心
3. 作用：函数参数弹性适配，不用固定参数个数，常用于工具封装、装饰器、函数传参转发

### 案例 1：用 *args 不定长位置参数求和

```python
def sum_all(*args):
    # args 是元组类型
    print("接收的位置参数元组：", args, type(args))
    total = 0
    for num in args:
        total += num
    return total

# 调用测试，传任意多个数字
print(sum_all(1, 2))
print(sum_all(10, 20, 30, 40))
print(sum_all())  # 不传参数返回0
```

```
接收的位置参数元组： (1, 2) <class 'tuple'>
3
接收的位置参数元组： (10, 20, 30, 40) <class 'tuple'>
100
接收的位置参数元组： () <class 'tuple'>
0
```

### 解包使用 `*`

把列表 / 元组打散成位置参数传入函数

```
nums = [5, 6, 7]
print(sum_all(*nums))  # 等价 sum_all(5,6,7)
```

### 案例 2：用 **kwargs 不定长关键字参数打印信息

```python
def show_user(**kwargs):
    # kwargs 是字典
    print("关键字参数字典：", kwargs, type(kwargs))
    for k, v in kwargs.items():
        print(f"{k}: {v}")

# 任意键值对调用
show_user(name="张三", age=22, gender="男")
show_user(name="李四", phone="13800138000")
show_user()
```

```
关键字参数字典： {'name': '张三', 'age': 22, 'gender': '男'} <class 'dict'>
name: 张三
age: 22
gender: 男
关键字参数字典： {'name': '李四', 'phone': '13800138000'} <class 'dict'>
name: 李四
phone: 13800138000
关键字参数字典： {} <class 'dict'>
```

### 字典解包 `**`

```
user_info = {"name": "王五", "height": 180}
show_user(**user_info)  # 打散字典为关键字参数
```



### 案例 3：`*args` + `**kwargs` 混合使用（最常用组合）

### 参数顺序硬性规则（必须遵守）

固定参数 → `*args``**kwargs` 错误写法：

```python
def order_info(order_id, *goods, **extra):
    print(f"订单号：{order_id}")
    print("购买商品：", goods)
    print("额外备注：", extra)
    print("-" * 30)

# 调用
order_info(1001, "手机", "耳机", address="杭州市", pay="支付宝")
order_info(1002, "键盘", time="2026-08-03")
```

### 返回值

**return 的作用：**

1. 返回结果给调用者
2. 结束函数执行

```python
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8
```

**没有 return 时返回 None**

```python
def print_hello():
    print("Hello")

result = print_hello()
print(result)  # None
```

**多返回值**

实际上是返回一个元组。

```python
def get_model_info():
    name = "gpt-4"
    price = 0.03
    max_tokens = 8192
    return name, price, max_tokens  # 返回元组

model, price, tokens = get_model_info()  # 元组解包
print(f"{model}: ${price}, {tokens} tokens")
```

输出：

```
gpt-4: $0.03, 8192 tokens
```

**提前返回**

用于简化逻辑。

```python
def validate_temperature(temp):
    """验证温度参数"""
    if temp < 0 or temp > 2:
        return False  # 提前返回
    return True

print(validate_temperature(0.7))  # True
print(validate_temperature(3.0))  # False
```

### AI 场景示例

```python
def build_prompt(system_msg, user_msg):
    """构造完整的 prompt"""
    return f"[System]\n{system_msg}\n\n[User]\n{user_msg}"

def count_tokens(text):
    """简单的 token 估算（字符数 ÷ 4）"""
    return len(text) // 4

def estimate_cost(text, price_per_1k=0.03):
    """估算文本的费用"""
    tokens = count_tokens(text)
    cost = (tokens / 1000) * price_per_1k
    return tokens, cost

# 使用函数
system = "你是一个 Python 助手"
user = "如何读取文件？"
prompt = build_prompt(system, user)

tokens, cost = estimate_cost(prompt)
print(f"Prompt:\n{prompt}")
print(f"\nToken 数: {tokens}")
print(f"预估费用: ${cost:.4f}")
```

### 课堂练习

**消息构造器**

编写函数 `create_message(role, content)`，返回消息字典。
编写函数 `add_message(messages, role, content)`，向消息列表添加消息。

参考答案：

```python
def create_message(role, content):
    """创建消息字典"""
    return {"role": role, "content": content}

def add_message(messages, role, content):
    """向消息列表添加消息"""
    msg = create_message(role, content)
    messages.append(msg)

# 测试
messages = []
add_message(messages, "system", "你是助手")
add_message(messages, "user", "你好")
add_message(messages, "assistant", "你好！")

for msg in messages:
    print(f"[{msg['role']}] {msg['content']}")
```

输出：

```
[system] 你是助手
[user] 你好
[assistant] 你好！
```

---

## 变量作用域

变量的作用域决定了它在哪里可以被访问。

### 局部变量

在函数内部定义的变量，只能在函数内部使用。

```python
def calculate():
    result = 100  # 局部变量
    print(result)

calculate()  # 100
# print(result)  # NameError: name 'result' is not defined
```

### 全局变量

在函数外部定义的变量，可以在函数内部读取。

```python
MODEL = "gpt-4"  # 全局变量

def get_model():
    print(MODEL)  # 可以读取全局变量

get_model()  # gpt-4
```

### 修改全局变量

如果要在函数内修改全局变量，需要使用 `global` 关键字。

```python
count = 0  # 全局变量

def increment():
    global count  # 声明要修改全局变量
    count += 1

increment()
increment()
print(count)  # 2
```

**但不推荐这样做**，容易导致代码混乱。更好的方式是通过参数和返回值：

```python
count = 0

def increment(n):
    """返回递增后的值"""
    return n + 1

count = increment(count)
count = increment(count)
print(count)  # 2
#注意: 本质上没有修改全局变量的值, 只是用函数的返回值给全局变量重新赋值了. 
```

### 作用域规则（LEGB）就近原则

Python 查找变量的顺序：
1. **L**ocal（局部）：函数内部,   访问外层函数, 需要nonlocal, 访问全局变量, global
2. **E**nclosing（外层）：嵌套函数的外层
3. **G**lobal（全局）：模块级别
4. **B**uilt-in（内置）：Python 内置.

```python
x = "global"  # 全局

def outer():
    x = "outer"  # 外层
    
    def inner():
        x = "inner"  # 局部
        print(x)
    
    inner()
    print(x)

outer()
print(x)
```

输出：

```
inner
outer
global
```

---

## lambda 表达式

lambda 是创建简单函数的快捷方式，适合一次性使用的简单函数。

### 基本语法

```python
lambda 参数: 表达式
```

**普通函数：**

```python
def add(a, b):
    return a + b

print(add(3, 5))  # 8
```

**lambda 表达式：**

```python
add = lambda a, b: a + b
print(add(3, 5))  # 8
```

### 使用场景

**1. 作为参数传递**

```python
# 对列表排序
models = [
    {"name": "gpt-3.5", "price": 0.002},
    {"name": "gpt-4", "price": 0.03},
    {"name": "claude", "price": 0.015}
]

# 按价格排序
models.sort(key=lambda x: x["price"])  #原地排序

for m in models:
    print(f"{m['name']}: ${m['price']}")
    
解释:    
lambda x: x["price"] 排序规则说明
x：代表列表里每一个字典元素，循环遍历 models 每一项
x["price"]：取出当前字典的价格数值，sort 会拿着这个数值做大小对比
等价于普通函数写法（lambda 简写）：

def get_price(item):
    return item["price"]

models.sort(key=get_price)
```

输出：

```
gpt-3.5: $0.002
claude: $0.015
gpt-4: $0.03
```

**2. 简单的数据转换**

```python

map(function, iterable, *iterables)
function：函数（可以普通函数、lambda）
iterable：可迭代对象（列表、元组、字符串等）
返回值：map 对象（迭代器），不能直接打印看到内容，一般转成 list()

案例: 
nums = [1,2,3,4]

def double(x):
    return x * 2


res = map(double, nums)
print(res)        # <map object at ...>
print(list(res))  # [2, 4, 6, 8]

#搭配lambda表达式使用
nums = [1,2,3,4]
res = list(map(lambda x: x*2, nums))
print(res)  # [2, 4, 6, 8]
```



```python
# 将列表中的字符串转为大写
words = ["hello", "world", "python"]
upper_words = list(map(lambda x: x.upper(), words))
print(upper_words)  # ['HELLO', 'WORLD', 'PYTHON']

# 过滤偶数
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
print(evens)  # [2, 4, 6]
```

**注意：**
- lambda 只能包含一个表达式
- 不能包含多行语句, 如果函数体有有多条语句, 那么只能使用普通函数. 
- 不能包含 if-elif-else（但可以用三元运算符）
- 复杂逻辑用普通函数

```python
# lambda 中使用三元表达式
get_grade = lambda score: "及格" if score >= 60 else "不及格"
print(get_grade(75))  # 及格
print(get_grade(45))  # 不及格
```

---

## 闭包

闭包是 Python 高级特性之一，允许函数嵌套中内层函数访问外层函数的变量，即使外层函数已执行完毕。核心价值是数据封装和状态保留。

数据封装: 内存函数可以访问到外层函数的变量. 即使外层函数已经执行完毕了.  原因: 内存函数保留了外层函数变量的引用. 

状态保留: 就是多个内层函数执行的结果互不影响.

### 闭包的构成条件

1. 外层函数内定义内层函数, 函数嵌套
2. 内层函数引用外层函数的变量（非全局变量）
3. 外层函数返回内层函数对象

闭包理解案例：

```python
# 构建闭包
def linear(a, b):
  def inner(x):
    return a * x + b

  return inner

y1 = linear(1, 2)
print(y1) 
print(y1(5)) 
```

### 课堂案例:闭包实战案例

#### 案例 1：计数器（状态保留）

```python
def counter():
    count = 0  # 外层函数变量（被闭包保留）
    def increment():
        nonlocal count  # 声明使用外层变量
        count += 1
        return count
    return increment

# 创建闭包实例
c1 = counter()
print(c1())  # 输出：1
print(c1())  # 输出：2
print(c1())  # 输出：3

# 多个闭包实例相互独立
c2 = counter()
print(c2())  # 输出：1（不影响c1的状态）
```

#### 案例 2：配置型函数（数据封装）

函数的参数是配置,返回一个函数.

```python
# 外层函数,为内层函数提供了倍数因子配置项
def make_multiplier(factor):
    """创建乘法器函数（闭包封装因子）"""
    # 内存函数提供了乘法操作
    def multiply(num):
        return num * factor
    return multiply

# 创建不同因子的乘法器
double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))  # 输出：10
print(triple(5))  # 输出：15
```

###  闭包的注意事项

1. 闭包会保留外层变量的引用，可能导致内存占用（避免保留大对象）

2. 外层变量若为可变类型（列表、字典），无需`nonlocal`即可修改

   ```python
   def outer():
       lst = []
       def inner(item):
           lst.append(item)  # 可变类型无需nonlocal
           return lst
       return inner
   
   add_item = outer()
   print(add_item(1))  # 输出：[1]
   print(add_item(2))  # 输出：[1, 2]
   ```

## 装饰器

装饰器是 Python 中动态增强函数 / 类功能的高级语法，基于闭包实现，核心优势是不修改原始代码即可扩展功能，符合 "开放 - 封闭" 原则。

装饰器是本质:**接收函数作为参数,返回一个新函数**。在不修改原函数源代码,不改动调用方式的前提下,给函数新增前置/后置逻辑功能.(日志/计时/权限校验/缓存/异常捕获)

### 为什么需要装饰器

在 AI 开发中经常需要：
- 记录函数调用日志.
- 重试失败的 API 调用
- 缓存结果
- 计算函数执行时间,  

装饰器让这些功能可以复用，不用重复写代码。

### 函数是对象

在 Python 中，函数也是对象，可以作为参数传递。

```python
def greet():
    return "Hello"

# 函数赋值给变量
func = greet
print(func())  # Hello

# 函数作为参数
def call_function(f):
    return f()

print(call_function(greet))  # Hello
```

### 基础装饰器

**最简单的装饰器：** 基于闭包, 函数也是对象

```python
def my_decorator(func):
    """装饰器函数"""
    def wrapper():
        print("函数执行前")
        result = func()  # 调用原函数
        print("函数执行后")
        return result
    return wrapper

# 使用装饰器
@my_decorator
def say_hello():
    print("Hello!")
    return "完成"

# 调用
say_hello()

@my_decorator代码等价于: 
wrapper =  my_decorator(say_hello)  
wrapper()
```

输出：
```
函数执行前
Hello!
函数执行后
```

### 带参数的装饰器

**装饰有参数的函数：**

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):  # 接收任意参数
        print(f"调用函数: {func.__name__}")
        print(f"参数: args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"返回值: {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

@log_decorator
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

# 使用
add(3, 5)
greet("Alice", greeting="Hi")

*args 参数
	作用：接收任意数量的位置参数（positional arguments）
	特点：将传入的位置参数收集为一个元组（tuple）
	使用场景：当不确定函数会接收多少个位置参数时使用
**kwargs 参数
	作用：接收任意数量的关键字参数（keyword arguments）
	特点：将传入的关键字参数收集为一个字典（dictionary）
	使用场景：当不确定函数会接收多少个关键字参数时使用
```

输出：
```
调用函数: add
参数: args=(3, 5), kwargs={}
返回值: 8
调用函数: greet
参数: args=('Alice',), kwargs={'greeting': 'Hi'}
返回值: Hi, Alice!
```

### 带参数的装饰器本身

需要额外一层函数接收参数，实现装饰器的灵活配置：

```python
def retry(max_attempts=3):
    """重试装饰器"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"尝试 {attempt + 1} 失败: {e}")
                    if attempt == max_attempts - 1:
                        raise
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_api_call():
    """模拟不稳定的 API 调用"""
    import random
    if random.random() < 0.7:
        raise ValueError("API 调用失败")
    return "成功"

# 使用
result = unstable_api_call()
print(result)
```

### AI 场景示例

**1. API 重试装饰器**

```python
import time

def retry_on_failure(max_attempts=3, delay=1):
    """API 调用失败时重试"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"第 {attempt + 1} 次失败: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                    else:
                        raise
        return wrapper
    return decorator

@retry_on_failure(max_attempts=3, delay=2)
def call_openai_api(prompt):
    """调用 OpenAI API"""
    # 模拟 API 调用
    import random
    if random.random() < 0.5:
        raise ConnectionError("网络错误")
    return "AI 的回复"

# 使用
response = call_openai_api("你好")
print(response)
```

**2. 计时装饰器**(统计函数执行消耗的时间)

```python
import time

def timer(func):
    """计算函数执行时间"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} 执行时间: {end - start:.2f} 秒")
        return result
    return wrapper

@timer
def process_large_text(text):
    """处理大文本 chunk """
    time.sleep(1)  # 模拟耗时操作
    return len(text)

# 使用
process_large_text("长文本" * 1000)
```

**3. 多个装饰器组合**

```python
@retry_on_failure(max_attempts=3)
@timer
def call_ai_with_retry(prompt):
    """带重试和计时的 API 调用"""
    # 模拟 API 调用
    time.sleep(0.5)
    return "AI 回复"

# 执行顺序：retry -> timer -> 函数本身
result = call_ai_with_retry("你好")
```

### 课堂练习(作业)

**日志装饰器**

创建一个装饰器，记录函数的调用信息。

参考答案：

```python
import logging

logging.basicConfig(level=logging.INFO)

def log_calls(func):
    """记录函数调用日志"""
    def wrapper(*args, **kwargs):
        logging.info(f"调用 {func.__name__}，参数: {args}, {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"{func.__name__} 返回: {result}")
        return result
    return wrapper

@log_calls
def send_message(role, content):
    """发送消息"""
    return {"role": role, "content": content}

# 测试
msg = send_message("user", "你好")
```

输出：
```
INFO:root:调用 send_message，参数: ('user', '你好'), {}
INFO:root:send_message 返回: {'role': 'user', 'content': '你好'}
```

---

**缓存结果：**

```python
def cache(func):
    """缓存函数结果"""
    cached = {}
    
    def wrapper(*args):
        if args not in cached:
            cached[args] = func(*args)
        return cached[args]
    return wrapper

@cache
def expensive_computation(n):
    """耗时计算"""
    print(f"计算 {n}...")
    time.sleep(1)
    return n * n

# 第一次调用：计算
print(expensive_computation(5))  # 计算 5...  25

# 第二次调用：从缓存读取
print(expensive_computation(5))  # 25（直接返回，不打印"计算"）
```



## 模块与导入

模块是包含 Python 代码的 `.py` 文件，可以被其他文件导入使用。

### 为什么需要模块

随着项目变大，把所有代码写在一个文件会很混乱。模块帮助我们：
- 组织代码
- 避免重复
- 便于维护
- 便于团队协作

### 导入标准库模块

Python 自带了很多有用的模块（标准库），可以直接导入使用。

**import 模块名**

```python
import math  # 导入 math 模块

print(math.pi)         # 3.141592653589793
print(math.sqrt(16))   # 4.0
print(math.ceil(3.2))  # 4（向上取整）
print(math.floor(3.8)) # 3（向下取整）
```

**from 模块 import 函数**

只导入需要的部分。

```python
from math import pi, sqrt

print(pi)       # 3.141592653589793
print(sqrt(16)) # 4.0
# print(math.pi)  # NameError: name 'math' is not defined
```

**import 模块 as 别名**

给模块起个短名字。

```python
import datetime as dt

now = dt.datetime.now()  # 使用别名 dt
print(now)
```

### 常用标准库模块

**os - 操作系统相关**

```python
import os

# 获取环境变量
api_key = os.getenv("OPENAI_API_KEY")
print(api_key)


# 获取环境变量
maven_home = os.getenv("MAVEN_HOME")
print(maven_home)

# 获取当前工作目录
print(os.getcwd())

```

**json - JSON 处理** 和python当中的字典高度重合.

```python
import json

# Python 字典转 JSON 字符串
data = {"name": "gpt-4", "price": 0.03}
json_str = json.dumps(data)
print(json_str)  # {"name": "gpt-4", "price": 0.03}

# JSON 字符串转 Python 字典
obj = json.loads(json_str)
print(obj["name"])  # gpt-4
```

**datetime - 日期时间处理**

datetime 模块用于处理日期和时间，在 AI 开发中非常常用。

```python
from datetime import datetime, timedelta   # 第一个datetime模块名称, 第二个 datetime 是类名称

# 获取当前时间
now = datetime.now()
print(now)  # 2024-06-11 15:30:45.123456

# 格式化输出
print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2024-06-11 15:30:45

# ISO 格式（API 常用）
print(now.isoformat())  # 2024-06-11T15:30:45.123456

# 创建指定时间
specific_time = datetime(2024, 6, 11, 15, 30, 0)
print(specific_time)

# 时间计算
tomorrow = now + timedelta(days=1)
one_hour_ago = now - timedelta(hours=1)
print(f"明天: {tomorrow}")
print(f"一小时前: {one_hour_ago}")

# 解析时间字符串
time_str = "2024-06-11 15:30:00"
parsed_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
print(parsed_time)
```

**常用格式化代码：**

- `%Y` - 4位年份（2024）
- `%m` - 2位月份（01-12）
- `%d` - 2位日期（01-31）
- `%H` - 24小时制小时（00-23）
- `%M` - 分钟（00-59）
- `%S` - 秒（00-59）

**time - 时间相关**

```python
import time

# 暂停执行
print("开始")
time.sleep(2)  # 暂停 2 秒
print("结束")

# 获取时间戳
timestamp = time.time()
print(timestamp)  # 1718096445.123456

# 计算执行时间
start = time.time()
# 执行一些操作
time.sleep(1)
end = time.time()
print(f"耗时: {end - start:.2f} 秒")
```

**random - 随机数**

```python
import random

# 随机整数
print(random.randint(1, 10))  # 1-10 之间的随机整数

# 随机选择
models = ["gpt-3.5", "gpt-4", "claude"]
print(random.choice(models))


"""
 random.random() 随机生成一个0-1之间的小数
"""
for i in range(1,101):
    print(random.random())

# 打乱列表
random.shuffle(models)
print(models)
```

---

## 自定义模块(重点)

### 创建模块

创建一个文件就是创建一个模块。

**示例：创建 `utils.py`**

```python
# utils.py
"""工具函数模块"""

def count_tokens(text):
    """估算 token 数量"""
    return len(text) // 4

def calculate_cost(tokens, price_per_1k=0.03):
    """计算费用"""
    return (tokens / 1000) * price_per_1k

# 模块级常量
DEFAULT_MODEL = "gpt-3.5-turbo"
```

**在其他文件中导入**

```python
# main.py
import utils

text = "这是一段测试文本"
tokens = utils.count_tokens(text)
cost = utils.calculate_cost(tokens)

print(f"Token 数: {tokens}")
print(f"费用: ${cost:.4f}")
print(f"默认模型: {utils.DEFAULT_MODEL}")
```

**或者只导入需要的函数**

```python
# main.py
from utils import count_tokens, calculate_cost

text = "这是一段测试文本"
tokens = count_tokens(text)
cost = calculate_cost(tokens)
print(f"Token 数: {tokens}, 费用: ${cost:.4f}")
```

### `__name__ == "__main__"`

这是 Python 中最常见的代码模式，用于区分模块是被导入还是直接运行。

#### 为什么需要这个判断

在 Python 中，每个模块都有一个内置变量 `__name__`：
- 当模块被**直接运行**时，`__name__` 的值是 `"__main__"`
- 当模块被**导入**时，`__name__` 的值是模块名（文件名）

这个机制让我们可以：
- 在模块中写测试代码
- 既能作为模块被导入，又能独立运行测试

#### 基础示例

```python
# utils.py
def count_tokens(text):
    """计算token数"""
    return len(text) // 4

def build_prompt(system, user):
    """构建prompt"""
    return f"[System]\n{system}\n\n[User]\n{user}"

# 这部分代码只在直接运行 utils.py 时执行
if __name__ == "__main__":
    print("=== 测试工具函数 ===")
    
    # 测试 count_tokens
    test_text = "Hello Python World"
    tokens = count_tokens(test_text)
    print(f"Token数: {tokens}")
    
    # 测试 build_prompt
    prompt = build_prompt("你是助手", "你好")
    print(f"\nPrompt:\n{prompt}")
```

**运行方式1：直接运行**
```bash
python utils.py
```
输出：
```
=== 测试工具函数 ===
Token数: 4
Prompt:
[System]
你是助手

[User]
你好
```

**运行方式2：被导入**
```python
# main.py
import utils

# 只导入函数，测试代码不会执行
tokens = utils.count_tokens("Hello")
print(tokens)  # 1
```

#### AI 场景示例

```python
# message.py
"""消息管理模块"""

def create_message(role, content):
    """创建消息字典"""
    return {"role": role, "content": content}

def add_message(messages, role, content):
    """向消息列表添加消息"""
    msg = create_message(role, content)
    messages.append(msg)

def print_messages(messages):
    """打印所有消息"""
    for msg in messages:
        print(f"[{msg['role']}] {msg['content']}")

# 测试代码：只在直接运行时执行
if __name__ == "__main__":
    print("=== 测试消息管理模块 ===\n")
    
    # 创建测试消息列表
    messages = []
    add_message(messages, "system", "你是一个Python助手")
    add_message(messages, "user", "如何读取文件？")
    add_message(messages, "assistant", "使用open()函数...")
    
    # 打印消息
    print_messages(messages)
    
    # 统计
    print(f"\n总消息数: {len(messages)}")
```

#### 常见使用场景

**1. 模块测试**
```python
# api_client.py
def call_api(prompt):
    """调用API（实际项目中）"""
    # 实际API调用代码
    pass

if __name__ == "__main__":
    # 测试API调用
    result = call_api("测试prompt")
    print(result)
```

**2. 命令行工具**
```python
# tool.py
def process_file(filename):
    """处理文件"""
    with open(filename) as f:
        return f.read()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        result = process_file(filename)
        print(result)
    else:
        print("用法: python tool.py <文件名>")
```

**3. 示例代码**
```python
# config.py
API_KEY = "your-api-key"
MODEL = "gpt-3.5-turbo"

if __name__ == "__main__":
    # 显示配置示例
    print("配置示例:")
    print(f"API_KEY: {API_KEY}")
    print(f"MODEL: {MODEL}")
```

#### 课堂练习

为 Day3 早期创建的工具函数添加测试代码。

参考答案：

```python
# token_utils.py
"""Token 计算工具"""

def count_tokens(text):
    """估算token数"""
    return len(text) // 4

def estimate_cost(text, price_per_1k=0.03):
    """估算费用"""
    tokens = count_tokens(text)
    return (tokens / 1000) * price_per_1k

if __name__ == "__main__":
    print("=== Token 工具测试 ===\n")
    
    # 测试数据
    test_texts = [
        "Hello",
        "这是一段测试文本",
        "Python is awesome!" * 10
    ]
    
    for text in test_texts:
        tokens = count_tokens(text)
        cost = estimate_cost(text)
        print(f"文本: {text[:20]}...")
        print(f"Token数: {tokens}")
        print(f"预估费用: ${cost:.4f}\n")
```

## 包管理

### 什么是包（Package）

当项目更大时，可以用文件夹组织模块，这个文件夹就叫"包"。

```
my_project/
├── main.py
└── ai_tools/          # 包
    ├── __init__.py    # 必须有这个文件，可以是空的. 此时ai_tools才是包
    ├── prompt.py
    └── message.py
```

**导入包中的模块**

```python
# main.py
from ai_tools import prompt
from ai_tools import message

# 或
from ai_tools.prompt import build_prompt
from ai_tools.message import create_message
```

### pip - 包管理工具

pip 是 Python 的包管理工具，用于安装第三方库。

**安装包**

```bash
pip install requests
```

**查看已安装的包**

```bash
pip list
```

**卸载包**

```bash
pip uninstall requests
```

**安装指定版本**

```bash
pip install requests==2.28.0
```

### requirements.txt

用于记录项目依赖，方便在其他环境安装。

**生成 requirements.txt**

```bash
pip freeze > requirements.txt
```

**内容示例：**

```
requests==2.28.0
python-dotenv==1.0.0
```

**安装依赖**

```bash
pip install -r requirements.txt
```

---

## 今日总结

### 核心知识点回顾

**1. 函数**
- 使用 `def` 定义函数
- 参数：位置参数(*args)、关键字参数(**kwargs)、默认参数
- 返回值：使用 `return`，可以返回多个值（元组）
- 函数的作用：代码复用、逻辑封装

**2. 变量作用域**

- 局部变量：函数内部定义
- 全局变量：函数外部定义
- 避免在函数内修改全局变量, global修饰 
- LEGB:访问  就近原则. 访问函数内容, 访问外层函数(nonlocal) ,访问全局(global), 内置

**3. lambda 表达式**

- 语法：`lambda 参数: 表达式`

- 适合简单的一次性函数

- 常用于排序(sort)、过滤(filter)、映射(map). 

  初学者: 可读性不高.
  [ 闭包/ 装饰器]

**4. 模块**

- 标准库：直接 `import` 使用
- 自定义模块：创建 `.py` 文件
- `__name__ == "__main__"` 判断是否直接运行

**5. 包管理**

- pip：安装、卸载第三方包
- requirements.txt：记录项目依赖

  

### 函数设计原则

1. **单一职责**：一个函数只做一件事
2. **参数适量**：不要超过 5 个参数
3. **命名清晰**：函数名表达功能
4. **避免副作用**：尽量通过返回值而不是修改全局变量
5. **添加文档**：复杂函数写 docstring

### 常见问题

**Q：什么时候应该把代码封装成函数？**
A：当一段代码需要重复使用，或者逻辑独立、可以单独命名时。

**Q：参数传递是值传递还是引用传递？** 
A：Python 中都是"传对象引用"。对于不可变类型（int、str、tuple），表现像值传递；对于可变类型（list、dict），修改会影响原对象。

java当中: 值传递, 引用传递. 



python当中数据类型: 

不可变对象:  str, typle,int, float ,  表面上看, 都是值传递.

可变对象: list dict . 引用传递.



**Q：为什么要用虚拟环境？**
A：避免不同项目的依赖冲突。项目 A 用 requests 2.28，项目 B 用 requests 3.0，没有虚拟环境会冲突。

**Q：import 和 from import 有什么区别？**
A：`import module` 导入整个模块，使用时要加模块名；`from module import func` 只导入特定内容，使用时直接用。

**Q：什么时候用 lambda，什么时候用普通函数？**
A：简单的一次性操作用 lambda（如排序的 key 函数），复杂逻辑或需要重用的用普通函数。

### 重点注意事项

1. **默认参数的陷阱**：不要用可变对象（list、dict）作为默认参数
   
   ```python
   # 错误
   def add_item(item, lst=[]):  # 默认参数是可变对象
       lst.append(item)
       return lst
   
   # 正确
   def add_item(item, lst=None):
       if lst is None:
           lst = []
       lst.append(item)
       return lst
```
   
2. **模块导入顺序**：标准库(python提供的内置库) → 第三方库(pip安装) → 自定义模块
   
   ```python
   import os
   import json
   import requests
   from utils import count_tokens
   ```
   
3. **避免循环导入**：A 导入 B，B 又导入 A，会报错

4. **函数返回值**：如果函数没有明确返回值，返回 None

## 当天作业

### 工具函数库(作业)

创建一个 `ai_utils.py` 模块，包含以下函数：

- `count_tokens(text)` - 估算 token 数
- `calculate_cost(tokens, price_per_1k)` - 计算费用
- `truncate_text(text, max_length)` - 截断文本到指定长度
- `format_messages(messages)` - 格式化消息列表为字符串

然后在 `main.py` 中导入并测试。

参考答案：

```python
# ai_utils.py
"""AI 工具函数库"""

def count_tokens(text):
    """估算 token 数量（字符数 ÷ 4）"""
    return len(text) // 4

def calculate_cost(tokens, price_per_1k=0.03):
    """计算费用"""
    return (tokens / 1000) * price_per_1k

def truncate_text(text, max_length):
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_messages(messages):
    """格式化消息列表"""
    result = []
    for msg in messages:
        line = f"[{msg['role']}] {msg['content']}"
        result.append(line)
    return "\n".join(result)  # join() 将列表元素用换行符连接

if __name__ == "__main__":
    # 测试代码
    print("测试 count_tokens:")
    print(count_tokens("Hello Python"))
    
    print("\n测试 calculate_cost:")
    print(f"${calculate_cost(1000):.4f}")
    
    print("\n测试 truncate_text:")
    print(truncate_text("这是一段很长的文本", 5))
```

```python
# main.py
"""主程序"""

from ai_utils import count_tokens, calculate_cost, format_messages

messages = [
    {"role": "system", "content": "你是助手"},
    {"role": "user", "content": "你好"},
    {"role": "assistant", "content": "你好！有什么可以帮你？"}
]

# 格式化输出
print("=== 消息列表 ===")
print(format_messages(messages))

# 统计 token
total_text = " ".join([msg["content"] for msg in messages])
tokens = count_tokens(total_text)
cost = calculate_cost(tokens)

print(f"\n=== 统计 ===")
print(f"总 Token 数: {tokens}")
print(f"预估费用: ${cost:.4f}")
```

输出：

```
=== 消息列表 ===
[system] 你是助手
[user] 你好
[assistant] 你好！有什么可以帮你？

=== 统计 ===
总 Token 数: 7
预估费用: $0.0002
```

### Prompt 构造器模块

创建 `prompt_builder.py` 模块，实现以下功能：

- `build_system_prompt(role_desc)` - 构造系统 prompt
- `build_user_prompt(task, context)` - 构造用户 prompt
- `build_full_prompt(system, user)` - 组合完整 prompt

参考答案：

```python
# prompt_builder.py
"""Prompt 构造器"""

def build_system_prompt(role_desc):
    """构造系统 prompt"""
    return f"你是一个{role_desc}。请按照要求回答问题。"

def build_user_prompt(task, context=""):
    """构造用户 prompt"""
    if context:
        return f"背景信息：{context}\n\n任务：{task}"
    return f"任务：{task}"

def build_full_prompt(system, user):
    """组合完整 prompt"""
    return f"[System]\n{system}\n\n[User]\n{user}"

if __name__ == "__main__":
    # 测试
    system = build_system_prompt("Python 编程助手")
    user = build_user_prompt("解释什么是函数", "初学者正在学习 Python")
    full = build_full_prompt(system, user)
    print(full)
```

输出：

```
[System]
你是一个Python 编程助手。请按照要求回答问题。

[User]
背景信息：初学者正在学习 Python

任务：解释什么是函数
```

### 消息管理器

创建一个完整的消息管理模块 `message_manager.py`，包含：

- 创建消息
- 添加消息
- 获取最近 N 条消息
- 统计各角色消息数量

参考答案：

```python
# message_manager.py
"""消息管理器"""

def create_message(role, content):
    """创建消息"""
    return {"role": role, "content": content}

def add_message(messages, role, content):
    """添加消息"""
    msg = create_message(role, content)
    messages.append(msg)
    return messages

def get_recent_messages(messages, n=5):
    """获取最近 N 条消息"""
    return messages[-n:]  # 负索引切片，取最后 n 个

def count_by_role(messages):
    """统计各角色消息数量"""
    counts = {}
    for msg in messages:
        role = msg["role"]
        counts[role] = counts.get(role, 0) + 1
    return counts

def filter_by_role(messages, role):
    """筛选指定角色的消息"""
    return [msg for msg in messages if msg["role"] == role]

if __name__ == "__main__":
    # 测试
    messages = []
    add_message(messages, "system", "你是助手")
    add_message(messages, "user", "你好")
    add_message(messages, "assistant", "你好！")
    add_message(messages, "user", "天气如何")
    add_message(messages, "assistant", "今天天气不错")
    
    print("最近 3 条消息:")
    for msg in get_recent_messages(messages, 3):
        print(f"  [{msg['role']}] {msg['content']}")
    
    print("\n消息统计:")
    counts = count_by_role(messages)
    for role, count in counts.items():
        print(f"  {role}: {count} 条")
```

输出：

```
最近 3 条消息:
  [user] 天气如何
  [assistant] 今天天气不错
  
消息统计:
  system: 1 条
  user: 2 条
  assistant: 2 条
```

### 配置管理器

创建 `config.py` 存储项目配置，`main.py` 读取并使用。

参考答案：

```python
# config.py
"""项目配置"""

# 模型配置
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_TEMPERATURE = 0.7
MAX_TOKENS = 2000

# 价格配置（每 1K tokens）
PRICING = {
    "gpt-3.5-turbo": 0.002,
    "gpt-4": 0.03,
    "claude-3": 0.015
}

# 系统消息
SYSTEM_MESSAGES = {
    "helper": "你是一个有帮助的AI助手",
    "coder": "你是一个专业的编程助手",
    "translator": "你是一个专业的翻译助手"
}

def get_price(model):
    """获取模型价格"""
    return PRICING.get(model, 0.03)  # 默认 0.03

def get_system_message(role):
    """获取系统消息"""
    return SYSTEM_MESSAGES.get(role, SYSTEM_MESSAGES["helper"])
```

```python
# main.py
"""主程序"""

import config

def show_config():
    print("=== 当前配置 ===")
    print(f"默认模型: {config.DEFAULT_MODEL}")
    print(f"温度: {config.DEFAULT_TEMPERATURE}")
    print(f"最大 tokens: {config.MAX_TOKENS}")
    
    print("\n=== 价格表 ===")
    for model, price in config.PRICING.items():
        print(f"{model}: ${price}/1K tokens")
    
    print("\n=== 系统消息 ===")
    for role in ["helper", "coder", "translator"]:
        msg = config.get_system_message(role)
        print(f"{role}: {msg}")

if __name__ == "__main__":
    show_config()
```

输出：

```
=== 当前配置 ===
默认模型: gpt-3.5-turbo
温度: 0.7
最大 tokens: 2000

=== 价格表 ===
gpt-3.5-turbo: $0.002/1K tokens
gpt-4: $0.03/1K tokens
claude-3: $0.015/1K tokens

=== 系统消息 ===
helper: 你是一个有帮助的AI助手
coder: 你是一个专业的编程助手
translator: 你是一个专业的翻译助手
```

