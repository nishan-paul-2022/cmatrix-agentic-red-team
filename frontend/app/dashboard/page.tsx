"use client";

import { ChatHeader } from "@/components/chat/chat-header";
import { ConversationSidebar } from "@/components/sidebar/conversation-sidebar";
import { ConversationProvider } from "@/contexts/conversation-context";
import { DashboardTable } from "@/features/dashboard/components/DashboardTable";
import { useDashboard } from "@/features/dashboard/hooks/useDashboard";

function DashboardContent() {
  const {
    history,
    isLoading,
    search,
    setSearch,
    deleteExchange,
    clearConversationHistory,
  } = useDashboard();

  return (
    <div className="flex h-screen bg-background">
      <div className="matrix-rain"></div>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-background">
        {/* Header */}
        <ChatHeader />
        <main className="flex-1 overflow-auto p-6">
          <div className="max-w-5xl mx-auto space-y-6">
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
              <p className="text-muted-foreground">
                Manage your conversation history and messages.
              </p>
            </div>

            <div className="bg-card rounded-lg border shadow-sm p-6">
              <DashboardTable
                data={history}
                isLoading={isLoading}
                search={search}
                onSearchChange={setSearch}
                onDelete={deleteExchange}
                onClearHistory={clearConversationHistory}
              />
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ConversationProvider>
      <DashboardContent />
    </ConversationProvider>
  );
}
