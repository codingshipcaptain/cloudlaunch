import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-movies',
  templateUrl: './movies.component.html',
  styleUrls: ['./movies.component.css']
})
export class MoviesComponent implements OnInit {
    allthings: any;
    showNew: boolean;
    listenShow(eventData){
        this.showNew = eventData;
    }

    constructor(private _httpService: HttpService, private _router: Router, ){}

    ngOnInit() {
        this.showNew = false
        this._httpService.getThings().subscribe(things => {
          console.log('things in things components: ', things);
          this.allthings = things;
        })
    }

    show(movie){
        console.log(movie);
        this._router.navigate(['/movies/'+movie._id]);
    }

    review(movie){
        console.log(movie);
        this._router.navigate(['/movies/'+movie._id+ '/review']);
    }

    gotoAdd(){
        this.showNew = true;
    }

}
