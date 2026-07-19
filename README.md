<h1 align="center">VideoFlix Backend</h1>

<p align="center">A Django REST Framework backend for a video streaming platform. It supports user authentication, protected video access, background video processing, thumbnails, and HLS streaming in multiple resolutions.</p>

## Setup & Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Drangello/BE4VideoFlix.git
cd BE4VideoFlix
```

### 2. Create environment file

Create a local `.env` file from the template:

```bash
cp .env.template .env
```

### 3. Start Docker containers

```bash
docker compose up -d
```

### 4. Check the backend

```bash
docker compose exec web python manage.py check
```

> The API will be available at `http://127.0.0.1:8000/`.

## Video Processing

Videos are uploaded through the Django Admin.

After upload, select a video and run the admin action:

```text
Ausgewählte Videos verarbeiten
```

The backend creates:

- a thumbnail
- HLS playlists
- 480p, 720p, and 1080p video segments

## Architecture & Apps

| App | Description |
|---|---|
| **`auth_app`** | Registration, activation, login, logout, token refresh and password reset. |
| **`videos_app`** | Video model, admin upload, background processing, thumbnails and HLS streaming. |
| **`common`** | Shared helpers, responses and validators. |
| **`core`** | Project settings, URLs, and Docker-ready configuration. |

## Security & Permissions

- **Authentication:** Protected endpoints use JWT authentication via HttpOnly cookies.
- **Videos:** Video list, playlists, and segments require authentication.
- **Users:** Accounts must be activated before login.
- **Tokens:** Refresh tokens are invalidated on logout.
- **Media:** Uploaded and generated media files are not committed to Git.

## Main API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/register/` | Register a new inactive user. |
| `GET` | `/api/activate/<uidb64>/<token>/` | Activate a user account. |
| `POST` | `/api/login/` | Login and set JWT cookies. |
| `POST` | `/api/logout/` | Logout and clear cookies. |
| `POST` | `/api/token/refresh/` | Refresh access token. |
| `POST` | `/api/password_reset/` | Request password reset email. |
| `POST` | `/api/password_confirm/<uidb64>/<token>/` | Set a new password. |
| `GET` | `/api/video/` | List processed videos. |
| `GET` | `/api/video/<id>/<resolution>/index.m3u8` | Get HLS playlist. |
| `GET` | `/api/video/<id>/<resolution>/<segment>` | Get HLS segment. |

## Testing

```bash
docker compose exec web python manage.py check
```

## Notes

Do not commit uploaded videos, generated thumbnails, HLS playlists, or HLS segments.
