import { Component } from '@angular/core';
import { AppHttpService } from '../../providers/app-http.service';

@Component({
  selector: 'dashboard',
  templateUrl: './dashboard.page.html',
  styleUrls: ['./dashboard.page.scss'],
})
export class DashboardPage {
  queryText = '';
  selectedGroupId = 'złota52';

  constructor(private http: AppHttpService) {
  }

  selectGroup(groupId: string) {
    this.selectedGroupId = groupId;
  }

}
