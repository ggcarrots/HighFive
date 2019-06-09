import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { AppHttpService } from '../../../providers/app-http.service';
import { BehaviorSubject, Subject } from 'rxjs';
import { debounceTime, distinctUntilChanged, filter, map, switchMap, takeUntil, tap } from 'rxjs/operators';
import { Initiative } from '../../../_models/initiative';

@Component({
  selector: 'initiatives-list',
  templateUrl: './initiatives-list.component.html',
  styleUrls: ['./initiatives-list.component.scss'],
})
export class InitiativesListComponent implements OnInit, OnDestroy {
  private readonly destroy$ = new Subject();
  private readonly groupId$ = new BehaviorSubject<string>(null);
  private readonly searchQuery$ = new BehaviorSubject<string>(null);
  initiatives: Initiative[];

  @Input()
  set groupId(value: string) {
    this.groupId$.next(value);
  }

  @Input()
  set searchQuery(value: string) {
    this.searchQuery$.next(value);
  }

  constructor(private http: AppHttpService) {
  }

  ngOnInit() {
    this.groupId$
      .pipe(
        takeUntil(this.destroy$),
        filter(Boolean),
        distinctUntilChanged(),
        tap(groupId => console.log({groupId})),
        switchMap(groupId => this.searchQuery$
          .pipe(
            debounceTime(600),
            switchMap(searchQuery => this.http.getInitiatives()
              .pipe(
                tap(groupId => console.log({groupId})),
                map(it => it.filter(init => {
                  if (!searchQuery) {
                    return init;
                  }
                  return init.title.toLowerCase().includes(searchQuery) || init.body.toLowerCase().includes(searchQuery);
                }))
              )
            )
          )
        )
      )
      .subscribe(initiatives => {
        this.initiatives = initiatives;
        initiatives.forEach(initiative => {
          if (String(initiative.body).length > 120) {
            initiative.truncateBody = true;
          }
        });
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
  }

  isLiked(initiative: Initiative): boolean {
    return initiative.user_vote === 1;
  }

  toggleLike(initiative: Initiative) {
    let obs;
    if (this.isLiked(initiative)) {
      obs = this.http.removevote(initiative.id);
    } else {
      obs = this.http.upvote(initiative.id);
    }

    obs
      .pipe(
        switchMap(it => this.http.getInitiatives())
      )
      .subscribe(it => {
        this.initiatives = it;
        this.initiatives.forEach(initiative => {
          if (String(initiative.body).length > 120) {
            initiative.truncateBody = true;
          }
        });
      });
  }

  trackBy(index: number, item: Initiative) {
    return item.id;
  }
}
