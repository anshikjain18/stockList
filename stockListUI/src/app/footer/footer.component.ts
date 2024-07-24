import {Component, OnInit} from '@angular/core';
import {NgOptimizedImage} from "@angular/common";

@Component({
  selector: 'app-footer',
  standalone: true,
  imports: [
    NgOptimizedImage
  ],
  templateUrl: './footer.component.html',
  styleUrl: './footer.component.css'
})
export class FooterComponent implements OnInit{
  private isFooterStuck: boolean = false;

  ngOnInit(): void {
    this.checkFooterPosition();
    window.addEventListener('resize', this.checkFooterPosition);
  }

  private checkFooterPosition() {
    const contentHeight = document.body.scrollHeight;
    const windowHeight = window.innerHeight;
    this.isFooterStuck = contentHeight < windowHeight;
  }
}
