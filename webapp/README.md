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

## Production

This app is built as a fully static single-page app (`ssr: false` in
`nuxt.config.ts`) and hosted on S3 as a static website. S3 answers requests
for URLs it has no object for (report permalinks, bad links) by redirecting
them to hashbang URLs (`/#!/...`) that resolve to `index.html`; the app then
routes them client-side to the intended page, or to the error/404 page if the
URL is not valid.

### Enable website hosting on the AWS S3 bucket:

**_The following command should be run only during the initial setup of the S3
bucket. Do not run this command again or it will wipe out the S3 website
redirection rules._**

```bash
aws s3 website s3://{{ S3 bucket name }}/ --index-document index.html --error-document index.html
```

### Add website redirection rules to S3 bucket

Website redirection rules need to be added to the S3 bucket for data to hydrate
properly when a report is referenced directly by its URL (permalink), and for
invalid URLs to reach the error/404 page.

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

Code in `middleware/hashbangRedirect.global.ts` catches and routes these redirects into fully hydrated report pages.

### Build preview

Run the statically built website locally:

```bash
npm run generate
npx serve .output/public
```

### Deployment

To deploy to our development S3 bucket, set environment variables if necessary, then run:

```bash
rm -fr .output
npm run generate
aws s3 sync .output/public s3://hydroviz-dev/ --acl public-read --delete
```

If a CloudFront distribution is placed in front of the production bucket, its
cache must also be invalidated after deploying:

```bash
aws cloudfront create-invalidation --distribution-id {{ distribution ID }} --paths "/*"
```
