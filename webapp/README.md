# hydroviz-webapp

## Setup

```
nvm use lts/jod
npm install
```

## Run

Running the local data API:

```
cd data-api
git checkout hydroviz_prototype_api
export FLASK_APP=application.py
export API_RAS_BASE_URL=https://zeus.snap.uaf.edu/rasdaman/
pipenv run flask run
```

Running the webapp:

```
cd hydroviz-webapp
npm run dev
```
