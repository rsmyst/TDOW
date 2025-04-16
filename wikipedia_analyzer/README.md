# Wikipedia Analyzer

A full-stack application that analyzes connections between Wikipedia articles and finds the shortest path between any two articles. Visualizes the "Six Degrees of Wikipedia" concept by showing how articles are connected via hyperlinks.

## Project Overview

The Wikipedia Analyzer consists of:

1. A React/Next.js frontend that provides an intuitive interface for finding paths between articles
2. A Flask backend that handles graph processing and path-finding algorithms
3. A dataset of Wikipedia articles (nodes) and their connections (edges)

## Getting Started

### Prerequisites

- Node.js 18+ and npm for the frontend
- Python 3.9+ for the backend
- Data files (provided in the `/data` directory)

### Installation

#### Backend Setup

1. Navigate to the project root
2. Create a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

#### Frontend Setup

1. Navigate to the `wikipedia_analyzer` directory:
   ```bash
   cd wikipedia_analyzer
   ```
2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

#### Start the Backend Server

1. From the project root, run:
   ```bash
   cd backend
   python server.py
   ```
2. The server will start on http://localhost:8000

#### Start the Frontend Server

1. From the `wikipedia_analyzer` directory:
   ```bash
   npm run dev
   ```
2. The frontend will be available at http://localhost:3000

## Architecture

### Frontend (Next.js)

The frontend is built with Next.js and uses:

- **TypeScript** for type safety
- **Framer Motion** for smooth animations
- **Tailwind CSS** for responsive styling

Key components:

- Main search interface with autocomplete for article selection
- Path visualization with animations for transitions between articles
- Statistics display showing information about the Wikipedia graph

File structure:

- `/src/app/page.tsx` - Main application component with search interface and path visualization
- `/src/app/layout.tsx` - Application layout component
- `/src/app/globals.css` - Global styles

### Backend (Flask)

The backend is built with Flask and uses:

- **NetworkX** for graph processing and shortest path algorithms
- **Flask-CORS** for cross-origin requests

Key endpoints:

- `/suggest` - Provides autocomplete suggestions for articles
- `/find-path` - Finds the shortest path between two Wikipedia articles
- `/path-statistics` - Returns precomputed statistics about the graph

Main components:

- `server.py` - Main Flask application with API endpoints
- `path_statistics.py` - Script for precomputing graph statistics

### Data

The application uses two main data files:

- `data/nodes.txt` - List of Wikipedia article titles (4,593 articles)
- `data/edges.txt` - Article connections via hyperlinks (over 100,000 connections)

Data structure:

- Nodes are represented by article titles
- Edges are represented by pairs of node indices

## Features

- **Article Search**: Type-ahead search for finding Wikipedia articles
- **Path Finding**: Discover the shortest path between any two Wikipedia articles
- **Path Visualization**: Visual representation of the path between articles
- **Graph Statistics**: View statistics about the Wikipedia graph, including:
  - Average path length
  - Distribution of path lengths
  - Graph diameter (longest shortest path)
  - Number of nodes and edges
  - Connected components analysis

## Technical Details

### Graph Processing

The application uses NetworkX to:

1. Load the graph from data files
2. Find shortest paths using Dijkstra's algorithm
3. Calculate graph statistics like diameter and connected components

### Performance Optimizations

- Article suggestions are limited to 10 results for faster rendering
- Path statistics are precomputed and saved to a JSON file
- Graph diameter calculation uses approximation algorithms for larger graphs

### Testing

The backend includes test files:

- `test_graph.py` - Tests for graph loading and processing
- `test_server.py` - Tests for API endpoints
- `run_tests.py` - Script to run all tests

Run tests with:

```bash
cd backend
python run_tests.py
```

## Deployment

The application can be deployed using:

- **Backend**: Gunicorn/uWSGI with Nginx for the Flask API
- **Frontend**: Vercel, Netlify or any Next.js-compatible hosting

## License

This project is open source and available under the MIT license.
