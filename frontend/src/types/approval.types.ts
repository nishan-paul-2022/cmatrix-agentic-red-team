/**
 * Types for HITL (Human-in-the-Loop) approval system
 */

export type RiskLevel = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';

export type ApprovalAction = 'approve' | 'reject';

export type ApprovalStatus = 'pending' | 'approved' | 'rejected' | 'not_found' | 'unknown';

export interface RiskInfo {
  risk_level: RiskLevel;
  reason: string;
  requires_approval: boolean;
  warning?: string;
  auto_reject_patterns?: string[];
  estimated_duration: string;
  reversible: boolean;
}

export interface PendingApproval {
  tool_name: string;
  tool_args: Record<string, any>;
  risk_info: RiskInfo;
  timestamp: string;
  all_tool_calls?: Array<[string, Record<string, any>]>;
}

export interface ApprovalRequest {
  action: ApprovalAction;
  modified_args?: Record<string, any>;
  reason?: string;
}

export interface ApprovalResponse {
  status: string;
  message: string;
  thread_id: string;
}

export interface PendingApprovalResponse {
  thread_id: string;
  status: ApprovalStatus;
  approval_request?: PendingApproval;
}

export interface ApprovalCardProps {
  threadId: string;
  toolName: string;
  toolArgs: Record<string, any>;
  riskInfo: RiskInfo;
  onApprove: (modifiedArgs?: Record<string, any>, reason?: string) => void;
  onReject: (reason?: string) => void;
}
