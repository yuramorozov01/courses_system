import { Component, OnInit, ViewChild } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { switchMap } from 'rxjs/operators';

import { StripeService, StripePaymentElementComponent } from 'ngx-stripe';
import { SetupIntent, StripeElementsOptions } from '@stripe/stripe-js';

import { PaymentService } from '../shared/services/payment/payment.service';
import { IClientSecret } from '../shared/interfaces/payment.interfaces';
import { MaterializeService } from '../shared/services/utils/materialize.service';

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
        locale: 'en',
        loader: 'always',
    };

    constructor(private http: HttpClient,
                private route: ActivatedRoute,
                private stripeService: StripeService,
                private paymentService: PaymentService) {
    }

    ngOnInit(): void {
        this.form = new FormGroup({
            name: new FormControl(null, [Validators.required]),
        });
        this.getClientSecret();
        this.form.disable();
        this.route.queryParams
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['setup_intent_client_secret']) {
                            return this.stripeService.retrieveSetupIntent(params['setup_intent_client_secret'])
						}
						return of(null);
					}
				)
			)
			.subscribe(
				(setupIntent) => {
                    if (setupIntent) {
                        let status = setupIntent.setupIntent.status;
                        let pm_id = setupIntent.setupIntent.payment_method;
                        switch (status) {
                            case 'succeeded': {
                                MaterializeService.toast('Success! Your payment method has been saved.');
                                break;
                            }
                            case 'processing': {
                                MaterializeService.toast('Processing payment details...');
                                break;
                            }
                            case 'requires_payment_method': {
                                MaterializeService.toast('Failed to process payment details. Please try another payment method.');
                                break;
                            }
                        }
                        let obs$ = this.paymentService.saveCard(pm_id);
                        obs$.subscribe(
                            (msg) => {

                            },
                            (error) => {
                                MaterializeService.toast(error.error);
                            }
                        );
                    }
                    this.form.enable();
				},
                (error) => {
                    MaterializeService.toast(error.error);
                }
			);
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
                return_url: `http://localhost:4200/save_card/`,
                payment_method_data: {
                    billing_details: {
                        name: this.form.get('name').value
                    }
                }
            }
        }).subscribe((result) => {
            MaterializeService.toast(result.error.message);
        });
    }
}
