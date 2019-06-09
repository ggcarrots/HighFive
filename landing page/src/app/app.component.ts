import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { MediaMatcher } from '@angular/cdk/layout';

interface MenuLink {
  href: string;
  label: string;
}


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit, OnDestroy {
  links: MenuLink[];
  mobileQuery: MediaQueryList;
  private _mobileQueryListener: () => void;

  constructor(changeDetectorRef: ChangeDetectorRef, media: MediaMatcher) {
    this.mobileQuery = media.matchMedia('(max-width: 600px)');
    this._mobileQueryListener = () => changeDetectorRef.detectChanges();
    this.mobileQuery.addListener(this._mobileQueryListener);
  }

  ngOnDestroy(): void {
    this.mobileQuery.removeListener(this._mobileQueryListener);
  }

  ngOnInit() {
    this.links = [
      {
        href: '/',
        label: 'Home',
      },
      {
        href: '/dashboard',
        label: 'Dashboard'
      },
      {
        href: '/history',
        label: 'History'
      },
      {
        href: '/stats',
        label: 'Stats'
      }
    ];
  }

  onClick(id: string){
    let x = document.querySelector(id);
    if (x){
      x.scrollIntoView();
    }
  }

}

