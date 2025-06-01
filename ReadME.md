# AuthGuard

# AuthenticGaurd

A Django-based authentication project with email confirmation, ready to deploy on Render.

## Features

- Custom user model (`email` as username).
- Sign-up with email confirmation.
- Login/logout/reset password (password reset pages can be added similarly).
- Robust security (SSL redirect, HSTS, secure cookies).
- Environment-driven settings (via `.env`).
- Static files served via WhiteNoise.
- Ready to deploy on Render with PostgreSQL (via `DATABASE_URL`).

## Quickstart (Local)

1. **Clone** this repository:

   ```bash
   git clone <repo_url> AccountAuthProj
   cd AccountAuthProj
