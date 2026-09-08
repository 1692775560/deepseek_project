<div align="center">

# 🤖 DeepSeek Project

**一站式 DeepSeek 实战项目合集：微信机器人 · 文档上传 · R1 本地部署 · 联网搜索插件**

*A collection of hands-on DeepSeek projects: WeChat bot, document upload, R1 local deployment & web search plugin.*

<p>
  <a href="https://github.com/1692775560/deepseek_project/stargazers"><img src="https://img.shields.io/github/stars/1692775560/deepseek_project?style=for-the-badge&logo=github&color=1f6feb" alt="Stars"></a>
  <a href="https://github.com/1692775560/deepseek_project/network/members"><img src="https://img.shields.io/github/forks/1692775560/deepseek_project?style=for-the-badge&logo=github&color=238636" alt="Forks"></a>
  <a href="https://github.com/1692775560/deepseek_project/issues"><img src="https://img.shields.io/github/issues/1692775560/deepseek_project?style=for-the-badge&logo=github&color=d29922" alt="Issues"></a>
  <img src="https://img.shields.io/github/last-commit/1692775560/deepseek_project?style=for-the-badge&logo=git&color=8957e5" alt="Last Commit">
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/DeepSeek-API-4D6BFE?style=for-the-badge&logo=openai&logoColor=white" alt="DeepSeek API">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen?style=for-the-badge" alt="PRs Welcome">
</p>

<p>
  <a href="#-项目矩阵">项目矩阵</a> •
  <a href="#-快速开始">快速开始</a> •
  <a href="#-star-历史">Star 历史</a> •
  <a href="#-贡献">贡献</a>
</p>

</div>

---

## 📦 项目矩阵

| 项目 | 说明 | 关键词 |
|:----:|:-----|:------|
| 🤖 [**we_chat_project**](./we_chat_project) | 对接 DeepSeek API 与微信接口的智能聊天机器人，支持自动化消息响应 | 微信机器人、多轮对话 |
| 📁 [**Document_upload_assistant**](./Document_upload_assistant) | 解决 DeepSeek 平台未开放文件上传 API 的本地化文件处理方案 | 文件解析、本地处理 |
| 🚀 [**deepseek_r1_deploy**](./deepseek_r1_deploy) | 基于魔搭社区快速部署 DeepSeek 蒸馏模型，服务器 / 本地均可运行，自带前端界面 | R1 部署、ModelScope |
| 🔍 [**LLM联网搜索插件**](./LLM联网搜索插件) | 为本地部署的大模型赋予联网搜索能力，支持 Google / Bing / 百度 | 联网搜索、LLM 插件 |

---

## 🚀 快速开始

<details open>
<summary><b>🤖 WeChat Assistant —— 微信智能聊天机器人</b></summary>

通过对接 DeepSeek API 与微信接口实现的智能聊天机器人，支持自动化消息响应。
*A WeChat chatbot integrated with DeepSeek's API for automated message replies.*

**核心功能**

- ✅ 微信消息实时监听
- ✅ DeepSeek 多轮对话接口调用
- ✅ 上下文敏感型回复生成
- ✅ 异常流量熔断机制

```bash
cd we_chat_project
pip install -r requirements.txt
```

</details>

<details>
<summary><b>📁 Document Upload Assistant —— 文档上传助手</b></summary>

为解决 DeepSeek 平台未开放文件上传 API 的技术限制，开发的本地化文件处理解决方案。
*Localized file processing solution addressing DeepSeek's lack of file upload API.*

```bash
cd Document_upload_assistant
pip install -r requirements.txt
```

</details>

<details>
<summary><b>🚀 DeepSeek R1 Deploy —— 蒸馏模型一键部署</b></summary>

快速使用魔搭社区部署 DeepSeek 蒸馏模型，服务器本地都可以运行，包含前端界面。
*Quickly deploy DeepSeek distilled models via ModelScope, runnable on servers or locally, with a built-in web UI.*

```bash
cd deepseek_r1_deploy
pip install -r requirements.txt
```

</details>

<details>
<summary><b>🔍 LLM 联网搜索插件 —— 让本地大模型连上互联网</b></summary>

本地部署的大语言模型通常无法直接联网搜索，这个插件可以帮助模型获取最新的互联网信息，从而提供更准确和及时的回答。
*A plugin that gives locally deployed LLMs web search capabilities for more accurate and timely responses.*

**功能特点**

- 🔍 支持多种搜索引擎（Google / Bing / 百度）
- 📝 获取搜索结果摘要，抓取网页详细内容
- 🤖 自动格式化搜索结果为适合 LLM 处理的提示词
- 🔌 提供简单的 API 接口，易于与各种 LLM 集成
- 📚 包含示例客户端代码，展示如何与本地 LLM 集成
- 🇨🇳 针对中文搜索优化，特别是百度搜索引擎
- ⏰ 支持获取实时时间信息
- 🛠️ 提供可配置的 Web 界面，方便调整各项参数

```bash
cd LLM联网搜索插件
pip install -r requirements.txt
```

</details>

---

## 📈 Star 历史

<div align="center">

[![Star History Chart](https://star-history.dera.page/svg?repos=1692775560/deepseek_project&type=Timeline)](https://star-history.dera.page/#1692775560/deepseek_project&Timeline)

</div>

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！如果这个项目对你有帮助，请点一个 ⭐ Star 支持一下～

<div align="center">

**如果对你有帮助，欢迎 Star ⭐ / Fork 🍴 / Watch 👀**

Made with ❤️ by [1692775560](https://github.com/1692775560)

</div>
