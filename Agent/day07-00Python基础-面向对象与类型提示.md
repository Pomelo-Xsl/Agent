# day6-01Python基础-面向对象与类型提示

## 学习目标

- 理解类和对象的概念
- 定义类、创建实例、使用方法(实例方法,类方法,静态方法)
- 添加类型提示提高代码可读性
- 使用 dataclass 简化数据类
- 使用 Pydantic 进行数据验证
- 从环境变量读取配置

---

## 面向对象编程基础

### 为什么需要面向对象

函数式编程处理简单任务很方便，但当数据和操作复杂时，面向对象能更好地组织代码。



**函数式：**

```python
# 管理用户
users = []

def add_user(name, email):
    users.append({"name": name, "email": email})

def get_user(name):
    for user in users:
        if user["name"] == name:
            return user
        
函数式编程 可以解决问题,复杂业务一级复杂数据处理,不推荐全部使用函数式编程. 
```

**面向对象：**
```python
class User:
    def __init__(self, name1, email2): #this关键字
        self.name = name1
        self.email = email2

# 数据和操作封装在一起
user = User("Alice", "alice@example.com")
print(user.name)
print(user.email)
```

### 类和对象

**类（Class）**：是对象的模板，定义了对象的属性和行为(方法)
**对象（Object）**：类的实例，实际存在的数据.

类比：
- 类 = 图纸（建筑设计图）
- 对象 = 建筑物（根据图纸建造的房子）

### 定义类

**基本语法：**

```python
# 直接定义在类当中,称之为方法.定义在类外的,称之为函数. 
    
class ClassName:
    """类的说明文档"""
    
    def __init__(self, param1, param2):
        """初始化方法（构造函数）"""
        self.attr1 = param1
        self.attr2 = param2
    
    def method1(self):
        """实例方法"""
        return self.attr1
```

**示例：**

```python
class Message:
    """消息类"""
    
    def __init__(self, role, content):
        self.role = role
        self.content = content
    
    def format(self):
        """格式化输出"""
        return f"[{self.role}] {self.content}"
    
    def token_count(self):
        """估算 token 数"""
        return len(self.content) // 4

# 创建对象
msg = Message("user", "你好")
print(msg.format())  # [user] 你好
print(msg.token_count())  # 0
```

### `__init__` 和 self

**`__init__`**：初始化方法，创建对象时自动调用, 等价于Java当中的构造器. 
**self**：指向对象本身，类似其他语言的 this.  self 调用方法的时候会被自动传入,不需要手动指定.

```python
class AIModel:
    def __init__(self, name, temperature=0.7):
        self.name = name
        self.temperature = temperature
    
    def describe(self):
        # self 指向当前对象
        return f"模型 {self.name}，温度 {self.temperature}"

# 创建对象
model1 = AIModel("gpt-4")
model2 = AIModel("claude-3", 0.9)

print(model1.describe())  # 模型 gpt-4，温度 0.7
print(model2.describe())  # 模型 claude-3，温度 0.9
```

### 实例方法、类方法、静态方法

**实例方法**：最常用，访问实例属性

```python
class Calculator:
    def add(self, a, b):
        return a + b
```

**类方法**：访问类属性，用 `@classmethod` 装饰

```python
class AIModel:
    model_count = 0  # 类属性
    
    def __init__(self, name):
        self.name = name
        AIModel.model_count += 1
    
    @classmethod
    def get_count(cls):
        return cls.model_count

# 使用
model1 = AIModel("gpt-4")
model2 = AIModel("claude-3")
print(AIModel.get_count())  # 2
```

**静态方法**：不访问类或实例属性，用 `@staticmethod` 装饰

```python
class TokenUtils:
    @staticmethod
    def estimate_tokens(text):
        return len(text) // 4
    
    @staticmethod
    def calculate_cost(tokens, price_per_1k):
        return (tokens / 1000) * price_per_1k

# 使用（不需要创建对象）
tokens = TokenUtils.estimate_tokens("Hello World")
cost = TokenUtils.calculate_cost(tokens, 0.03)
```

### AI 场景示例

