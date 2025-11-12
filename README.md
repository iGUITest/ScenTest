# 📱 ScenTest: Scenario-based and GUI-Guided Mobile App Testing via Knowledge Graph

## 📑 Table of Contents

- [I. Configuration Guide](#i-configuration-guide)
- [II. The Construction and Use of Knowledge Graph](#ii-the-construction-and-use-of-knowledge-graph)
  - [2.1 Configuration Database](#21-configuration-database)
  - [2.2 The Logic of Knowledge Graph Generation](#22-the-logic-of-knowledge-graph-generation)
  - [2.3 Graph Query Steps](#23-graph-query-steps)
- [III. Code Structure Guidelines](#iii-code-structure-guidelines)
- [IV. Configure File Details](#iv-configure-file-details)

---

## I. ⚙️ Configuration Guide

### 📋 Prerequisites

1. **Python Version**: 3.6 - 3.7 🐍

2. **Package Installation**: 📦 
   ```bash
   pip install -r requirements.txt
   ```
   See `requirements.txt` file for the complete list of required packages.

3. **Picture Processing Environment**: 🖼️
   Configure the relevant environment for picture processing according to `/PicAnalysis/README.md`. This article makes adjustments to the Usage part, see below for details.

4. **Neo4j Database**: 🗄️
   Download and configure Neo4j version 3.5.5 (or any 3.x.x version).

---

## II. 🕸️ The Construction and Use of Knowledge Graph

### 2.1 🔧 Configuration Database

#### 💡 Understanding Neo4j Database Structure

Neo4j is a graph database. For different function points, we should set up different graph databases. For example:
- Create a graph database named `login` to store all data related to the login function point
- Create a graph database named `airport` to store all data related to the subscription ticket

#### 📊 Supported Function Points

<table>
<tr><th>Num.</th><th>Database Name</th><th>Description</th></tr>
<tr><td>1</td><td>🔐 login</td><td>Login functionality</td></tr>
<tr><td>2</td><td>✈️ airport</td><td>Airport/ticket booking</td></tr>
<tr><td>3</td><td>📝 register</td><td>Registration functionality</td></tr>
<tr><td>4</td><td>🛒 shopping</td><td>Shopping functionality</td></tr>
<tr><td>5</td><td>📧 email</td><td>Email functionality</td></tr>
</table>

#### 🚀 Configuration Steps

1. **Modify the Neo4j Configuration File**:
   - Open the `conf` file in the Neo4j folder
   - Edit the database name (default is `graph.db`)
   
   ![Neo4j Configuration](PICS/neo4j-conf.png)

2. **Start Neo4j**: 🚀
   - Open command line as administrator 👨‍💼
   - Run: `neo4j.bat console` (for Windows; Mac users should check the equivalent command)
   - Open http://localhost:7474/ in your browser to access the knowledge graph interactive interface 🌐
   - Test with query: `MATCH (a) RETURN a` (equivalent to MySQL's `SELECT *`)

---

### 2.2 🔨 The Logic of Knowledge Graph Generation

#### ⚡ Core Methods

Run `MobileKG/GenerateKG/main.py` to start the knowledge graph generation process:

<table>
<tr><th>Method/Parameter</th><th>Explanation</th></tr>
<tr><td><code>analyze()</code></td><td>Feature extraction from the original test report</td></tr>
<tr><td><code>connect()</code></td><td>Analyze the content of the test report extracted by feature, and extract the relationship of the relevant content</td></tr>
<tr><td><code>generate()</code></td><td>Perform coreference resolution on the data extracted from the relationship and add it to the knowledge graph</td></tr>
<tr><td>Import RunConfig File</td><td>Configuration required at runtime, please refer to this file for specific parameter content</td></tr>
</table>

#### 📝 General Operation Steps

**Step 1️⃣: Configure Graph Type**
- Modify the `graph_type` in `MobileKG/Config/RunConfig.py` to the specified function point, such as `login` or `airport`

**Step 2️⃣: Prepare Original Data**
- Put the original test report into the `MobileKG/Data/Original` folder
- Alternatively, use another folder and modify the `original_data_path` in `MobileKG/Config/RunConfig.py`

**Step 3️⃣: Run Feature Extraction**
- Run the `analyze()` method in `MobileKG/GenerateKG/main.py`
- The system will automatically disassemble the picture and text information of the test report
- Results are saved to the folder pointed to by `analyze_data_path` (default: `MobileKG/Data/Analyze`)

**Step 4️⃣: Run Relationship Extraction**
- Run the `connect()` method in `MobileKG/GenerateKG/main.py`
- The system will automatically combine the disassembled data from the previous step
- A new folder with the current timestamp will be created
- Results are saved to the folder pointed to by `connect_data_path` (default: `MobileKG/Data/Result`)

**Step 5️⃣: Start Neo4j Database**
- Configure the database of the specified function point according to Section 2.1
- Open command line as administrator
- Run: `neo4j.bat console`

**Step 6️⃣: Generate Knowledge Graph**
- Modify `generate_data_path` in `MobileKG/Config/RunConfig.py`
- Set the value to the path of the folder created with the timestamp in Step 4
- Run the `generate()` method in `MobileKG/GenerateKG/main.py`

**Step 7️⃣: Verify Generation**
- Open http://localhost:7474/
- Enter `MATCH (a) RETURN a` in the input box
- If the knowledge graph is displayed, the generation is successful ✅

#### ⚡ Directly Load Pre-generated Knowledge Graph

To load a pre-generated knowledge graph (e.g., login function):

1. Set `generate_data_path` in `MobileKG/Config/RunConfig.py` to `../Data/Result/login/`
2. Run the `generate()` method in `MobileKG/GenerateKG/main.py`
3. Open http://localhost:7474/ and enter `MATCH (a) RETURN a` to verify ✅

#### 🔧 Troubleshooting

**⚠️ Issue: `synonyms` package download timeout**

The `synonyms` package needs to download `words.vector.gz` on first use, which may be very slow.

- **✅ Solution 1**: Set the proxy, please refer to the welcome section of https://github.com/chatopera/Synonyms
- **✅ Solution 2**: Manually download the compressed package from https://github.com/chatopera/Synonyms/releases/download/3.15.0/words.vector.gz or use the pre-downloaded version (Baidu Pan link: https://pan.baidu.com/s/1PpHrOYEbW8xQ_25EgP2JQg, extraction code: `37j4`). Place it in the folder indicated by the error message.

**⚠️ Issue: `py2neo` package cannot connect to Neo4j**

Try the connection method described in: https://blog.csdn.net/sinat_33846443/article/details/109023259

---

### 2.3 🔍 Graph Query Steps

#### 💡 Basic Usage

Call the `next_step()` method in `MobileKG/SearchKG/main.py`. This method requires three parameters:

![Search KG Method Parameters](PICS/searchKG的方法.png)

#### 📱 Example: "Dewu" APP Login

**Scenario**: Analyzing the start page of the login function point of the "Dewu" APP

<img src="PICS/Dewu1.PNG" style="width:50%"/>

**Step 1️⃣: Prepare the Image and Split Data** 🖼️

```python
import cv2
from MobileKG.LayoutAnalysis.LayoutMain import split

picture = cv2.imread('../Test/pictures/dewu-01.png', 0)
split_dic = split('../Test/pictures/dewu-01.png')
```

**Step 2️⃣: Define Components** 🎯

```python
page1_components = {
    "components": [
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '得物'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '购买'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '服务'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '我'},
    ]
}
```

**Step 3️⃣: Set Parameters** ⚙️

- `last_component_id`: Set to `0` for the first screenshot (no predecessor node)
- `search_all`: Recommended to use the default value for faster search

**Step 4️⃣: Execute Query** 🚀

```python
result = next_step(picture, split_dic, page1_components, 0)
print(result)
```

**Step 5️⃣: Process Return Value** 📊

The method returns an array containing all components that need to be operated on the page:

```python
{
    'status': 'success', 
    'data': [
        {
            'category': 'Button', 
            'ocr': '我', 
            'operation': 'click', 
            'cnt': '我', 
            'cnt_id': 12, 
            'x1': 262, 
            'y1': 1761, 
            'x2': 566, 
            'y2': 1781
        }
    ]
}
```

**Complete Code Example** 💻

```python
import cv2
from MobileKG.LayoutAnalysis.LayoutMain import split
from MobileKG.SearchKG.main import next_step

# Load image and perform layout analysis
picture = cv2.imread('../Test/pictures/dewu-01.png', 0)
split_dic = split('../Test/pictures/dewu-01.png')

# Define page components
page1_components = {
    "components": [
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '得物'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '购买'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '服务'},
        {"category": "Button", "x1": 262, "y1": 1761, "x2": 566, "y2": 1781, "ocr": '我'},
    ]
}

# Query knowledge graph for next step
result = next_step(picture, split_dic, page1_components, 0)
print(result)
```

---

## III. 📂 Code Structure Guidelines

### 3.1 🌐 Overview

- **`MobileKG`**: Django backend 🔧
- **`kgfront`**: Vue frontend 🖥️

**📌 Note**: Due to time constraints, the front and back ends are not connected. The temporary front-end display strategy generates fake JSON data from the `MobileKG/Test/FormFrontEnd` file in the back-end.

---

### 3.2 ⚙️ Config Folder

This folder stores special configuration information for the knowledge graph.

| File | Description |
|------|-------------|
| `RunConfig.py` | Runtime parameter configuration (intermediate result paths, similarity thresholds, etc.) |
| `OperationConfig.csv` | Pre-defined operation types (click, input, etc.) |
| `WidgetConfig.csv` | Pre-defined widget types (button, text box, etc.) |
| `SimilarTXTConfig.json` | Configures which texts the knowledge graph considers similar (domain-specific thesaurus) |
| `TypicalLayoutConfig.json` | Configures similar layouts for finding operable controls during query |
| `SearchPolicy.json` | Configures two query modes available during knowledge graph querying |

**📌 Note**: `OperationConfig.csv` and `WidgetConfig.csv` store constant entities that can be directly loaded without analysis when generating a knowledge graph from scratch.

---

### 3.3 💾 Data Folder

| Folder | Description |
|--------|-------------|
| `Original` | Stores original data for building the knowledge graph (application level, not function point level) |
| `Analyze` | Stores intermediate data results after feature extraction from `Original` folder |
| `Result` | Stores data that has completed feature extraction and relation extraction, ready for `generate()` method |

---

### 3.4 🧪 FuncTest Folder

| File/Folder | Description |
|-------------|-------------|
| `test.py` | Realizes the whole process of querying the map through a screenshot |
| `screenshot/` | Used to store query results |
| `screenshot/origin/` | Stores original images to be queried |
| `screenshot/widget_res/` | Stores results after widget extraction |
| `screenshot/KG_res/` | Draws the result controls from knowledge graph query |

**💡 Usage**: Add the path to be queried to the parameters of the `searchKG()` method in `FuncTest/test.py`.

---

### 3.5 🔨 GenerateKG Folder

This folder handles knowledge graph generation.

| File/Folder | Description |
|-------------|-------------|
| `GenerateMain.py` | Startup entry file for building knowledge graphs |
| `Operation/` | All operations in the generation process (feature extraction, relationship extraction, coreference resolution) |
| `PO/` | Data classes needed to generate the knowledge graph |

---

### 3.6 📐 LayoutAnalysis Folder

This folder performs layout analysis operations on pictures.

**💡 Usage**: 
- Not used during construction, but during the query process
- Divides input screenshots into regions by horizontal dimension
- Performs SIFT similarity matching between divided regions and layout pictures in Config
- If threshold is exceeded, matching is successful and the control is locked

**📄 Main File**: `LayoutMain.py`

---

### 3.7 🗄️ Neo4j Folder

This folder contains operations for the Neo4j graph database.

| File | Description |
|------|-------------|
| `GraphAdd.py` | Creates a new database in Neo4j |
| `GraphSearch.py` | Searches for data in Neo4j database |

---

### 3.8 🖼️ PicAnalysis Folder

This folder is responsible for the recognition and extraction of text and controls from pictures.

---

### 3.9 🎨 PICS Folder

Stores images used in `README.md` documentation.

---

### 3.10 🔍 SearchKG Folder

This folder contains the general entry for querying the knowledge graph.

**💡 Usage**: 
- Call the `next_step()` method in `SearchMain.py`
- For specific usage and precautions, please refer to Section 2.3 and the notes in the document

---

### 3.11 🧰 Test Folder

This folder stores intermediate results when debugging the knowledge graph and provides interfaces for quick debugging.

| File | Description |
|------|-------------|
| `DrawLine.py` | Quickly draw control recognition results, layout analysis results, and map query results |
| `FormFrontEnd.py` | Quickly generate the JSON file that the front-end demo needs (requires data in Data folder) |

---

### 3.12 📝 TextAnalysis Folder

This folder contains tools for text analysis.

**✨ Features**:
- Interface for `jieba` word segmentation
- Segment the recurrence steps and analyze parts of speech
- Identify gerunds, etc.

**📌 Note**: `LanguageChange.py` has not been implemented. Currently only supports Chinese. 🇨🇳

---

### 3.13 🤖 WidAnalysis Folder

Stores a pre-trained CNN model that identifies whether a widget in a picture is a button or a text box.

---

## IV. 📋 Configure File Details

### 4.1 📖 SimilarTXTConfig.json

**🎯 Purpose**: Specifies synonyms under a knowledge domain.

This file helps the system understand that certain terms are equivalent in the context of mobile application testing.

---

### 4.2 🎨 TypicalLayoutConfig.json

**🎯 Purpose**: Locates specified controls through layout configuration.

For pictures where the text is not sufficient to help with positioning, this configuration provides a layout-based method to locate the specified control.

---

### 4.3 🔍 SearchPolicy.json

**🎯 Purpose**: Defines query strategies.

The system provides two query methods:
1. **Text-based similarity query** 📝
2. **Layout-based identification query** 🖼️

Both query methods are guaranteed to execute, with layout queries preceding text queries.

**Configuration Options**:
- **`both`**: Execute both layout and text queries ✅
- **`layout`**: If layout query finds the control, skip text query ⚡

Use the `type` attribute to specify the desired behavior.

---

## 📄 License

Please refer to the project license file for usage terms and conditions.

---

## 📬 Contact

For questions or issues, please refer to the project repository or contact the development team.
