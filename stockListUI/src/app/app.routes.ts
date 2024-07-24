import { Routes } from '@angular/router';
import {LoginComponent} from "./auth/login/login.component";
import {AdminComponent} from "./auth/admin/admin.component";
import {authGuard} from "./auth/auth.guard";
import {SignupComponent} from "./auth/signup/signup.component";

export const routes: Routes = [
  {
    path: '', redirectTo: '/login', pathMatch: 'full'
  },
  {
    path: 'login', component: LoginComponent
  },
  {
    path: 'signup', component: SignupComponent
  },
  {
    path: 'admin', component: AdminComponent, canActivate: [authGuard]
  }
];
