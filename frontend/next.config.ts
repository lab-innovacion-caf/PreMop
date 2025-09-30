import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export", // Indica que el proyecto será exportado como estático
  images: {
    unoptimized: true, // Requerido si usas la optimización de imágenes de Next.js
  },
  env: {
    BACKEND_URL: process.env.BACKEND_URL
  }
};

export default nextConfig;

