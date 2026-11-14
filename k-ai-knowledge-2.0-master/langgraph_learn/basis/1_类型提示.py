# 变量类型提示就是给变量值加上类型说明
num: int = 100
num = '你好啊'  # Expected type 'int', got 'str' instead
num = [10, 20, 30]  # Expected type 'int', got 'list[int]' instead
print(num)

price: float = 12.5
message: int = 'hello'  # Expected type 'int', got 'str' instead
is_male: bool = True
result: None = None
result = 1  # Expected type 'None', got 'int' instead

# 注意：可以先写变量的类型注解，以后再赋值
school: str  # 注意，这里只是声明你这个变量的类型，但是没有真正地创建变量
# print(school)  # NameError: name 'school' is not defined
school = 'qinghua'

# hobbies 是列表，并且列表中的所有元素必须是 str 类型
# hobbies: list[str] = ['爱好A', '爱好B', '爱好C']
# hobbies: list = ['爱好A', '爱好B', '爱好C']  # 限制是列表，但是里面的元素类型不限制
# hobbies.append('学习 AI')
# print(hobbies)
# hobbies.append(100)
# print(hobbies)

# hobbies 是列表,并且列表中的元素，可以是：str 或 int 类型
hobbies: list[str | int] = ['爱好A', '爱好B', '爱好C']
hobbies.append(100)
