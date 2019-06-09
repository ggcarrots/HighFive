import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Initiative } from '../_models/initiative';
import { InitiativeComment } from '../_models/comment';
import { NewInitiative } from '../_models/new-initiative';

@Injectable({
  providedIn: 'root'
})
export class AppHttpService {

  constructor(private http: HttpClient) {
  }

  getInitiatives(): Observable<Initiative[]> {
    return this.http.get<Initiative[]>('/v1/initiatives');
  }

  getInitiative(id: string): Observable<Initiative> {
    return this.http.get<Initiative>(`/v1/initiatives/${id}`);
  }

  upvote(initiativeId: string): Observable<Initiative> {
    return this.http.post<Initiative>(`/v1/initiatives/${initiativeId}/upvote`, null);
  }

  downvote(initiativeId: string): Observable<Initiative> {
    return this.http.post<Initiative>(`/v1/initiatives/${initiativeId}/downvote`, null);
  }

  removevote(initiativeId: string): Observable<Initiative> {
    return this.http.post<Initiative>(`/v1/initiatives/${initiativeId}/removevote`, null);
  }

  getComments(initiativeId: string): Observable<InitiativeComment[]> {
    return this.http.get<InitiativeComment[]>(`/v1/comments?initiative_id=${initiativeId}`);
  }

  upvoteComment(initiativeId: number): Observable<Initiative> {
    return this.http.post<Initiative>(`/v1/comments/${initiativeId}/upvote`, null);
  }

  removevoteComment(initiativeId: number): Observable<Initiative> {
    return this.http.post<Initiative>(`/v1/comments/${initiativeId}/removevote`, null);
  }

  createInitiative(body: NewInitiative): Observable<any> {
    return this.http.post<any>(`/v1/initiatives`, body)
  }

}
