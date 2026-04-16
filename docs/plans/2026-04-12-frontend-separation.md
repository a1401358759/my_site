# Django + React 前后端分离改造 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在保持现有数据模型不变的前提下，为博客提供面向 React 前端的 API，并创建一个响应式、简约、现代化的新前端页面。

**Architecture:** 后端继续使用 Django 单体服务，新增 `/api/mysite/v1/*` 聚合接口作为 BFF 层。前端在独立目录使用 React + Vite 构建，通过 HTTP 调用 Django API 获取文章、侧栏、轮播与详情数据。页面采用单列内容 + 右侧信息区（移动端折叠为纵向）实现简洁布局。

**Tech Stack:** Django 3.x, MySQL, Redis, React 18, Vite 5, React Router, 原生 CSS variables。

### Task 1: 梳理现有数据结构并定义 API 输出字段

**Files:**
- Modify: `api/views.py`
- Modify: `api/forms.py`

**Step 1: 定义文章列表/详情序列化函数**

在 `api/views.py` 中新增私有函数，统一输出字段（id、标题、作者、分类、标签、时间、阅读量、摘要等）。

**Step 2: 定义首页聚合查询参数表单**

在 `api/forms.py` 增加 `HomeFeedForm`，包含 `keyword/tag/classification/page_num/page_size`。

**Step 3: 运行基础检查**

Run: `python3 manage.py check`
Expected: `System check identified no issues`。

### Task 2: 新增前后端分离 API

**Files:**
- Modify: `api/views.py`
- Modify: `api/urls.py`

**Step 1: 新增首页聚合接口**

新增 `home_feed`，返回：文章分页、热门文章、分类统计、标签统计、归档统计、banner、ads、友链。

**Step 2: 新增文章详情接口**

新增 `article_detail`，返回文章完整内容、上下篇、更新时间间隔等。

**Step 3: 注册路由**

在 `api/urls.py` 增加：
- `/api/mysite/v1/home/`
- `/api/mysite/v1/articles/<int:article_id>/`

**Step 4: 运行检查**

Run: `python3 manage.py check`
Expected: `System check identified no issues`。

### Task 3: 创建独立 React 前端项目

**Files:**
- Create: `/Users/yangxuefeng/work/my_site_frontend/*`

**Step 1: 初始化 Vite React 项目**

Run: `npm create vite@latest my_site_frontend -- --template react`

**Step 2: 安装依赖**

Run: `npm install && npm install react-router-dom`

**Step 3: 编写 API 层与页面结构**

新增 `src/api/client.js` 与 `src/api/blog.js`，封装对 Django API 的调用；新增首页与详情页组件。

**Step 4: 编写响应式样式**

在 `src/styles.css` 中定义统一变量、卡片网格、移动端断点与交互动效。

### Task 4: 联调与构建验证

**Files:**
- Modify: `/Users/yangxuefeng/work/my_site_frontend/src/*`

**Step 1: 本地联调默认 API 地址**

默认使用 `http://127.0.0.1:8000`（可由 `VITE_API_BASE_URL` 覆盖）。

**Step 2: 前端构建验证**

Run: `npm run build`
Expected: 构建成功并输出 `dist/`。

**Step 3: 后端检查**

Run: `python3 manage.py check`
Expected: 无配置错误。

### Task 5: 交付说明

**Files:**
- Modify: `README.md`（可选）

**Step 1: 说明 API 用法与前端启动方式**

给出后端运行、前端运行、环境变量、核心接口说明。

**Step 2: 输出完整表结构字段说明**

覆盖所有业务表（Author、Article、Tag、Classification、Links、CarouselImg、Music、OwnerMessage、Subscription、Visitor、Comments）及继承字段。
