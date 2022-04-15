import { Component, OnInit, ViewChild } from '@angular/core';

import { Observable } from 'rxjs';

import { PaymentService } from '../shared/services/payment/payment.service';
import { ICourseList } from '../shared/interfaces/courses.interfaces';
import { IRefundResult } from '../shared/interfaces/payment.interfaces';
import { MaterializeService } from '../shared/services/utils/materialize.service';


@Component({
  selector: 'app-purchased-courses-page',
  templateUrl: './purchased-courses-page.component.html',
  styleUrls: ['./purchased-courses-page.component.css']
})
export class PurchasedCoursesPageComponent implements OnInit {

	courses$: Observable<ICourseList[]>;

	constructor(private paymentService: PaymentService) { }

	ngOnInit(): void {
		this.courses$ = this.paymentService.getPurchasedCourses();
        this.courses$.subscribe(
            (course: ICourseList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

    refund(course: ICourseList) {
        // this.buyModal.open(course);
        const decision = window.confirm('Are you sure you want to refund this course?');
        if (decision) {
            this.paymentService.refundCourse(course.id).subscribe(
                (refundResult: IRefundResult) => {
                    let price = (refundResult.amount / 100).toFixed(2);
                    window.alert(`Status: ${refundResult.status}\nPrice: ${price}\nMessage: ${refundResult.failure_reason || 'OK'}`);
                },
                (error) => {
                    MaterializeService.toast(error.error);
                }
            );
        }
    }
}
