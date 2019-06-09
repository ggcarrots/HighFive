import {Component, OnInit} from '@angular/core';
import {AppHttpService} from '../_services/app-http.service';

// import { Topic } from '../_models/topic';

@Component({
  selector: 'app-topics-page',
  templateUrl: './topics-page.component.html',
  styleUrls: ['./topics-page.component.scss'],
})
export class TopicsPageComponent implements OnInit {
  // private topics: Topic[];

  constructor(private http: AppHttpService) {
  }

  ngOnInit(): void {
  }

  // ngOnInit() {
  //   this.http.getTopics()
  //     .subscribe(topic => this.topics = topic)
  // }

}
