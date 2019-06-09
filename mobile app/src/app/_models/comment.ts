export interface InitiativeComment {
  id: number;
  initiative_id: string;
  user: User;
  body: string;
  votes: number;
  date_created: Date;
  user_vote: null;
}

export interface User {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  badge: string;
}
