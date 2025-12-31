/**
 * ApprovalCard Component
 *
 * Displays a rich UI for approving/rejecting dangerous tool executions
 * with risk visualization, parameter editing, and audit trail support.
 */

import React, { useState } from "react";
import { ApprovalCardProps, RiskLevel } from "@/types/approval.types";

const ApprovalCard: React.FC<ApprovalCardProps> = ({
  threadId,
  toolName,
  toolArgs,
  riskInfo,
  onApprove,
  onReject,
}) => {
  const [isEditing, setIsEditing] = useState(false);
  const [modifiedArgs, setModifiedArgs] = useState<Record<string, any>>(toolArgs);
  const [approvalReason, setApprovalReason] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  // Risk-based styling
  const getRiskColor = (level: RiskLevel): string => {
    const colors = {
      CRITICAL: "border-red-500 bg-red-50",
      HIGH: "border-orange-500 bg-orange-50",
      MEDIUM: "border-yellow-500 bg-yellow-50",
      LOW: "border-green-500 bg-green-50",
    };
    return colors[level] || "border-gray-500 bg-gray-50";
  };

  const getRiskBadgeColor = (level: RiskLevel): string => {
    const colors = {
      CRITICAL: "bg-red-600 text-white",
      HIGH: "bg-orange-600 text-white",
      MEDIUM: "bg-yellow-600 text-white",
      LOW: "bg-green-600 text-white",
    };
    return colors[level] || "bg-gray-600 text-white";
  };

  const formatToolName = (name: string): string => {
    return name
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  const handleApprove = async () => {
    setIsProcessing(true);
    try {
      await onApprove(isEditing ? modifiedArgs : undefined, approvalReason || undefined);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReject = async () => {
    setIsProcessing(true);
    try {
      await onReject(approvalReason || undefined);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleArgChange = (key: string, value: string) => {
    setModifiedArgs((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  return (
    <div
      className={`approval-card border-l-4 p-6 rounded-lg shadow-lg mb-4 ${getRiskColor(
        riskInfo.risk_level
      )}`}
    >
      {/* Header with Risk Badge */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span
            className={`px-3 py-1 rounded-full text-sm font-bold ${getRiskBadgeColor(
              riskInfo.risk_level
            )}`}
          >
            {riskInfo.risk_level} RISK
          </span>
          <span className="text-sm text-gray-600">⏱️ {riskInfo.estimated_duration}</span>
        </div>
        {!riskInfo.reversible && (
          <span className="text-xs text-red-600 font-semibold">⚠️ IRREVERSIBLE</span>
        )}
      </div>

      {/* Tool Information */}
      <h3 className="text-xl font-bold mb-2 text-gray-800">
        🔐 Approval Required: {formatToolName(toolName)}
      </h3>

      <p className="text-gray-700 mb-4">{riskInfo.reason}</p>

      {/* Warning Banner */}
      {riskInfo.warning && (
        <div className="bg-yellow-100 border-l-4 border-yellow-500 p-3 mb-4 rounded">
          <p className="text-yellow-800 font-semibold">{riskInfo.warning}</p>
        </div>
      )}

      {/* Parameters Display/Edit */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-medium text-gray-700">Tool Parameters</label>
          <button
            onClick={() => setIsEditing(!isEditing)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
            disabled={isProcessing}
          >
            {isEditing ? "❌ Cancel Editing" : "✏️ Modify Parameters"}
          </button>
        </div>

        <div className="bg-gray-900 text-sky-400 p-4 rounded-lg font-mono text-sm overflow-x-auto">
          {isEditing ? (
            <div className="space-y-2">
              {Object.entries(modifiedArgs).map(([key, value]) => (
                <div key={key} className="flex items-center gap-2">
                  <span className="text-blue-400">{key}:</span>
                  <input
                    type="text"
                    value={String(value)}
                    onChange={(e) => handleArgChange(key, e.target.value)}
                    className="flex-1 bg-gray-800 text-sky-400 px-2 py-1 rounded border border-gray-700 focus:border-sky-500 focus:outline-none"
                  />
                </div>
              ))}
            </div>
          ) : (
            <pre className="whitespace-pre-wrap">{JSON.stringify(toolArgs, null, 2)}</pre>
          )}
        </div>
      </div>

      {/* Approval Reason (Optional) */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Approval Reason (Optional - for audit trail)
        </label>
        <input
          type="text"
          value={approvalReason}
          onChange={(e) => setApprovalReason(e.target.value)}
          placeholder="e.g., Approved for security audit"
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          disabled={isProcessing}
        />
      </div>

      {/* Action Buttons */}
      <div className="flex gap-3">
        <button
          onClick={handleApprove}
          disabled={isProcessing}
          className="flex-1 bg-sky-600 hover:bg-sky-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {isProcessing ? (
            <>
              <span className="animate-spin">⏳</span>
              Processing...
            </>
          ) : (
            <>✅ Approve & Execute</>
          )}
        </button>

        <button
          onClick={handleReject}
          disabled={isProcessing}
          className="flex-1 bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg transition-colors flex items-center justify-center gap-2"
        >
          {isProcessing ? (
            <>
              <span className="animate-spin">⏳</span>
              Processing...
            </>
          ) : (
            <>❌ Reject</>
          )}
        </button>
      </div>

      {/* Additional Info */}
      <div className="mt-4 pt-4 border-t border-gray-300">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <span>Thread ID: {threadId}</span>
          {!riskInfo.reversible && (
            <span className="text-red-600 font-semibold">⚠️ This operation cannot be undone</span>
          )}
        </div>
      </div>
    </div>
  );
};

export default ApprovalCard;
