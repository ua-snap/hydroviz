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

## Deployment

To deploy to our development S3 bucket, set environment variables if necessary, then run:

```bash
rm -fr .output
npm run generate
aws s3 sync .output/public s3://hydroviz-dev/ --acl public-read --delete
```
