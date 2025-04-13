# LINE ChatBot Documentation

## Project Overview

This project is a LINE ChatBot built using FastAPI and the LINE Messaging API. It is designed to handle text messages and provide appropriate responses.

## Installation Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/m3monster/LINE-ChatBot-Gemini
   cd gemini-bot
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   Install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Application**:
   Use Uvicorn to run the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Interact with the Bot**:
   The bot listens for incoming messages on the `/callback` endpoint. Ensure your LINE Developer Console is configured to send events to this endpoint.

## Configuration

- **Environment Variables**:
  - `LINE_CHANNEL_SECRET`: Your LINE channel secret.
  - `LINE_CHANNEL_ACCESS_TOKEN`: Your LINE channel access token.

These can be set in a `.env` file in the root directory of the project.

## Dependencies

The project requires the following Python packages:
- `line-bot-sdk>=3.0.0`
- `fastapi`
- `uvicorn`
- `python-dotenv`
- `google-genai`
- `pydantic`

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. 