```python
class ChatMessage:
    """对话消息类"""
    
    def __init__(self, role, content):
        self.role = role
        self.content = content
    
    def to_dict(self):
        """转为字典（API 格式）"""
        return {"role": self.role, "content": self.content}
    
    def token_count(self):
        """估算 token 数"""
        return len(self.content) // 4

class ChatSession:
    """对话会话类"""
    
    def __init__(self, system_prompt=""):
        self.messages = []
        if system_prompt:
            self.add_message("system", system_prompt)
    
    def add_message(self, role, content):
        """添加消息"""
        msg = ChatMessage(role, content)
        self.messages.append(msg)
    
    def get_messages(self):
        """获取所有消息（字典格式）"""
        return [msg.to_dict() for msg in self.messages]
    
    def total_tokens(self):
        """计算总 token 数"""
        return sum(msg.token_count() for msg in self.messages)

# 使用
session = ChatSession("你是一个Python助手")
session.add_message("user", "什么是类？")
session.add_message("assistant", "类是面向对象编程的基础")

print(f"消息数: {len(session.messages)}")
print(f"总 tokens: {session.total_tokens()}")
print(session.get_messages())
```

输出：
```
消息数: 3
总 tokens: 9
[{'role': 'system', 'content': '你是一个Python助手'}, {'role': 'user', 'content': '什么是类？'}, {'role': 'assistant', 'content': '类是面向对象编程的基础'}]
```

### 课堂练习(作业)

**模型配置类**

创建一个 `AIModelConfig` 类，管理模型配置。

参考答案：

```python
class AIModelConfig:
    """AI 模型配置类"""
    
    def __init__(self, model="gpt-3.5-turbo", temperature=0.7, max_tokens=2000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def validate(self):
        """验证配置"""
        if not (0 <= self.temperature <= 2):
            return False, "温度必须在 0-2 之间"
        if self.max_tokens <= 0:
            return False, "max_tokens 必须大于 0"
        return True, "配置合法"
    
    def to_dict(self):
        """转为字典"""
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

# 测试
config = AIModelConfig("gpt-4", 0.7, 2000)
is_valid, message = config.validate()
print(f"验证结果: {message}")
print(f"配置: {config.to_dict()}")
```

输出：
```
验证结果: 配置合法
配置: {'model': 'gpt-4', 'temperature': 0.7, 'max_tokens': 2000}
```

---

## 继承

### 继承

继承让子类复用父类的代码，实现代码重用。

**基本语法：**

```python
# 父类
class Parent:
    def method1(self):
        return "Parent method"
# 子类
class Child(Parent):  # 继承 Parent
    #定义特有方法.
    def method2(self):
        return "Child method"
    

# 子类可以使用父类的方法
obj = Child()
print(obj.method1())  # Parent method
print(obj.method2())  # Child method
```

**重写父类方法：**

```python
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):  # 重写父类方法
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

dog = Dog()
cat = Cat()
print(dog.speak())  # Woof!
print(cat.speak())  # Meow!
```

**调用父类方法：**

```python
class BaseModel:
    def __init__(self, name):
        self.name = name

    def describe(self):
        return f"模型: {self.name}"


class GPTModel(BaseModel):
    def __init__(self, name, version):
        # super().__init__(name)  # 调用父类的 __init__
        BaseModel.__init__(self, name) #这种方式,需要传递self
        self.version = version

    def describe(self):
        #base_desc = super().describe()  # 调用父类的 describe
        base_desc = BaseModel.describe(self)
        return f"{base_desc}, 版本: {self.version}"


model = GPTModel("GPT", "4")
print(model.describe())  # 模型: GPT, 版本: 4
```

### AI 场景示例

```python
class BaseMessage:
    """基础消息类"""
    
    def __init__(self, content):
        self.content = content
    
    def token_count(self):
        return len(self.content) // 4
    
    def to_dict(self):
        raise NotImplementedError("子类必须实现 to_dict")

class UserMessage(BaseMessage):
    """用户消息"""
    
    def to_dict(self):
        return {"role": "user", "content": self.content}

class AssistantMessage(BaseMessage):
    """助手消息"""
    
    def __init__(self, content, model="gpt-4"):
        super().__init__(content)
        self.model = model
    
    def to_dict(self):
        return {
            "role": "assistant",
            "content": self.content,
            "model": self.model
        }

# 使用
user_msg = UserMessage("你好")
assistant_msg = AssistantMessage("你好！", "gpt-4")

print(user_msg.to_dict())
print(assistant_msg.to_dict())
print(f"用户消息 tokens: {user_msg.token_count()}")
```

