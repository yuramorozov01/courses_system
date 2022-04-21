import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '../../../../../environments/environment';

import { AuthService } from '../../../services/auth/auth.service';

@Component({
    selector: 'app-site-layout',
    templateUrl: './site-layout.component.html',
    styleUrls: ['./site-layout.component.css']
})
export class SiteLayoutComponent implements OnInit {

    title = environment.title

    links = [
        {
            url: '/',
            name: 'Main',
        },
        {
            url: '/save_card',
            name: 'Save card',
        },
        {
            url: '/buy_courses',
            name: 'Buy course',
        },
        {
            url: '/purchased_courses',
            name: 'Purchased courses',
        },
    ];

    constructor(public authService: AuthService,
                private router: Router) {
    }

    ngOnInit(): void {
    }

    logout(event: Event) {
        event.preventDefault();
        this.authService.logout();
        this.router.navigate(['/']);
    }

}
