import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'truncatedText'
})
export class TruncatedTextPipe implements PipeTransform {

  transform(value: string, shouldTruncate: boolean): any {
    if (!shouldTruncate) {
      return value;
    }
    return `${value.slice(0, 120)}...  `;
  }

}
