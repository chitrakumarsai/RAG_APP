# RAG-Based LLM Full-Stack Application<br>

This is a full-stack web application that enables users to upload documents, query an index built from those documents,<br> and retrieve responses powered by a Large Language Model (LLM) using **Retrieval-Augmented Generation (RAG)**.
<br>
## The application consists of:<br>

* **Frontend**: A React-based user interface.<br>
* **Backend**: A Flask API server that interacts with the index server.<br>
* **Index Server**: A Python-based service managing document indexing and query processing using LlamaIndex.<br>

## Features<br>

* Upload files to build an index.<br>
* Query the indexed documents using natural language.<br>
* Retrieve results with relevant context provided by LlamaIndex.<br>

## Technologies Used<br>

### **Backend** <br>
* Python 3.11<br>
* **Flask:** For serving API requests.<br>
* **Flask-CORS:** For cross-origin requests.<br>
* **LlamaIndex:** To manage document indexing and querying.<br>
### **Frontend**
* **React:** For building the user interface.<br>
* **Bootstrap:** For styling the application.<br>
## Deployment<br>
**Docker:** For containerizing and deploying the application.<br>
## Project Structure<br>
```
RAG_APP/
├── backend/                   # Backend Flask application
│   ├── app.py                 # Flask API server
│   ├── index_server.py        # Index server for LlamaIndex
│   ├── requirements.txt       # Backend dependencies
├── frontend/                  # React frontend
│   ├── src/                   # Source code for the frontend
│   ├── Dockerfile             # Dockerfile for frontend
│   ├── package.json           # Frontend dependencies
├── data/                      # Directory for uploaded files
├── storage/                   # Directory for storing index files
├── .env                       # Environment variables
├── docker-compose.yml         # Docker Compose configuration
└── README.md                  # This README file
```
## Installation and Setup<br>

## Prerequisites<br>
* Docker and Docker Compose installed on your machine.<br>
* An OpenAI API Key (required for LlamaIndex).<br>
## Environment Variables<br>
* Create a `.env` file in the project root and include your OpenAI API key:<br>
* `OPENAI_API_KEY=your_openai_api_key`<br>
## Steps to Run the Application<br>
* Clone the Repository:<br>
* `git clone <repository_url>`<br>
* `cd RAG_APP`<br>
## Build and Start the Containers:<br>
* `docker-compose up --build`<br>
## Access the Application:<br>
* **Frontend:** `http://localhost:3000`<br>
* **Backend (API):** `http://localhost:5001`<br>
## API Endpoints<br>

### Query Index<br>
* **URL:** `/query`<br>
* **Method:** `GET`<br>
* **Parameters:** `text` (required): The query string.<br>
#### Example:<br>
```
curl "http://localhost:5001/query?text=What%20is%20a%20transformer"
```
## Upload File<br>
* **URL:** `/uploadFile`<br>
* **Method:** `POST`<br>
* **Parameters:** `file` (required): The file to upload.<br> <br>

## Example:<br>
```
curl -X POST -F "file=@example.txt" http://localhost:5001/uploadFile
```
## Frontend Features<br>

* **Upload Document:** Use the "Upload File" button to add documents to the index.<br>
* **Query Index:** Enter your query in the text box and press "Submit Query" to retrieve results.<br>
Troubleshooting<br>

## Common Issues<br>
#### Port Conflicts:<br>
* Ensure ports 3000, 5001, and 5602 are not in use.<br>
* Update `docker-compose.yml` or application code to use alternative ports if needed.<br>
#### Timeout Connecting to index_server:<br>
* Verify that the `index_server` is running and accessible on port 5602.<br>
#### Check Docker logs for errors:<br>
* docker-compose logs index_server<br>
#### Empty Replies from Server:<br>
* Check if `.env` contains a valid OpenAI API key.<br>
* Ensure the `index_server` is initialized with documents in the `/app/data` directory.<br>
## Development<br>

### Backend<br>
* Install dependencies:<br>
`pip install -r backend/requirements.txt`<br>
* Run the Flask API server:<br>
`python backend/app.py`<br>
### Frontend<br>
* Install dependencies:<br>
`cd frontend`<br>
`npm install`<br>
* Start the React development server:<br>
`npm start`<br>
## Contributing<br>

### Contributions are welcome! Please follow these steps:<br>

* Fork the repository.<br>
* Create a new branch for your feature or bug fix.<br>
* Submit a pull request with a detailed explanation of your changes.<br>
### License<br>

This project is licensed under the MIT License. See the LICENSE file for details.
