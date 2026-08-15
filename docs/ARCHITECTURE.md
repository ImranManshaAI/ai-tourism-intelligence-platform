# AI Tourism Intelligence Platform — Architecture

## 1. Overview

The AI Tourism Intelligence Platform uses a single backend API that serves multiple client applications.

The backend is client-agnostic. Business logic and domain rules must remain inside the backend and must not depend on whether the request originated from web, mobile, or admin clients.

The backend is responsible for core application logic, data access, authentication, document processing, AI/RAG services, validation, security, and integration with external services.

Clients are responsible for presentation and user interaction.

---

## 2. Client Applications

The platform is designed to support:

- Public Web Application
- Future Mobile Application
- Admin Dashboard

All clients communicate with the same versioned backend API.

```text
                    AI Tourism Intelligence Platform
                               |
                        FastAPI Backend
                           /api/v1
                               |
          +--------------------+--------------------+
          |                    |                    |
          v                    v                    v
     Public Web          Mobile Application     Admin Dashboard
       Client                 Client                Client
```

The backend must not contain client-specific business logic.

The same domain services and API contracts should be reusable by web, mobile, and admin clients.

---

## 3. Backend Responsibilities

The backend is responsible for:

* Authentication and authorization
* Destination management
* Document management
* Document ingestion and processing
* Retrieval-Augmented Generation (RAG)
* AI Assistant responses
* Source and citation information
* Data validation
* Security controls
* Error handling
* Logging and observability
* Database access
* External AI service integration
* API versioning
* Production deployment and runtime configuration

Clients are responsible for presentation and user interaction.

---

## 4. API Architecture

The backend exposes a versioned REST API.

The current API version is:

```text
/api/v1
```

Example endpoints:

```text
GET  /api/v1/destinations
GET  /api/v1/destinations/{id}
POST /api/v1/assistant/query
```

The API must remain independent of the client platform.

A web client and mobile client must be able to consume the same endpoint when they require the same business operation.

---

## 5. API Versioning

All public API endpoints use:

```text
/api/v1
```

Breaking API changes must use a new API version rather than silently changing the existing contract.

For example:

```text
/api/v1/...
/api/v2/...
```

Existing clients using `/api/v1` must remain functional until a controlled migration is completed.

---

## 6. Standard API Response

Successful JSON responses use a consistent response envelope:

```json
{
  "data": {},
  "error": null
}
```

Collection responses use the same envelope:

```json
{
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 0,
    "total_pages": 0
  },
  "error": null
}
```

Error responses use:

```json
{
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
```

The error structure must remain consistent across authentication, destinations, documents, AI services, and future endpoints.

---

## 7. Authentication and Authorization

Protected endpoints use JWT Bearer authentication:

```http
Authorization: Bearer <access_token>
```

Phase 1 uses a single administrative role:

```text
admin
```

Public tourism endpoints do not require administrative authentication.

Administrative write operations require authentication and authorization.

Public registration must not be exposed as unrestricted self-registration.

Initial administrative accounts must be provisioned through a controlled process.

Future role-based access control may be introduced if TDCP confirms that multiple administrative tiers are required.

---

## 8. Core Phase 1 API Areas

The initial backend API includes:

### Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
```

`/auth/register` is restricted to controlled administrative provisioning.

### Destinations

```text
GET    /api/v1/destinations
GET    /api/v1/destinations/{id}

POST   /api/v1/destinations
PUT    /api/v1/destinations/{id}
DELETE /api/v1/destinations/{id}
```

Public users can read destinations.

Administrative users can create, update, and delete destinations.

### Documents

```text
POST /api/v1/documents/upload
GET  /api/v1/documents
```

Document management is restricted to administrative users.

### AI Assistant

```text
POST /api/v1/assistant/query
```

The endpoint accepts a user question and returns an AI-generated answer with source references for traceability.

The backend plan defines the Assistant flow as embedding the incoming question, retrieving relevant chunks from the vector store, constructing the prompt, calling Gemini, and returning the answer with source information.

---

## 9. Destination Data

The Phase 1 destination model contains:

* `id`
* `name`
* `description`
* `images`
* `opening_hours`
* `ticket_price`
* `facilities`
* `travel_tips`
* `latitude`
* `longitude`
* `embedding_id`
* `created_at`
* `updated_at`

The backend owns validation and persistence of destination data.

The frontend and mobile application must not implement separate business rules for destination validation.

---

## 10. Document and RAG Architecture

The document pipeline is responsible for:

1. PDF upload
2. File validation
3. Raw document storage
4. Text extraction
5. OCR fallback for scanned documents
6. Text cleaning
7. Chunking
8. Embedding generation
9. Vector storage
10. Retrieval during AI queries
11. Source traceability

The planned document pipeline uses:

```text
PDF
 |
 v
