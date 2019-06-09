import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AppHttpService } from '../../providers/app-http.service';
import { Location } from '@angular/common';

@Component({
  selector: 'new-initiative',
  templateUrl: './new-initiative.page.html',
  styleUrls: ['./new-initiative.page.scss'],
})
export class NewInitiativePage implements OnInit {
  rootForm = new FormGroup({
    title: new FormControl('', Validators.required),
    body: new FormControl('')
  });

  submitted: boolean;

  constructor(private http: AppHttpService,
              private location: Location) {
  }

  ngOnInit() {
  }

  updateTitle(text: string){
    this.rootForm.get('title').setValue(text)
  }

  createInitiative(){
    this.http.createInitiative(this.rootForm.value)
      .subscribe(success => {
        this.location.back();
      })
  }



}
