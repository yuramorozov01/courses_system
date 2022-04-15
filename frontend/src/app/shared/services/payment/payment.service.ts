import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IClientSecret, ICardList, IPaymentResult } from '../../interfaces/payment.interfaces';
import { ParserService } from '../utils/parser.service';
import { FormGroup } from '@angular/forms';
import { ICourseList } from '../../interfaces/courses.interfaces';

@Injectable({
    providedIn: 'root',
})
export class PaymentService {
    constructor(private http: HttpClient,
                private parserService: ParserService) {
    }
    
    getClientSecret(): Observable<IClientSecret> {
        return this.http.get<IClientSecret>('/api/v1/payment/client_secret/');
    }
    
    saveCard(pm_id: string): Observable<any> {
        let body = new FormData();
        body.set('pm_id', pm_id);
        return this.http.post<any>('/api/v1/card/save_card/', body);
    }
    
    getCoursesToBuy(): Observable<ICourseList[]> {
        return this.http.get<ICourseList[]>('/api/v1/course/to_buy/');
    }

    getSavedCards(): Observable<ICardList[]> {
        return this.http.get<ICardList[]>('/api/v1/card/');
    }

    buyCourse(pm_id: string, course_id: number): Observable<IPaymentResult> {
        let body = new FormData();
        body.set('pm_id', pm_id);
        body.set('course_id', course_id.toString());
        return this.http.post<IPaymentResult>('/api/v1/payment/buy_course/', body);
    }

    getPurchasedCourses(): Observable<ICourseList[]> {
        return this.http.get<ICourseList[]>('/api/v1/course/purchased/');
    }

    refundCourse(course_id: number): Observable<any> {
        let body = new FormData();
        body.set('course_id', course_id.toString());
        return this.http.post<any>('/api/v1/payment/refund/', body);
    }
}
