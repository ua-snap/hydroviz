# hydroviz-webapp

## Setup

```
nvm use lts/jod
npm install
```

## Running for development

For static-only local development (no interaction with an API, using fixtures taken from https://github.com/ua-snap/data-api/commit/f9ba6916dd6f94b2e959baacb75f4e35b9b3781b):

```
export HYDROVIZ_USE_STATIC_FIXTURES=true

```

For development with a backend API, export the `SNAP_API_URL` env var to the desired location (local or remote, defaults to `https://earthmaps.io`).

Running the webapp:

```
cd webapp
npm run dev
```

## Deploying to production

(work in progress)

### Enable website hosting on the AWS S3 bucket:

**_The following command should be run only during the initial setup of the S3
bucket. Do not run this command again or it will wipe out the S3 website
redirection rules._**

```bash
aws s3 website s3://{{ S3 bucket name }}/ --index-document index.html --error-document index.html
```

### Add website redirection rules to S3 bucket

Website redirection rules need to be added to the S3 bucket for data to hydrate
properly when a report is referenced directly by its URL (permalink).

From the AWS web interface for the S3 bucket, go to:

Properties → Static website hosting → Edit

In the "Redirection rules" text area, add the following:

```
[
    {
        "Condition": {
            "HttpErrorCodeReturnedEquals": "404"
        },
        "Redirect": {
            "HostName": "{{ finalized URL for tool }}",
            "Protocol": "http",
            "ReplaceKeyPrefixWith": "#!/"
        }
    },
    {
        "Condition": {
            "HttpErrorCodeReturnedEquals": "403"
        },
        "Redirect": {
            "HostName": "{{ finalized URL for tool }}",
            "Protocol": "http",
            "ReplaceKeyPrefixWith": "#!/"
        }
    }
]
```

Code in `app.vue` catches and routes these redirects into fully hydrated report pages.
