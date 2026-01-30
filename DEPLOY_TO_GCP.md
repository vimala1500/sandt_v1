# Deploying Your Python Dash App to Google Cloud Run

## Complete Beginner's Guide

This guide will walk you through deploying the Stock Backtesting Dashboard to Google Cloud Run, step by step. Don't worry if you've never used Google Cloud Platform (GCP) before – we'll explain everything!

---

## Table of Contents

1. [What You'll Need](#what-youll-need)
2. [Part 1: Setting Up Google Cloud](#part-1-setting-up-google-cloud)
3. [Part 2: Installing and Configuring Google Cloud SDK](#part-2-installing-and-configuring-google-cloud-sdk)
4. [Part 3: Creating Your GCP Project](#part-3-creating-your-gcp-project)
5. [Part 4: Setting Up Docker](#part-4-setting-up-docker)
6. [Part 5: Deploying to Cloud Run](#part-5-deploying-to-cloud-run)
7. [Part 6: Optional - Adding Cloud SQL Database](#part-6-optional---adding-cloud-sql-database)
8. [Part 7: Managing Your Deployment](#part-7-managing-your-deployment)
9. [Troubleshooting](#troubleshooting)
10. [Cost Estimates](#cost-estimates)

---

## What You'll Need

Before we start, make sure you have:
- A computer with internet access
- A Google account (Gmail account)
- A credit card (for GCP - don't worry, we'll stay in the free tier!)
- About 30-60 minutes of time

**Why do you need a credit card?** Google requires it to verify your identity, but they won't charge you without your permission. New users get $300 in free credits, and Cloud Run has a generous free tier.

---

## Part 1: Setting Up Google Cloud

### Step 1.1: Create a Google Cloud Account

**Why?** You need a GCP account to use any Google Cloud services.

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Accept the Terms of Service
4. Click "Activate" to start your free trial
5. Fill in your billing information
   - Select your country
   - Choose "Individual" for account type
   - Enter your credit card details
   - Click "Start my free trial"

**What just happened?** You now have a Google Cloud account with $300 in free credits valid for 90 days.

### Step 1.2: Enable Billing

**Why?** Even though we're using free tier services, GCP requires an active billing account.

1. In the [Google Cloud Console](https://console.cloud.google.com), click the hamburger menu (☰) in the top-left
2. Navigate to **Billing**
3. If prompted, create a new billing account
4. Verify your billing account is active (you should see a green checkmark)

---

## Part 2: Installing and Configuring Google Cloud SDK

**What is the Cloud SDK?** It's a set of command-line tools that let you interact with Google Cloud from your computer's terminal.

### Step 2.1: Install Google Cloud SDK

#### For Windows:
1. Download the installer from [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
2. Run the installer (`GoogleCloudSDKInstaller.exe`)
3. Follow the installation wizard
4. Check both options:
   - "Start Google Cloud SDK Shell"
   - "Run `gcloud init`"
5. Click "Finish"

#### For Mac:
1. Open Terminal
2. Install Homebrew if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Google Cloud SDK:
   ```bash
   brew install --cask google-cloud-sdk
   ```

#### For Linux:
1. Open your terminal
2. Run these commands:
   ```bash
   curl https://sdk.cloud.google.com | bash
   exec -l $SHELL
   ```

### Step 2.2: Initialize the SDK

**Why?** This connects your local computer to your Google Cloud account.

1. Open your terminal (or Google Cloud SDK Shell on Windows)
2. Run:
   ```bash
   gcloud init
   ```
3. Follow the prompts:
   - Choose **"Log in with a new account"** (usually option 1)
   - This will open a browser window
   - Select your Google account
   - Click "Allow" to grant permissions
   - Close the browser tab and return to your terminal

**What just happened?** Your computer can now communicate with Google Cloud using your credentials.

### Step 2.3: Verify Installation

Run this command to check everything is working:
```bash
gcloud --version
```

You should see output showing the version numbers of various components.

---

## Part 3: Creating Your GCP Project

**What is a project?** In GCP, a project is a container for all your resources (apps, databases, etc.). Think of it as a folder that keeps everything organized.

### Step 3.1: Create a New Project

**Option A: Using Command Line (Recommended)**

1. Open your terminal
2. Create a project (replace `my-dash-app` with your preferred project ID):
   ```bash
   gcloud projects create my-dash-app-123 --name="Stock Dashboard"
   ```

   **Important:** 
   - Project IDs must be globally unique across all of Google Cloud
   - Use lowercase letters, numbers, and hyphens only
   - Between 6-30 characters
   - Example: `stock-dashboard-john-2024`

3. Set this as your active project:
   ```bash
   gcloud config set project my-dash-app-123
   ```

**Option B: Using Cloud Console**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the project dropdown at the top
3. Click "NEW PROJECT"
4. Enter a project name: "Stock Dashboard"
5. The project ID will auto-generate (you can customize it)
6. Click "CREATE"
7. Wait for the project to be created (takes about 30 seconds)
8. Select your new project from the dropdown

### Step 3.2: Link Billing to Your Project

**Why?** Projects need to be linked to a billing account to use most services (even free tier ones).

Using command line:
```bash
# List available billing accounts
gcloud billing accounts list

# Link billing to your project (replace BILLING_ACCOUNT_ID)
gcloud billing projects link my-dash-app-123 --billing-account=BILLING_ACCOUNT_ID
```

Or in Cloud Console:
1. Go to **Billing** in the left menu
2. Click "My Projects"
3. Find your project and click the three dots
4. Click "Change billing"
5. Select your billing account
6. Click "Set account"

### Step 3.3: Enable Required APIs

**Why?** GCP services are modular. You need to explicitly enable the services you want to use.

Enable Cloud Run and Container Registry:
```bash
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

**What do these services do?**
- `run.googleapis.com`: Cloud Run service for running containers
- `containerregistry.googleapis.com`: Storage for your Docker images
- `cloudbuild.googleapis.com`: Builds your Docker images in the cloud

This might take 1-2 minutes. You'll see a success message when done.

---

## Part 4: Setting Up Docker

**What is Docker?** Docker packages your application and all its dependencies into a "container" – a standardized unit that runs the same way everywhere.

**Why do we need it?** Cloud Run runs containerized applications. We need to package our Dash app into a Docker container.

### Step 4.1: Install Docker

#### For Windows:
1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Follow the installation wizard
4. Restart your computer when prompted
5. Start Docker Desktop from the Start menu
6. Wait for Docker to start (you'll see a green icon in the system tray)

#### For Mac:
1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Open the downloaded `.dmg` file
3. Drag Docker to your Applications folder
4. Open Docker from Applications
5. Grant necessary permissions
6. Wait for Docker to start (whale icon in menu bar will stop animating)

#### For Linux:
```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install docker.io

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to docker group (to run without sudo)
sudo usermod -aG docker $USER

# Log out and back in for changes to take effect
```

### Step 4.2: Verify Docker Installation

```bash
docker --version
```

You should see the Docker version number.

### Step 4.3: Test Docker

Run a simple test:
```bash
docker run hello-world
```

If you see a "Hello from Docker!" message, everything is working!

### Step 4.4: Understand the Dockerfile

**What is a Dockerfile?** It's a recipe that tells Docker how to build your application container.

Our project includes a `Dockerfile`. Let's look at what it does:

```dockerfile
FROM python:3.11-slim
```
- Starts with a lightweight Python 3.11 image

```dockerfile
WORKDIR /app
```
- Sets `/app` as the working directory inside the container

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```
- Copies and installs Python dependencies

```dockerfile
COPY . .
```
- Copies all application code into the container

```dockerfile
EXPOSE 8080
```
- Tells Docker the app will listen on port 8080 (Cloud Run's default)

```dockerfile
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:server
```
- Starts the application using Gunicorn (a production web server)

---

## Part 5: Deploying to Cloud Run

Now for the exciting part – deploying your app to the cloud!

### Step 5.1: Navigate to Your Project

Open your terminal and navigate to the project directory:
```bash
cd /path/to/sandt_v1
```

For example:
- Windows: `cd C:\Users\YourName\Projects\sandt_v1`
- Mac/Linux: `cd ~/Projects/sandt_v1`

### Step 5.2: Configure Docker for GCP

**Why?** This tells Docker to authenticate with Google Cloud so it can upload your container image.

```bash
gcloud auth configure-docker
```

When prompted, type `y` and press Enter.

### Step 5.3: Build Your Container Image

**What happens here?** Docker reads your Dockerfile and creates a container image with your app inside.

```bash
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard
```

**Important:** Replace `my-dash-app-123` with your actual project ID!

**What's happening?**
- `gcloud builds submit`: Sends your code to Google Cloud Build
- `--tag gcr.io/...`: Names your container image
- Google Cloud Build reads your Dockerfile and builds the image
- The image is stored in Google Container Registry (gcr.io)

This will take 3-5 minutes the first time. You'll see:
- Uploading source code
- Building the Docker image
- Pushing to Container Registry
- A success message with the image name

### Step 5.4: Deploy to Cloud Run

**The big moment!** Deploy your containerized app:

```bash
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --region us-central1 \
  --allow-unauthenticated
```

**Let's break this down:**
- `stock-dashboard`: The name of your Cloud Run service
- `--image`: The container image we just built
- `--region us-central1`: Deploy to the US Central region (choose one close to your users)
- `--allow-unauthenticated`: Allow public access without login

**Available regions:** `us-central1`, `us-east1`, `europe-west1`, `asia-east1`, etc.

You'll be asked:
```
Allow unauthenticated invocations to [stock-dashboard] (y/N)?
```
Type `y` and press Enter (this makes your app publicly accessible).

**Deployment takes 1-2 minutes.** When complete, you'll see:
```
Service [stock-dashboard] revision [stock-dashboard-00001-xyz] has been deployed and is serving 100 percent of traffic.
Service URL: https://stock-dashboard-xyz-uc.a.run.app
```

### Step 5.5: Access Your App

**Congratulations!** Your app is now live! 🎉

1. Copy the Service URL from the deployment output
2. Paste it in your web browser
3. Your Stock Backtesting Dashboard should load!

The URL format is:
```
https://[service-name]-[hash]-[region].a.run.app
```

**Bookmark this URL** – it's your permanent app address!

### Step 5.6: View Your Deployment in Cloud Console

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Make sure your project is selected at the top
3. You'll see your `stock-dashboard` service
4. Click on it to see:
   - Service URL
   - Revision history
   - Metrics (requests, latency, etc.)
   - Logs

---

## Part 6: Optional - Adding Cloud SQL Database

**When do you need this?** If your app needs to store data persistently (user accounts, saved backtests, etc.), you'll need a database.

**What is Cloud SQL?** A fully managed database service (MySQL, PostgreSQL, or SQL Server).

### Step 6.1: Enable Cloud SQL API

```bash
gcloud services enable sqladmin.googleapis.com
```

### Step 6.2: Create a Cloud SQL Instance

**What's an instance?** A dedicated database server running in Google Cloud.

Create a PostgreSQL instance:
```bash
gcloud sql instances create stock-dashboard-db \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --region=us-central1
```

**Options explained:**
- `stock-dashboard-db`: Name of your database instance
- `--database-version=POSTGRES_15`: PostgreSQL version 15
- `--tier=db-f1-micro`: Smallest instance (free tier eligible)
- `--region=us-central1`: Same region as your Cloud Run service

**This takes 5-10 minutes.** You'll see a progress indicator.

### Step 6.3: Set Root Password

```bash
gcloud sql users set-password postgres \
  --instance=stock-dashboard-db \
  --password=YOUR_SECURE_PASSWORD
```

**Important:** Choose a strong password! Replace `YOUR_SECURE_PASSWORD`.

### Step 6.4: Create a Database

```bash
gcloud sql databases create stockdata --instance=stock-dashboard-db
```

This creates a database named `stockdata` in your instance.

### Step 6.5: Connect Cloud Run to Cloud SQL

**Important Security Note:** For production deployments, use Google Secret Manager to store sensitive credentials securely. For this beginner guide, we'll use environment variables, but please upgrade to Secret Manager for production apps.

Get your instance connection name:
```bash
gcloud sql instances describe stock-dashboard-db --format="value(connectionName)"
```

This outputs something like: `my-dash-app-123:us-central1:stock-dashboard-db`

Re-deploy your Cloud Run service with database connection:
```bash
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --add-cloudsql-instances my-dash-app-123:us-central1:stock-dashboard-db \
  --update-env-vars DB_USER=postgres,DB_NAME=stockdata,INSTANCE_CONNECTION_NAME=my-dash-app-123:us-central1:stock-dashboard-db \
  --set-secrets=DB_PASS=db-password:latest
```

**What changed?**
- `--add-cloudsql-instances`: Connects your Cloud Run service to the database
- `--update-env-vars`: Sets environment variables your app can use to connect
- `--set-secrets`: Securely injects the database password from Secret Manager

**Setting up Secret Manager (Recommended):**
```bash
# Enable Secret Manager API
gcloud services enable secretmanager.googleapis.com

# Create a secret for the database password
echo -n "YOUR_SECURE_PASSWORD" | gcloud secrets create db-password --data-file=-

# Grant Cloud Run access to the secret
gcloud secrets add-iam-policy-binding db-password \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

**For beginners using environment variables (less secure):**
```bash
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --add-cloudsql-instances my-dash-app-123:us-central1:stock-dashboard-db \
  --update-env-vars DB_USER=postgres,DB_PASS=YOUR_SECURE_PASSWORD,DB_NAME=stockdata,INSTANCE_CONNECTION_NAME=my-dash-app-123:us-central1:stock-dashboard-db
```

### Step 6.6: Update Your Application Code

To use the database, you'll need to modify your Python code. Here's an example using SQLAlchemy:

1. Add to `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   sqlalchemy==2.0.23
   ```

2. Create a database utility file `utils/database.py`:
   ```python
   import os
   from sqlalchemy import create_engine
   
   def get_db_connection():
       """Create database connection using environment variables"""
       db_user = os.environ.get('DB_USER', 'postgres')
       db_pass = os.environ.get('DB_PASS', '')
       db_name = os.environ.get('DB_NAME', 'stockdata')
       instance_connection_name = os.environ.get('INSTANCE_CONNECTION_NAME', '')
       
       # For Cloud SQL, use Unix socket connection
       if instance_connection_name:
           connection_string = f"postgresql://{db_user}:{db_pass}@/{db_name}?host=/cloudsql/{instance_connection_name}"
       else:
           # For local development
           db_host = os.environ.get('DB_HOST', 'localhost')
           connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}"
       
       engine = create_engine(connection_string)
       return engine
   ```

3. Rebuild and redeploy following Steps 5.3-5.4

---

## Part 7: Managing Your Deployment

### Viewing Logs

**Why?** Logs help you debug issues and understand what's happening with your app.

```bash
# View recent logs (using current recommended approach)
gcloud alpha run services logs read stock-dashboard --region=us-central1

# Stream live logs
gcloud alpha run services logs tail stock-dashboard --region=us-central1
```

**Alternative using Cloud Logging:**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=stock-dashboard" --limit 50 --format json
```

Or in Cloud Console:
1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click your service
3. Click the "LOGS" tab

### Updating Your App

Made changes to your code? Deploy the update:

```bash
# Build new image
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard

# Deploy update
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --region us-central1
```

**Cloud Run creates a new revision** and automatically switches traffic to it.

### Scaling Configuration

Cloud Run auto-scales by default, but you can customize:

```bash
gcloud run services update stock-dashboard \
  --min-instances=0 \
  --max-instances=10 \
  --concurrency=80 \
  --memory=512Mi \
  --region=us-central1
```

**Options:**
- `--min-instances=0`: Scale to zero when not in use (saves money!)
- `--max-instances=10`: Maximum containers to run
- `--concurrency=80`: Max requests per container
- `--memory=512Mi`: Memory per container (256Mi, 512Mi, 1Gi, 2Gi, 4Gi)

### Deleting Your App

To delete the Cloud Run service:
```bash
gcloud run services delete stock-dashboard --region=us-central1
```

To delete the entire project (removes everything):
```bash
gcloud projects delete my-dash-app-123
```

**Warning:** Deleting a project is permanent!

---

## Troubleshooting

### Issue: "Permission denied" errors

**Solution:** Make sure you're logged in:
```bash
gcloud auth login
gcloud auth application-default login
```

### Issue: Build fails with "requirements.txt not found"

**Solution:** Make sure you're in the project directory:
```bash
pwd  # Check current directory
cd /path/to/sandt_v1
```

### Issue: App loads but shows errors

**Solution:** Check logs:
```bash
gcloud alpha run services logs tail stock-dashboard --region=us-central1
```

Look for Python errors or missing dependencies.

### Issue: "Service timeout" errors

**Solution:** Increase timeout:
```bash
gcloud run services update stock-dashboard \
  --timeout=300 \
  --region=us-central1
```

### Issue: Database connection fails

**Solution:** Verify:
1. Cloud SQL instance is running
2. Cloud Run has `--add-cloudsql-instances` configured
3. Environment variables are set correctly
4. Database credentials are correct

### Issue: "No data found for symbol" errors

**Symptoms:** Dashboard fails to fetch stock data (e.g., "No data found for symbol MSFT")

**Root Cause:** Network connectivity issues preventing access to Yahoo Finance API

**Solutions:**

1. **Enable egress connectivity:**
   ```bash
   gcloud run services update stock-dashboard \
     --vpc-egress all-traffic \
     --region=us-central1
   ```

2. **Check service logs for network errors:**
   ```bash
   gcloud run services logs tail stock-dashboard --region=us-central1
   ```
   Look for: "Connection refused", "DNS resolution", "Timeout", or "Max retries exceeded"

3. **Adjust timeout and retry parameters:**
   ```bash
   gcloud run services update stock-dashboard \
     --set-env-vars YFINANCE_TIMEOUT=60,YFINANCE_MAX_RETRIES=5 \
     --timeout=300 \
     --region=us-central1
   ```

4. **Test external connectivity:**
   ```bash
   # From Cloud Shell, test Yahoo Finance access
   curl -I https://query1.finance.yahoo.com/
   ```

5. **For VPC-restricted environments, use VPC connector:**
   ```bash
   # Create connector
   gcloud compute networks vpc-access connectors create stock-connector \
     --region=us-central1 \
     --network=default \
     --range=10.8.0.0/28
   
   # Update service
   gcloud run services update stock-dashboard \
     --vpc-connector=stock-connector \
     --vpc-egress=all-traffic \
     --region=us-central1
   ```

**Important:** Yahoo Finance API requires internet access. Ensure Cloud Run can reach:
- `query1.finance.yahoo.com`
- `query2.finance.yahoo.com`
- `fc.yahoo.com`

### Issue: Docker build is very slow

**Solution:** Check your `.dockerignore` file to exclude unnecessary files:
- `venv/`
- `.git/`
- `__pycache__/`
- Test files

---

## Cost Estimates

### Free Tier (Generous!)

**Cloud Run:**
- 2 million requests per month
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds of compute time
- All FREE

**Cloud SQL (if used):**
- f1-micro instance: ~$7-10/month
- 30 GB storage free
- Backups charged separately

### Typical Costs for Low Traffic

For a personal project with moderate traffic:
- Cloud Run: **$0-5/month** (likely $0 on free tier)
- Cloud SQL f1-micro: **$7-10/month**
- Storage: **< $1/month**

**Total: ~$8-15/month** (if using database)

### Cost Optimization Tips

1. **Scale to zero:** Use `--min-instances=0` so you're not charged when the app isn't used
2. **Choose the right region:** Pick one close to your users for better performance and lower egress costs
3. **Monitor usage:** Set up billing alerts in Cloud Console
4. **Stop unused services:** Delete resources you're not using

Set up a billing alert:
1. Go to [Cloud Console Billing](https://console.cloud.google.com/billing)
2. Click "Budgets & alerts"
3. Click "CREATE BUDGET"
4. Set threshold (e.g., $10/month)
5. Add your email for alerts

---

## Next Steps

Congratulations! You've successfully deployed your Dash app to Google Cloud Run! 🎉

**What you've learned:**
1. ✅ Set up Google Cloud Platform
2. ✅ Created a GCP project
3. ✅ Containerized a Python application with Docker
4. ✅ Deployed to Cloud Run
5. ✅ (Optional) Connected a Cloud SQL database
6. ✅ Managed and monitored your deployment

**Recommended next steps:**
1. Set up a custom domain name for your app
2. Add HTTPS (automatic with Cloud Run)
3. Implement user authentication
4. Set up CI/CD for automatic deployments
5. Monitor performance metrics
6. Implement caching for better performance

**Useful Resources:**
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Dash Documentation](https://dash.plotly.com/)
- [Google Cloud Free Tier](https://cloud.google.com/free)

**Need help?** 
- Check [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-run)
- Visit [Google Cloud Community](https://cloud.google.com/community)
- Read the [Cloud Run troubleshooting guide](https://cloud.google.com/run/docs/troubleshooting)

---

## Summary of Key Commands

```bash
# Initial setup
gcloud init
gcloud projects create my-dash-app-123
gcloud config set project my-dash-app-123
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --region us-central1 \
  --allow-unauthenticated

# View logs
gcloud alpha run services logs tail stock-dashboard --region=us-central1

# Update app
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --region us-central1
```

---

**Happy deploying!** 🚀
