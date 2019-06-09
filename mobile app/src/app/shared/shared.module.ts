import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TruncatedTextPipe } from './truncated-text.pipe';

@NgModule({
  declarations: [TruncatedTextPipe],
  exports: [TruncatedTextPipe],
  imports: [
    CommonModule
  ]
})
export class SharedModule { }
