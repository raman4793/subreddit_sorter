import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { Subreddit } from './subreddit';

@Injectable({
  providedIn: 'root'
})
export class SubredditService {

  constructor(private http: HttpClient) { }

  getSubreddits() : Observable<Subreddit[]> {
    return this.http.get<Subreddit[]>("http://localhost:5000/v1/subreddits")
  }

}
