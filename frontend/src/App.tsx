import React, { useState } from "react";
import { queryIndex } from "./apis/queryIndex";
import { insertDocument } from "./apis/insertDocument";
import "bootstrap/dist/css/bootstrap.min.css";

const App = () => {
    const [file, setFile] = useState<File | null>(null); // For holding the selected file
    const [message, setMessage] = useState(""); // For showing upload status messages
    const [query, setQuery] = useState(""); // For holding the query input
    const [answer, setAnswer] = useState(""); // For displaying the query result

    // Function to handle file upload
    const handleFileUpload = async () => {
        try {
            if (!file) {
                setMessage("No file selected!");
                return;
            }

            setMessage("Uploading...");
            await insertDocument(file); // Call the API to upload the file
            setMessage("File uploaded successfully!");
        } catch (error) {
            console.error("Error uploading file:", error);
            setMessage("Error uploading file.");
        }
    };

    // Function to handle query submission
    const handleQuerySubmit = async () => {
        try {
            if (!query) {
                setAnswer("Please enter a query.");
                return;
            }

            setAnswer("Processing your query...");
            const response = await queryIndex(query); // Call the API to query the index
            setAnswer(response.answer);
        } catch (error) {
            console.error("Error querying index:", error);
            setAnswer("Error processing query.");
        }
    };

    return (
        <div className="container mt-5">
            <div className="card shadow-lg p-4" style={{ maxWidth: "600px", margin: "0 auto", borderRadius: "15px" }}>
                <h2 className="text-center mb-4" style={{ color: "#4a90e2" }}>CKS RAG APP</h2>

                {/* Query Section */}
                <div className="mb-4">
                    <h4>Query the Index</h4>
                    <p className="text-muted">Type your query and click "Submit Query" to get an answer.</p>
                    <div className="d-flex">
                        <input
                            type="text"
                            className="form-control"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Enter your query"
                        />
                        <button
                            className="btn btn-primary ml-2"
                            onClick={handleQuerySubmit}
                            style={{ borderRadius: "10px" }}
                        >
                            Submit Query
                        </button>
                    </div>
                    {answer && <p className="mt-3 text-center"><strong>Answer:</strong> {answer}</p>}
                </div>

                <hr />

                {/* File Upload Section */}
                <div>
                    <h4>Upload a File</h4>
                    <p className="text-muted">Choose a file and click "Upload File" to add it to the index.</p>
                    <div className="d-flex flex-column align-items-center">
                        <input
                            type="file"
                            id="file-upload"
                            style={{ display: "none" }}
                            onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
                        />
                        <label
                            htmlFor="file-upload"
                            className="btn btn-outline-primary btn-lg mb-3"
                            style={{
                                width: "80%",
                                textAlign: "center",
                                padding: "10px 20px",
                                borderRadius: "10px",
                            }}
                        >
                            Choose File
                        </label>
                        <button
                            className="btn btn-primary btn-lg"
                            onClick={handleFileUpload}
                            disabled={!file}
                            style={{
                                width: "80%",
                                padding: "10px 20px",
                                borderRadius: "10px",
                            }}
                        >
                            Upload File
                        </button>
                    </div>
                    {file && (
                        <p className="mt-3 text-center">
                            <strong>Selected File:</strong> {file.name}
                        </p>
                    )}
                    {message && (
                        <div
                            className="alert alert-info mt-4 text-center"
                            style={{ fontSize: "16px", fontWeight: "bold" }}
                        >
                            {message}
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default App;
