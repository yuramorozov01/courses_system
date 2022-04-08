import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { environment } from '../environments/environment';

import { AppRoutingModule } from './app-routing.module';

import { TokenInterceptor } from './shared/services/auth/token.interceptor';

import { AppComponent } from './app.component';

import { NgxStripeModule } from 'ngx-stripe';

import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';

import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';

import { LoaderComponent } from './shared/components/loader/loader.component';

import { MainPageComponent } from './main-page/main-page.component';
import { SaveCardPageComponent } from './save-card-page/save-card-page.component';


@NgModule({
    declarations: [
        AppComponent,
        LoginPageComponent,
        SiteLayoutComponent,
        RegisterPageComponent,
        LoaderComponent,
        MainPageComponent,
        SaveCardPageComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        ReactiveFormsModule,
        HttpClientModule,
        NgxStripeModule.forRoot('pk_test_51Klu3LAHqNRVS0KISPMpiwdsfNoxqHzpXiugFK75pAblu2G4QxtepoFUKHJBpLn05VeeuktUqxUWLS4HDwFKZREF00a4toleLW'),
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            multi: true,
            useClass: TokenInterceptor,
        },
        DatePipe,
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
}
