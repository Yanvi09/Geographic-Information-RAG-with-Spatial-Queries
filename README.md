
# 🌍 GeoRAG Intelligence Demo — Environmental & Urban Planning AI
A next-generation application for environmental monitoring, disaster planning, and smart city development.  
Combines geospatial visualization, geospatial intelligence, and AI-driven semantic search to help planners, researchers, and policy-makers make data-driven decisions.

Deployment-Link: https://github.com/Yanvi09/Geographic-Information-RAG-with-Spatial-Queries

2. Tech Stack
Frontend

->React + Vite — fast, modular frontend setup.
->@react-three/fiber — React renderer for three.js.
->@react-three/drei — ready-to-use helpers for 3D scenes.
->three.js — industry-standard WebGL 3D graphics library.

Backend (Python)

->GeoPandas — geospatial data analysis.
=->Shapely — geometric operations.
->Folium — interactive maps.
->Sentence Transformers — embedding generation for semantic search.
->ChromaDB — vector database for fast similarity queries.
->OpenAI API — natural language understanding & generation.
->Streamlit — web UI for backend visualization.
->Pillow — image processing utilities.

3. ```Project Structure
   project-root/
│
├── frontend/                # React Three Fiber app
│   ├── src/
│   │   ├── components/      # Reusable 3D and UI components
│   │   ├── assets/          # Models, textures, images
│   │   └── main.jsx         # App entry
│   ├── index.html
│   └── package.json
│
├── backend/                 # Python API & AI/Geo logic
│   ├── app.py               # Streamlit or FastAPI entry point
│   ├── data/                # GeoJSON / shapefiles
│   ├── models/              # Saved embeddings/models
│   ├── requirements.txt     # Python dependencies
│   └── utils/               # Helper scripts
│
└── README.md  ```

4. Installation
Frontend
cd frontend
npm install
npm run dev

5.Backend
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py

6. Dependencies
Frontend (package.json)
{
  "dependencies": {
    "@react-three/drei": "^10.6.1",
    "@react-three/fiber": "^9.3.0",
    "three": "^0.179.1"
  }
}

7.Backend (requirements.txt)
->geopandas
->shapely
->folium
->sentence-transformers
->chromadb
->openai
->streamlit
->pillow

7.1. Environment Variables

Create .env in backend/:

OPENAI_API_KEY=your_openai_key
CHROMADB_PATH=./backend/models/chroma

7.2.## Prerequisites
- **Node.js** ≥ 18.x  
- **Python** ≥ 3.9  
- **pip** ≥ 21.0  
- **Git**

8. Running the Project

1>Start Backend

cd backend
streamlit run app.py

2>Start Frontend

cd frontend
npm run dev

9.Access:

->Frontend: http://localhost:5173
->Backend (Streamlit): http://localhost:8501

10.## Deployment
For public deployment, you can use:
- **Streamlit Cloud** for backend
- **Vercel** or **Netlify** for frontend

11. Future Enhancements

->Optional TailwindCSS for UI styling.
->Optional Axios for API calls.
->WebSocket support for real-time AI and map updates.
->Additional 3D asset pipeline integration.  



