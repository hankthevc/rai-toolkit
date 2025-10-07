# Deployment Guide

This guide covers deploying the rai-toolkit Streamlit app to production environments.

## Streamlit Cloud Deployment (Recommended for Demo/Portfolio)

Streamlit Cloud offers free hosting for public GitHub repositories. Follow these steps to deploy:

### Prerequisites

1. Push your rai-toolkit repository to GitHub
2. Create a free account at [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub account to Streamlit Cloud

### Deployment Steps

1. **Navigate to Streamlit Cloud Dashboard**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"

2. **Configure App Settings**
   - **Repository:** `yourusername/rai-toolkit`
   - **Branch:** `main`
   - **Main file path:** `project1_risk_framework/app.py`
   - **App URL:** Choose a custom subdomain (e.g., `rai-toolkit-demo`)

3. **Advanced Settings (Optional)**
   - Python version: `3.11`
   - No additional secrets required for demo mode

4. **Deploy**
   - Click "Deploy"
   - Wait 2-3 minutes for build completion
   - Your app will be live at `https://yourusername-rai-toolkit.streamlit.app`

### Post-Deployment

**Generate Sample Data for Analytics:**

The analytics dashboard requires sample data. Since Streamlit Cloud doesn't persist the `data/` folder, you have two options:

**Option 1: Commit sample data to repo (for demo purposes)**
```bash
python scripts/generate_sample_data.py --count 150
git add data/sample_assessments.json
git commit -m "Add sample analytics data"
git push
```

**Option 2: Generate on-the-fly (recommended for production)**
Modify `pages/1_📊_Analytics.py` to generate sample data if the file doesn't exist:

```python
if not data_path.exists():
    # Generate sample data on first load
    from scripts.generate_sample_data import generate_assessments
    assessments = generate_assessments(150)
    data_path.parent.mkdir(parents=True, exist_ok=True)
    with data_path.open('w') as f:
        json.dump(assessments, f)
```

### Updating the Deployment

Streamlit Cloud auto-deploys on every git push to the configured branch. To update:

```bash
git add .
git commit -m "Update risk assessment framework"
git push origin main
```

Changes appear live within 1-2 minutes.

---

## Alternative Deployment Options

### Docker Container

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Generate sample data
RUN python scripts/generate_sample_data.py --count 150

EXPOSE 8501

CMD ["streamlit", "run", "project1_risk_framework/app.py", "--server.address", "0.0.0.0"]
```

Build and run:

```bash
docker build -t rai-toolkit .
docker run -p 8501:8501 rai-toolkit
```

Access at `http://localhost:8501`

---

### Heroku Deployment

1. Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run project1_risk_framework/app.py
   ```

2. Create `setup.sh`:
   ```bash
   #!/bin/bash
   mkdir -p ~/.streamlit/
   echo "[server]
   headless = true
   port = $PORT
   enableCORS = false
   " > ~/.streamlit/config.toml

   python scripts/generate_sample_data.py --count 150
   ```

3. Deploy:
   ```bash
   heroku create rai-toolkit
   git push heroku main
   ```

---

### AWS EC2 / Cloud VM

1. SSH into your instance
2. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3-pip
   ```

3. Clone and setup:
   ```bash
   git clone https://github.com/yourusername/rai-toolkit.git
   cd rai-toolkit
   pip3 install -r requirements.txt
   python3 scripts/generate_sample_data.py --count 150
   ```

4. Run with nohup or systemd:
   ```bash
   nohup streamlit run project1_risk_framework/app.py --server.port 8501 &
   ```

5. Configure nginx reverse proxy (optional):
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

---

## Security Considerations

### For Public Demos
- ✓ Sample data contains no real PII
- ✓ Decision Records are ephemeral (download only, no storage)
- ✓ No authentication required (publicly accessible)

### For Internal/Production Use

**Add Authentication:**

Use Streamlit's built-in auth or deploy behind SSO:

```python
# Add to app.py
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    credentials,
    cookie_name='rai_toolkit_auth',
    key='random_signature_key'
)

name, authentication_status, username = authenticator.login('Login', 'main')

if not authentication_status:
    st.stop()
```

**Data Persistence:**

Connect to database instead of JSON files:

```python
# Replace file-based storage with PostgreSQL/MongoDB
import psycopg2

conn = psycopg2.connect(os.environ['DATABASE_URL'])
df = pd.read_sql("SELECT * FROM assessments", conn)
```

**Audit Logging:**

Track all assessments:

```python
import logging

logging.basicConfig(filename='audit.log', level=logging.INFO)
logging.info(f"Assessment created: {assessment_id} by {owner}")
```

---

## Performance Optimization

### Caching

The app already uses `@st.cache_data` for policy pack loading. For production, add:

```python
@st.cache_resource
def init_database_connection():
    return create_db_pool()
```

### Resource Limits

Streamlit Cloud free tier:
- 1 GB RAM
- 1 CPU core
- Sleeping after 7 days of inactivity

For high-traffic deployments, upgrade to Streamlit Cloud Teams or self-host.

---

## Monitoring & Observability

### Streamlit Cloud Built-in Metrics

View usage stats in the Streamlit Cloud dashboard:
- Page views
- Active users
- Error rates

### Custom Telemetry (Production)

Add `streamlit-analytics` or integrate with tools like Datadog:

```bash
pip install streamlit-analytics
```

```python
import streamlit_analytics

with streamlit_analytics.track():
    # Your app code
```

---

## Troubleshooting

### App Won't Start

**Error:** "No module named 'common'"

**Fix:** Ensure `common/` directory exists and contains `__init__.py`:
```bash
ls -la common/__init__.py
```

### Analytics Page Shows "No Data"

**Error:** `data/sample_assessments.json` not found

**Fix:** Generate sample data:
```bash
python scripts/generate_sample_data.py --count 150
```

Or commit the generated file to git (see Streamlit Cloud section above).

### Slow Performance

**Symptom:** App takes >5 seconds to load

**Fix:** Check caching decorators are applied to expensive functions:
- `load_policy_packs()` should use `@st.cache_data`
- `load_assessment_data()` should use `@st.cache_data`

---

## Next Steps After Deployment

1. **Add Custom Domain (Streamlit Cloud Teams)**
   - Upgrade to Teams plan ($20/month)
   - Configure CNAME: `demo.yourdomain.com -> xxx.streamlit.app`

2. **Set Up CI/CD for Automated Testing**
   - GitHub Actions already configured (`.github/workflows/ci.yml`)
   - Add deployment workflow to run tests before merging

3. **Integrate with Ticketing System**
   - Replace download button with Jira/ServiceNow API calls
   - Auto-create tickets with Decision Record attachments

4. **Enable User Feedback**
   - Add `st.feedback()` widget for control recommendations
   - Track satisfaction metrics per tier

---

## Support

For deployment issues:
- Streamlit Cloud: [docs.streamlit.io](https://docs.streamlit.io)
- Project issues: [github.com/yourusername/rai-toolkit/issues](https://github.com/yourusername/rai-toolkit/issues)

