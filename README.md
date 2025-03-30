# MCP in Telegram

# 🚀 AI-Powered Message Control Protocol (MCP) for Telegram

<div align="center">
  <img src="https://media.giphy.com/media/L1R1tvI9svkIWwpVYr/giphy.gif" width="400">
</div>

## 🔍 Project Overview
MCP is an AI-driven moderation system designed to enhance security and automate content filtering on Telegram. It leverages machine learning to detect and mitigate:
- Hate speech and abusive content  
- Spam and phishing attempts  
- Fake news and malicious URLs    

---

## ✨ Key Features  

### 1️⃣ **PurgeBot** 🧹  
> *"No toxicity allowed!"*  
- 🚨 Detects **hate speech** & abusive images  
- ⚠️ Warns sender → **auto-removes repeat offenders**  
- 🔥 *2-strike policy*  

### 2️⃣ **SpamKeeper** 🛡️  
> *"Bye-bye spam!"*  
- 🤖 ML-powered spam detection  
- 🗑️ Auto-deletes + notifies sender  

### 3️⃣ **SecurityBot** 🔒  
> *"Phishing? Not on my watch!"*  
- 🌐 Blocks malicious URLs  
- 📢 Flags fake news in real-time  

### 4️⃣ Terragate 🌐  
> *"Geo-Fencing for confidential chat"* 

📍 Restricts group access by location  
🛂 Enterprise-grade boundary control


### 5️⃣ MessageBouncer 🛂  
> *"AI gatekeeper for your chats"*  

✋ Pre-approves suspicious messages  
🤖 Context-aware questioning system 
### 6️⃣ ShadowMsg 👤  
> *"Stealth moderation system"*  

👻 Hidden message filtering  
🔍 Secret keyword tracking

---

## 🛠️ Tech Stack  
| Category       | Tools                                                                 |
|----------------|-----------------------------------------------------------------------|
| **Backend**    | Python (Telethon), PyTorch                                            |
| **AI/ML**      | OpenAI API, Google Perspective API, Toxic-Bert                       |
| **Automation** | Telegram Bot API, Webhooks                                            |
| **Geo-Fence**  | Aiogram (Async Telegram Bot Framework)                                |

---

## 🎯 Target Users  
| 👥 Community Admins | 🏢 Enterprises | 🏛️ Governments | 🏫 Schools |  
|---------------------|---------------|----------------|------------|  

---

## 🌟 Why MCP?  
✔️ **All-in-one AI moderation**  
✔️ **Real-time protection**  
✔️ **Scalable for large groups**  

<div align="center">
  <img src="https://media.giphy.com/media/3o7TKSjRrfIPjeiVyM/giphy.gif" width="300">
</div>

---

## 🚧 Implementation Roadmap  
```mermaid
graph LR
  A[Current: Middleware Bot] --> B[Future: Proxy Protocol]  
  B --> C[Direct Telegram Integration]
