import { Component, OnInit } from '@angular/core';

import { AuthService } from './shared/services/auth/auth.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
    constructor(private auth: AuthService) {

    }

    ngOnInit() {
        const potentialToken = localStorage.getItem('auth-access');
        if (potentialToken !== null) {
            this.auth.setAccessToken(potentialToken);
        }
    }
}
