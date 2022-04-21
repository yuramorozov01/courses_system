import { ElementRef } from '@angular/core';

declare var M;

export class MaterializeService {
    static toast(msg: any) {
        if (typeof msg === 'string') {
            M.toast({html: msg});
        } else {
            Object.keys(msg).forEach((key) => {
                if (msg[key] instanceof Array) {
                    msg[key].forEach(function(value) {
                        M.toast({html: key + ': ' + value});
                    });
                } else if (typeof msg[key] === 'string') {
                    M.toast({html: key + ': ' + msg[key]});
                }
            });
        }
    }

    static initializeParallax(ref: ElementRef) {
        M.Parallax.init(ref.nativeElement);
    }

    static initializeModal(ref: ElementRef) {
        M.Modal.init(ref.nativeElement);
        return M.Modal.getInstance(ref.nativeElement);
    }

    static updateTextInputs() {
        M.updateTextFields();
    }
}
