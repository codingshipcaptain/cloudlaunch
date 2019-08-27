import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

    constructor(private _http: HttpClient){ }

    getThings():Observable<object>{
        let tempObservable;
        return tempObservable = this._http.get('/api/all')
    }

    getOne(id:string):Observable<object>{
        let tempObservable;
        return tempObservable = this._http.get('/api/one/'+id)
    }

    createOne(newOne):Observable<object>{
        let tempObservable;
        console.log(newOne);
        return tempObservable = this._http.post('/api/new/', newOne)
    }

    updateOne(id:string, body):Observable<object>{
        let tempObservable;
        return tempObservable = this._http.put('/api/update/'+id, body)
    }

    deleteOne(id:string):Observable<object>{
        let tempObservable;
        return tempObservable = this._http.delete('/api/remove/'+id)
    }
    reviewAdd(id:string, review: any):Observable<object>{
        let tempObservable;
        return tempObservable = this._http.put('/api/review/add/'+id, review)
    }
    reviewDelete(id: string, review):Observable<object>{
        let tempObservable;
        return tempObservable = this._http.put('/api/review/delete/'+id, review)
    }
}
