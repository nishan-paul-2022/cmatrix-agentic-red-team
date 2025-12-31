"use client";

import React from "react";
import ApprovalCard from "@/components/approval/ApprovalCard";
import { useApproval } from "@/hooks/use-approval";
import { PendingApproval } from "@/types/approval.types";

interface ApprovalMessageProps {
  threadId: string;
  pendingApproval: PendingApproval;
  onActionComplete?: () => void;
}

export function ApprovalMessage({
  threadId,
  pendingApproval,
  onActionComplete,
}: ApprovalMessageProps) {
  const { approve, reject } = useApproval(threadId);
  const [isActionTaken, setIsActionTaken] = React.useState(false);

  const handleApprove = async (modifiedArgs?: Record<string, any>, reason?: string) => {
    const result = await approve(modifiedArgs, reason);
    if (result) {
      setIsActionTaken(true);
      if (onActionComplete) onActionComplete();
    }
  };

  const handleReject = async (reason?: string) => {
    const result = await reject(reason);
    if (result) {
      setIsActionTaken(true);
      if (onActionComplete) onActionComplete();
    }
  };

  if (isActionTaken) {
    return null;
  }

  return (
    <ApprovalCard
      threadId={threadId}
      toolName={pendingApproval.tool_name}
      toolArgs={pendingApproval.tool_args}
      riskInfo={pendingApproval.risk_info}
      onApprove={handleApprove}
      onReject={handleReject}
    />
  );
}