---

### 多继承

java不能实现多继承的. python当中可以实现多继承.

一个子类继承多个父类，语法为 `class 子类名(父1, 父2, ...)`，方法查找顺序遵循 “从左到右、先子类后父类”。 

```python
class Car:
    """
	 定义汽车类
    """
    def __init__(self,brand,model,color,owner):
        self.brand = brand    # 品牌
        self.model = model    # 型号
        self.color = color    # 颜色
        self.__owner = owner    # 拥有者

    def start(self): #启动
        print(f"{self.brand}的{self.model}正在启动...")
    def run(self): # 运行
        print(f"{self.brand}的{self.model}正在行驶...")
    def stop(self):
        print(f"{self.brand}的{self.model}行驶停止...")
    def get_owner(self):
        return self.__owner[0:1] + "**"
    def charge(self):
        print(f"{self.brand}的{self.model}正在补充燃料...")

#定义类 华为智驾
class HuaweiAiDriving:
    """
    华为AI智能驾驶
    """
    def __init__(self,version="V1.0"):
        self.version = version

    def run(self):
        print(f"使用华为AI智能驾驶系统{self.version}正在行驶...")

#定义问界汽车,实现多继承
class WenjieCar(Car,HuaweiAiDriving):
    """
    问界汽车
    """
    #重写父类的init方法
    def __init__(self,brand,model,color,owner, version):
        # 调用父类的init方法
        #Car.__init__(self,brand,model,color,owner)
        #super()调用了第一个父类的init方法.
        super().__init__(brand,model,color,owner)
        #使用类名调用
        HuaweiAiDriving.__init__(self)
        self.version = version

    #重写父类的run方法
    def run(self):
        Car.run(self)
        HuaweiAiDriving.run(self)


if __name__ == "__main__":
    # 默认调用Car的init方法.
    wenjie = WenjieCar("华为","V1.0","蓝色","张三","V1.1")
    print(wenjie.__dict__)
    wenjie.start()
    wenjie.stop()
    wenjie.charge()
    print(wenjie.get_owner())
    # 调用重写后的run方法.
    print("---")
    wenjie.run()
```

### 方法的解析顺序

多继承时，通过 `类名.__mro__` 可查看方法查找顺序（先子类，再父类从左到右，最后 `object`）。

> 从结果也可以看出任何类的继承链最终都指向object，即object是所有类的父类
>
> ```python
> class A:
>     def func(self):
>         print("A")
> 
> class B(A):
>     def func(self):
>         print("B")
> 
> class C(A):
>     def func(self):
>         print("C")
> 
> class D(B, C):
>     pass
> 
> # 查看 MRO
> print(D.__mro__)  # 输出：(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
> 
> d = D()
> d.func()  # 输出：B（优先查找左父类 B）
> ```
>
> 

## 多态

多态是指同一方法在不同对象上表现出不同行为，核心是 “子类重写父类方法”，配合统一的调用接口，实现灵活扩展。

1. 父类定义统一接口；
2. 子类重写该接口，实现个性化逻辑；
3. 统一调用父类接口，自动适配不同子类对象。

### 标准多态

```python
# 父类（统一接口）
class Animal:
    def move(self):
        pass  # 父类仅定义接口，不实现具体逻辑

# 子类1：重写方法
class Dog(Animal):
    def move(self):
        print("狗跑")

# 子类2：重写方法
class Fish(Animal):
    def move(self):
        print("鱼游")

# 子类3：重写方法
class Bird(Animal):
    def move(self):
        print("鸟飞")

# 统一调用接口（多态核心：同一方法适配不同对象）
def animal_move(animal):
    animal.move()

# 传入不同子类对象
animal_move(Dog())   # 输出：狗跑
animal_move(Fish())  # 输出：鱼游
animal_move(Bird())  # 输出：鸟飞
```

