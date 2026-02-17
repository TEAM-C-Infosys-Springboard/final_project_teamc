Completed testing and validation for PyKV project.

# PyKV: A Scalable In-Memory Key-Value Store with Persistence

## 📌 Overview

PyKV is a backend system project that implements a **high-performance in-memory key-value store** with **automatic file-based persistence**. The system combines the speed of in-memory data access with the reliability of persistent storage, ensuring that data is not lost during application restarts or crashes.

The project is designed to demonstrate **core backend system concepts** such as storage engines, persistence mechanisms, and REST API integration.

---

## 🎯 Problem Statement

- In-memory data stores provide fast access but lose data on shutdown.
- Persistent databases ensure durability but introduce latency.
- There is a need for a lightweight system that balances **speed and reliability**.

PyKV addresses this problem by storing data in memory while persistently saving it to disk.

---

## ✅ Objectives

- Implement an in-memory key-value store
- Ensure data persistence across restarts
- Support crash-safe recovery
- Expose functionality through REST APIs
- Provide a clean and demo-friendly backend system

---

## 🏗️ System Architecture

PyKV follows a modular architecture with three main layers:

1. **Core Engine**
   - Handles in-memory data storage
   - Supports PUT, GET, and DELETE operations
   - Uses hash-based data structures for O(1) access

2. **Persistence Layer**
   - Saves data to disk in JSON format
   - Automatically triggered on data modification
   - Loads data during application startup

3. **API Layer**
   - Built using FastAPI
   - Exposes RESTful endpoints
   - Uses Swagger UI for testing and demonstration

---

## 🔧 Technologies Used

- **Programming Language:** Python  
- **Framework:** FastAPI  
- **Server:** Uvicorn  
- **Storage Format:** JSON  
- **Tools:** VS Code, GitHub  

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|------|---------|-------------|
| POST | `/put` | Store or update a key-value pair |
| GET | `/get/{key}` | Retrieve the value for a given key |
| DELETE | `/delete/{key}` | Delete a key-value pair |

## Contribution Update

- Reviewed project structure
- Improved documentation clarity
- No core logic or functionality was modified

---

