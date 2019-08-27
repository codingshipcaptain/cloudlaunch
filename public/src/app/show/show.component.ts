import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { HttpService} from '../http.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-show',
  templateUrl: './show.component.html',
  styleUrls: ['./show.component.css']
})
export class ShowComponent implements OnInit {
    reviews: any;
    movie: any;

    constructor(
        private _httpService: HttpService,
        private _router: Router,
        private _route: ActivatedRoute
    ){}

    ngOnInit() {
        this.movie = {};
        this.reviews = [];
        this._route.params.subscribe(params=> {
            console.log("Params", params);
            this._httpService.getOne(params['id']).subscribe(data => {
                this.reviews = data['reviews'];
                this.movie = data;
            })
        })
    }

    deleteMovie(){
        console.log("MOVIE TO DELETE:", this.movie)
        this._httpService.deleteOne(this.movie._id).subscribe(data =>{
            console.log(data)});
        this._router.navigate(['/movies']);
    }

    reviewRemoval(i, review){
        console.log("DELETE LINE: ", review)
        console.log("Index: ", i)
        this._httpService.reviewDelete(this.movie._id, review).subscribe(data =>{
            console.log(data);
            this.reviews.splice(i,1)
        })
    }

    return(){this._router.navigate(['/movies'])}

}