### 鸭子多态

如果它走起来像鸭子、叫起来像鸭子，那它就是鸭子.

只要对象具备需要的方法 / 属性，就可以直接当成目标类型使用

```python
class Duck:
    def speak(self):
        print("嘎嘎嘎")

class Person:
    def speak(self):
        print("学人模仿鸭子叫")

class Dog:
    def bark(self):
        print("汪汪汪")

# 函数：只要能调用speak()就放行，不限制类型
def duck_call(animal):
    animal.speak()

duck_call(Duck())    # 正常
duck_call(Person())  # 正常，虽然不是鸭子类，但是有speak方法
# duck_call(Dog())  # 报错：Dog没有speak()，不符合“鸭子特征”
```



## 封装：私有属性与 `@property`

封装: 定义在方法内部,也是封装的一种体现.  

java当中封装:  private int age; setter | getter,

封装是面向对象的核心特性，通过隐藏内部实现细节，只暴露必要的接口。 案例: 定义了一个selt.age属性,现在age不能直接被外部访问,要想访问必须通过公共的接口来访问,这就是python当中的封装.

### 私有属性

Python 中使用下划线前缀表示私有：
- `_attribute`：单下划线，约定为"内部使用"（弱私有）
- `__attribute`：双下划线，名称改写机制（强私有）

```python
class APIClient:
    def __init__(self, api_key):
        self._api_key = api_key      # 单下划线：约定为私有
        self.__secret = "secret123"   # 双下划线：强私有, 等价与private
    
    def get_key_preview(self):
        return self._api_key[:10] + "..."

client = APIClient("sk-1234567890abcdefghij")
print(client._api_key)           # 可以访问，但不建议
# print(client.__secret)         # AttributeError（无法直接访问）
print(client.get_key_preview())  # sk-1234567...
```

**实际开发建议：**

- 使用单下划线 `_` 表示私有（Python 社区约定）

- 双下划线 `__` 很少使用（除非真的需要防止子类覆盖)

  

### 私有方法

```python
class Person:
    # 私有方法
    def __private_method(self):
        print("这是私有方法")

    # 公开方法调用私有方法
    def public_method(self):
        self.__private_method()

p = Person()
p.public_method()  # 输出：这是私有方法（通过公开接口调用）
p.__private_method()  # 报错：AttributeError（外部无法直接调用）

#添加类型直接访问:
p._Person__private_method()
```



### `@property` 装饰器

`@property` 装饰器可将方法伪装成属性，简化接口调用，同时支持读写控制。

主要功能:

- 简化访问：将方法调用变为属性访问，无需添加括号
- 数据封装：实现对私有属性的安全访问
- 动态计算：返回基于其他属性计算得出的值

设计优点:

- 简洁语法：提供更直观的 API
- 向后兼容：可以在不改变接口的情况下从简单属性转换为复杂计算
- 权限控制：配合 setter 和 deleter 实现访问控制

**基础用法：**

```python
class ChatSession:
    def __init__(self):
        self._messages = []
    
    @property
    def message_count(self):
        """消息数量（只读属性）"""
        return len(self._messages)
    
    def add_message(self, role, content):
        self._messages.append({"role": role, "content": content})

session = ChatSession()
session.add_message("user", "你好")
session.add_message("assistant", "你好！")

print(session.message_count)  # 2（像访问属性一样）
# session.message_count = 10  # AttributeError（只读，不能赋值）
```

**getter 和 setter：**

```python
class ModelConfig:
    def __init__(self, temperature=0.7):
        self._temperature = temperature
    
    @property
    def temperature(self):
        """获取温度参数"""
        return self._temperature
    
    @temperature.setter
    def temperature(self, value):
        """设置温度参数（带验证）"""
        if not 0 <= value <= 2:
            raise ValueError("temperature 必须在 0-2 之间")
        self._temperature = value

config = ModelConfig()
print(config.temperature)  # 0.7

config.temperature = 0.9   # 通过 setter 设置
print(config.temperature)  # 0.9

# config.temperature = 3.0  # ValueError: temperature 必须在 0-2 之间
```

注意: @property装饰的方法不要和变量重名，否则可能导致无限递归

