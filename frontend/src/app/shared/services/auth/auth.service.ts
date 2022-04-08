import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import { IUser, IUserMe, IJWT, IAccess, IRefresh } from '../../interfaces/auth.interfaces';


@Injectable({
    providedIn: 'root'
})
export class AuthService {

    private access: string = null;
    private refresh: string = null;

    constructor(private http: HttpClient) {

    }

    register(user: IUser): Observable<IUser> {
        return this.http.post<IUser>('/auth/users/', user);
    }

    login(user: IUser): Observable<IJWT> {
        return this.http.post<IJWT>('/auth/jwt/create/', user)
            .pipe(
                tap(
                    ({refresh, access}) => {
                        localStorage.setItem('auth-refresh', refresh);
                        this.setRefreshToken(refresh);
                        localStorage.setItem('auth-access', access);
                        this.setAccessToken(access);
                    }
                )
            );
    }

    me(): Observable<IUserMe> {
        return this.http.get<IUserMe>('/auth/users/me/');
    }

    setAccessToken(access: string) {
        this.access = access;
    }

    getAccessToken(): string {
        return this.access;
    }

    setRefreshToken(refresh: string) {
        this.refresh = refresh;
    }

    isAuthenticated(): boolean {
        return !!this.access;
    }

    refreshAccessToken(refresh: string): void {
        this.http.post<IAccess>('/auth/jwt/refresh/', {refresh: refresh})
            .pipe(
                tap(
                    ({access}) => {

                        localStorage.setItem('auth-access', access);
                        this.setAccessToken(access);
                    }
                )
            );
    }

    logout() {
        this.setAccessToken(null);
        this.setRefreshToken(null);
        localStorage.clear();
    }
}
