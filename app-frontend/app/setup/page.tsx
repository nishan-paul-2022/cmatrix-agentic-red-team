"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * /setup — redirect to landing page.
 * CMatrix is now Google OAuth ONLY. Anyone can sign up automatically
 * by logging in with their Google account. No manual setup required.
 */
export default function SetupPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/");
  }, [router]);
  return null;
}
