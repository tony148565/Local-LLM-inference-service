# 本地 LLM 事件判讀後端（Local LLM Event Decision Backend）

本專案為一套本地 LLM 後端系統，將影像事件資料轉換為結構化決策（decision），供後端系統直接使用。

---

## 系統概述

本系統建立一條事件驅動的決策流程：

Tracking → Event Extraction → LLM 判讀 → 結構化輸出

將電腦視覺的偵測結果轉換為具語意的事件，再透過 LLM 轉為可被系統調用的決策。

---

## 系統架構

系統主要分為三個層級：

### 1. 事件抽取層（Track2Event）

將 tracking 資料轉換為具語意的事件（如 `person_staying`），並抽取關鍵特徵：

- duration（停留時間）
- speed（平均速度）
- distance（移動距離）

---

### 2. 判讀層（LLM Backend）

使用本地 LLM（llama-cpp-python）進行事件判讀，並輸出結構化結果：

- ignore
- log_event
- notify
- alert

---

### 3. 流程編排層（Orchestration）

- 負責工具呼叫與流程控制
- 串接事件抽取與 LLM 判讀
- 透過 FastAPI 提供 API 介面

---

## 核心特點

### 結構化輸出（Structured Output）

將 LLM 回應限制為固定 JSON schema，避免自由文字造成系統不穩定。

---

### Decision Policy 設計

根據以下條件進行判讀：

- 事件持續時間（duration）
- 事件數量（event count）
- 事件類型（event type）

---

### Debug 測試機制

支援 injected event 測試（假資料注入）：

- 不需重跑影片即可驗證 decision 行為
- 可重複測試 decision policy 穩定性

---

### GPU 推論加速

使用 llama-cpp-python CUDA 版本，透過 `n_gpu_layers` 啟用 GPU offload，加速本地推論。

---

## 技術棧

- Python / FastAPI
- llama-cpp-python（本地 LLM）
- OpenCV（影像處理）
- multiprocessing / IPC（流程整合）

---

## 範例輸出

```json
{
  "action": "notify",
  "priority": "medium",
  "reason": "偵測到長時間停留事件"
}