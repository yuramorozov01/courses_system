import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Subscription } from 'rxjs';

import { AuthService } from '../shared/services/auth/auth.service';
import { MaterializeService } from '../shared/services/utils/materialize.service';

@Component({
    selector: 'app-login-page',
    templateUrl: './login-page.component.html',
    styleUrls: ['./login-page.component.css']
})
export class LoginPageComponent implements OnInit, OnDestroy {

    form: FormGroup;

    aSub: Subscription;

    constructor(private auth: AuthService,
                private router: Router,
                private route: ActivatedRoute) {
    }

    ngOnInit(): void {
        if (this.auth.isAuthenticated()) {
            this.router.navigate(['/']);
        }

        this.form = new FormGroup({
            username: new FormControl(null, [Validators.required]),
            password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
        });

        this.route.queryParams.subscribe((params: Params) => {
            if (params['registered']) {
                MaterializeService.toast('You have been registered and you can login');
            } else if (params['accessDenied']) {
                MaterializeService.toast('You have to login');
            } else if (params['sessionFailed']) {
                MaterializeService.toast('Please, login to system again');
            }
        });
    }

    ngOnDestroy(): void {
        if (this.aSub) {
            this.aSub.unsubscribe();
        }
    }

    onSubmit() {
        this.form.disable();
        this.aSub = this.auth.login(this.form.value).subscribe(
            (tokens: any) => {
                this.router.navigate(['/']);
            },
            error => {
                MaterializeService.toast(error.error);
                this.form.enable();
            }
        );
    }

}
