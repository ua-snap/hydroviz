# hydroviz-webapp

## Setup

```
nvm use lts/hydrogen
npm install
```

## Run

```
cd data-api
git checkout hydroviz_v2
export FLASK_APP=application.py
export API_RAS_BASE_URL=https://zeus.snap.uaf.edu/rasdaman/
pipenv run flask run
```

```
cd hydroviz-webapp
npm run dev
```
