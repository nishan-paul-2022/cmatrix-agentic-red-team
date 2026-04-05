import type { NextRequest } from "next/server";

export const runtime = "edge";

const PYTHON_BACKEND_URL = process.env.PYTHON_BACKEND_URL || "http://localhost:8000";

export async function POST(req: NextRequest) {
  try {
    const { message, history = [] } = await req.json();

    if (!message) {
      return new Response("Message is required", { status: 400 });
    }

    console.log("[Frontend] Routing request to Python backend:", PYTHON_BACKEND_URL);

    // Get auth token from request headers
    const authHeader = req.headers.get("authorization");

    // Call Python backend
    const response = await fetch(`${PYTHON_BACKEND_URL}/api/v1/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(authHeader ? { Authorization: authHeader } : {}),
      },
      body: JSON.stringify({
        message,
        history,
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error("[Frontend] Python backend error:", response.status, errorText);

      // Provide user-friendly error messages
      let errorMessage = "Backend error occurred";
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.detail || errorJson.error || errorMessage;
      } catch {
        errorMessage = errorText || errorMessage;
      }

      return new Response(JSON.stringify({ error: errorMessage }), {
        status: response.status,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Forward the streaming response from Python backend
    return new Response(response.body, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    });
  } catch (error: any) {
    console.error("[Frontend] Error in chat route:", error?.message);

    // Check if backend is unreachable
    if (error?.cause?.code === "ECONNREFUSED" || error?.message?.includes("fetch failed")) {
      return new Response(
        JSON.stringify({
          error: `Cannot connect to Python backend. Please ensure the backend is running on ${PYTHON_BACKEND_URL.split(
            ":"
          ).pop()}.`,
        }),
        {
          status: 503,
          headers: { "Content-Type": "application/json" },
        }
      );
    }

    return new Response(JSON.stringify({ error: "Internal server error" }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
