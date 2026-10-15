This is the [SrotGraph](https://github.com/parth-patel/srotgraph) frontend — a Next.js application for the evidence-preserving intelligence system.

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Project Structure

- `src/app/` — Next.js App Router pages
- `src/components/` — React components
- `src/lib/` — Utility functions and API client
- `src/types/` — TypeScript type definitions

## API Integration

The frontend connects to the SrotGraph backend API. See `src/lib/api.ts` for the API client configuration.

## Development

Run the backend API first, then start the frontend:

```bash
# Terminal 1: Backend
cd backend && uvicorn srotgraph.main:app --reload

# Terminal 2: Frontend
cd frontend && pnpm dev
```

The frontend will be available at http://localhost:3000.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.


