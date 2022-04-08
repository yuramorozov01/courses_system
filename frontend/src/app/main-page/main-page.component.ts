import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

import { MaterializeService } from '../shared/services/utils/materialize.service';

@Component({
    selector: 'app-main-page',
    templateUrl: './main-page.component.html',
    styleUrls: ['./main-page.component.css']
})
export class MainPageComponent implements OnInit {


    constructor() { }

    ngOnInit(): void {
    }
}
