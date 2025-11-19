"use client";

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/contexts/auth-context';

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading, checkSetupStatus } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  const [isCheckingSetup, setIsCheckingSetup] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      // Public routes that don't require authentication
      const publicRoutes = ['/login', '/setup'];
      const isPublicRoute = publicRoutes.some(route => pathname.startsWith(route));

      if (isLoading) {
        return; // Wait for auth to load
      }

      // Check if setup is complete
      const isSetupComplete = await checkSetupStatus();
      setIsCheckingSetup(false);

      if (!isSetupComplete) {
        // Setup not complete, redirect to setup
        if (pathname !== '/setup') {
          router.push('/setup');
        }
        return;
      }

      // Setup is complete, check authentication
      if (!isAuthenticated && !isPublicRoute) {
        // Not authenticated and trying to access protected route
        router.push('/login');
      } else if (isAuthenticated && isPublicRoute) {
        // Already authenticated, redirect to home
        router.push('/');
      }
    };

    checkAuth();
  }, [isAuthenticated, isLoading, pathname, router, checkSetupStatus]);

  // Show loading state
  if (isLoading || isCheckingSetup) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="matrix-rain"></div>
        <div className="text-center z-10">
          <div className="loading-spinner mb-4"></div>
          <p className="text-primary">Loading...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
