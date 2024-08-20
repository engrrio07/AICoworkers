# AICoworkers

AICoworkers is an innovative application that allows users to create and manage their own AI agent teams using CrewAI. This Streamlit-based web application enables users to build customized AI crews for various tasks, whether personal or professional.

## Features

- Create and manage AI agents with specific roles and goals
- Automatic optimization of agent prompts using OpenAI's GPT-4o
- User-specific data storage in PostgreSQL database
- Scalable architecture to handle multiple users simultaneously
- Docker support for easy deployment

## Prerequisites

- Python 3.9+
- PostgreSQL database
- OpenAI API key

## Installation

1. Clone the repository
2. Install the required packages: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory and add the following environment variables:
```
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@host:port/aicoworkers
```

## Running the Application

### Locally

1. Ensure your virtual environment is activated.
2. Run the Streamlit app: `streamlit run app.py`
3. Open your web browser and navigate to `http://localhost:8501`.

### Using Docker

1. Build the Docker image: `docker build -t ai_coworkers .`
2. Run the Docker container: `docker run -p 8501:8501 --env-file .env ai_coworkers`
3. Open your web browser and navigate to `http://localhost:8501`.

## Usage

1. Enter your username when prompted.
2. Use the sidebar to add new AI agents by specifying their roles and goals.
3. The application will automatically optimize agent prompts when you have more than one agent.
4. View your AI crew in the main area of the application.
5. (Future feature) Create tasks and assign them to your AI agents.
6. (Future feature) Run your AI crew to complete the assigned tasks.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [OpenAI](https://openai.com/)

## Support

If you encounter any problems or have any questions, please open an issue in the GitHub repository.
