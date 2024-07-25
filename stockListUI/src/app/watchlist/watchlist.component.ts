import {Component, inject, OnInit} from '@angular/core';
import {NgOptimizedImage} from "@angular/common";
import {MatIcon} from "@angular/material/icon";
import {HttpClient, HttpHeaders, HttpResponse} from "@angular/common/http";
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {Router, RouterLink} from "@angular/router";
import {environment} from "../../environments/environment";

@Component({
  selector: 'app-watchlist',
  standalone: true,
  imports: [
    NgOptimizedImage,
    MatIcon,
    FormsModule,
    ReactiveFormsModule,
    RouterLink
  ],
  templateUrl: './watchlist.component.html',
  styleUrl: './watchlist.component.css'
})
export class WatchlistComponent implements OnInit{
  createWatchlistClicked: boolean = false;
  watchlistClicked: boolean = false;
  apiUrl = environment.apiUrl;
  watchlistName: string = '';
  watchlists: any;
  protected watchlistForm: FormGroup;
  router = inject(Router);

  constructor(private http: HttpClient, private fb: FormBuilder) {
    this.watchlistForm = this.fb.group({
      watchlistName: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.http.get(`${this.apiUrl}`, {}).subscribe(res => {
      this.watchlists = res;
    });
  }

  createWatchlist() {
    if (this.watchlistForm.valid) {
      const body = {
        'name': this.watchlistForm.value.watchlistName,
        'investments': []
      }
      this.http.post(`${this.apiUrl}watchlist`, body).subscribe(
        (response) => {
          window.location.reload();
        }
      );
    }
  }

  toggleCreateWatchlistPopup() {
    this.createWatchlistClicked = !this.createWatchlistClicked;
  }

  get_ts_date(ms: any) {
    let date = new Date(ms)
    return date.getDate() + "-" + date.getMonth() + "-" + date.getFullYear();
  }

  toggleWatchlistDetail() {
    this.watchlistClicked = !this.watchlistClicked;
  }
}
