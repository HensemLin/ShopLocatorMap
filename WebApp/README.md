# Interactive Shop Location Map - Frontend

Built with Vite React and Tailwind CSS

## Overview

This React application, configured with Vite, displays a simple map with markers for shop locations. The styling is powered by Tailwind CSS, offering a sleek and responsive design.

## Prerequisites

- Node.js and npm
- Backend application running and accessible
- Tailwind CSS (automatically installed with other dependencies)

## Setup

1. **Installation** :

- Install required packages (including Tailwind CSS):
  <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">npm install
  </code></div></div></pre>
- Tailwind CSS is included in the project dependencies and will be installed during this step.

2. **Tailwind Configuration** :

- Ensure `tailwind.config.js` and `postcss.config.js` are set up correctly for Tailwind CSS.
- If you make changes to Tailwind's configuration, you might need to rebuild your styles.

3. **API Key** :

- Fetch an API key by making a GET request to `http://{your-backend-ip}:8000/API/createAPI/`.
- Add the API key to the `.env` file as `VITE_APP_API_KEY`.

4. **Launch the Frontend** :

- Run the application:
  <pre><div class="bg-black rounded-md"><div class="flex items-center relative text-gray-200 bg-gray-800 dark:bg-token-surface-primary px-4 py-2 text-xs font-sans justify-between rounded-t-md"></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">npm run dev
  </code></div></div></pre>

### Usage

- The frontend will be accessible at `http://localhost:3000`.
