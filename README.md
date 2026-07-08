# Global Consult presentation app

Single-page consulting presentation app for `global-consult.ro`, served by Passenger through `passenger_wsgi.py`.

## Local preview

```powershell
python scripts/serve.py
```

Open `http://localhost:8000`.

## SSH deployment

The server is expected to use SSH private/public key authentication. Your public key must be installed on the server, usually in `~/.ssh/authorized_keys` for the SSH user. Keep the private key on your machine and point `SSH_KEY` to it.

Copy `.deploy.env.example` to `.deploy.env` and fill in the server details.

```powershell
Copy-Item .deploy.env.example .deploy.env
notepad .deploy.env
.\scripts\deploy.ps1
```

Example `.deploy.env`:

```text
SSH_HOST=global-consult.ro
SSH_USER=your_ssh_user
SSH_PORT=22
REMOTE_PATH=/home/your_user/global-consult.ro
SSH_KEY=C:\Users\Iulian\.ssh\global-consult
```

The deployment script packages the app, uploads it with `scp`, extracts it on the server, and touches `tmp/restart.txt` so Passenger reloads the new version.

Expected server setup:

- SSH key access enabled for the hosting account.
- The matching public key is present in the server user's `~/.ssh/authorized_keys`.
- `REMOTE_PATH` points to the Passenger app directory for `global-consult.ro`.
- The domain document root serves this Passenger app.
- `python3` and `unzip` are available on the server.

For automatic deployments from GitHub, add these repository secrets and use `.github/workflows/deploy.yml`:

- `SSH_HOST`
- `SSH_USER`
- `SSH_PORT`
- `SSH_PRIVATE_KEY` with the full private key content, including the `BEGIN` and `END` lines.
- `REMOTE_PATH`

Pushing to `main` will deploy the latest version.

## Contact form email

The contact form posts to `/contact` and sends email from `office@global-consult.ro` to `office@global-consult.ro`.

For the zip/upload workflow, edit the SMTP constants at the top of `passenger_wsgi.py` before creating the zip:

```python
SMTP_HOST = "mail.global-consult.ro"
SMTP_PORT = 587
SMTP_USER = "office@global-consult.ro"
SMTP_PASSWORD = "your_mailbox_password"
SMTP_SECURITY = "starttls"
```

Use `SMTP_SECURITY = "ssl"` with `SMTP_PORT = 465` if your hosting provider gives SSL SMTP settings instead of STARTTLS.

The submitted visitor email is set as `Reply-To`, so replies go to the person who filled in the form while the message is still sent from `office@global-consult.ro`.
