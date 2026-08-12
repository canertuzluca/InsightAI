# InsightAI 🤖

**Enterprise Multi-Agent AI Decision Engine**

InsightAI, şirket verileri üzerinde doğal dil ile soru-cevap ve analiz gerçekleştiren, **RAG, Text-to-SQL, Analytics ve Multi-Agent Orchestration** teknolojilerini bir araya getiren yapay zekâ destekli bir kurumsal asistan sistemidir.

Kullanıcı, şirket verileri hakkında doğal dilde bir soru sorar. Sistem sorunun türünü analiz eder, gerekli araçları seçer ve birden fazla aracı gerektiğinde sıralı şekilde çalıştırarak doğrulanmış bir cevap üretir.

---

## 🚀 Features

* 🧠 **Multi-Agent Orchestration**
* 🔀 **Intelligent Tool Routing**
* 🗄️ **Text-to-SQL**
* 📚 **RAG (Retrieval-Augmented Generation)**
* 📊 **Sales Analytics**
* 🔍 **Self-Validation**
* 💬 **Natural Language Interface**
* 📈 **Interactive Analytics Dashboard**
* 🔄 **Multi-Step Agent Execution**

---

## 🏗️ Architecture

```text
                    ┌─────────────────────┐
                    │       User          │
                    │ Natural Language    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Router Agent     │
                    │   Tool Selection     │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │ SQL Tool    │   │  RAG Tool   │   │  Analytics  │
      │ Text-to-SQL │   │ Vector      │   │    Tool     │
      └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
             │                 │                 │
             ▼                 ▼                 ▼
       PostgreSQL           Qdrant          Pandas
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Orchestrator      │
                    │  Multi-Step Logic   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Response Generator  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Validation Agent    │
                    │  Answer Checking    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Final Answer     │
                    └─────────────────────┘
```

---

## 🧠 Agent Workflow

InsightAI soruyu tek bir araçla cevaplamak zorunda değildir.

Örneğin:

> "Caner Tuzluca hangi departmanda çalışıyor ve bu departmanın satış performansı nedir?"

Sistem şu şekilde çalışabilir:

```text
User Question
      │
      ▼
Router Agent
      │
      ▼
SQL Tool
      │
      │ → IT Department
      ▼
Orchestrator
      │
      ▼
Analytics Tool
      │
      │ → Sales Performance
      ▼
Response Generator
      │
      ▼
Validation Agent
      │
      ▼
Final Answer
```

Bu yapı sayesinde sistem **tek adımlı tool calling** yerine gerektiğinde **multi-step reasoning ve tool orchestration** gerçekleştirebilir.

---

## 🛠️ Technologies

| Technology   | Purpose                                       |
| ------------ | --------------------------------------------- |
| Python       | Core development                              |
| LangGraph    | Agent orchestration                           |
| LLM          | Natural language understanding and generation |
| PostgreSQL   | Structured company data                       |
| Qdrant       | Vector database                               |
| RAG          | Document-based knowledge retrieval            |
| Pandas       | Data analytics                                |
| Streamlit    | User interface                                |
| Git / GitHub | Version control                               |

---

## 📂 Project Structure