```python
class Person:

    @property
    def name(self):
        return self.name

p = Person()
p.name # 报错：RecursionError: maximum recursion depth exceeded
```



### AI 场景示例

```python
class APIClient:
    """API 客户端"""
    
    def __init__(self, api_key):
        self._api_key = api_key
        self._request_count = 0
        self._total_tokens = 0
    
    @property
    def api_key(self):
        """显示 API Key 预览（隐藏真实值）"""
        if len(self._api_key) > 10:
            return self._api_key[:10] + "..." + self._api_key[-4:]
        return "***"
    
    @property
    def request_count(self):
        """请求次数（只读）"""
        return self._request_count
    
    @property
    def total_tokens(self):
        """总 token 数（只读）"""
        return self._total_tokens
    
    @property
    def average_tokens(self):
        """平均每次请求的 token 数（计算属性）"""
        if self._request_count == 0:
            return 0
        return self._total_tokens / self._request_count
    
    def call_api(self, prompt, tokens_used):
        """调用 API"""
        self._request_count += 1
        self._total_tokens += tokens_used
        return f"Response for: {prompt}"

# 使用
client = APIClient("sk-1234567890abcdefghijklmnop")
print(f"API Key: {client.api_key_preview}")  # sk-1234567...mnop

client.call_api("你好", 100)
client.call_api("天气", 150)

print(f"请求次数: {client.request_count}")      # 2
print(f"总tokens: {client.total_tokens}")       # 250
print(f"平均tokens: {client.average_tokens}")   # 125.0
```

### 使用场景

**1. 只读属性**

```python
class Message:
    def __init__(self, content):
        self._content = content
        self._timestamp = datetime.now()
    
    @property
    def timestamp(self):
        """时间戳（只读）"""
        return self._timestamp
    
    @property
    def content_preview(self):
        """内容预览（只读）"""
        return self._content[:50] + "..." if len(self._content) > 50 else self._content
```

**2. 计算属性**

```python
class TokenCounter:
    def __init__(self):
        self._input_tokens = 0
        self._output_tokens = 0
    
    @property
    def total_tokens(self):
        """总 tokens（计算得出）"""
        return self._input_tokens + self._output_tokens
    
    @property
    def cost(self):
        """费用（根据 tokens 计算）"""
        return (self._input_tokens * 0.002 + self._output_tokens * 0.004) / 1000
```

**3. 属性验证**

```python
class ChatConfig:
    def __init__(self):
        self._max_tokens = 2000
    
    @property
    def max_tokens(self):
        return self._max_tokens
    
    @max_tokens.setter
    def max_tokens(self, value):
        if not isinstance(value, int):
            raise TypeError("max_tokens 必须是整数")
        if value <= 0:
            raise ValueError("max_tokens 必须大于 0")
        if value > 4000:
            raise ValueError("max_tokens 不能超过 4000")
        self._max_tokens = value
```

### 课堂练习(作业)

**安全的 API 配置类**

创建一个配置类，使用私有属性和 @property 保护敏感信息。

参考答案：

```python
from datetime import datetime

class APIConfig:
    """API 配置类"""
    
    def __init__(self, api_key, model="gpt-3.5-turbo"):
        self._api_key = api_key
        self._model = model
        self._created_at = datetime.now()
    
    @property
    def api_key_masked(self):
        """返回隐藏的 API Key"""
        return "*" * (len(self._api_key) - 4) + self._api_key[-4:]
    
    @property
    def model(self):
        """模型名称"""
        return self._model
    
    @model.setter
    def model(self, value):
        """设置模型（带验证）"""
        allowed_models = ["gpt-3.5-turbo", "gpt-4", "claude-3"]
        if value not in allowed_models:
            raise ValueError(f"不支持的模型: {value}")
        self._model = value
    
    @property
    def age_seconds(self):
        """配置存在时长（秒）"""
        return (datetime.now() - self._created_at).total_seconds()

# 测试
config = APIConfig("sk-1234567890")
print(f"API Key: {config.api_key_masked}")  # **********7890
print(f"模型: {config.model}")               # gpt-3.5-turbo

config.model = "gpt-4"
print(f"新模型: {config.model}")             # gpt-4

# config.model = "unknown"  # ValueError: 不支持的模型
```

