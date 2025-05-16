# System Architecture Diagram

This diagram represents the system architecture for the devin_tokunou project.

## Components

- **Windows**: Host operating system
- **WSL (Windows Subsystem for Linux)**: Linux compatibility layer
- **Ubuntu**: Linux distribution running on WSL
- **FastAPI**: Python web framework for building APIs
- **Database**: Database system running on Ubuntu
- **OpenAI API**: External API service for AI capabilities

## Diagram

```mermaid
graph TD
    A[Windows] --> B[WSL]
    B --> C[Ubuntu]
    C --> D[FastAPI]
    C --> E[Database]
    D <--> E
    D --> F[OpenAI API]
    
    style A fill:#dae8fc,stroke:#6c8ebf
    style B fill:#f5f5f5,stroke:#666666
    style C fill:#ffe6cc,stroke:#d79b00
    style D fill:#d5e8d4,stroke:#82b366
    style E fill:#fff2cc,stroke:#d6b656
    style F fill:#f8cecc,stroke:#b85450
```

## Connections

- **FastAPI <--> Database**: Bidirectional communication for data storage and retrieval
- **FastAPI --> OpenAI API**: FastAPI sends requests to OpenAI API for AI capabilities

## Environment

The application is hosted on Ubuntu running within WSL on a Windows host. Both FastAPI and the database are running on the same Ubuntu environment, while the OpenAI API is an external service.
