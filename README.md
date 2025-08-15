# 🚀 MCP Prompt Context Server

A comprehensive **Model Context Protocol (MCP)** server built with **FastMCP** to accelerate enterprise software development through intelligent project planning, template generation, and Firebase integration.

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Available Tools](#-available-tools)
- [Firebase Integration](#-firebase-integration)
- [Documentation](#-documentation)
- [Examples](#-examples)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🛠️ Core MCP Tools
- **Requirements Collection**: Intelligent project requirement gathering with phased implementation plans
- **Template Generation**: Base and advanced prompt templates for various project types
- **Process Automation**: Comprehensive automation analysis and recommendations
- **Firebase Integration**: Seamless Firebase project management and file operations

### 🔥 Firebase Capabilities
- **Project Plan Management**: Download and manage project plans from Firebase
- **File Operations**: Upload, download, and manage files in Firebase Storage
- **Firestore Integration**: Query and manage Firestore documents
- **GDPR Compliance**: Built-in GDPR compliance tools and templates

### 🏗️ Project Templates
- **Web Applications**: React, Vue, Angular templates
- **API Development**: REST, GraphQL service templates
- **Machine Learning**: ML pipeline and model templates
- **E-commerce**: Complete e-commerce store templates
- **Mobile Apps**: Banking, IoT, and general mobile app templates

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Firebase functions)
- Firebase CLI (optional, for deployment)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Prerna-2055/MCP.git
   cd MCP-1
   ```

2. **Set up Python environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Firebase (Optional)**
   ```bash
   # Copy the example config and update with your credentials
   cp firebase.example.ts firebase.ts
   # Edit firebase.ts with your Firebase configuration
   ```

4. **Run the MCP Server**
   ```bash
   python sever.py
   ```

## 🎯 Usage

### Basic MCP Server Usage

```python
from fastmcp import FastMCP

# The server provides several tools:
# 1. collect_requirements - Project planning
# 2. provide_base_template - Template generation
# 3. provide_advanced_template - Enhanced templates
# 4. analyze_process_automation - Process analysis
# 5. download_firebase_txt_file - Firebase integration
# 6. list_firebase_files - Firebase file management
```

### Example: Collect Project Requirements

```python
# Use the collect_requirements tool
result = collect_requirements(
    project_name="E-commerce Platform",
    project_type="webapp",
    complexity="high",
    tech_stack="React, Node.js, PostgreSQL",
    deadline_weeks=12
)
```

### Example: Firebase Integration

```python
# Download project plans from Firebase
result = download_firebase_txt_file(
    firebase_url="https://your-firebase-function-url",
    filename="My_Project_Plan.txt",
    save_as_cline_rules=True
)
```

## 📁 Project Structure

```
MCP-1/
├── 📄 sever.py                     # Main MCP server
├── 📄 requirements.txt             # Python dependencies
├── 📄 firebase.ts                  # Firebase configuration (template)
├── 📄 .gitignore                   # Git ignore rules
├── 📄 README.md                    # This file
│
├── 📁 firebase-integration/        # Firebase setup and functions
│   ├── 📄 firebase.json           # Firebase project config
│   ├── 📄 firestore.rules         # Firestore security rules
│   └── 📁 firebase-functions/      # Cloud functions
│       └── 📁 functions/
│           ├── 📄 index.js         # Main functions
│           ├── 📄 file-operations.js
│           └── 📄 package.json
│
├── 📁 MCP_workflow/                # Sample project workflows
│   └── 📁 couchbase-store/        # E-commerce example
│       └── 📁 backend/
│           ├── 📄 server.js
│           ├── 📄 .env.example     # Environment template
│           └── 📁 config/
│
├── 📁 firebase-ready-components/   # Ready-to-use components
│   ├── 📄 firebaseConfig.js
│   ├── 📄 useFirebaseAPI.js
│   └── 📄 ProjectRequirements.jsx
│
├── 📁 test_files/                  # Test scripts
│   ├── 📄 test_tools.py
│   ├── 📄 test_firebase_functions.py
│   └── 📄 test_enhanced_options.py
│
└── 📁 docs/                        # Documentation
    ├── 📄 FIREBASE_SETUP_GUIDE.md
    ├── 📄 LOVABLE_SETUP.md
    ├── 📄 ENHANCED_OPTIONS_GUIDE.md
    └── 📄 HOW_TO_USE_FIREBASE_MCP_TOOL.md
```

## 🛠️ Available Tools

### 1. `collect_requirements`
Collects project requirements and generates implementation plans.

**Parameters:**
- `project_name` (string): Name of the project
- `project_type` (string): Type (api, webapp, ml, cli, service)
- `complexity` (string): Complexity level (low, medium, high)
- `tech_stack` (string, optional): Technology stack
- `deadline_weeks` (int, optional): Project deadline in weeks

### 2. `provide_base_template`
Returns base prompt templates for different use cases.

**Parameters:**
- `use_case` (string): Use case type (api, webapp, ml)

### 3. `provide_advanced_template`
Enhances base templates with advanced details.

**Parameters:**
- `base_template` (string): Base template to enhance
- `style` (string, optional): Style (clean_code, security_first, performance)

### 4. `analyze_process_automation`
Provides detailed process automation analysis.

**Parameters:**
- `process_name` (string): Name of the process
- `primary_goal` (string): Main objective
- `trigger_type` (string): Trigger mechanism
- `trigger_details` (string): Trigger specifics
- `success_outcome` (string): Success criteria

### 5. `download_firebase_txt_file`
Downloads text files from Firebase and converts to .cline rules.

**Parameters:**
- `firebase_url` (string): Firebase function URL
- `project_id` (string, optional): Firebase project ID
- `filename` (string, optional): Specific filename
- `save_as_cline_rules` (bool, optional): Convert to .cline format

### 6. `list_firebase_files`
Lists available files in Firebase Firestore.

**Parameters:**
- `project_id` (string, optional): Firebase project ID
- `collection` (string, optional): Firestore collection name
- `limit` (int, optional): Maximum files to return

## 🔥 Firebase Integration

### Setup Firebase

1. **Install Firebase CLI**
   ```bash
   npm install -g firebase-tools
   ```

2. **Initialize Firebase**
   ```bash
   cd firebase-integration
   firebase login
   firebase init
   ```

3. **Deploy Functions**
   ```bash
   firebase deploy --only functions
   ```

### Firebase Configuration

Create a `firebase.ts` file with your configuration:

```typescript
// firebase.ts
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getFunctions } from "firebase/functions";

const firebaseConfig = {
  projectId: "your-project-id",
  appId: "your-app-id",
  storageBucket: "your-storage-bucket",
  apiKey: "your-api-key",
  authDomain: "your-auth-domain",
  messagingSenderId: "your-sender-id"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const functions = getFunctions(app);

export { db, functions };
```

## 📚 Documentation

### Setup Guides
- [Firebase Setup Guide](FIREBASE_SETUP_GUIDE.md) - Complete Firebase integration setup
- [Lovable Integration](LOVABLE_SETUP.md) - Integration with Lovable platform
- [Enhanced Options Guide](ENHANCED_OPTIONS_GUIDE.md) - Advanced configuration options

### Usage Guides
- [Firebase MCP Tool Usage](HOW_TO_USE_FIREBASE_MCP_TOOL.md) - Detailed tool usage
- [Firebase Testing Guide](firebase-testing-guide.md) - Testing Firebase functions
- [Quick Deploy Guide](QUICK_DEPLOY.md) - Fast deployment instructions

### Reference
- [Firestore Query Guide](FIRESTORE_QUERY_AND_FILE_GUIDE.md) - Database operations
- [GDPR Compliance](GDPR_ECOMMERCE_FIRESTORE_EXAMPLE.md) - GDPR implementation
- [MCP Architecture](FIREBASE_MCP_ARCHITECTURE_DIAGRAM.md) - System architecture

## 💡 Examples

### Sample Project Plans
- [Banking App](Banking_App_Project_Plan.txt) - Mobile banking application
- [E-commerce Store](CouchBase_E-commerce_Store_Project_Plan.txt) - Full e-commerce platform
- [DeFi Platform](DeFi_Trading_Platform_Project_Plan.txt) - Decentralized finance app
- [IoT System](Smart_Home_IoT_System_Project_Plan.txt) - Smart home automation
- [Analytics Dashboard](CouchBase_Analytics_Dashboard_Project_Plan.txt) - Data analytics platform

### Code Examples
- React components with Firebase integration
- Custom hooks for API management
- GDPR-compliant data handling
- Automated testing scripts

## 🔧 Development

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test files
python test_tools.py
python test_firebase_functions.py
python test_enhanced_options.py
```

### Environment Setup

```bash
# Copy environment template
cp MCP_workflow/couchbase-store/backend/.env.example .env

# Edit with your configuration
nano .env
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add tests for new features
- Update documentation for API changes
- Ensure Firebase functions are properly tested

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastMCP** - For the excellent MCP framework
- **Firebase** - For cloud infrastructure and services
- **Lovable** - For platform integration capabilities
- **Community Contributors** - For ongoing improvements and feedback

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Prerna-2055/MCP/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Prerna-2055/MCP/discussions)
- **Documentation**: Check the `docs/` directory for detailed guides

---

**Made with ❤️ for the developer community**
