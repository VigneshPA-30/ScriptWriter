# 📝 ScriptWriter

ScriptWriter is an AI-powered tool that helps content creators generate viral video scripts effortlessly. It uses Google's Gemini model through a multi-agent system to automate research, topic ideation, hook creation, and script writing. Whether you're a YouTuber, TikToker, or social media content creator, ScriptWriter streamlines your content creation process.

![ScriptWriter Demo](ScriptWriter.gif)

## ✨ Features

- 🎯 **Niche Selection**: Customize content for your specific niche
- 🔍 **Topic Generation**: Get AI-powered topic suggestions using web research and trend analysis
- 📚 **Automated Research**: Comprehensive topic research with reliable sources and emotional hooks
- 🎣 **Hook Generation**: Create attention-grabbing hooks based on proven viral patterns
- ✍️ **Full Script Creation**: Generate 170-200 word scripts optimized for short-form video
- 🤖 **Multi-Agent System**: Specialized AI agents working together for optimal results
- 🎨 **User-Friendly Interface**: Simple and intuitive web interface

## 🚀 Getting Started

### Prerequisites

#### Option 1: Local Installation
- Python 3.12 or higher
- uv (Python package manager)
- Git
- Google Gemini API key

#### Option 2: Docker Installation
- Docker
- Docker Compose
- Git
- Google Gemini API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/VigneshPA-30/ScriptWriter.git
cd ScriptWriter
```

2. Choose your installation method:

#### Option 1: Local Installation

1. Set up Python virtual environment using uv
```bash
uv venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

2. Install Python dependencies with uv
```bash
# Install dependencies from pyproject.toml
uv pip install .
```

3. Set up environment variables in `.env` file
```bash
GEMINI_API_KEY="your-api-key-here"
YOUTUBE_API_KEY="your-youtube-api-key-here"
```

#### Option 2: Docker Installation

1. Copy the example environment file
```bash
cp .env.example .env
```

2. Add your API keys to the `.env` file
```bash
GEMINI_API_KEY="your-api-key-here"
YOUTUBE_API_KEY="your-youtube-api-key-here"
```

3. Build and run with Docker Compose
```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:8001
- Backend API: http://localhost:8000

### Running the Application

1. Start the Backend Server
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

2. Start the Frontend Server (in a new terminal)
```bash
cd frontend
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

3. Access the application in your browser at `http://localhost:8001`

## 🎯 How to Use

1. **Select Your Niche**
   - Choose your content niche (e.g., Technology, Fitness, Education)
   - The Research Agent will use this to find trending topics

2. **Generate Topics**
   - The AI will search the web for current trends in your niche
   - Get 6 potential viral topic ideas with justification
   - Select the most appealing topic for your video

3. **Research Phase**
   - The Topic Research Agent gathers comprehensive information
   - Focuses on surprising, emotional, or counterintuitive facts
   - Includes verified sources for credibility

4. **Create Hooks**
   - The Hook Agent analyzes the research to create attention-grabbing openings
   - Uses proven patterns from successful viral videos
   - Choose the most compelling hook for your audience

5. **Generate Full Script**
   - The Script Agent combines the hook and research into a cohesive script
   - Optimized length of 170-200 words for short-form video
   - Ready-to-use format with proper pacing and structure

## 🛠️ Project Structure

```
ScriptWriter/
├── backend/                # FastAPI backend server
│   ├── main.py            # Main API endpoints
│   ├── agents.py          # Multi-agent system implementation
│   ├── models.py          # Gemini model configuration
│   ├── prompts.py         # Agent instructions and prompts
│   ├── tools.py           # Web search and content tools
│   ├── scripts_fetch.py   # Example script database
│   └── utils.py           # Utility functions
├── frontend/              # Frontend application
│   ├── app.py            # Frontend server
│   ├── static/           # Static files (JS, CSS)
│   └── templates/        # HTML templates
└── pyproject.toml        # Project dependencies and configuration
```

## � Docker Usage

When running with Docker, the application is split into two services:

1. **Frontend Service**
   - Runs on port 8001
   - Handles the user interface
   - Auto-reloads on code changes

2. **Backend Service**
   - Runs on port 8000
   - Provides the API endpoints
   - Auto-reloads on code changes

### Docker Commands

Start the application:
```bash
docker-compose up
```

Start in detached mode:
```bash
docker-compose up -d
```

Rebuild containers:
```bash
docker-compose up --build
```

Stop the application:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

## �📚 API Documentation

Once the backend server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔧 Dependencies

Key dependencies include:
- FastAPI for the backend API
- Gemini/LiteLLM for AI capabilities
- googlesearch-python for web research
- youtube-transcript-api for example scripts
- uvicorn for the ASGI server
- Jinja2 for frontend templating

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions, please [open an issue](https://github.com/VigneshPA-30/ScriptWriter/issues) on GitHub.

---

Made with ❤️ by VigneshPA-30
