import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { environment } from '../../environments/environment';

@Injectable()
export class AuthHttpInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    if (!req.url.startsWith('/v1')) {
      console.log('doesnt start with /v1');
      return next.handle(req);
    }

    const newUrlReq = req.clone({
      url: `${environment.apiUrl}${req.url}`
    });

    if (!this.authService.isAuthorized()) {
      console.log('not-authorized');
      return next.handle(newUrlReq);
    }
    const authReq = newUrlReq.clone({
      headers: newUrlReq.headers.set('Authorization', `Basic ${this.authService.getBaseAuthToken()}`)
    });
    return next.handle(authReq);
  }

}