---

## 类型提示

类型提示让代码更易读、易维护，IDE 能提供更好的代码补全。

类型提示不会强制限制代码运行,Python依旧是动态语言,只是给编译器,阅读者看的标注. 

### 基础类型提示

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

# 变量类型提示
age: int = 25
name: str = "Alice"
is_active: bool = True
```

### 复杂类型提示

```python
from typing import List, Dict, Optional, Union, Any

# 列表, messages是一个列表类型. 列表当中的每个元素是 str 
def process_messages(messages: List[str]) -> int:
    return len(messages)

# 字典
def get_config() -> Dict[str, Any]:
    return {"model": "gpt-4", "temperature": 0.7}

# 可选值等价于Optional[Dict]= Union[Dict,None] 函数返回值有两种情况,字典Dict ,控制None,所以以后调用这个函数的时候,看到Optional就知道,拿到结果一定要判断空,直接取会报错
def find_user(name: str) -> Optional[Dict]:  
    # 可能返回字典或 None
    return {"name": name} if name else None

# 多种类型,Union[类型1,类型2,类型3...]：变量可以是括号里任意一种类型。
def format_value(value: Union[int, str, float]) -> str:
    return str(value)

注意: python3.10 简化写法, 可以使用 | 替代Union
    def test(x: int | str | float):
    pass
```

总结: 

`Optional` 就是**专门标记可能返回 None 的场景**，是业务最常用的注解；

`Union` 用于多类型兼容，多个确定类型任选其一；

类型提示只是标注，不阻断程序运行，主要用于规范代码、团队协作、IDE 提示；

空值场景优先用`Optional`，不要手写`Union[X, None]`。

### AI 场景示例

```python
from typing import List, Dict, Optional


