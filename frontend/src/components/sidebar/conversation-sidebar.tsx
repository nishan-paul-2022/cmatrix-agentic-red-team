"use client";

import React from 'react';
import { Plus, Search, MessageSquare } from 'lucide-react';
import { useConversations } from '@/contexts/conversation-context';
import { ConversationItem } from './conversation-item';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

interface ConversationSidebarProps {
  className?: string;
}

export function ConversationSidebar({ className }: ConversationSidebarProps) {
  const {
    conversations,
    activeConversation,
    isLoading,
    createConversation,
    selectConversation,
  } = useConversations();

  const [searchQuery, setSearchQuery] = React.useState('');
  const [isCreating, setIsCreating] = React.useState(false);

  const filteredConversations = React.useMemo(() => {
    if (!searchQuery.trim()) return conversations;

    return conversations.filter(conversation =>
      conversation.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      (conversation.last_message && conversation.last_message.toLowerCase().includes(searchQuery.toLowerCase()))
    );
  }, [conversations, searchQuery]);

  const handleCreateConversation = async () => {
    if (isCreating) return;

    try {
      setIsCreating(true);
      await createConversation();
    } catch (error) {
      console.error('Failed to create conversation:', error);
    } finally {
      setIsCreating(false);
    }
  };

  const handleSelectConversation = (conversation: any) => {
    selectConversation(conversation);
  };

  return (
    <div className={cn("flex flex-col h-full bg-sidebar border-r", className)}>
      {/* Header */}
      <div className="p-4 border-b">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Conversations</h2>
          <Button
            onClick={handleCreateConversation}
            disabled={isCreating}
            size="sm"
            className="h-8 w-8 p-0"
          >
            <Plus className="h-4 w-4" />
          </Button>
        </div>

        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search conversations..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="pl-9"
          />
        </div>
      </div>

      {/* Conversations List */}
      <div className="flex-1 overflow-y-auto">
        <div className="p-2">
          {isLoading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
            </div>
          ) : filteredConversations.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-8 text-center">
              <MessageSquare className="h-12 w-12 text-muted-foreground mb-4" />
              <p className="text-sm text-muted-foreground mb-2">
                {searchQuery ? 'No conversations found' : 'No conversations yet'}
              </p>
              <p className="text-xs text-muted-foreground">
                {searchQuery ? 'Try a different search term' : 'Create your first conversation to get started'}
              </p>
            </div>
          ) : (
            <div className="space-y-1">
              {filteredConversations.map((conversation) => (
                <ConversationItem
                  key={conversation.id}
                  conversation={conversation}
                  isActive={activeConversation?.id === conversation.id}
                  onClick={() => handleSelectConversation(conversation)}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}