Validation
 |
 v
Raw Document Storage
 |
 v
Text Extraction
 |
 +-----> OCR fallback for scanned documents
 |
 v
Cleaning
 |
 v
Chunking
 |
 v
Embeddings
 |
 v
Chroma Vector Store
 |
 v
RAG Retrieval
 |
 v
Gemini
 |
 v
Source-Cited Answer
```

The backend plan specifies approximately 300–500 token chunks with approximately 50-token overlap for the initial pipeline.

The AI Assistant response must include source document or destination references for traceability.

---

## 11. Core Data and AI Services

The backend will integrate the following major components:

```text
                    FastAPI API
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
     PostgreSQL        Chroma         Gemini
          |              |              |
      Users/Admins    Documents       AI Answers
      Destinations    Chunks          + Sources
```

PostgreSQL is the primary relational data store.

Chroma is the initial vector store for the RAG pipeline.

Gemini is the planned external LLM service for AI generation.

The architecture should allow the vector store or AI provider to be replaced later without requiring client-side changes.

---

## 12. Mobile Compatibility

The backend is designed to support a future mobile application without requiring a separate mobile backend.

The mobile application will consume the same versioned REST API used by the web application.

The backend must not contain UI-specific logic such as:

```text
if web:
    ...

if mobile:
    ...
```

Client-specific presentation decisions belong to the respective client application.

The API should return domain data and business results rather than UI instructions.

---

## 13. Pagination

Collection endpoints should support pagination.

Example:

```text
GET /api/v1/destinations?page=1&page_size=20
```

Example response:

```json
{
  "data": {
    "items": [],
    "page": 1,
    "page_size": 20,
    "total": 0,
    "total_pages": 0
  },
  "error": null
}
```

Pagination prevents clients, particularly mobile clients, from downloading unnecessarily large datasets.

Pagination should be applied consistently to collection endpoints where appropriate.

---

## 14. Media and Images

APIs should return references or URLs for images and other media rather than unnecessarily transferring large binary assets through JSON responses.

Destination image handling should remain independent of the client platform.

Web and mobile clients should be able to consume the same image references.

The final production storage/CDN strategy will be selected during deployment planning.

---

## 15. Security Principles

The backend must follow these security principles:

* Never commit secrets to Git.
* Never store passwords in plaintext.
* Use secure password hashing.
* Never expose password hashes through API responses.
* Load secrets through environment/configuration management.
* Validate all external input.
* Validate uploaded files.
* Enforce authentication on protected endpoints.
* Enforce authorization server-side.
* Never trust frontend authorization checks as a security boundary.
* Never expose internal stack traces to clients.
* Never expose database exceptions to clients.
* Never expose filesystem paths to clients.
* Never expose API keys or other secrets.
* Apply appropriate request size limits.
* Apply appropriate file size and type restrictions.
* Apply rate limiting where appropriate.
* Use secure production configuration.
* Keep production credentials under TDCP-owned accounts where applicable.

---

## 16. Error Handling

The backend must use predictable HTTP status codes and the standard error response envelope.

Common status codes include:

```text
200  Successful request
201  Resource created
204  Successful deletion with no response body
400  Bad request
401  Authentication required or invalid
403  Authenticated but not authorized
404  Resource not found
409  Resource conflict
413  Request/file too large
415  Unsupported media type
422  Validation failure
429  Rate limit exceeded
500  Unexpected server error
```

Production responses must not expose internal implementation details.

---

## 17. Configuration and Secrets

Application configuration is centralized through the backend settings layer.

Local development may use a `.env` file.

The `.env` file must never be committed to Git.

A committed `.env.example` file will document required configuration variables without containing real secrets.

The backend plan identifies configuration such as:

```text
DATABASE_URL
GEMINI_API_KEY
JWT_SECRET
CHROMA_PERSIST_DIR
```

Production secrets must be supplied through the deployment environment or an appropriate secret-management mechanism.

Production credentials must be handed over under TDCP-owned accounts rather than remaining under personal developer accounts.

---

## 18. Observability and Reliability

The backend should be designed for controlled failure and operational visibility.

The production system should provide:

* Structured application logging
* Health checks
* Appropriate exception handling
* Request validation
* External service failure handling
* Database failure handling
* AI service failure handling
* Clear client-safe error responses
* Monitoring and operational logs where supported by the deployment environment

The `/health` endpoint provides the initial application health check.

---

## 19. Deployment Architecture

The production deployment is planned around containerized services.

The backend will eventually provide its own Dockerfile.

The planned production architecture includes:

```text
                    Internet
                       |
                       v
                     Nginx
                       |
          +------------+------------+
          |                         |
          v                         v
     Frontend App              Backend API
                                    |
                     +--------------+--------------+
                     |              |              |
                     v              v              v
                PostgreSQL        Chroma         Gemini
