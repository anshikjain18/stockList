import {HttpEvent, HttpHandlerFn, HttpRequest} from "@angular/common/http";
import {Observable} from "rxjs";

export function authInterceptor(req: HttpRequest<unknown>, next: HttpHandlerFn): Observable<HttpEvent<unknown>> {
  const reqWithHeader = req.clone({
    headers: req.headers.set('Authorization', `Bearer ${localStorage?.getItem('access_token')}`)
  });
  return next(reqWithHeader);
}
