"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

/**
 * /login — redirect to landing page.
 * Authentication now happens entirely via Google OAuth initiated from /.
 */
export default function LoginPage() {
  const router = useRouter();
  useEffect(() => {
    router.replace("/");
  }, [router]);
  return null;
}
