import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Subscription } from 'rxjs';

import { AuthService } from '../shared/services/auth/auth.service';
import { MaterializeService } from '../shared/services/utils/materialize.service';

@Component({
    selector: 'app-register-page',
    templateUrl: './register-page.component.html',
    styleUrls: ['./register-page.component.css']
})
export class RegisterPageComponent implements OnInit, OnDestroy {

    form: FormGroup;

    aSub: Subscription;

    constructor(private auth: AuthService,
                private router: Router,
                private route: ActivatedRoute) {
    }

    ngOnInit(): void {
        if (this.auth.isAuthenticated()) {
            this.router.navigate(['/harmonic_signal']);
        }

        this.form = new FormGroup({
            email: new FormControl(null, [Validators.required, Validators.email]),
            username: new FormControl(null, [Validators.required]),
            password: new FormControl(null, [Validators.required, Validators.minLength(6)]),
        });
    }

    ngOnDestroy(): void {
        if (this.aSub) {
            this.aSub.unsubscribe();
        }
    }

    onSubmit() {
        this.form.disable();
        this.aSub = this.auth.register(this.form.value).subscribe(
            () => {
                this.router.navigate(['/'], {
                    queryParams: {
                        registered: true,
                    }
                });
            },
            error => {
                console.log(error);
                MaterializeService.toast(error.error);
                this.form.enable();
            }
        );
    }
}
