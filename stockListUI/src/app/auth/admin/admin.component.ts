import {Component, inject, OnInit} from '@angular/core';
import {AuthService} from "../auth.service";
import {Router} from "@angular/router";
import {WatchlistComponent} from "../../watchlist/watchlist.component";
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [
    WatchlistComponent
  ],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css'
})
export class AdminComponent {
}
