import {inject, Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {catchError, of, tap} from "rxjs";
import {LoginResponse} from "../model";
import {Router} from "@angular/router";
import {environment} from "../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor() { }

  httpClient = inject(HttpClient);
  apiUrl = environment.apiUrl
  router = inject(Router);

  signup(data: any) {
    return this.httpClient.post(`${this.apiUrl}auth/signup`, data);
  }

  login(data: any) {
    return this.httpClient.post<LoginResponse>(`${this.apiUrl}auth/login`, data)
      .pipe(
        tap(response => localStorage?.setItem('access_token', response['access_token'])),
        catchError(error => {
          console.error('Error logging in: ', error);
          return of(null);
        })
      )
  }

  logout() {
    this.httpClient.post(`${this.apiUrl}auth/logout`, {}).subscribe(data => {
      this.router.navigate(['/login']).then();
    })
    localStorage?.removeItem('access_token');
  }

  isLoggedIn() {
    return localStorage?.getItem('access_token') !== null;
  }
}
