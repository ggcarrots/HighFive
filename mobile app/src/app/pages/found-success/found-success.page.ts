import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'found-success',
  templateUrl: './found-success.page.html',
  styleUrls: ['./found-success.page.scss'],
})
export class FoundSuccessPage implements OnInit {

  constructor(private location: Location) { }

  ngOnInit() {
  }

  closePanel() {
    this.location.back();
  }

}