```

The final deployment infrastructure and hosting provider will be selected based on what TDCP can maintain after handover.

---

## 20. CI/CD

The project will use GitHub-based version control with feature branches and reviewed pull requests.

Production hardening includes a basic GitHub Actions workflow that:

1. Runs tests.
2. Builds the application.
3. Validates the project on pushes to `main`.

Deployment automation will be introduced after the core application is stable.

---

## 21. Repository and Development Workflow

Development follows small, verifiable checkpoints:

```text
Implement
   |
   v
Run tests / validation
   |
   v
Inspect Git changes
   |
   v
Commit
   |
   v
Push
   |
   v
Integration / review
```

Feature work should use dedicated branches.

Changes should be reviewed before merging into `main`.

Small commits should represent meaningful, verified changes.

---

## 22. Client Integration Principle

The frontend and future mobile application should communicate with the backend through a centralized API client layer.

Clients should not scatter direct API calls throughout UI components.

The client architecture should provide a single place for:

* Base API URL
* Authentication headers
* Request handling
* Response parsing
* Error handling
* API versioning

This allows the backend contract to remain stable while client implementations evolve independently.

---

## 23. Architecture Evolution

The architecture is intentionally modular.

Phase 1 focuses on:

* Authentication
* Destinations
* Documents
* RAG
* AI Assistant

Phase 2 adds:

* Semantic search
* Hotels
* Events
* Trip Planner

Phase 3 adds production hardening such as:

* Additional roles if confirmed by TDCP
* Analytics
* Containerization
* CI/CD
* Production deployment
* Secure production environment configuration

The vector database should only be migrated from Chroma to another solution such as Qdrant if a real scaling requirement justifies the migration.

New functionality should be added without unnecessarily coupling the backend to a particular client platform.

---

## 24. High-Level System Architecture

```text
                         AI Tourism Intelligence Platform
                                      |
                                Client Layer
                                      |
             +------------------------+------------------------+
             |                        |                        |
             v                        v                        v
       Public Web              Future Mobile             Admin UI
             |                        |                        |
             +------------------------+------------------------+
                                      |
                                      v
                              FastAPI /api/v1
                                      |
        +-----------------------------+-----------------------------+
        |                             |                             |
        v                             v                             v
   Auth & Users                 Destination Service           Document Service
        |                             |                             |
        v                             v                             v
   PostgreSQL                   PostgreSQL                 Storage + Processing
                                                                    |
                                                                    v
                                                               Chroma
                                                                    |
                                                                    v
                                                               RAG Service
                                                                    |
                                                                    v
                                                                  Gemini
                                                                    |
                                                                    v
                                                           Source-Cited Answer
```

The backend remains the single source of business logic and API contracts for all supported clients.

```

