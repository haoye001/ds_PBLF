# DeepSeek 智能会议助手 - Code Wiki

## 目录
1. [项目概述](#项目概述)
2. [项目架构](#项目架构)
3. [核心模块说明](#核心模块说明)
4. [关键类与函数](#关键类与函数)
5. [依赖关系](#依赖关系)
6. [项目运行方式](#项目运行方式)
7. [数据流与交互流程](#数据流与交互流程)
8. [扩展开发指南](#扩展开发指南)

---

## 项目概述

### 项目简介
DeepSeek 智能会议助手是一个基于 DeepSeek API 的智能会议室管理与会议辅助系统，支持会议室查询、预约、取消、会议总结等功能。

### 核心功能
- ✅ **意图识别**：精准识别用户的自然语言意图
- ✅ **会议预约**：智能解析时间、人数、会议室信息
- ✅ **状态管理**：实时会议室状态同步
- ✅ **会议总结**：AI 生成专业会议纪要
- ✅ **多轮对话**：支持上下文连续对话
- ✅ **用户管理**：管理员和普通用户角色分离
- ✅ **AI 性格切换**：多种助手性格模式

### 技术栈
- **Web 框架**：Streamlit
- **AI 服务**：DeepSeek API (OpenAI 兼容)
- **数据处理**：Pandas
- **可视化**：Plotly
- **环境管理**：python-dotenv

---

## 项目架构

### 整体架构图
```
deepseek_meeting_assistant/
├── app/
│   ├── backend/          # 后端业务逻辑层
│   │   ├── ai_service.py     # AI 服务模块
│   │   ├── data_manager.py   # 数据管理模块
│   │   ├── chat_manager.py   # 聊天历史管理
│   │   └── __init__.py
│   ├── frontend/         # 前端界面层
│   │   ├── login_page.py     # 登录页面
│   │   ├── admin_panel.py    # 管理员面板
│   │   ├── meeting_page.py   # 会议页面
│   │   └── __init__.py
│   └── main.py           # 主入口文件
├── requirements.txt      # 项目依赖
└── README.md
```

### 设计模式
项目采用 **MVC (Model-View-Controller)** 架构模式：
- **Model (模型层)**：[app/backend/](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/) - 负责业务逻辑和数据处理
- **View (视图层)**：[app/frontend/](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/frontend/) - 负责界面展示和用户交互
- **Controller (控制层)**：[app/main.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/main.py) - 协调前后端交互

---

## 核心模块说明

### 1. 后端模块 (app/backend/)

#### ai_service.py - AI 服务模块
**职责**：处理与 DeepSeek API 的交互，包括意图识别和会议总结生成

**核心功能**：
- 意图识别：解析用户自然语言输入，识别查询、预约、取消、总结等意图
- 会议总结：根据会议记录生成结构化的会议纪要

#### data_manager.py - 数据管理模块
**职责**：管理会议室和用户数据

**核心功能**：
- 会议室管理：状态查询、更新、修改
- 用户管理：登录验证、用户增删改查

#### chat_manager.py - 聊天历史管理
**职责**：管理多轮对话的历史记录

**核心功能**：
- 添加消息到历史记录
- 获取历史记录（支持限制数量）
- 清空历史记录

### 2. 前端模块 (app/frontend/)

#### login_page.py - 登录页面
**职责**：处理用户登录流程，包含验证码验证

**核心功能**：
- 用户角色选择（管理员/普通用户）
- 用户名密码输入
- 验证码生成与验证

#### admin_panel.py - 管理员面板
**职责**：提供管理员专属功能界面

**核心功能**：
- 修改会议记录
- 用户管理（查看、添加、修改、删除）

#### meeting_page.py - 会议页面
**职责**：主界面展示，包含聊天界面和侧边栏

**核心功能**：
- 多轮对话界面
- 会议室状态展示
- AI 性格切换
- 会议总结生成与导出

### 3. 主入口 (app/main.py)
**职责**：整合前后端模块，控制应用流程

**核心功能**：
- 初始化会话状态
- 登录验证流程
- 意图处理与响应生成
- 界面布局协调

---

## 关键类与函数

### 后端模块

#### MeetingRoom 类 (data_manager.py)
会议室管理类

```python
class MeetingRoom:
    def __init__(self)
    def get_room_status(self, room_name)
    def update_room_status(self, room_name, status, booking_info=None)
    def get_all_rooms(self)
    def modify_room(self, room_name, status=None, capacity=None, equipment=None, new_booking=None)
```

**成员变量**：
- `meeting_rooms`：字典，存储所有会议室信息

**方法说明**：
| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `__init__` | 无 | 无 | 初始化 3 个默认会议室 |
| `get_room_status` | `room_name` (str) | dict/None | 获取指定会议室状态 |
| `update_room_status` | `room_name`, `status`, `booking_info` | bool | 更新会议室状态和预约信息 |
| `get_all_rooms` | 无 | dict | 获取所有会议室 |
| `modify_room` | `room_name`, `status`, `capacity`, `equipment`, `new_booking` | bool | 完整修改会议室信息 |

---

#### UserManager 类 (data_manager.py)
用户管理类

```python
class UserManager:
    def __init__(self)
    def login(self, username, password, role)
    def get_user(self, username)
    def get_all_users(self)
    def add_user(self, username, password, name, role)
    def update_user(self, username, name=None, password=None, role=None)
    def delete_user(self, username)
```

**成员变量**：
- `users`：字典，存储用户信息

**默认用户**：
| 用户名 | 密码 | 角色 | 姓名 |
|--------|------|------|------|
| admin | admin123 | admin | 管理员 |
| user1 | user123 | user | 张三 |
| user2 | user123 | user | 李四 |

**方法说明**：
| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `login` | `username`, `password`, `role` | dict/None | 验证用户登录信息 |
| `add_user` | `username`, `password`, `name`, `role` | bool | 添加新用户 |
| `update_user` | `username`, `name`, `password`, `role` | bool | 更新用户信息 |
| `delete_user` | `username` | bool | 删除用户（admin 不可删除） |

---

#### ChatHistory 类 (chat_manager.py)
聊天历史管理类

```python
class ChatHistory:
    def __init__(self)
    def add_message(self, user_input, ai_response)
    def get_history(self, limit=None)
    def clear(self)
    def to_dict(self)
```

**成员变量**：
- `chat_history`：列表，存储聊天记录

**方法说明**：
| 方法名 | 参数 | 返回值 | 描述 |
|--------|------|--------|------|
| `add_message` | `user_input`, `ai_response` | 无 | 添加消息到历史 |
| `get_history` | `limit` (int, optional) | list | 获取历史记录 |
| `clear` | 无 | 无 | 清空历史记录 |

---

#### recognize_intent 函数 (ai_service.py)
意图识别函数

```python
def recognize_intent(user_input, context=None)
```

**参数**：
- `user_input` (str)：用户输入文本
- `context` (list, optional)：对话上下文

**返回值**：dict
```json
{
  "intent": "query|book|cancel|summarize|unknown|error",
  "time": "时间信息",
  "participants": 人数,
  "room": "会议室名称",
  "topic": "会议主题"
}
```

**意图类型**：
- `query`：查询会议室状态
- `book`：预约会议室
- `cancel`：取消预约
- `summarize`：总结会议
- `unknown`：未知意图
- `error`：处理错误

---

#### generate_meeting_summary 函数 (ai_service.py)
会议总结生成函数

```python
def generate_meeting_summary(meeting_notes, topic=None)
```

**参数**：
- `meeting_notes` (str)：会议记录内容
- `topic` (str, optional)：会议主题

**返回值**：str - 格式化的会议纪要（Markdown 格式）

---

### 前端模块

#### show_login_page 函数 (login_page.py)
显示登录页面

```python
def show_login_page()
```

**返回值**：tuple `(username, password, role)`

---

#### show_admin_panel 函数 (admin_panel.py)
显示管理员面板侧边栏

```python
def show_admin_panel()
```

---

#### show_edit_meetings 函数 (admin_panel.py)
显示修改会议记录界面

```python
def show_edit_meetings(meeting_room_manager)
```

**参数**：
- `meeting_room_manager` (MeetingRoom)：会议室管理实例

---

#### show_manage_users 函数 (admin_panel.py)
显示用户管理界面

```python
def show_manage_users(user_manager)
```

**参数**：
- `user_manager` (UserManager)：用户管理实例

---

#### show_chat_interface 函数 (meeting_page.py)
显示聊天界面

```python
def show_chat_interface(chat_history, meeting_room_manager, recognize_intent_func)
```

**参数**：
- `chat_history` (list)：聊天历史记录
- `meeting_room_manager` (MeetingRoom)：会议室管理实例
- `recognize_intent_func` (function)：意图识别函数

**返回值**：tuple `(clear_chat, process_input, user_input)`

---

#### show_right_sidebar 函数 (meeting_page.py)
显示右侧侧边栏

```python
def show_right_sidebar(meeting_room_manager, generate_summary_func)
```

**参数**：
- `meeting_room_manager` (MeetingRoom)：会议室管理实例
- `generate_summary_func` (function)：总结生成函数

---

### 主入口模块

#### init_session_state 函数 (main.py)
初始化会话状态

```python
def init_session_state()
```

**初始化的会话状态**：
- `meeting_room_manager`：会议室管理实例
- `user_manager`：用户管理实例
- `chat_history`：聊天历史实例
- `current_user`：当前登录用户
- `admin_mode`：管理员模式
- `current_summary`：当前会议总结

---

#### main 函数 (main.py)
主程序入口

```python
def main()
```

**流程**：
1. 初始化会话状态
2. 检查登录状态
3. 显示登录页面或主界面
4. 处理用户输入和意图
5. 生成响应并更新界面

---

## 依赖关系

### 外部依赖 (requirements.txt)

| 包名 | 版本要求 | 用途 |
|------|----------|------|
| openai | >=1.0.0 | DeepSeek API 调用（兼容 OpenAI SDK） |
| streamlit | >=1.28.0 | Web 应用框架 |
| pandas | >=1.5.0 | 数据处理 |
| plotly | >=5.0.0 | 数据可视化 |
| python-dotenv | >=1.0.0 | 环境变量管理 |

### 模块依赖关系图

```
main.py
├── backend/
│   ├── ai_service.py
│   │   ├── openai
│   │   └── python-dotenv
│   ├── data_manager.py
│   └── chat_manager.py
└── frontend/
    ├── login_page.py
    ├── admin_panel.py
    └── meeting_page.py
        └── streamlit
```

---

## 项目运行方式

### 环境配置

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 配置 API Key
创建 `.env` 文件：
```env
DEEPSEEK_API_KEY=your_api_key_here
```

#### 3. 运行应用
```bash
streamlit run app/main.py
```

### 部署方式

#### 本地开发
- 直接运行上述命令即可
- 访问：http://localhost:8501

#### 云服务器部署
1. 上传项目到服务器
2. 安装依赖
3. 配置 API Key
4. 运行应用
5. 开放 8501 端口
6. 访问：http://your-server-ip:8501

---

## 数据流与交互流程

### 登录流程
```
用户输入 → show_login_page() → UserManager.login() 
→ 验证成功 → 存储 current_user → 跳转主界面
```

### 意图识别与处理流程
```
用户输入 
  → recognize_intent() (调用 DeepSeek API)
  → 解析意图类型
    ├─ query → 查询会议室状态
    ├─ book → 更新会议室状态
    ├─ cancel → 取消预约
    ├─ summarize → 提示上传文件
    └─ unknown → 友好提示
  → 添加到 chat_history
  → 刷新界面
```

### 会议总结生成流程
```
用户上传文件 
  → 读取文件内容
  → generate_meeting_summary() (调用 DeepSeek API)
  → 显示总结
  → 支持下载导出
```

---

## 扩展开发指南

### 添加新的意图类型
1. 修改 [ai_service.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/ai_service.py#L13-L38) 中的 `SYSTEM_PROMPT`，添加新的意图说明
2. 在 [main.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/main.py#L91-L123) 中添加对应的处理逻辑

### 添加新的会议室
修改 [data_manager.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/data_manager.py#L24-L29) 中 `MeetingRoom.__init__` 方法

### 添加新的前端页面
1. 在 [app/frontend/](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/frontend/) 目录下创建新文件
2. 在 `__init__.py` 中导出
3. 在 [main.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/main.py) 中导入并使用

### 配置 DeepSeek API
确保 `.env` 文件中正确配置了 API Key，Base URL 已设置为 `https://api.deepseek.com`

---

## 关键文件速查表

| 文件 | 主要内容 |
|------|----------|
| [app/main.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/main.py) | 主程序入口，协调整个应用 |
| [app/backend/ai_service.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/ai_service.py) | AI 意图识别和会议总结 |
| [app/backend/data_manager.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/data_manager.py) | 会议室和用户数据管理 |
| [app/backend/chat_manager.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/backend/chat_manager.py) | 聊天历史管理 |
| [app/frontend/login_page.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/frontend/login_page.py) | 登录页面 |
| [app/frontend/admin_panel.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/frontend/admin_panel.py) | 管理员功能 |
| [app/frontend/meeting_page.py](file:///d:/Desktop/deepseek/deepseek_meeting_assistant/app/frontend/meeting_page.py) | 主会议界面 |
