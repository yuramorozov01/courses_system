import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';

import { Observable } from 'rxjs';

import { MaterializeService } from '../../services/utils/materialize.service';
import { PaymentService } from '../../services/payment/payment.service';
import { ICourseList } from '../../interfaces/courses.interfaces';
import { ICardList } from '../../interfaces/payment.interfaces';

@Component({
    selector: 'app-buy-modal',
    templateUrl: './buy-modal.component.html',
    styleUrls: ['./buy-modal.component.css']
})
export class BuyModalComponent implements OnInit, AfterViewInit {
    @ViewChild('modal') modalRef: ElementRef;
    cards$: Observable<ICardList[]>;


    private modalElement;
    public course: ICourseList;

    constructor(private paymentService: PaymentService) {
    }

    ngOnInit(): void {
        this.cards$ = this.paymentService.getSavedCards();
        this.cards$.subscribe(
            (cards: ICardList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
    }

    ngAfterViewInit() {
        this.modalElement = MaterializeService.initializeModal(this.modalRef);
    }

    public open(course: ICourseList) {
        this.course = course;
        this.modalElement.open();
    }

    public buy() {
        const decision = window.confirm('Are you sure you want to buy this course?');
        if (decision) {
            this.modalElement.close();
        }
    }
}
