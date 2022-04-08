import { Component, OnInit, ViewChild } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { StripeService, StripePaymentElementComponent, StripeCardComponent } from 'ngx-stripe';
import { StripeCardElementOptions, StripeElementsOptions } from '@stripe/stripe-js';

import { PaymentService } from '../shared/services/payment/payment.service';
import { IClientSecret } from '../shared/interfaces/payment.interfaces';

@Component({
    selector: 'app-save-card-page',
    templateUrl: './save-card-page.component.html',
    styleUrls: ['./save-card-page.component.css']
})
export class SaveCardPageComponent implements OnInit {
    public clientSecret: IClientSecret;
    public clientSecret$: Observable<IClientSecret>;

    @ViewChild(StripePaymentElementComponent) paymentElement: StripePaymentElementComponent;

    form: FormGroup;

    elementsOptions: StripeElementsOptions = {
        locale: 'en'
    };

    constructor(private http: HttpClient,
                private stripeService: StripeService,
                private paymentService: PaymentService) {
    }

    ngOnInit(): void {
        this.form = new FormGroup({
            name: new FormControl(null, [Validators.required]),
        });
        this.getClientSecret();
    }

    public getClientSecret(): void {
        this.clientSecret$ = this.paymentService.getClientSecret();
        this.clientSecret$.subscribe(
            (clientSecret: IClientSecret) => {
                this.clientSecret = clientSecret;
                this.elementsOptions.clientSecret = clientSecret.client_secret;
            }
        );
    }

    public saveCard() {
        this.stripeService.confirmSetup({
            elements: this.paymentElement.elements,
            confirmParams: {
                return_url: 'http://localhost:4200/',
                payment_method_data: {
                    billing_details: {
                        name: this.form.get('name').value
                    }
                }
            }
        }).subscribe((result) => {
            console.log(result);
        });
    }
}
