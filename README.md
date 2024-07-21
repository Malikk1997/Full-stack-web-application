Overview
This project demonstrates a comprehensive full-stack application that integrates a web-based frontend with a robust backend server, leveraging GPU acceleration for intensive processing tasks. The solution encompasses:

Frontend Development: Utilized HTML, CSS, and JavaScript to create an intuitive user interface.
Backend Development: Implemented a server using Python and Flask to handle API requests and interact with the GPU.
GPU Processing: Connected the backend to a GPU server for high-performance computation.
Result Integration: Displayed the processed results on the frontend UI.

Architecture - 

Frontend
Technologies: HTML, CSS, JavaScript
Description: Developed a responsive and interactive web page using HTML for structure, CSS for styling, and JavaScript for dynamic behavior and asynchronous communication with the backend server.
Backend
Technologies: Python, Flask
Description: Built a Flask-based API server to handle incoming requests, manage file uploads, and interact with the GPU server. The backend processes the uploaded media files and returns the results.
GPU Server Integration
Description: Configured the backend to communicate with a GPU server for processing. The GPU server performs resource-intensive tasks and returns processed results to the Flask server.
Result Display
Description: Implemented functionality in the frontend to display processed output received from the backend. The results are dynamically updated on the user interface, providing real-time feedback on the processing status.

Features
User Interface: Allows users to upload media files and initiate processing.
Backend API: Handles file uploads, processing requests, and communication with the GPU server.
GPU Acceleration: Leverages GPU for efficient processing of media files.
Result Presentation: Displays processed results on the web page with status updates.
