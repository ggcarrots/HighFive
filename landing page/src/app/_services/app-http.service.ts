import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';
import { Topic } from '../_models/topic';

@Injectable({
  providedIn: 'root'
})
export class AppHttpService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {

  }

  getTopics(): Observable<Topic[]> {
    return this.http.get<Topic[]>(`${this.apiUrl}/v1/topics`);
  }
}
