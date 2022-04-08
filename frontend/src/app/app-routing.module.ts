import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthGuard } from './shared/services/auth/auth.guard';

import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';

import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';

import { MainPageComponent } from './main-page/main-page.component';
import { SaveCardPageComponent } from './save-card-page/save-card-page.component';

const routes: Routes = [
    {
        path: '',
        component: SiteLayoutComponent,
        children: [
            {
                path: 'login',
                component: LoginPageComponent,
            },
            {
                path: 'register',
                component: RegisterPageComponent,
            },
            {
                path: '',
                component: MainPageComponent,
                canActivate: [AuthGuard],
            },
            {
                path: 'save_card',
                component: SaveCardPageComponent,
                canActivate: [AuthGuard],
            },
        ],
    },
];

@NgModule({
    imports: [
        RouterModule.forRoot(routes),
    ],
    exports: [
        RouterModule,
    ],
})
export class AppRoutingModule {
}
