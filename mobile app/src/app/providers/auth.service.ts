import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage';
import { BehaviorSubject, Observable } from 'rxjs';
import { filter } from 'rxjs/operators';
import { Router } from '@angular/router';

export interface UserInfo {
  username: string;
  password: string;
}

const NOT_INITIATED = null;
const LOGGED_OUT = undefined;

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private userInfo$ = new BehaviorSubject(NOT_INITIATED);

  constructor(private storage: Storage,
              private router: Router) {
    this.storage.get('userInfo').then(storageInfo => {
      if (storageInfo) {
        this.authorize(JSON.parse(storageInfo));
        this.router.navigateByUrl('/dashboard');
      }
    });
  }

  authorize(userInfo: UserInfo) {
    console.log('newUser', userInfo);
    this.userInfo$.next(userInfo);
    this.storage.set('userInfo', JSON.stringify(userInfo));
  }

  isAuthorized(): boolean {
    return !!this.userInfo$.value;
  }

  isAuthorized$(): Observable<boolean> {
    return this.userInfo$.pipe(
      filter(it => it !== NOT_INITIATED)
    );
  }

  getBaseAuthToken(): string {
    return btoa(`${this.userInfo$.value.username}:${this.userInfo$.value.password}`);
  }

  logout(): void {
    this.userInfo$.next(LOGGED_OUT);
    this.storage.remove('userInfo');
  }

  getUserInfo(): UserInfo {
    return this.userInfo$.value;
  }
}
