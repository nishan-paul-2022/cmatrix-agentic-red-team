/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  async rewrites() {
    // Determine backend URL at runtime (handled by Next.js in production)
    // In standalone mode, next.config.mjs is evaluated at startup.
    // If PYTHON_BACKEND_URL is missing, we default to the host gateway for Docker.
    const backendUrl = process.env.PYTHON_BACKEND_URL || "http://172.17.0.1:3012";
    console.warn(`[Next.js Config] Initializing rewrites with backend: ${backendUrl}`);

    return [
      {
        source: "/api/:path*",
        destination: `${backendUrl}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
