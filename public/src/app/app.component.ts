import { Component, OnInit } from '@angular/core';
import { HttpService} from './http.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    title = 'PROJECT';
    attribute: any;
    allthings: any;
    updateClick(eventData){
        this.attribute = eventData;
    }

    constructor(private _httpService: HttpService, private _router: Router){};

    ngOnInit(){
        this._router.navigate(['movies']);
    }
}
