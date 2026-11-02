# MASHWORKS website (React)

1. Put your images in the `public/` folder (same file names as before):
   mashworks-logo-gold.png, mashworks_workers_reduced.jpg, interior installation.jpg,
   bathroom set installation.jpg, paving.jpg, bathroom tiling.jpg, shower installation.jpg,
   welding.jpg, ceiling installation.jpg, painting.jpg
2. `npm install`
3. `npm run dev`   (preview on your computer)
4. `npm run build` (creates the `dist/` folder to upload to your host)

## Publishing on GitHub Pages
GitHub Pages cannot run React source files directly, so the site must be built first.
This project includes `.github/workflows/deploy.yml` which builds it automatically on every push.
In your repo: Settings -> Pages -> Source -> choose "GitHub Actions".
Upload ALL files from this folder (including the hidden `.github` folder) to the repo root.
