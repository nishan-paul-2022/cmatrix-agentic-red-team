/**
 * useApproval Hook
 *
 * Custom hook for managing HITL approval workflows
 */

import { useState, useCallback } from "react";
import { useAuth } from "@/contexts/auth-context";
import { PendingApprovalResponse, ApprovalRequest, ApprovalResponse } from "@/types/approval.types";

// Get API base URL (already includes /api/v1)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const useApproval = (threadId: string) => {
  const { token } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getPendingApproval = useCallback(async (): Promise<PendingApprovalResponse | null> => {
    if (!token || !threadId) return null;

    setIsLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/approvals/${threadId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to get pending approval: ${response.statusText}`);
      }

      const data: PendingApprovalResponse = await response.json();
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Unknown error";
      setError(errorMessage);
      console.error("Error getting pending approval:", err);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, [token, threadId]);

  const approveOrReject = useCallback(
    async (
      action: "approve" | "reject",
      modifiedArgs?: Record<string, any>,
      reason?: string
    ): Promise<ApprovalResponse | null> => {
      if (!token || !threadId) return null;

      // Prevent double-clicks
      if (isLoading) {
        console.warn("Request already in progress, ignoring duplicate click");
        return null;
      }

      setIsLoading(true);
      setError(null);

      try {
        const requestBody: ApprovalRequest = {
          action,
          modified_args: modifiedArgs,
          reason,
        };

        const response = await fetch(`${API_BASE_URL}/approvals/${threadId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Failed to ${action} approval: ${response.status} ${errorText}`);
        }

        const data: ApprovalResponse = await response.json();
        return data;
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : "Unknown error";
        setError(errorMessage);
        console.error(`Error ${action}ing approval:`, err);
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    [token, threadId, isLoading]
  );

  const approve = useCallback(
    async (modifiedArgs?: Record<string, any>, reason?: string) => {
      return approveOrReject("approve", modifiedArgs, reason);
    },
    [approveOrReject]
  );

  const reject = useCallback(
    async (reason?: string) => {
      return approveOrReject("reject", undefined, reason);
    },
    [approveOrReject]
  );

  return {
    getPendingApproval,
    approve,
    reject,
    isLoading,
    error,
  };
};
