# 🛡️ High-Performance Fraud Detection Pipeline (6M+ Transactions)

A production-ready project focused on developing a highly efficient, low-latency financial fraud detection model on an extremely imbalanced large-scale dataset (~6.3 million transactions) using **CatBoost**.

## 🚀 Key Achievements & Architecture Solutions

*   **Big Data Optimization**: Bypassing heavy `scikit-learn` preprocessing pipelines, all data was packed into native **`catboost.Pool`** binary structures. This eliminated RAM bottlenecks and shrank CPU training time for 6M rows to just **10 minutes**.
*   **Business-Driven Threshold Tuning**: Rejected the naive default classification threshold (`0.5`) and aggressive class-weight balancing (which triggered a massive 94% false-positive rate). Instead, the decision boundary was mathematically optimized using the **Precision-Recall (PR) Curve**.
*   **Production-Ready Inference**: Implemented a lightweight, procedural (non-OOP) prediction pipeline designed for seamless microservice integration (FastAPI/Flask). Inference latency per single transaction is **under 2 ms**.

## 📥 Model Artifacts & Downloads

Since the binary model weights and config files are too heavy for standard Git storage, they are hosted externally:

*   **[Direct link to the binary CatBoost weights](https://drive.google.com/file/d/1hFJ2l-zuXI-2zV--5Ha6QOnkNAk-XjsH/view?usp=drive_link)** 



## 📊 Results & Metrics (Test Split: 1.27M Rows)

By finding the optimal precision-recall balance at `best_threshold = 0.0943`, the model achieves a perfect equilibrium for financial compliance:

*   **Support**: Heavily imbalanced test set (1,270,904 legitimate transactions / 1,620 fraud cases).
*   **Precision**: **80.00%** — False alarms dropped hundreds of times compared to the baseline model, preventing customer frustration.
*   **Recall**: **80.00%** — Successfully intercepts 4 out of 5 actual fraudulent operations.
*   **F1-Score**: **0.8000**
*   **ROC-AUC**: **0.8998**

### Confusion Matrix
*   **True Negative**: 1,270,580 (Legitimate transactions correctly allowed)
*   **False Positive**: 324 (Minimal false blockages)
*   **False Negative**: 324 (Missed fraud cases)
*   **True Positive**: 1,296 (Fraudulent transactions successfully blocked)

## 🛠️ Feature Importance (Key Decision Drivers)

Analysis using CatBoost's native feature evaluation revealed the main indicators triggering fraud detection:
1. `newbalanceOrig` — Origin account balance after the transaction.
2. `oldbalanceOrg` — Origin account balance before the transaction.
3. `amount` — Total transaction value.

4.  <img width="2400" height="1200" alt="feature_importance" src="https://github.com/user-attachments/assets/c04f76b2-9175-4731-a7e7-94029e8f0c09" />

## 🚀 Deployment & API (predict.py)

The repository includes a lightweight web service built with **FastAPI** to serve the model for real-time inference. The service automatically validates incoming requests via **Pydantic** models and returns an immediate transaction verdict.

### Environment Setup & Local Run

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   * On Windows:
     ```bash
     venv\Scripts\activate
     ```
   * On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Uvicorn server:**
   ```bash
   python predict.py
   ```

### Interactive Documentation (Swagger UI)
Once the server is up, open your browser and navigate to:
👉 `http://localhost:8000/docs`

This interactive Swagger UI provides the auto-generated **OpenAPI JSON Schema**, allowing backend developers to review exact data fields and test requests live via the **"Try it out"** button.

### API Specification

* **Method:** `POST`
* **Endpoint:** `/predict`
* **Request Body Format (JSON):**
```json
{
  "step": 1,
  "type": "TRANSFER",
  "amount": 5000.00,
  "oldbalanceOrg": 5500.00,
  "newbalanceOrig": 500.00,
  "oldbalanceDest": 0.00,
  "newbalanceDest": 5000.00
}
```

* **Successful Response Format (JSON):**
```json
{
  "status": "success",
  "verdict": "BLOCK",
  "fraud_probability": 0.85412,
  "threshold_applied": 0.0943
}
```
*Note: If `fraud_probability` is greater than or equal to `0.0943`, the service returns `"BLOCK"`, otherwise it returns `"ALLOW"`.*
