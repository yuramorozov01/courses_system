import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { Observable } from 'rxjs';

import { MaterializeService } from '../../services/utils/materialize.service';
import { PaymentService } from '../../services/payment/payment.service';
import { ICourseList } from '../../interfaces/courses.interfaces';
import { ICardList, IPaymentResult } from '../../interfaces/payment.interfaces';

@Component({
    selector: 'app-buy-modal',
    templateUrl: './buy-modal.component.html',
    styleUrls: ['./buy-modal.component.css']
})
export class BuyModalComponent implements OnInit, AfterViewInit {
    @ViewChild('modal') modalRef: ElementRef;
    cards$: Observable<ICardList[]>;
    form: FormGroup;

    private modalElement;
    public course: ICourseList;

    constructor(private paymentService: PaymentService) {
    }

    ngOnInit(): void {
        this.form = new FormGroup({
            pm_id: new FormControl(null, [Validators.required,]),
		});

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
            if (this.form.invalid) {
                window.alert('You have to choose card to buy this course!')
            } else {
                let pm_id = this.form.get('pm_id').value;
                this.paymentService.buyCourse(pm_id, this.course.id).subscribe(
                    (paymentResult: IPaymentResult) => {
                        let price = (this.course.price / 100).toFixed(2);
                        window.alert(`Status: ${paymentResult.status}\nPrice: ${paymentResult.currency} ${price}`);
                        this.modalElement.close();
                    },
                    (error) => {
                        MaterializeService.toast(error.error);
                    }
                );
            }
        }
    }
}
