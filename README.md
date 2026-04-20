# Local LLM Backend Service

本專案為一套本地 LLM 後端服務，提供通用 API 與結構化輸出能力，並支援不同應用場景的決策邏輯實作。

---

## 系統概述

本系統提供一組 LLM backend API，支援不同類型的推論需求：

- 通用文字分析（analyze）
- 結構化輸出（classify）
- 事件判讀（event → decision，應用案例）

整體流程：
```text
input → LLM → structured / text output
```

事件判讀流程可串接外部工具（如 Track2Event），形成完整 decision pipeline。

---

## 本專案負責內容

本 repo 主要負責：

- LLM 推論封裝（local / openai）
- API 層設計（analyze / classify / decision）
- Structured Output 設計（JSON schema）
- 系統流程控制（orchestration）
- Debug 與測試機制（injected events）

不包含：

- tracking 演算法
- 偵測模型訓練

---

## 系統分層

### Core Backend

提供通用 LLM 能力：

- analyze（文字生成）
- classify（結構化輸出）

---

### Application Layer

基於特定場景的應用邏輯：

- event decision（事件判讀）

**decision 為應用案例，不屬於核心 backend 功能**

---

## API 功能

### 1. Analyze（通用 LLM）

提供基本 LLM 推論能力：
```text
input → LLM → text output
```

適用於一般分析、問答與內容生成。

---

### 2. Classify（Structured Output）

將文字轉換為結構化結果：

```json
{
  "topic": "...",
  "sentiment": "...",
  "urgency": "..."
}
```

特點：

- JSON schema 約束
- 自動 retry 機制
- 提升輸出穩定性

---

### 3. Event Decision（應用案例）

將事件資料轉換為決策：

```text
Event → LLM → Decision JSON
```

輸出：
```json
{
  "action": "notify",
  "priority": "medium",
  "reason": "..."
}
```

此功能為特定場景（事件判讀）之應用邏輯，並非 backend 核心功能。

---

## 外部整合（Track2Event）

Track2Event Repo：

https://github.com/tony148565/Track2Event

負責：

- 將 tracking 資料轉換為事件（如 person_staying）
- 提供特徵：duration / speed / distance

本 backend 負責：

- 接收事件資料
- 進行 LLM 判讀
- 輸出 decision

>Track2Event 與本專案為獨立 repo  
>透過事件格式進行串接  

---

## 核心設計

### LLM Router

支援多 backend：

- local（llama-cpp-python）
- openai（接口預留）

---

### Structured Output

將 LLM 回應限制為 JSON schema：

- 提升穩定性
- 適合後端系統使用
- 降低 parsing error

---

### Decision Policy

根據事件特徵進行判讀：

- duration
- event count
- event type

採用 rule + LLM 混合策略

---

### Debug 測試機制

支援 injected event 測試：

- 不需依賴 Track2Event
- 可快速驗證 decision 行為
- 支援多種測試情境

---

### GPU 推論

使用 llama-cpp-python CUDA：

- 支援 n_gpu_layers
- 啟用 GPU offload
- 提升推論效能

---

## 技術棧

- Python
- FastAPI
- llama-cpp-python
- RESTful API
- multiprocessing / IPC

---

## 系統定位

本專案定位為：

- LLM Backend Service
- Structured Output Engine
- Decision Pipeline（應用層）

而非：

- 視覺模型
- tracking 系統

---

## 設計目標

本系統核心目標為：

將 LLM 能力轉換為「可被後端系統穩定使用的服務」

透過：

- API abstraction
- structured output
- 可擴充的應用層設計

支援不同場景的 decision 邏輯實作