class ChatAPI:
    """对话 API 类"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key: str = api_key
        self.model: str = model
    
    def send_message(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """发送消息（模拟）"""
        if not messages:
            return None
        
        # 模拟 API 调用
        return "这是 AI 的回复"
    
    def count_tokens(self, text: str) -> int:
        """计算 token 数"""
        return len(text) // 4

# 使用
api = ChatAPI("sk-xxx", "gpt-4")
messages = [
    {"role": "user", "content": "你好"}
]
response = api.send_message(messages)
print(response)
```

---

## dataclass

dataclass 是 Python 3.7+ 的特性，简化数据类的定义。 



### 基本用法

**传统方式：**

```python
class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content
    
    def __repr__(self):
        return f"Message(role={self.role}, content={self.content})"
    
    痛点:属性一多，__init__、__repr__、__eq__全部手写，维护麻烦、容易写错
```

**使用 dataclass：**

```python
from dataclasses import dataclass

@dataclass
class Message:
    role: str
    content: str

# 自动生成 __init__、__repr__, __eu__, __str__ 等方法
msg = Message("user", "你好")
print(msg)  # Message(role='user', content='你好')

解决: ：只定义字段，所有构造、打印、比较方法全部自动生成。
```

### 默认值和字段

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ModelConfig:
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    tags: List[str] = field(default_factory=list)  # 没创建一个实例,都会给当前这个实例分配一个[],不是多实例共享. default_factory 默认工厂.  只要是可变类型,都要field赋值.
    #tags: List[str] = [] #数据安全问题. 

config = ModelConfig()
print(config)

原因：Python 在类定义阶段就创建了空列表，所有实例共享同一个列表对象，A 实例修改列表，B 实例跟着变。
👉 解决方案：field(default_factory=list)，每次实例化时新建一个独立空列表。
```

### @dataclass核心参数

```python
@dataclass(
    init=True,       # 是否自动生成__init__，默认True
    repr=True,       # 是否自动生成__repr__，默认True, 等价与__str__
    eq=True,         # 是否自动生成__eq__等值判断，默认True
    order=False,     # 是否生成大小比较(__lt__,__gt__)，开启后可以 < > 对比对象
    frozen=False,    # 是否冻结（不可变对象），True之后属性不能修改
    kw_only=False,   # Python3.8+ 实例化只能用关键字传参.
)

frozen=True 冻结类（常量配置，禁止修改属性）
适合配置类、枚举类，防止运行时被意外篡改
kw_only=True 强制关键字传参，避免参数顺序传错. 位置传参容易出现问题. 
```



### AI 场景示例

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChatMessage:
    role: str
    content: str
    
    def token_count(self) -> int:
        return len(self.content) // 4

# xxxRequest 对象, 就是来封装前台提交的参数. 
@dataclass
class ChatRequest:
    model: str
    messages: List[ChatMessage]
    temperature: float = 0.7
    max_tokens: int = 2000
    stream: bool = False


# 使用
msg1 = ChatMessage("user", "你好")
msg2 = ChatMessage("assistant", "你好！")

request = ChatRequest(
    model="gpt-4",
    messages=[msg1, msg2]
)

print(request)
```

---

## Pydantic

Pydantic 是强大的数据验证库，常用于 API 开发和配置管理。

核心:BaseModel 

所有数据模型都要继承BaseMadel,等价于数据模板/实体类,对比之前手写Message类. 

手写类需要自己写 __init__, __repr__,手动类型判断.

Pydantic BaseModel 自动生成构造/自动校验/自动格式化输出,自带序列化

### 安装

```bash
pip install pydantic
```

### 基本用法

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    name: str
    age: int
    email: str

# 自动验证类型
user = User(name="Alice", age=25, email="alice@example.com")
print(user)
print(user.model_dump())  # 转为字典

# 类型错误会抛出异常
try:
    invalid_user = User(name="Bob", age="not a number", email="bob@example.com")
except Exception as e:
    print(f"验证失败: {e}")
```

### 字段验证

默认情况下,Pydantic只在实例创建的时候做参数校验.

开启 `validate_assignment=True`：

> **实例化之后，后续动态修改对象属性时，依然执行字段校验**

```python
from pydantic import BaseModel, Field

class ModelConfig(BaseModel):
    model: str = Field(..., description="模型名称") # ...参数表示当前属性必须,不能省略
    temperature: float = Field(0.7, ge=0, le=2, description="温度参数")
    max_tokens: int = Field(1024, gt=0, description="最大 token 数")
    
    class Config:
        # 配置
        validate_assignment = True  # 赋值时也验证,不开启的时候只有在创建实例的时候才校验

# 使用
config = ModelConfig(model="gpt-4", temperature=0.8)
print(config)

# 尝试设置非法值
try:
    config.temperature = 3.0  # 超出范围
except Exception as e:
    print(f"验证失败: {e}")
```

### AI 场景示例

```python
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str = Field(..., min_length=1)
    
    @validator('content')
    def content_not_empty(cls, v):
        if not v.strip():
            raise ValueError('内容不能为空')
        return v

class ChatRequest(BaseModel):
    model: str = Field(default="gpt-3.5-turbo")
    messages: List[ChatMessage] = Field(..., min_items=1)
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=2000, gt=0, le=4000)
    stream: bool = False

# 使用
try:
    request = ChatRequest(
        model="gpt-4",
        messages=[
            ChatMessage(role="user", content="你好")
        ],
        temperature=0.8
    )
    print(request.model_dump_json(indent=2))
except Exception as e:
    print(f"验证失败: {e}")
```

------

## 今日总结

### 核心知识点回顾

**1. 面向对象**

- 类和对象：类是模板，对象是实例
- `__init__`：初始化方法,创建对象的时候自动调用.
- self：指向对象本身, 类似与java当中this关键字. 不需要手动传入self
- 实例方法、类方法、静态方法(定义工具)

**2. 继承与多态**

- 继承：`class Child(Parent,Parent2)` python当中多继承. 底层父类Object
- 重写方法：子类定义同名方法
- super()：调用父类方法, 推荐
- 类名.方法名称()  可以调用父类的方法. 
- 多态: 标准多态, 父子类继承关系. 子类对父类方法的重写.
- 鸭子多态:  不要父子继承关系.

**3. 类型提示**

- 基础类型：int, str, float, bool
- 复杂类型：List, Dict, Optional, Union
- 函数注解：参数类型和返回值类型

**4. dataclass**

- @dataclass 装饰器, 装饰类的.
- 自动生成 `__init__`、`__repr__` 等 
- field()：处理可变默认值. 尤其注意 list 

**5. Pydantic**

- 第三方库,使用的时候必须pip isntall xxx 
- BaseModel：数据验证基类(父类), 提供__init__等一系列方法. 
- Field：字段约束
- validator：自定义验证器
- model_dump()：转为字典, 将对象转换成字典.

### Python vs Java 对比

| 特性      | Python                         | Java                            |
| --------- | ------------------------------ | ------------------------------- |
| 类定义    | `class Name:`                  | `class Name {}`                 |
| 构造函数  | `__init__(self, ...)`          | `Name(...)`                     |
| this/self | self（显式）必须在方法参数声明 | this（隐式）                    |
| 继承      | `class Child(Parent) 多继承`   | `class Child extends Parent` 单 |
| 类型提示  | 可选（typing）                 | 强制                            |
| 数据类    | @dataclass                     | record（Java 14+）              |

### 常见问题

**Q：什么时候用函数，什么时候用类？**
A：数据和操作紧密相关时用类；简单工具函数用函数。

**Q：self 是什么？**
A：指向当前对象的引用，类似 Java 的 this，但必须显式写出。

**Q：类型提示是强制的吗？**
A：python提供的类型提示不是强制的，Python 运行时不检查类型，但 IDE 和工具会用它提示错误。 

**Q：Pydantic 和 dataclass 的区别？**
A：dataclass 只是简化定义，Pydantic 还提供运行时验证。提供的类型验证必须满足的,否则提示错误信息. 

### 重点注意事项

1. **`__init__` 的 self**：第一个参数必须是 self

2. **可变默认值陷阱**：

   ```python
   # 错误
   def __init__(self, items=[]):
       self.items = items  # 所有实例共享同一个列表, 不要这样使用. A 实例和 B 共享一个列表, A修改了B会被影响到. 
   
   # 正确
   def __init__(self, items=None):
       self.items = items if items else []
   ```

```
   
3. **类型提示不影响运行**：写错了不会报错，只是 IDE 提示警告信息. 运行不报错.


## 当天作业

### AI 对话客户端

创建一个完整的 AI 对话客户端类。

参考答案：

​```python
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import json

load_dotenv()

class ChatMessage(BaseModel):
    """对话消息"""
    role: str = Field(..., pattern="^(system|user|assistant)$")
    content: str

class ChatConfig(BaseModel):
    """对话配置"""
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = "gpt-3.5-turbo"
    temperature: float = Field(0.7, ge=0, le=2)
    max_tokens: int = Field(2000, gt=0)

class AIChat:
    """AI 对话客户端"""
    
    def __init__(self, config: ChatConfig):
        self.config = config
        self.messages: List[ChatMessage] = []
        self.base_url = "https://api.openai.com/v1"
    
    def add_system_message(self, content: str):
        """添加系统消息"""
        msg = ChatMessage(role="system", content=content)
        self.messages.append(msg)
    
    def add_user_message(self, content: str):
        """添加用户消息"""
        msg = ChatMessage(role="user", content=content)
        self.messages.append(msg)
    
    def send(self) -> Optional[str]:
        """发送消息"""
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.config.model,
            "messages": [msg.model_dump() for msg in self.messages],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # 保存助手回复
            assistant_msg = ChatMessage(role="assistant", content=content)
            self.messages.append(assistant_msg)
            
            return content
        except Exception as e:
            print(f"API 调用失败: {e}")
            return None
    
    def get_history(self) -> List[Dict]:
        """获取对话历史"""
        return [msg.model_dump() for msg in self.messages]
    
    def save_history(self, filename: str):
        """保存对话历史"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.get_history(), f, ensure_ascii=False, indent=2)

# 使用
config = ChatConfig(
    api_key="sk-xxx",
    model="gpt-3.5-turbo",
    temperature=0.7
)

chat = AIChat(config)
chat.add_system_message("你是一个Python助手")
chat.add_user_message("什么是类？")

# 发送并获取回复
response = chat.send()
if response:
    print(f"AI: {response}")

# 保存历史
chat.save_history("chat_history.json")
```

------

