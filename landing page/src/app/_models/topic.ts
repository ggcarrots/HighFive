export interface Topic {
  id: number;
  source: string;
  labels: string[];
  is_manual_mode: boolean;
  is_archived: boolean;
  priority: number;
  messages: TopicMessage[]
}

interface TopicMessage {
  id: number;
  text: string;
  date: string;
  consultant_id?: number;
  is_author_consultant: boolean;
  is_author_customer: boolean;
  is_author_bot: boolean;
  attachment: {}
}

