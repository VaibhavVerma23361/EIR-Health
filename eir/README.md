# Eir - AI Medical Diagnosis System

An advanced multimodal AI system for medical diagnosis using 7 Ollama models.

## Architecture

1. **Domain Classification Model** - Identifies the medical domain
2. **5 Parallel Analysis Models** - Perform concurrent diagnosis
3. **Best Output Selection** - Returns the most accurate diagnosis

## Tech Stack

- **Frontend**: Next.js 15 + TypeScript + Tailwind CSS
- **Backend**: Flask/FastAPI (to be deployed on GPU server)
- **Models**: Ollama (running on GPU server)
- **Deployment**: Vercel (frontend) + GPU Server (backend)

## Getting Started

### Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## Deployment

### Frontend (Vercel)
1. Push to GitHub
2. Connect repository to Vercel
3. Deploy automatically

### Backend (GPU Server)
Instructions coming soon...

## Current Status

- ✅ UI Design Complete (with mock API)
- ⏳ Backend API Wrapper (pending)
- ⏳ Model Integration (in progress by team)
- ⏳ Production Deployment (pending)

## Features

- Clean, professional medical interface
- Real-time diagnosis processing
- Confidence scoring
- Domain classification
- Responsive design
- Error handling

## Note

Currently using mock API responses. Will be connected to actual Ollama models once backend is ready.
