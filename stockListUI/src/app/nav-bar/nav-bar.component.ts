import {Component, inject} from '@angular/core';
import {MatButtonModule} from "@angular/material/button";
import {MatMenuModule} from "@angular/material/menu";
import {MatIconModule} from "@angular/material/icon";
import {MatToolbar} from "@angular/material/toolbar";
import {AuthService} from "../auth/auth.service";
import {AdminComponent} from "../auth/admin/admin.component";

@Component({
  selector: 'app-nav-bar',
  standalone: true,
  imports: [MatButtonModule, MatMenuModule, MatIconModule, MatToolbar],
  templateUrl: './nav-bar.component.html',
  styleUrl: './nav-bar.component.css'
})
export class NavBarComponent {
  authService = inject(AuthService);
  protected readonly AdminComponent = AdminComponent;

  public logout(){
    this.authService.logout();
  }
}