```text
InsightAI/
│
├── app/
│   ├── agents/
│   │   ├── response_generator.py
│   │   └── analytics_response_generator.py
│   │
│   ├── graph/
│   │   ├── nodes.py
│   │   ├── state.py
│   │   └── workflow.py
│   │
│   ├── llm/
│   │   ├── agent_decision.py
│   │   ├── tool_router_llm.py
│   │   ├── validator.py
│   │   └── openai_client.py
│   │
│   ├── prompts/
│   │   ├── decision_prompt.py
│   │   ├── validation_prompt.py
│   │   └── sql_prompt.py
│   │
│   ├── rag/
│   │   └── search.py
│   │
│   ├── tools/
│   │   ├── sql_tool.py
│   │   ├── rag_tool.py
│   │   └── analytics_tool.py
│   │
│   └── ...
│
├── data/
├── docs/
├── scripts/
├── tests/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 💬 Example Queries

### RAG

```text
Çalışanların yıllık ücretli izin hakkı kaç gün?
```

**Example response:**

> Çalışanların yıllık ücretli izin hakkı 20 gündür.

---

### SQL

```text
Caner Tuzluca hangi departmanda çalışıyor?
```

**Example response:**

> Caner Tuzluca IT departmanında çalışıyor.

---

### SQL + Analytics

```text
Caner Tuzluca hangi departmanda çalışıyor ve bu departmanın satış performansı nedir?
```

Sistem önce çalışanının departmanını SQL üzerinden bulur, ardından ilgili departmanın satış verilerini Analytics Tool ile analiz eder.

---

### RAG + SQL + Analytics

```text
Şirketin uzaktan çalışma politikası nedir ve IT departmanının satış performansı nasıldır?
```

Bu sorguda sistem hem şirket dokümanlarından politika bilgisini hem de veritabanından departman bilgisini kullanarak satış analizi gerçekleştirir.

---

## 📊 Analytics

InsightAI satış verileri üzerinde aşağıdaki metrikleri hesaplayabilir:

* Toplam gelir
* Toplam satış
* Toplam ürün miktarı
* Ortalama satış tutarı
* En yüksek gelir elde edilen ay
* En düşük gelir elde edilen ay
* Büyüme oranı
* Aylık gelir trendi

Streamlit arayüzü üzerinden analitik sonuçlar interaktif bir dashboard olarak görüntülenebilir.

---

## 🔍 Self-Validation

InsightAI yalnızca cevap üretmekle kalmaz.

Final cevap oluşturulduktan sonra **Validation Agent** tarafından kontrol edilir.

Validation Agent:

1. Tool sonuçlarını inceler.
2. Üretilen cevabı kontrol eder.
3. Sayısal değerleri karşılaştırır.
4. Cevabın soruyu gerçekten yanıtlayıp yanıtlamadığını kontrol eder.
5. Desteklenmeyen bilgi olup olmadığını kontrol eder.

Örneğin:

```text
Tool Results
     │
     ▼
Response Generator
     │
     ▼
Final Answer
     │
     ▼
Validation Agent
     │
     ├── PASS
     │
     └── FAIL
```

Bu yapı, LLM tarafından üretilen cevapların güvenilirliğini artırmayı amaçlamaktadır.

---

## 🖥️ Running the Project

Virtual environment oluşturulduktan sonra gerekli bağımlılıklar yüklenebilir:

```bash
pip install -r requirements.txt
```

Streamlit uygulamasını başlatmak için:

```bash
streamlit run app.py
```

Uygulama çalıştırıldığında kullanıcı doğal dil üzerinden şirket verileri hakkında sorular sorabilir.

---

## 🧪 Testing

Agent workflow'u test etmek için:

```bash
python -m scripts.test_real_agent_loop
```

Python dosyalarının syntax kontrolü için:

```bash
python -m py_compile app.py
```

Graph import kontrolü:

```bash
python -c "from app.graph.workflow import graph; print('GRAPH OK')"
```

---

## 🎯 Project Goals

InsightAI'nin temel amacı, kurumsal şirket verilerine erişimi doğal dil üzerinden kolaylaştırırken farklı veri kaynaklarını ve yapay zekâ araçlarını tek bir agentic sistem altında birleştirmektir.

Proje özellikle şu konseptleri göstermektedir:

* Agentic AI
* Multi-Agent Systems
* Tool Calling
* RAG
* Text-to-SQL
* Data Analytics
* LLM Orchestration
* Self-Validation
* Enterprise AI

---

## 📌 Project Status

**Completed — Functional Prototype**

InsightAI şu anda:

* ✅ SQL sorguları gerçekleştirebiliyor
* ✅ RAG üzerinden doküman arayabiliyor
* ✅ Satış verilerini analiz edebiliyor
* ✅ Birden fazla tool'u sıralı şekilde çalıştırabiliyor
* ✅ Agent karar mekanizmasına sahip
* ✅ Final cevapları validate edebiliyor
* ✅ Streamlit üzerinden kullanılabiliyor
* ✅ GitHub üzerinde versiyon kontrolü altında

---

## 👨‍💻 Author

**Caner Tuzluca**

Computer Engineering

GitHub: `canertuzluca`

---

## 📄 License

This project is developed for educational and portfolio purposes.
