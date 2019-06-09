import { Component, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { distinctUntilChanged, filter, map, switchMap, takeUntil } from 'rxjs/operators';
import { Observable, Subject } from 'rxjs';
import { AppHttpService } from '../../providers/app-http.service';
import { Initiative } from '../../_models/initiative';
import { InitiativeComment } from '../../_models/comment';

@Component({
  selector: 'initiative-details',
  templateUrl: './initiative-details.page.html',
  styleUrls: ['./initiative-details.page.scss'],
})
export class InitiativeDetailsPage implements OnInit, OnDestroy {
  alreadyFounded = false;
  private readonly destroy$ = new Subject();
  initiative: Initiative;
  private paramChange: Observable<string>;
  private comments: InitiativeComment[];

  constructor(private activatedRoute: ActivatedRoute,
              private http: AppHttpService,
              private router: Router) {
  }

  ngOnInit() {
    this.paramChange = this.activatedRoute.paramMap
      .pipe(
        takeUntil(this.destroy$),
        map(it => it.get('id')),
        filter(Boolean),
        distinctUntilChanged(),
      );

    this.paramChange
      .pipe(
        switchMap(id => this.http.getInitiative(id))
      )
      .subscribe(initiative => {
        this.initiative = initiative;
        if (String(initiative.body).length > 120) {
          initiative.truncateBody = true;
        }
      });

    this.paramChange
      .pipe(
        switchMap(id => this.http.getComments(id))
      )
      .subscribe(comments => {
        this.comments = comments;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
  }

  isLiked(user_vote: number): boolean {
    return user_vote === 1;
  }

  toggleLike(initiative: Initiative) {
    let obs;
    if (this.isLiked(initiative.user_vote)) {
      obs = this.http.removevote(initiative.id);
    } else {
      obs = this.http.upvote(initiative.id);
    }

    obs
      .subscribe(it => {
        this.initiative = it;
        if (String(this.initiative.body).length > 120) {
          this.initiative.truncateBody = true;
        }
      });
  }

  toggleCommentLink(comment: InitiativeComment) {
    let obs;
    if (this.isLiked(comment.user_vote)) {
      obs = this.http.removevoteComment(comment.id);
    } else {
      obs = this.http.upvoteComment(comment.id);
    }

    obs
      .subscribe((it: InitiativeComment) => {
        comment.votes = it.votes;
        comment.user_vote = it.user_vote;
      });
  }

  requestFounding() {
    this.router.navigateByUrl('/found-success');
    setTimeout(() => {
      this.alreadyFounded = true;
    }, 500);
  }

}
