import { Injectable } from '@angular/core';
import { FormGroup } from '@angular/forms';

@Injectable({
    providedIn: 'root',
})
export class ParserService {
    constructor() {
    }

    getValuesFromFormGroup(formGroup: FormGroup): FormData {
        const formData = new FormData();
        const valuesFromFormGroup = formGroup.value;
        Object.keys(valuesFromFormGroup).forEach((key) => {
            let value = valuesFromFormGroup[key];
            if (value == null) {
                value = '';
            }
            formData.append(key, value);
        });
        return formData;
    }
}
