import { Component, OnInit, ViewChild } from '@angular/core';

import { Observable } from 'rxjs';

import { BuyModalComponent } from '../shared/components/buy-modal/buy-modal.component';
import { PaymentService } from '../shared/services/payment/payment.service';
import { ICourseList } from '../shared/interfaces/courses.interfaces';
import { MaterializeService } from '../shared/services/utils/materialize.service';

@Component({
  selector: 'app-buy-courses-page',
  templateUrl: './buy-courses-page.component.html',
  styleUrls: ['./buy-courses-page.component.css']
})
export class BuyCoursesPageComponent implements OnInit {
    @ViewChild('buyModal') buyModal: BuyModalComponent;

	courses$: Observable<ICourseList[]>;

	constructor(private paymentService: PaymentService) { }

	ngOnInit(): void {
		this.courses$ = this.paymentService.getCoursesToBuy();
        this.courses$.subscribe(
            (course: ICourseList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

    buy(course: ICourseList) {
        this.buyModal.open(course);
    }
}
