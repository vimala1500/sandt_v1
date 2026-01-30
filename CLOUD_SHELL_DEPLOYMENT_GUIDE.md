# Deploy to Google Cloud Using Only Cloud Shell

## Complete Step-by-Step Guide for Beginners

This guide will show you how to deploy the Stock Backtesting Dashboard to Google Cloud Run using **only your web browser** and Google Cloud Shell. No local installations required!

**What is Google Cloud Shell?** It's a free, browser-based terminal that comes pre-installed with all the tools you need (gcloud, docker, git, etc.). You can access it from anywhere with just a browser.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Access Google Cloud Shell](#step-1-access-google-cloud-shell)
3. [Step 2: Set Up Your GCP Project](#step-2-set-up-your-gcp-project)
4. [Step 3: Clone the Repository](#step-3-clone-the-repository)
5. [Step 4: Build Docker Image](#step-4-build-docker-image)
6. [Step 5: Push to Container Registry](#step-5-push-to-container-registry)
7. [Step 6: Deploy to Cloud Run](#step-6-deploy-to-cloud-run)
8. [Step 7: Access Your Deployed App](#step-7-access-your-deployed-app)
9. [Managing Your Deployment](#managing-your-deployment)
10. [Troubleshooting](#troubleshooting)
11. [Cost Information](#cost-information)

---

## Prerequisites

Before starting, you need:

- ✅ A Google account (Gmail)
- ✅ A web browser (Chrome, Firefox, Safari, or Edge)
- ✅ A Google Cloud Platform account with billing enabled
  - New users get **$300 in free credits** for 90 days
  - A credit card is required for verification (but you won't be charged without permission)

**Don't have a GCP account yet?**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Sign in with your Google account
3. Click "Activate" to start your free trial
4. Complete the billing setup (required even for free tier)

**That's it!** No need to install anything on your computer.

---

## Step 1: Access Google Cloud Shell

Google Cloud Shell is a free, browser-based terminal that comes with everything pre-installed.

### Opening Cloud Shell

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Make sure you're signed in with your Google account
3. Look for the **Cloud Shell icon** (>_) in the top-right corner of the page
4. Click the icon to open Cloud Shell

**What just happened?** A terminal window opened at the bottom of your browser! This is Cloud Shell - a full Linux environment running in the cloud.

### Verify Cloud Shell is Ready

In the Cloud Shell terminal, run these commands to verify everything is installed:

```bash
# Check gcloud (Google Cloud SDK)
gcloud --version

# Check Docker
docker --version

# Check git
git --version
```

**Expected output:** You should see version numbers for all three tools. If you do, you're ready to proceed!

**Note:** Cloud Shell provides 5 GB of persistent disk storage in your home directory (`$HOME`). Your files will remain between sessions.

---

## Step 2: Set Up Your GCP Project

Every Google Cloud deployment needs a project. Think of it as a container for all your resources.

### Create a New Project

1. **Choose a unique project ID.** It must be globally unique across all of Google Cloud. Examples:
   - `stock-dashboard-yourname-2024`
   - `my-backtest-app-123`
   - `dash-app-john-456`

2. **Create the project** (replace `my-dash-app-123` with your chosen ID):

```bash
gcloud projects create my-dash-app-123 --name="Stock Dashboard"
```

**What you'll see:** A success message confirming your project was created.

3. **Set it as your active project:**

```bash
gcloud config set project my-dash-app-123
```

4. **Verify your project is active:**

```bash
gcloud config get-value project
```

This should output your project ID.

### Link Billing to Your Project

**Why?** Even free tier services require a billing account to be linked.

```bash
# List your available billing accounts
gcloud billing accounts list
```

This shows your billing account ID (format: `XXXXXX-YYYYYY-ZZZZZZ`).

```bash
# Link billing to your project (replace BILLING_ACCOUNT_ID with your actual ID)
gcloud billing projects link my-dash-app-123 \
  --billing-account=BILLING_ACCOUNT_ID
```

**Tip:** If you prefer using the web UI, you can also link billing through the Cloud Console:
- Go to **Billing** → **My Projects**
- Find your project and click **"⋮" (three dots)** → **"Change billing"**

### Enable Required APIs

Enable the services you'll need:

```bash
# Enable Cloud Run (for hosting your app)
gcloud services enable run.googleapis.com

# Enable Artifact Registry (for storing Docker images)
gcloud services enable artifactregistry.googleapis.com

# Enable Cloud Build (for building Docker images)
gcloud services enable cloudbuild.googleapis.com
```

**This takes 1-2 minutes.** Wait for confirmation messages.

**What just happened?** You've activated the Google Cloud services needed to build and deploy your app.

---

## Step 3: Clone the Repository

Now let's get the code into Cloud Shell.

### Clone the Repository

```bash
# Navigate to your home directory
cd ~

# Clone the repository
git clone https://github.com/vimala1500/sandt_v1.git

# Navigate into the project directory
cd sandt_v1
```

### Verify the Code is Ready

Check that all necessary files are present:

```bash
# List files in the directory
ls -la
```

**You should see:**
- `app.py` - Main application file
- `Dockerfile` - Instructions for building the Docker image
- `requirements.txt` - Python dependencies
- Other folders: `dashboard/`, `backtesting/`, `utils/`

**Good to go?** Let's build the Docker image!

---

## Step 4: Build Docker Image

Docker packages your application into a "container" that can run anywhere. Cloud Shell has Docker pre-installed, so you can build images directly.

### Understanding the Build Process

The `Dockerfile` in the repository contains instructions for:
1. Starting with a Python 3.11 base image
2. Installing all Python dependencies
3. Copying your application code
4. Configuring the app to run on port 8080

### Configure Docker Authentication

First, configure Docker to work with Google Cloud:

```bash
gcloud auth configure-docker
```

When prompted, type `y` and press Enter.

### Build the Docker Image Using Cloud Build

**Method 1: Using Cloud Build (Recommended - Faster)**

Cloud Build is Google's cloud-based build service. It's faster than building locally in Cloud Shell.

```bash
# Replace 'my-dash-app-123' with YOUR project ID
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard
```

**What's happening:**
- Your code is uploaded to Cloud Build
- Cloud Build reads your `Dockerfile`
- It builds the Docker image in the cloud
- The finished image is stored in Google Container Registry (gcr.io)

**This takes 3-5 minutes.** You'll see:
- ✓ Uploading source code
- ✓ Building steps
- ✓ Pushing to Container Registry
- ✓ Success message with image name

**Method 2: Building Locally in Cloud Shell (Alternative)**

If you prefer to build directly in Cloud Shell:

```bash
# Build the image
docker build -t gcr.io/my-dash-app-123/stock-dashboard .

# Push to Container Registry
docker push gcr.io/my-dash-app-123/stock-dashboard
```

**Note:** Local builds in Cloud Shell can be slower due to limited resources.

---

## Step 5: Push to Container Registry

If you used Cloud Build in Step 4, **your image is already pushed!** You can skip to Step 6.

If you built locally with Docker, you need to push the image:

```bash
# Push the image to Google Container Registry
docker push gcr.io/my-dash-app-123/stock-dashboard
```

This uploads your Docker image to Google's container registry where Cloud Run can access it.

### Verify Your Image

Check that your image was uploaded successfully:

```bash
gcloud container images list
```

You should see `gcr.io/my-dash-app-123/stock-dashboard` in the list.

**Alternative:** View your images in the Cloud Console:
1. Navigate to **Container Registry** in the Cloud Console
2. You should see your `stock-dashboard` image

---

## Step 6: Deploy to Cloud Run

Now for the exciting part - deploying your app to Cloud Run!

### Deploy Your Container

```bash
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 512Mi \
  --timeout 300
```

**Let's break down what each option does:**

- `stock-dashboard` - Name of your Cloud Run service
- `--image` - The Docker image to deploy
- `--platform managed` - Use fully managed Cloud Run (no need to manage servers)
- `--region us-central1` - Deploy to US Central region (you can choose others like `us-east1`, `europe-west1`, `asia-east1`)
- `--allow-unauthenticated` - Allow public access (anyone can visit your app)
- `--port 8080` - The port your app listens on (matches your Dockerfile)
- `--memory 512Mi` - Allocate 512MB memory per instance
- `--timeout 300` - Allow requests up to 300 seconds (5 minutes)

### Confirm Public Access

When prompted:
```
Allow unauthenticated invocations to [stock-dashboard] (y/N)?
```

Type `y` and press Enter.

**Why?** This makes your app publicly accessible so anyone can use it. If you skip this, only authenticated users could access it.

### Wait for Deployment

**Deployment takes 1-2 minutes.** You'll see progress indicators.

**Success!** When complete, you'll see:
```
Service [stock-dashboard] revision [stock-dashboard-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://stock-dashboard-xyz123-uc.a.run.app
```

**Copy the Service URL** - this is your app's permanent address!

---

## Step 7: Access Your Deployed App

### Open Your App

1. Copy the Service URL from the deployment output
2. Paste it into a new browser tab
3. Your Stock Backtesting Dashboard should load! 🎉

The URL format is:
```
https://[service-name]-[hash]-[region].a.run.app
```

**Example:** `https://stock-dashboard-xyz123-uc.a.run.app`

### Verify It's Working

You should see:
- The Stock Backtesting Dashboard interface
- Interactive charts and controls
- No errors in the browser console

**Congratulations!** Your app is now live on the internet and accessible from anywhere!

### Bookmark Your URL

Save the Service URL - it won't change unless you delete and redeploy the service.

---

## Managing Your Deployment

### View Your Service Details

```bash
# Get service information
gcloud run services describe stock-dashboard --region us-central1
```

This shows:
- Service URL
- Latest revision
- Traffic allocation
- Configuration details

### View Logs

**Method 1: Streaming Logs**

```bash
# Stream live logs from your application
gcloud run services logs tail stock-dashboard \
  --region us-central1
```

**Method 2: View Recent Logs**

```bash
# Read recent logs
gcloud run services logs read stock-dashboard \
  --region us-central1 \
  --limit 50
```

**Method 3: Using Cloud Console**

1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click on your `stock-dashboard` service
3. Click the **"LOGS"** tab
4. View logs with filtering and search capabilities

### Update Your Application

Made changes to the code? Here's how to deploy updates:

```bash
# 1. Navigate to your project directory
cd ~/sandt_v1

# 2. Pull latest changes (if working with a repository)
git pull origin main

# 3. Rebuild the Docker image
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard

# 4. Deploy the updated image
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --region us-central1
```

**Cloud Run automatically:**
- Creates a new revision
- Routes traffic to the new revision
- Keeps the old revision for potential rollback

### Rollback to a Previous Version

If something goes wrong, you can quickly rollback:

```bash
# List all revisions
gcloud run revisions list --service stock-dashboard --region us-central1

# Rollback to a specific revision
gcloud run services update-traffic stock-dashboard \
  --to-revisions=stock-dashboard-00001-abc=100 \
  --region us-central1
```

### Scale Your Application

Adjust scaling settings:

```bash
gcloud run services update stock-dashboard \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80 \
  --region us-central1
```

**Options explained:**
- `--min-instances 0` - Scale to zero when not in use (saves money!)
- `--max-instances 10` - Maximum number of container instances
- `--concurrency 80` - Maximum concurrent requests per instance

### Delete Your Service

To remove the Cloud Run service:

```bash
gcloud run services delete stock-dashboard --region us-central1
```

**Warning:** This deletes the service but not the Docker image. The image remains in Container Registry.

To also delete the Docker image:

```bash
gcloud container images delete gcr.io/my-dash-app-123/stock-dashboard
```

---

## Troubleshooting

### Issue: Permission Denied Errors

**Solution:** Ensure you're authenticated:

```bash
gcloud auth login
```

Follow the prompts to authenticate in your browser.

### Issue: "Billing Not Enabled" Error

**Solution:** Enable billing for your project:

```bash
# List billing accounts
gcloud billing accounts list

# Link billing (replace with your billing account ID)
gcloud billing projects link my-dash-app-123 \
  --billing-account=XXXXXX-YYYYYY-ZZZZZZ
```

### Issue: API Not Enabled

**Solution:** Enable the required API:

```bash
# If you see an error about a specific API, enable it
gcloud services enable [API_NAME].googleapis.com

# Example:
gcloud services enable run.googleapis.com
```

### Issue: Build Timeout

**Solution:** If your build times out, you may need to increase the timeout:

```bash
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard \
  --timeout=20m
```

### Issue: Service Not Responding

**Solution:** Check the logs for errors:

```bash
gcloud run services logs tail stock-dashboard --region us-central1
```

Look for Python errors, missing dependencies, or configuration issues.

### Issue: Out of Memory Errors

**Solution:** Increase memory allocation:

```bash
gcloud run services update stock-dashboard \
  --memory 1Gi \
  --region us-central1
```

### Issue: Cold Start Delays

**Problem:** First request after period of inactivity is slow.

**Solution:** Set minimum instances to keep at least one instance warm:

```bash
gcloud run services update stock-dashboard \
  --min-instances 1 \
  --region us-central1
```

**Note:** This increases costs as you'll be charged for the idle instance.

### Issue: Cloud Shell Session Timeout

**Problem:** Cloud Shell disconnects after 20 minutes of inactivity.

**Solution:** 
- Your files in `$HOME` are persistent and will remain
- Simply reconnect and continue where you left off
- For long-running builds, use Cloud Build (it continues even if Cloud Shell disconnects)

### Getting Help

- **Documentation:** [Cloud Run Documentation](https://cloud.google.com/run/docs)
- **Community:** [Stack Overflow - google-cloud-run](https://stackoverflow.com/questions/tagged/google-cloud-run)
- **Support:** [Google Cloud Support](https://cloud.google.com/support)

---

## Cost Information

### Free Tier

Cloud Run offers a generous free tier **every month**:

- **2 million requests** per month
- **360,000 GB-seconds** of memory
- **180,000 vCPU-seconds** of compute time
- **1 GB** outbound network traffic

**For a personal project with low-moderate traffic, you'll likely stay in the free tier!**

### Typical Costs for Low Traffic

If you exceed the free tier, costs are very reasonable:

- **Cloud Run:** $0.00002400 per vCPU-second, $0.00000250 per GB-second
- **Container Registry Storage:** $0.026 per GB per month
- **Network Egress:** $0.12 per GB (after free tier)

**Example:** A site with 10,000 page views per month:
- Likely: **$0-2/month** (mostly within free tier)
- Maximum: **~$5/month** (if you exceed free tier)

### Cost Optimization Tips

1. **Scale to zero:** Use `--min-instances=0` (default) so you're not charged when idle
2. **Right-size memory:** Start with 512Mi; only increase if needed
3. **Choose nearby regions:** Reduces latency and data transfer costs
4. **Monitor usage:** Set up billing alerts

### Set Up Billing Alerts

Protect yourself from unexpected charges:

```bash
# You can set this up in Cloud Console:
# 1. Go to Billing → Budgets & alerts
# 2. Create budget
# 3. Set threshold (e.g., $5 or $10)
# 4. Add email notification
```

Or via Cloud Shell:

```bash
# Create a budget with email alert at 50%, 90%, and 100%
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Monthly Budget" \
  --budget-amount=10 \
  --threshold-rule=percent=0.5 \
  --threshold-rule=percent=0.9 \
  --threshold-rule=percent=1.0
```

---

## Advanced: Using Artifact Registry (Modern Alternative)

Google is moving from Container Registry (gcr.io) to Artifact Registry. Here's how to use Artifact Registry instead:

### Create an Artifact Registry Repository

```bash
# Create a Docker repository in Artifact Registry
gcloud artifacts repositories create stock-dashboard-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for stock dashboard"
```

### Configure Docker for Artifact Registry

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Build and Push to Artifact Registry

```bash
# Build with Cloud Build (targeting Artifact Registry)
gcloud builds submit \
  --tag us-central1-docker.pkg.dev/my-dash-app-123/stock-dashboard-repo/stock-dashboard

# Deploy from Artifact Registry
gcloud run deploy stock-dashboard \
  --image us-central1-docker.pkg.dev/my-dash-app-123/stock-dashboard-repo/stock-dashboard \
  --region us-central1 \
  --allow-unauthenticated
```

**Why use Artifact Registry?**
- Modern, more feature-rich
- Better vulnerability scanning
- Recommended for new projects
- Will eventually replace Container Registry

---

## Summary

### Quick Reference Commands

```bash
# Setup
gcloud projects create my-dash-app-123 --name="Stock Dashboard"
gcloud config set project my-dash-app-123
gcloud billing projects link my-dash-app-123 --billing-account=BILLING_ACCOUNT_ID
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# Clone and build
cd ~
git clone https://github.com/vimala1500/sandt_v1.git
cd sandt_v1
gcloud builds submit --tag gcr.io/my-dash-app-123/stock-dashboard

# Deploy
gcloud run deploy stock-dashboard \
  --image gcr.io/my-dash-app-123/stock-dashboard \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Manage
gcloud run services logs tail stock-dashboard --region us-central1
gcloud run services describe stock-dashboard --region us-central1
gcloud run services list
```

### What You've Learned

✅ How to use Google Cloud Shell (no local installations needed!)  
✅ How to create and configure a GCP project  
✅ How to clone a GitHub repository in Cloud Shell  
✅ How to build Docker images using Cloud Build  
✅ How to push images to Google Container Registry  
✅ How to deploy containerized apps to Cloud Run  
✅ How to manage and monitor your deployment  
✅ How to optimize costs  

### Next Steps

- ✨ **Set up a custom domain** for your app
- 🔐 **Add authentication** to restrict access
- 🔄 **Set up CI/CD** for automatic deployments
- 📊 **Monitor performance** with Cloud Monitoring
- 🗄️ **Add a database** (Cloud SQL) for persistent data
- 🌍 **Use Cloud CDN** for faster global access

### Resources

- [Cloud Run Quickstarts](https://cloud.google.com/run/docs/quickstarts)
- [Cloud Shell Documentation](https://cloud.google.com/shell/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [This Repository's Standard Deployment Guide](DEPLOY_TO_GCP.md) (for local development setup)

---

**Happy deploying! 🚀**

*Questions or issues? Open an issue on the [GitHub repository](https://github.com/vimala1500/sandt_v1/issues).*
