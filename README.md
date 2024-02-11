# EROptimizer

ADD MORE HERE

## Getting Started

Follow these steps to set up and run the project:

### Prerequisites

- Python 3.x
- npm (Node.js package manager)
- ffmpeg

### Installation

1. **Create a Python Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate` 
   ```
2. **Install Python Dependencies**
3. **Install Node Modules:**:
    ```bash
    cd react-flask-app
    npm install
    ```
4. **Set Up Environment Variables:**
    Generate an OpenAI API key and Google Key:
    ```bash
    echo "OPENAI_API_KEY={your_openai_api_key}" > react-flask-app/api/.env
    echo "REACT_APP_GOOGLE_API_KEY={your_google_api_key}" > react-flask-app/.env
    ```
    
### Running the Application

1. **Start the app: In 2 seperate windows run**:
    ```
    npm run start-api
    npm start
    ```
    Visit 127.0.0.1:3000/client for the client interface.
    Visit 127.0.0.1:3000/server for the server interface

   
