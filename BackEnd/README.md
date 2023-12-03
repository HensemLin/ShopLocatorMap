# Shop Location Scraper and Geolocator - Backend

## Overview

This FastAPI backend performs web scraping to retrieve shop names and addresses, then uses OpenStreetMap to determine their locations. The data is stored in a MySQL database.

## Prerequisites

- MySQL Database
- Python 3.11+
- FastAPI, Uvicorn, and other dependencies listed in `requirements.txt`

## Setup

1. **Database Setup** :

- Create a MySQL database and schema.
- Set up the following environment variables in `.env` file:
  - `DATABASE_HOSTNAME`
  - `DATABASE_PORT`
  - `DATABASE_PASSWORD`
  - `DATABASE_NAME` (name of the schema you created)
  - `DATABASE_USERNAME`

2. **Installation** :

- Install dependencies:
  <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs">pip install -r requirements.txt
  </code></div></div></pre>

3. **Launch the Backend** :

- Run the following command:
  <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-lua">uvicorn app.main:app --reload
  </code></div></div></pre>

## Usage

- The backend API will be accessible at `http://localhost:8000`.
