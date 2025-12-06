# Deploying to Render with Docker

This guide explains how to deploy your FastAPI backend to Render using the provided Dockerfile.

## Prerequisites

- A [Render account](https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- MongoDB Atlas account (or another cloud MongoDB provider)

## Deployment Steps

### 1. Prepare Your MongoDB Database

Since Render won't run MongoDB locally, you need a cloud MongoDB instance:

1. Create a free MongoDB Atlas cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Get your MongoDB connection string (it will look like: `mongodb+srv://username:password@cluster.mongodb.net/`)
3. Keep this connection string handy for the next step

### 2. Deploy to Render

1. **Log in to Render** at [dashboard.render.com](https://dashboard.render.com)

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your Git repository
   - Select the repository containing this backend code

3. **Configure the Service**
   - **Name**: Choose a name for your service (e.g., `teacher-backend`)
   - **Region**: Select the region closest to your users
   - **Branch**: Select your main branch (usually `main` or `master`)
   - **Root Directory**: Leave blank (or specify if your backend is in a subdirectory)
   - **Runtime**: Select **Docker**
   - **Instance Type**: Choose "Free" for testing or "Starter" for production

4. **Set Environment Variables**
   
   Click "Advanced" and add the following environment variables:
   
   | Key | Value | Example |
   |-----|-------|---------|
   | `MONGO_URL` | Your MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/` |
   | `DB_NAME` | Your database name | `kevin_assignment_db` |
   | `ENVIRONMENT` | `production` | `production` |
   | `API_PREFIX` | `/rent-easy/api` | `/rent-easy/api` |
   
   > **Note**: Render automatically provides the `PORT` environment variable, so you don't need to set it.

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build your Docker image and deploy it
   - Wait for the deployment to complete (usually 2-5 minutes)

### 3. Access Your API

Once deployed, your API will be available at:
```
https://your-service-name.onrender.com
```

For example, if your API prefix is `/rent-easy/api`, your endpoints will be at:
```
https://your-service-name.onrender.com/rent-easy/api/...
```

### 4. Update Frontend Configuration

Update your frontend to point to the new Render URL instead of `localhost:8000`.

## Automatic Deployments

Render automatically redeploys your service when you push to your connected Git branch. No manual intervention needed!

## Monitoring and Logs

- View logs in the Render dashboard under your service → "Logs"
- Monitor service health under "Metrics"
- Set up alerts for downtime or errors

## Troubleshooting

### Build Fails

- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Dockerfile syntax

### Service Won't Start

- Check the runtime logs
- Verify environment variables are set correctly
- Ensure MongoDB connection string is valid

### Connection Issues

- Verify MongoDB Atlas allows connections from anywhere (0.0.0.0/0) or add Render's IP ranges
- Check that your MongoDB user has proper permissions

## Cost Considerations

- **Free Tier**: Services spin down after 15 minutes of inactivity (cold starts)
- **Starter Tier** ($7/month): Always running, no cold starts
- **MongoDB Atlas**: Free tier available (512MB storage)

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
