export interface Initiative {
  id: string;
  title: string;
  imageUrl: string;
  body: string;
  cover: string;
  date_created: Date;
  date_edited: Date;
  is_edited: boolean;
  votes: number;
  shares_count: number;
  comments_count: number;
  author: Author;
  is_starred: boolean;
  user_vote: number;
  truncateBody?: boolean;
}

export interface Author {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  badge: string;
}
