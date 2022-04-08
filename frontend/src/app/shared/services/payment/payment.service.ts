import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IClientSecret } from '../../interfaces/payment.interfaces';
import { ParserService } from '../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
    providedIn: 'root',
})
export class PaymentService {
    constructor(private http: HttpClient,
                private parserService: ParserService) {
    }

    getClientSecret(): Observable<IClientSecret> {
        return this.http.get<IClientSecret>('/api/v1/payments/client_secret/');
    }
}
